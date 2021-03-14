# Source: https://www.pluralsight.com/guides/importing-image-data-into-numpy-arrays

import PIL # need to do -> pip install Pillow
print('Pillow Version:', PIL.__version__) # This should run to make sure you have pillow installed

from PIL import Image as I

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

def write3dMatrixToTxt(filename):
    image = MI.imread(filename) # read by matplotlib instead of Pillow, so it's array lahos kinda
    print("This may take a while...")
    resultTxt = open("array_image.txt", "w")
    numpy.set_printoptions(threshold=sys.maxsize)
    resultTxt.write(image.__repr__()) # image.__repr__ converts the array into string
    resultTxt.close()
    print("Done!")
    height, width, channels = image_arr.shape

def blackAndWhiteinatorOld(filename):
    image = I.open(imgFilename) # Open with Pillow Image
    image_arr = numpy.asarray(image) # Convert to numpy array

    # given a 800x450 image, the size of the arrays are arr[450][800][3]
    # this means first index is prolly height, 2nd index is width and final index is channel
    image_bw = image_arr.copy() # make a copy of the array so that they don't point to same reference since pic is read-only
    bw_threshold = 128 # set it higher to be more strict (color needs to be brighter) if when mu black
    for height in range(len(image_bw)):
        for width in range(len(image_bw[height])):
            for channels in range(len(image_bw[height][width])):
                if len(image_bw[height][width]) == 3:
                    image_bw[height][width] = [255, 255, 255] if image_bw[height][width].mean() >= bw_threshold else [0, 0, 0]
                elif len(image_bw[height][width]) == 4: # naay alpha channel
                    image_bw[height][width] = [255, 255, 255, 255] if image_bw[height][width][:3].mean() >= bw_threshold else [0, 0, 0, 255]

    displayImage(image_bw)
    # return image_bw

def blackAndWhiteinator(filename):
    image = I.open(imgFilename) # Open with Pillow Image
    image_arr = numpy.asarray(image) # Convert to numpy array
    height, width = image_arr.shape[:2]

    image_bw = numpy.zeros((height, width, 3)) # create empty array composed of zero's
    bw_threshold = 128 # set it higher to be more strict (color needs to be brighter) if when mu black
    for i in range(height):
        for j in range(width):
            image_bw[i][j] = [255, 255, 255] if image_arr[i][j].mean() >= bw_threshold else [0, 0, 0]

    # displayImage(image_bw)
    return image_bw


# imgFilename = 'test/koala.jpeg'
imgFilename = 'dataset/images/maksssksksss1.png'
# printAsArray(imgFilename)

def measureTimeDiff(): # don't forget to comment the displaying of the images
    import time
    ts = time.time()
    blackAndWhiteinatorOld(imgFilename)
    t = (time.time() -ts)
    print("Old Algo: {:} ms".format(t*1000))

    ts = time.time()
    blackAndWhiteinator(imgFilename)
    t = (time.time() -ts)
    print("New Algo: {:} ms".format(t*1000))

blackAndWhiteinator(imgFilename)
