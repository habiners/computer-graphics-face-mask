############################### Mid Level Smoothing ###############
import matplotlib.pyplot as plt
import numpy as np
import skimage.io

imgFileName = input("Enter Image File Name: ")
try:
    f = open(imgFileName)
    userMaskX = input("Enter Mask: ")
    userMaskY = input("by: ")
    userSigma = input("Enter Sigma: ")
    oldImage = skimage.io.imread(imgFileName)
    oldImage = skimage.color.rgb2gray(oldImage)# file opening

    def applyFilter (image, mask):
        row, col = image.shape
        m,n = mask.shape
        new = np.zeros((row+m-1, col+n-1))
        n = n//2
        m = m//2
        filteredImage = np.zeros(image.shape)
        new[m:new.shape[0] - m, n:new.shape[1] - n] = image
        for i in range(m, new.shape[0]- m):
            for j in range(n, new.shape[1]-n):
                temp = new[i-m:i+m+1, j-m:j+m+1]
                result = temp*mask
                filteredImage[i-m,j-n] = result.sum()
    
        return filteredImage# filter application

    def gaussianFormula(m, n, sigma):
        gaussian = np.zeros((m,n))
        m = m//2
        n = n//2
        for x in range(-m, m+1):
            for y in range(-n, n+1):
                x1 = sigma*(np.pi)**2
                x2 = np.exp(-(x**2 + y**2)/(2*sigma**2))
                gaussian[x+m, y+n] = (1/x1)*x2
        return gaussian# filter formula

    newImage = applyFilter(oldImage, gaussianFormula(int(userMaskX),int(userMaskY),int(userSigma)))
    plt.imshow(oldImage,cmap = "gray")
    plt.title("Old Image")
    plt.figure()
    plt.imshow(newImage,cmap = "gray")
    plt.title("New Image")
    plt.show()
except IOError:
    print("File not accessible")
############################### Mid Level Smoothing ###############