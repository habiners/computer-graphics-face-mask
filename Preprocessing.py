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
    image = I.open(filename) # Open with Pillow Image
    image_arr = numpy.asarray(image) # Convert to numpy array
    print(image_arr)

def printImageAsMatrix(filename):
    image = MI.imread(filename)
    print(image) # Prints the array

def displayImage(image): # NOT filename, needs to be an image/arr jud!
    pyplot.imshow(image) # load it for pyplot.show()
    pyplot.show() # display the array of pixels as an image

def displayMultipleImages(*images):
    foo = len(images)
    bazz = 1
    fig = pyplot.figure()
    for image in images:        
        fig.add_subplot(100 + foo * 10 + bazz)
        pyplot.title('Image ' + str(bazz))
        pyplot.imshow(image)
        bazz += 1
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
    image = I.open(filename) # Open with Pillow Image
    return numpy.asarray(image) # Convert to numpy array

def pilImgToNumpyarr(pil_img):
    return numpy.asarray(pil_img) # Convert to numpy array

def numpyarrToPilImg(image_arr):
    return I.fromarray(image_arr.astype('uint8'), 'RGB')

def gaussianBlur(filename, blur=5):
    image = I.open(filename) # Open with Pillow Image
    return numpy.asarray(image.filter(ImageFilter.GaussianBlur(blur)))

def gaussianBlurArr(image_arr, blur=5): # if from numpy array
    image = numpyarrToPilImg(image_arr)
    return numpy.asarray(image.filter(ImageFilter.GaussianBlur(blur)))

def blackAndWhiteinator(image_arr, bw_threshold=128): # set threshold higher to be more strict (color needs to be brighter) if when mu black
    height, width = image_arr.shape[:2]
    rgb = True if len(image_arr.shape) >= 3 else False

    image_bw = numpy.zeros((height, width, 3)) # create empty array composed of zero's
    if rgb:
        for i in range(height):
            for j in range(width):
                if image_arr[i][j][:3].mean() >= bw_threshold:
                    image_bw[i][j] = [255, 255, 255]
    else:
        for i in range(height):
            for j in range(width):
                if image_arr[i][j] >= bw_threshold:
                    image_bw[i][j] = [255, 255, 255]

    return image_bw

def gaussianBlurToBW(filename, blur=5, bw_threshold=128):
    return blackAndWhiteinator(gaussianBlur(filename, blur), bw_threshold)

def grayscaleinator(image_arr):
    height, width = image_arr.shape[:2]

    image_gray = numpy.zeros((height, width)) # create empty array composed of zero's
    for i in range(height):
        for j in range(width):
            image_gray[i][j] = numpy.sum(numpy.multiply(image_arr[i][j][:3], [0.2989, 0.5870, 0.1140]))
    return image_gray

def grayscaleinatorPil(image_arr): # if using Pillow
    image = numpyarrToPilImg(image_arr)
    return image.convert('L')

def grayscaleGaussianBW(filename, blur=5, bw_threshold=128): # Grayscales the image, adds gaussian blur, then converts to b&w
    image = I.open(filename).convert('L').filter(ImageFilter.GaussianBlur(blur)) # Open with Pillow Image and convert to grayscale
    return blackAndWhiteinator(pilImgToNumpyarr(image), bw_threshold)



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

# displayImage(blackAndWhiteinator(imgToNumpyarr(imgFilename), bw_threshold=128))
# displayImage(gaussianBlurToBW(imgFilename, blur=5, bw_threshold=128))
# displayImage(grayscaleGaussianBW(imgFilename, blur=5, bw_threshold=150))

# Immediate B&W vs Gaussian to B&W vs Grayscale to Gaussian to B&W
displayMultipleImages(
    blackAndWhiteinator(imgToNumpyarr(imgFilename), bw_threshold=128), 
    gaussianBlurToBW(imgFilename, blur=5, bw_threshold=128), 
    grayscaleGaussianBW(imgFilename, blur=5, bw_threshold=150)) #def thresh is 128, half of 255
