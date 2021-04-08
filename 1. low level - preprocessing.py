# Source: https://www.pluralsight.com/guides/importing-image-data-into-numpy-arrays

import PIL # need to do -> pip install Pillow
print('Pillow Version:', PIL.__version__) # This should run to make sure you have pillow installed

from PIL import Image as I
from PIL import ImageFilter

from matplotlib import image as MI
from matplotlib import pyplot
import numpy
import sys

def getImageInformationUsingPillow(filename):
    image = I.open(filename)
    print(image.format)
    print(image.size)
    print(image.mode)
    image.show() # naay prompt mu ask what to use to open
    print(image)

def getImageInformationUsingMatPlotLib(filename):
    image = MI.imread(filename) # load image as pixel array
    print(f"Image Datatype: {image.dtype}")
    print(f"Image Shape: {image.shape}")

def printAsArray(filename):
    image = I.open(imgFilename) # Open with Pillow Image
    image_arr = numpy.asarray(image) # Convert to numpy array
    print(image_arr)

def printImageAsMatrix(filename):
    image = MI.imread(filename)
    print(image) # Prints the array

def displayImage(image): # NOT filename, needs to be an image/arr jud!
    pyplot.imshow(image) # load it for pyplot.show()
    pyplot.show() # display the array of pixels as an image

def displayTwoImages(image, image2): # NOT filename, needs to be an image/arr jud!
    fig = pyplot.figure()
    fig.add_subplot(121)
    pyplot.title('Original')
    pyplot.imshow(image)
    fig.add_subplot(122)
    pyplot.title('Filtered')
    pyplot.imshow(image2)
    pyplot.show()

def write3dMatrixToTxt(filename):
    image = MI.imread(filename) # read by matplotlib instead of Pillow, so it's array lahos kinda
    print("This may take a while...")
    resultTxt = open("array_image.txt", "w")
    numpy.set_printoptions(threshold=sys.maxsize)
    resultTxt.write(image.__repr__()) # image.__repr__ converts the array into string
    resultTxt.close()
    print("Done!")

def imgToNumpyarr(filename):
    image = I.open(imgFilename) # Open with Pillow Image
    return numpy.asarray(image) # Convert to numpy array

def gaussianBlur(filename, blur):
    image = I.open(imgFilename) # Open with Pillow Image
    return numpy.asarray(image.filter(ImageFilter.GaussianBlur(blur)))

def blackAndWhiteinator(image_arr, bw_threshold=128): # set threshold higher to be more strict (color needs to be brighter) if when mu black
    height, width = image_arr.shape[:2]

    image_bw = numpy.zeros((height, width, 3)) # create empty array composed of zero's
    # image_bw = numpy.zeros((height, width)) # create empty array composed of zero's
    for i in range(height):
        for j in range(width):
            if image_arr[i][j][:3].mean() >= bw_threshold:
                # image_bw[i][j] = 1
                image_bw[i][j] = [255, 255, 255] 

    return image_bw

def gaussianBlurToBW(filename, blur=5, bw_threshold=128):
    return blackAndWhiteinator(gaussianBlur(filename, blur), bw_threshold)

def grayscaleinator(filename):
    image = I.open(imgFilename) # Open with Pillow Image
    image_arr = numpy.asarray(image) # Convert to numpy array
    height, width = image_arr.shape[:2]

    # image_gray = numpy.zeros((height, width)) # create empty array composed of zero's
    image_gray = numpy.zeros((height, width, 3)) # create empty array composed of zero's
    for i in range(height):
        for j in range(width):
            # image_gray[i][j][1] = image_arr[i][j][1]
            image_gray[i][j] = (numpy.multiply(image_arr[i][j][:3], [0.2989, 0.5870, 0.1140]))
            # image_gray[i][j] = numpy.sum(numpy.multiply(image_arr[i][j][:3], [0.2989, 0.5870, 0.1140]))

    # print(image_gray)
    return image_gray


imgFilename = 'test/koala.jpeg'
# imgFilename = 'test/test.jpg'
# imgFilename = 'dataset/images/maksssksksss0.png'
# imgFilename = 'dataset/images/maksssksksss1.png'

def measureTimeDiff(func1, func2): # pass the functions with lambda, eg lambda: blackAndWhiteinator(imgFilename)
    import time
    ts = time.time()
    func1()
    t = (time.time() -ts)
    print("Algo 1: {:} ms".format(t*1000))

    ts = time.time()
    func2()
    t = (time.time() -ts)
    print("Algo 2: {:} ms".format(t*1000))

# measureTimeDiff(lambda: gaussianBlurToBW(imgFilename, 3), lambda: blackAndWhiteinator(imgToNumpyarr(imgFilename)))
# displayImage(gaussianBlur(imgFilename, 3))
# displayImage(blackAndWhiteinator(imgFilename))
displayImage(gaussianBlurToBW(imgFilename, 2, 150))

# displayTwoImages(grayscaleinator(imgFilename), blackAndWhiteinator(imgFilename))
# displayTwoImages(gaussianBlurToBW(imgFilename, 1), blackAndWhiteinator(imgToNumpyarr(imgFilename)))
