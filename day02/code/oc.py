# import
# from import
import cv2 as cv
# 读取图片
img = cv.imread('1.jpg')
print(img.shape)
cv.imshow("cv",img)# 闪一下就没了，所以要设置一个等待时间
cv.waitKey(0)