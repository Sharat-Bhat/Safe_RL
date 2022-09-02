import numpy, cv2
img = numpy.zeros([5,5,3])

img[:,:,0] = numpy.ones([5,5])*64/255.0
img[:,:,1] = numpy.ones([5,5])*128/255.0
img[:,:,2] = numpy.ones([5,5])*192/255.0
img[2,4,1] = 0
print(img.shape[:][:][0])
dim = (img.shape[0]*100, img.shape[1]*100)
img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
# cv2.imwrite('color_img.jpg', img)
cv2.imshow("Resized image", img)
cv2.waitKey()