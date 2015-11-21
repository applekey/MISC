import cv2


a=  cv2.imread('/Users/applekey/Documents/results/a.png',0)
b=  cv2.imread('/Users/applekey/Documents/results/b.png',0)
c=  cv2.imread('/Users/applekey/Documents/results/c.png',0)
d=  cv2.imread('/Users/applekey/Documents/results/d.png',0)


imga = cv2.addWeighted( a, 0.5, b, 0.5, 0.0);
imgb = cv2.addWeighted( c, 0.5, d, 0.5, 0.0);
img = cv2.addWeighted( imga, 0.5, imgb, 0.5, 0.0);
# cv2.imshow('image',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

cv2.imwrite('/Users/applekey/Documents/results/e.png',img)
