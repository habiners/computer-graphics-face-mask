import PIL, PIL.Image as I, PIL.ImageFilter as ImageFilter
import numpy as np
from matplotlib import pyplot as P

"""
This class uses canny edge detection under the hood

Canny edge detection uses the ff steps to get the edges:
1 Converting to grayscale 
2 Blurring
3 Sobel operation
4 Non-maxima suppression
5 Thresholding


filename = path of the image to use
blur = blur radius for the gaussian blur
low and high = determines whether an edge should be rendered or not

each edge has a gaussian approximation
> if edge approx is below LOW, it is not drawn as an edge
> if edge approx is between LOW and HIGH, it is drawn only if it has the highest approx in its neighborhood
> if edge approx is HIGH and above, it is drawn

NOTE

Uses Pillow. So pls use pillow too to avoid complications
Gaussian blur is yet to be implemented manually (currently using packag idk if this is ok)
BMP files when converted to numpy array only contains False as its cells' value. I commented the code that recreates this error below

"""

class ImageEdge:
    def __init__(self, filename, blur = 1, low = 0.1, high = 0.2):
        self.raw = I.open(filename)
        self._low = low
        self._high = high

    # returns the Pillow Image file
    def getImage(self): 
        return self.raw

    # returns numpy array representation of image
    def getImageArray(self): 
        if hasattr(self, 'imgarray'):
            return self._imgarray
        
        self._imgarray = np.asarray(self.raw)
        return self._imgarray

    # returns numpy array in the shape of [height][width][3]
    # the [3] of this array is the [r,g,b] values of the edges
    def getImageEdge(self):
        img = self.getImage().convert('LA').filter(ImageFilter.GaussianBlur(radius=1))
        res, x, y, theta = self._sobel()
        res2 = self._suppress(res, theta)
        res3 = self._double_thresh(res2)
        return res3
    
    # underscore functions are meant to be private
    def _sobel(self):
        mask_x = [
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1],
        ]

        mask_y = [
            [-1, -2, -1],
            [0, 0, 0],
            [1, 2, 1],
        ]
        
        img = self.getImageArray()
        arr = np.asarray(img)

        height, width, n = arr.shape
        res = x_res = y_res = np.zeros((height, width, 3))

        for x in range(1, height - 1):
            for y in range(1, width - 1):
                img_space = arr[x-1:x+2, y-1:y+2, 0]
                x_product = mask_x * img_space
                x_sum = x_product.sum()/1020
                x_res[x][y] = [x_sum] * 3

                y_product = mask_y * img_space
                y_sum = y_product.sum()/1020
                y_res[x][y] = [y_sum] * 3

                approx = (x_sum**2 + y_sum**2) ** 0.5
                res[x][y] = [approx] * 3
        
        theta = np.arctan2(y_res, x_res) * 180 / np.pi
        theta = theta[:, :, :1]

        return (res, x_res, y_res, theta)

    def _suppress(self, sobel, theta):
        res = np.copy(sobel)
        height, width, n = sobel.shape
        for x in range(1, height - 1):
            for y in range(1, width - 1):
                if theta[x][y] == 0:
                    if sobel[x][y][0] < sobel[x][y - 1][0] or sobel[x][y][0] < sobel[x][y + 1][0]:
                        res[x][y] = [0] * 3
                        
                if theta[x][y] == 45:
                    if sobel[x][y][0] < sobel[x - 1][y - 1][0] or sobel[x][y][0] < sobel[x + 1][y + 1][0]:
                        res[x][y] = [0] * 3

                if theta[x][y] == 90:
                    if sobel[x][y][0] < sobel[x + 1][y][0] or sobel[x][y][0] < sobel[x - 1][y][0]:
                        res[x][y] = [0] * 3

                if theta[x][y] == 135:
                    if sobel[x][y][0] < sobel[x - 1][y + 1][0] or sobel[x][y][0] < sobel[x + 1][y - 1][0]:
                        res[x][y] = [0] * 3
        return res

    def _double_thresh(self, sobel):
        low = self._low
        high = self._high
        res = np.copy(sobel)
        height, width, n = sobel.shape
        for x in range(height):
            for y in range(width):
                if sobel[x][y][0] <= low:
                    res[x][y] = [0] * 3
                elif sobel[x][y][0] > low and sobel[x][y][0] < high:
                    edge = False
                    for i in range(-1, 1):
                        for j in range(-1, 1):
                            if sobel[x + i][y + j][0] >= high:
                                edge = True
                                break
                    
                    if not edge:
                        res[x][y] = [0] * 3
        
        return res


edge = ImageEdge('test/test.png', 1, 0.15, 0.2)

# TESTING EDGE
P.imshow(edge.getImageEdge())
P.show()


# RECREATE BMP ERROR
# edge = ImageEdge('test/koala bw via paint.bmp', 1, 0.05, 0.1)
# P.imshow(edge.getImageArray())
# P.show()



# ------------------------------------------------------------------------------------------
# CODE FOR MANUAL GAUSSIAN FILTERING (TO BE MODIFIED)
# Issues: must use Pillow for compatibility

# imgFileName = input("Enter Image File Name: ")
# try:
#     f = open(imgFileName)
#     userMaskX = input("Enter Mask: ")
#     userMaskY = input("by: ")
#     userSigma = input("Enter Sigma: ")
#     oldImage = skimage.io.imread(imgFileName)
#     oldImage = skimage.color.rgb2gray(oldImage)# file opening

#     def applyFilter (image, mask):
#         row, col = image.shape
#         m,n = mask.shape
#         new = np.zeros((row+m-1, col+n-1))
#         n = n//2
#         m = m//2
#         filteredImage = np.zeros(image.shape)
#         new[m:new.shape[0] - m, n:new.shape[1] - n] = image
#         for i in range(m, new.shape[0]- m):
#             for j in range(n, new.shape[1]-n):
#                 temp = new[i-m:i+m+1, j-m:j+m+1]
#                 result = temp*mask
#                 filteredImage[i-m,j-n] = result.sum()
    
#         return filteredImage# filter application

#     def gaussianFormula(m, n, sigma):
#         gaussian = np.zeros((m,n))
#         m = m//2
#         n = n//2
#         for x in range(-m, m+1):
#             for y in range(-n, n+1):
#                 x1 = sigma*(np.pi)**2
#                 x2 = np.exp(-(x**2 + y**2)/(2*sigma**2))
#                 gaussian[x+m, y+n] = (1/x1)*x2
#         return gaussian# filter formula

#     newImage = applyFilter(oldImage, gaussianFormula(int(userMaskX),int(userMaskY),int(userSigma)))
#     plt.imshow(oldImage,cmap = "gray")
#     plt.title("Old Image")
#     plt.figure()
#     plt.imshow(newImage,cmap = "gray")
#     plt.title("New Image")
#     plt.show()
# except IOError:
#     print("File not accessible")



