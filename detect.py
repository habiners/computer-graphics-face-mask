import numpy as np
import cv2
from Preprocessing import gaussianBlur, displayImage, grayscaleinator as gs, imgToNumpyarr
import os
import sys

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
nose_cascade = cv2.CascadeClassifier('classifier/nose.xml')
mouth_cascade = cv2.CascadeClassifier('classifier/mouth.xml')




# """"

# - [/] Convert the face, eyes, nose, and mouth to use the detectMultiScale3
# - [/] Retrieve the confidence rate of the facial features
# - [/] Combine them to a single object

# {
#     face: 0.6,
#     eyes: 0.6,
#     nose: 0.6,
#     mouth: 0.6,
#     tag: 1
# }

# - [/] Run this function on all the images in the data set so that all the weights of the faces in the dataset can be gathered into one array



# [
#    {
#         face: 0.6,
#         eyes: 0.6,
#         nose: 0.6,
#         mouth: 0.6,
#         tag: 1
#     },
#    {
#         face: 0.6,
#         eyes: 0.6,
#         nose: 0.6,
#         mouth: 0.6,
#         tag: 1`
#     },
#    {
#         face: 0.6,
#         eyes: 0.6,
#         nose: 0.6,
#         mouth: 0.6,
#         tag: 1
#     },
# ]

# - [/] Export this array into another file


# """"


 
class Detector:
    def get_multiple_face_data(self, path, test=True):
        files = [f for f in os.listdir(path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))]
        #files = files[0:20]
        res = []

        for f in files:
            data = self.get_face_data(path + '/' + f, test)

            for d in data:
                res.append(d)

        return res

    def get_face_data(self, name, test=True):
        blurred = gaussianBlur(name, 2)
        gray = np.array(gs(blurred), dtype="uint8")
        (faces, level, score) = face_cascade.detectMultiScale3(gray, 1.1, 2, outputRejectLevels=True)

        res = []
        img = cv2.imread(name, cv2.IMREAD_COLOR)

        for index in range(len(faces)):
            obj = {}
            face = faces[index]
            (x, y, w, h) = face

            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]

            (eyes, iscore) = self._get_eyes(face, roi, roi_color) 
            (nose, nscore) = self._get_nose(face, roi, roi_color, eyes)
            (mouth, mscore) = self._get_mouth(face, roi, roi_color)
            
            obj['face'] = score[index][0] # normalize before iassign ngari
            obj['eye1'] = iscore[0] # normalize before iassign ngari
            obj['eye2'] = iscore[1] # normalize before iassign ngari
            obj['nose'] = nscore # normalize before iassign ngari
            obj['mouth'] = mscore # normalize before iassign ngari

            if test == True:
                cv2.imshow("image", img)
                cv2.waitKey(1200)
                cv2.destroyAllWindows()
                tag = input("Wearing facemask? (1/0): ")
                obj['name'] = name
                obj['box'] = [x, y, w, h]
                obj['tag'] = tag

            res.append(obj)

        return res

    # private
    def _get_eyes(self, face, roi, image, threshold=5):
        (eyes, level, score) = eye_cascade.detectMultiScale3(roi, 1.05, threshold, outputRejectLevels=True)

        second_highest = highest = roi.shape[1]
        best = second_best = None

        num_eyes = len(eyes)

        for index in range(num_eyes):
            eye = eyes[index]
            (x, y, w, h) = eye

            if y < highest:
                second_highest = highest
                second_best = best
                highest = y
                best = index
            elif y < second_highest:
                second_highest = y
                second_best = index
        
        for index in range(num_eyes):
            if index == best or index == second_best:
                (x, y, w, h) = eyes[index]
                cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
        
        to_return = [[None, None], [0,0]]

        to_return[0][0] = eyes[best] if not best is None else None
        to_return[1][0] = score[best] if not best is None else 0
        to_return[0][1] = eyes[second_best] if not second_best is None else None
        to_return[1][1] = score[second_best] if not second_best is None else 0

        return to_return

    def _get_nose(self, face, roi, image, eyes=None, threshold=5):
        best_nose = None
        (nose, level, score) = nose_cascade.detectMultiScale3(roi, 1.05, threshold, outputRejectLevels=True)

        if len(nose) > 0:
            mid = roi.shape[1] / 2
            nose_diff = 10000
            iy = eyes[0][1] if not eyes[0] is None else 0
            
            for index in range(len(nose)):
                (ex,ey,ew,eh) = nose[index]
                diff = abs(ey - mid)
                if diff < nose_diff and ey > iy:
                    best_nose = index
        
        score = list(map(lambda a: a[0], score))

        if not best_nose is None:
            (x, y, w, h) = nose[best_nose]
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
            return (nose[best_nose], score[best_nose])

        return (None, 0)
    
    def _get_mouth(self, face, roi, image, nose=None, threshold=5):
        best_mouth = None
        (mouth, level, score) = mouth_cascade.detectMultiScale3(roi, 1.05, threshold, outputRejectLevels=True)
        
        if len(mouth) > 0:
            mid = roi.shape[1] / 2
            mouth_diff = 0

            for index in range(len(mouth)):
                (ex,ey,ew,eh) = mouth[index]
                if ey > mid:
                    diff = abs(ey - mid)
                    if diff > mouth_diff:
                        best_mouth = index
        
        score = list(map(lambda a: a[0], score))
        
        if not best_mouth is None:
            (x, y, w, h) = mouth[best_mouth]
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,0),2)
            return (mouth[best_mouth], score[best_mouth])

        return (None, 0)



test = Detector()
res = test.get_multiple_face_data('dataset/images')

# write
resultTxt = open("image_data.txt", "w")
np.set_printoptions(threshold=sys.maxsize)
resultTxt.write(res.__repr__()) 
resultTxt.close()







            # mid = eyes[1][1] + (eyes[1][3] / 2) if not eyes[1] is None else (y + h) / 2
            # nose_mid = nose[1] + (nose[3] / 2) if not nose is None else (y + h) / 2


        # res = {}

        # """
        #     {
        #         test/image1.jpg: [
        #             {
        #                 face: (1,2,3,4),
        #                 eyes: [(1,2,3,4), (1,2,3,4)],
        #                 nose: (1,2,3,4)
        #                 mouth: (1,2,3,4),
        #             }
        #         ]
        #     }
        # """

        # arr = []

        # for face in faces:
        #     obj = {}
        #     (x, y, w, h) = face
        #     cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        #     roi = gray[y:y+h, x:x+w]
        #     obj["coord"] = face
        #     obj["eyes"] = (eyes, iscore) = self._get_eyes(face, roi)
        #     obj["nose"] = (nose, nscore) = self._get_nose(face, roi, eyes)
        #     obj["mouth"] = self._get_mouth(face, roi, nose)
        #     arr.append(obj)

        # res[name] = arr
        # return res

    # def displayFaceData(self, obj):
    #     key = list(obj)[0]
    #     img = imgToNumpyarr(key)
    #     item = obj[key]

    #     for face in item:
    #         (x, y, w, h) = face["coord"]
    #         roi = img[y:y+h, x:x+w]
            
    #         cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

    #         if not face["eyes"] is None:
    #             for (x, y, w, h) in face['eyes']:
    #                 cv2.rectangle(roi,(x,y),(x+w,y+h),(0,255,0),2)

    #         if not face["nose"] is None:
                # (x, y, w, h) = face["nose"]
                # cv2.rectangle(roi,(x,y),(x+w,y+h),(0,0,255),2)

    #         if not face["mouth"] is None:
                # (x, y, w, h) = face["mouth"]
                # cv2.rectangle(roi,(x,y),(x+w,y+h),(0,0,0),2)

    #     displayImage(img)  

        # loop sa eyes
        # compare with current best
            # if best then replace current to this
        # return (eyes, score)



        # libog
        # if len(eyes) > 0:
        #     eyes = eyes[eyes[:,1].argsort()]
        #     best_eyes = [eyes[0]]

        #     if len(eyes) > 1:
        #         best_eyes.append(eyes[1])

        #     return best_eyes
        # else:
        #     return None
    