import time
import numpy
import math
import scipy
from scipy import interpolate

file = open('matrix.txt', 'w')

matrix_R = numpy.matrix('0   10   30   60    80    100   100   100   100   100   100;\
			 0   0    10   40    0     90    80    80    100   100   100;\
			 0   0    0    30    0     80    70    80    90    100   100;\
			 0   0    0    20    0     70    60    75    90    100   100;\
			 0   0    5    10    0     60    50    70    80    100   100;\
			 0   10   20   30    40    50    60    70    80    90    100;\
		         25  20   50   50    50    50    50    50    55    60    100;\
		         25  20   50   50    50    50    50    60    60    75    75;\
		         25  30   50   50    50    50    50    60    70    75    75;\
			 50  50   50   50    50    50    50    55    65    75    75;\
			 50  50   50   50    50    50    50    55    65    75    75')

matrix_L = numpy.matrix('25   30   40   50   50    50    55    60    60    65    75;\
			 25   25   30   20   0     50    50    50    65    65    75;\
			 25   25   25   20   0     50    50    50    70    75    75;\
			 25   25   25   30   0     50    50    60    70    80    75;\
			 25   25   25   30   0     50    60    70    80    80    100;\
			 0    10   20   30   40    50    60    70    80    90    100;\
			 0    10   50   50   50    60    60    70    80    90    100;\
			 0    10   50   60   60    70    60    70    90    100   100;\
			 0    10   60   80   80    80    70    75    90    100   100;\
			 40   60   80   100  100   100   90    90    90    100   100;\
			 50   50   50   50   50    100   90    90    90    100   100')

inKsize = len(matrix_L)
outKsize = 101

kernelOut = numpy.zeros((outKsize, outKsize), numpy.uint8)

z = matrix_L
y = matrix_R

x = numpy.arange(11)
y = numpy.arange(11)

xx = numpy.linspace(x.min(), x.max(), outKsize)
yy = numpy.linspace(y.min(), y.max(), outKsize)

newKernel = interpolate.RectBivariateSpline(x, y, z)
kernelOut = newKernel(xx, yy)
#print (kernelOut)

p = len(kernelOut)
#for i in range(5):
#	print(row)
#	print kernelOut[i]
#	file.write(kernelOut[i])

numpy.savetxt(file, kernelOut)
file.close()
print(kernelOut)
