import numpy as np
import scipy.misc

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
    enhanced_image = np.zeros((2*x_size,2*y_size))
    
    for x in range(0,x_size,2):
	for y in range(0,y_size,2):
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
    return enhanced_image

    

sample = scipy.misc.imread('google.jpg',True)

print 'image size:',sample.shape

print 'SAMPLE IMAGE'
print sample

sample_4x = upscale_image(sample)
print 'SAMPLE 4_X'
print sample_4x

scipy.misc.imsave('test_4xxx.jpg',sample_4x)

