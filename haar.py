import numpy as np
import cv2
from Preprocessing import gaussianBlur, displayImage, grayscaleinator as gs, imgToNumpyarr


"""

resize	
grayscale	
Make integral image function	
Run haar function		
> loop sa image	
	
output: generate 2d array	
feed csv into adaboost	
make xml	


"""


class Detector:
    @staticmethod
    def makeXML(csv):
        print("Hello world")

    @staticmethod
    def _haar(image):
        image = Detector._resize(image, 200)
        gray = np.array(gs(image), dtype="uint8")
        integral = cv2.integral(gray)
        
        integral = integral[1:, 1:]

        h, w = integral.shape
        
        # loop for first rect
        

        while True:
            # dynamic ang shape
            # to be changed
            x, y = 2, 1
            rect = np.zeros((2, 1), dtype=int)
            rect_h, rect_w = rect.shape

            if rect_h <= h and rect_w <= w:
                break

            """

              0 1 2 3 4 5
            0[][][][][][]
            1[][][][][][]
            2[][][][][][]
            3[][][][][][]
            4[][][][][][]
            5[][][][][][]

            """

            # range(0, 5) = iterate through 0, 1, 2, 3, 4 
            # for that rect

            for row in range(0, h - rect_h + 1):
                for col in range(0, w - rect_w + 1):
                    val = Detector._area1(row, col, integral, rect)


        # expected output to be fed sa cascade_classifier/adaboost

        """

        FOR FACES

                feature1        feature2        feature3            feature10000000         class
        image   132             123             32                  8                       Face
        image2  132             123             32                  8                       Face
        image3  132             123             32                  8                       Face
        image3  132             123             32                  8                       Face
        image3  132             123             32                  8                       Face
        

        FOR NONFACES

                feature1        feature2        feature3            feature10000000         class
        image   132             123             32                  8                       NonFace
        image2  132             123             32                  8                       NonFace
        image3  132             123             32                  8                       NonFace


        """

        # loop for second rect
        # for row in image:
        #     for col in image:
                

        # loop for third rect
        # for row in image:
        #     for col in image:
                


        # loop for fourth rect
        # for row in image:
        #     for col in image:

        # loop here
        # haar
    

    def _checkHaar(row, col, image, rect):
        if not image:
            raise Exception("Image not valid")
        
        rect_h, rect_w = rect.shape
        im_h, im_w = image.shape

        if row + rect_h - 1 > im_h or col + rect_w - 1 > im_w:
            raise Exception(f"Invalid coordinates {row},{col} for rectangle of shape {rect_h},{rect_w}")

    # [b][b]
    # [b][b]
    # [w][w]
    # [w][w]

    def _area1(row, col, image, rect):
        rect_h, rect_w = rect.shape
        im_h, im_w = image.shape

        try:
            Detector._checkHaar(row, col, image, rect)

            if rect_h%2 != 0:
                raise Exception(f"Invalid shape for rectangle {rect_h}{rect_w}")
        except Exception as e:
            print(e)

        mini_rect = np.zeros((int(rect_h/2), rect_w), dtype=int)

        black = Detector._findarea(row, col, image, mini_rect)
        white = Detector._findarea(int(row + rect_h/2), col, image, mini_rect)

        return black - white
        
    # [w][w][b][b]
    # [w][w][b][b]

    def _area2(row, col, image, rect):
        rect_h, rect_w = rect.shape
        im_h, im_w = image.shape
        
        try:
            Detector._checkHaar(row, col, image, rect)
            
            if rect_w%2 != 0:
                raise Exception(f"Invalid shape for rectangle {rect_h}{rect_w}")
        except Exception as e:
            print(e)
        

        mini_rect = np.zeros((rect_h, int(rect_w/2)), dtype=int)

        white = Detector._findarea(row, col, image, mini_rect)
        black = Detector._findarea(row, col + int(rect_w/2), image, mini_rect)

        return black - white
        
    # [w][b][w]
    # [w][b][w]
    
    def _area3(row, col, image, rect):
        rect_h, rect_w = rect.shape
        im_h, im_w = image.shape
        
        try:
            Detector._checkHaar(row, col, image, rect)

            if rect_w%3 != 0:
                raise Exception(f"Invalid shape for rectangle {rect_h}{rect_w}")
        except Exception as e:
            print(e)
        
        mini_rect = np.zeros((rect_h, int(rect_w/3)), dtype=int)

        white1_area = Detector._findarea(row, col, image, mini_rect)
        black1_area = Detector._findarea(row, col + int(rect_w/3), image, mini_rect)
        white2_area = Detector._findarea(row, col + int(rect_w * 2/3), image, mini_rect)

        return black1_area - white1_area - white2_area

    # [w][b]
    # [b][w]
    def _area4(row, col, image, rect):
        rect_h, rect_w = rect.shape
        im_h, im_w = image.shape
        try:
            Detector._checkHaar(row, col, image, rect)

            if rect_h%2 != 0 or  rect_w%2 != 0:
                raise Exception(f"Invalid shape for rectangle {rect_h}{rect_w}")

        except Exception as e:
            print(e)
            
        mini_rect = np.zeros((int(rect_h/2), int(rect_w/2)), dtype=int)

        white1_area = Detector._findarea(row, col, image, mini_rect)
        black1_area = Detector._findarea(row, col + int(rect_w/2), image, mini_rect)

        black2_area = Detector._findarea(row + int(rect_h/2), col, image, mini_rect)
        white2_area = Detector._findarea(row + int(rect_h/2), col + int(rect_w/2), image, mini_rect)

        return black1_area + black2_area - white1_area - white2_area

    
    def _findarea(row, col, image, rect):
        rect_h, rect_w = rect.shape
        im_h, im_w = image.shape
        
        bottom_right = image[row + rect_h - 1][col + rect_w - 1]

        # if way top and left
        if row - 1 < 0 and col - 1 < 0:
            whole_area = bottom_right
        
        # if way left but naay top
        elif col - 1 < 0:
            whole_area = bottom_right - image[row - 1][col + rect_w - 1]
        
        # if way top but naay left
        elif row - 1 < 0:
            whole_area = bottom_right - image[row + rect_h - 1][col - 1]

        # else
        else:
            whole_area = bottom_right - image[row - 1][col + rect_w - 1] - image[row + rect_h - 1][col - 1] + image[row - 1][col - 1]

        return whole_area


    @staticmethod
    def _resize(image, w):
        image = imgToNumpyarr(image)
        percent = w/image.shape[1]
        h = int(percent * image.shape[0])
        return cv2.resize(image, (w, h))



# driver

# Detector.makeXML("test")
Detector._haar("dataset\images\maksssksksss14.png")
