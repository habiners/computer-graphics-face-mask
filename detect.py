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
    def generateData(self, path):
        files = [f for f in os.listdir(path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))]
        files = files[:3]
        res = []

        for f in files:
            data = self.getFaceData(path + '/' + f)

            for d in data:
                res.append(d)


        res = np.array(res)

        # write into a file 
        resultTxt = open("image_data.txt", "w")
        np.set_printoptions(threshold=sys.maxsize)
        resultTxt.write(res.tostring()) 
        resultTxt.close()

    def getFaceData(self, name):
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

            (eyes, iscore) = self._get_eyes(face, roi) 
            (nose, nscore) = self._get_nose(face, roi, eyes)
            (mouth, mscore) = self._get_mouth(face, roi, nose)

            # displayImage(img)
            # cv2.namedWindow('image',cv2.WINDOW_NORMAL)
            cv2.imshow("image", img)
            cv2.waitKey(1700)
            cv2.destroyAllWindows()

            tag = input("Wearing facemask? (1/0): ")

            obj['face'] = score[index][0] # normalize before iassign ngari
            obj['eyes'] = iscore # normalize before iassign ngari
            obj['nose'] = nscore # normalize before iassign ngari
            obj['mouth'] = mscore # normalize before iassign ngari
            obj['name'] = name
            obj['box'] = [x, y, w, h]
            obj['tag'] = tag

            res.append(obj)

        return res

    # private
    def _get_eyes(self, face, roi, threshold=5):
        (x, y, w, h) = face
        (eyes, level, score) = eye_cascade.detectMultiScale3(roi, 1.05, threshold, outputRejectLevels=True)

        second_highest = highest = roi.shape[1]
        best = second_best = None

        num_eyes = len(eyes)


        for index in range(num_eyes):
            eye = eyes[index]
            (x, y, w, h) = eye

            if y < highest:
                best = index
                highest = y
            elif y < second_highest:
                second_highest = y
                second_best = index
        
        if num_eyes > 1:
            return ([eyes[best], eyes[second_best]], [score[best], score[second_best]])
        
        return (None, 0)

    def _get_nose(self, face, roi, eyes=None, threshold=5):
        (x, y, w, h) = face
        best_nose = None
        (nose, level, score) = nose_cascade.detectMultiScale3(roi, 1.05, threshold, outputRejectLevels=True)

        if len(nose) > 0:
            eye_mid = eyes[1][1] + (eyes[1][3] / 2) if not eyes is None else (y + h) / 2
            nose_diff = 10000
            
            for index in range(len(nose)):
                (ex,ey,ew,eh) = nose[index]
                diff = abs(ey - eye_mid)
                if diff < nose_diff:
                    best_nose = (nose[index], index)
            

        
        return best_nose if not best_nose is None else (None, 0)
    
    def _get_mouth(self, face, roi, nose=None, threshold=5):
        (x, y, w, h) = face
        best_mouth = None
        (mouth, level, score) = mouth_cascade.detectMultiScale3(roi, 1.05, threshold, outputRejectLevels=True)
        if len(mouth) > 0:
            nose_mid = nose[1] + (nose[3] / 2) if not nose is None else (y + h) / 2
            mouth_diff = 10000

            for index in range(len(mouth)):
                (ex,ey,ew,eh) = mouth[index]
                if ey > nose_mid:
                    diff = abs(ey - nose_mid)
                    if diff < mouth_diff:
                        best_mouth = (mouth[index], index)
        
        return best_mouth if not best_mouth is None else (None, 0)



test = Detector()
print(test.generateData('dataset/images'))









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
    #             (x, y, w, h) = face["nose"]
    #             cv2.rectangle(roi,(x,y),(x+w,y+h),(0,0,255),2)

    #         if not face["mouth"] is None:
    #             (x, y, w, h) = face["mouth"]
    #             cv2.rectangle(roi,(x,y),(x+w,y+h),(0,0,0),2)

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
    