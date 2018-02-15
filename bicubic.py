import numpy as np
import scipy.misc
import Image
import sys
import time
import math

def update_progress(job_title, progress,size):
    length = 50 
    block = int(round(length*progress))
    msg = "\r{0}: [{1}] {2}%".format(job_title, "#"*block + "-"*(length-block), round(progress*100, 2))
    if progress >= 1: msg += " DONE\r\n"
    sys.stdout.flush()
    sys.stdout.write(msg)
    #sys.stdout.flush()

def p(x,y,a):
    sum = 0
    for i in range(0,4):
	for j in range(0,4):
	    sum += a[i][j] * x**i * y**j

    return sum

    

def bicubic(sample):
    left_m = np.array(np.mat('1 0 0 0; 0 0 1 0; -3 3 -2 -1; 2 -2 1 1'))
    right_m = np.array(np.mat('1 0 -3 2; 0 0 3 -2; 0 1 -2 1; 0 0 -1 1'))

    mid_m = np.zeros((4,4))

    mid_m[0][0] = sample[0][0]
    mid_m[0][1] = sample[0][1]
    mid_m[1][0] = sample[1][0]
    mid_m[1][1] = sample[1][1]

    sample_grad_x,sample_grad_y = np.gradient(sample)
    sample_grad_xy = np.gradient(sample_grad_x)[1]

    mid_m[0][2] = sample_grad_y[0][0]
    mid_m[0][3] = sample_grad_y[0][1]
    mid_m[1][2] = sample_grad_y[1][0]
    mid_m[1][3] = sample_grad_y[1][1]

    mid_m[2][0] = sample_grad_x[0][0]
    mid_m[2][1] = sample_grad_x[0][1]
    mid_m[3][0] = sample_grad_x[1][0]
    mid_m[3][1] = sample_grad_x[1][1]

    mid_m[2][2] = sample_grad_xy[0][0]
    mid_m[2][3] = sample_grad_xy[0][1]
    mid_m[3][2] = sample_grad_xy[1][0]
    mid_m[3][3] = sample_grad_xy[1][1]

    #print 'MIDDLE MATRIX'
    #print mid_m

    result = np.dot(np.dot(left_m ,mid_m), right_m)

    return result

def upscale_image(image):

    x_size,y_size = image.shape
    size = x_size*y_size        #will use it as a global variable
    enhanced_image = np.zeros((2*x_size,2*y_size),np.uint8)
    nsum = 0

    for x in range(0,x_size,2):
	   for y in range(0,y_size,2):
	    nsum = nsum+1        
	    sample = np.zeros((2,2))
	    sample[0][0] = image[x][y]
	    if x + 1 < x_size and y < y_size:
		sample[1][0] = image[x+1][y]
	    if x < x_size and y + 1 < y_size:
		sample[0][1] = image[x][y+1]
	    if x +1 < x_size and y+1 < y_size:
		sample[1][1] = image[x+1][y+1]
		
	    a = bicubic(sample)
	    #print 'COEFFICENTS'
	    #print a
	    for i in range(0,4):
		for j in range(0,4):
		    if 2*x + i < 2*x_size and 2*y +j < 2*y_size:
		        #enhanced_image[2*x+i][2*y+j] = sample_4x[i][j] 
			enhanced_image[2*x + i][2 * y + j] = p(i,j,a)
		size_f = float(size)
		size_f = size_f/4
		#time.sleep(0.1)
	    update_progress("Super Resolution at work", nsum/size_f,size_f)
    update_progress("Super Resolution at work", 1,size_f)
            
    print nsum
    return enhanced_image

    

def psnr(original,sample_4x,m,n):
	sum=0
	for i in range(0,m):
		for j in range(0,n):
			sum+=(original[i,j] - sample_4x[i,j])**2
	mse=sum/(m*n)

	ps=20*math.log10(255)-10*math.log10(mse)
	return ps


sample = scipy.misc.imread('sam.jpg',True)
size_x,size_y = sample.shape

sample_down = scipy.misc.imresize(sample,(size_x/2,size_y/2)) 

print 'image size:',sample_down.shape

print 'SAMPLE IMAGE'
print sample_down

sample_4x = upscale_image(sample_down)
print 'SAMPLE 4_X'
print sample_4x

#im = Image.fromarray(sample_4x)
#im = im.convert('RGB')
#im.save('test_image_new.jpg')


scipy.misc.imsave('new_test_4xxx.jpg',sample_4x)

print 'PSNR IS: ' + str(psnr(sample_4x,sample,size_x,size_y))+ "dB"
