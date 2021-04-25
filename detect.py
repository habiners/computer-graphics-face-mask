import numpy as np
import cv2
from Preprocessing import gaussianBlur, displayImage, grayscaleinator as gs, imgToNumpyarr

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
nose_cascade = cv2.CascadeClassifier('classifier/nose.xml')
mouth_cascade = cv2.CascadeClassifier('classifier/mouth.xml')



 
class Detector:
    def getFaceData(self, name):
        # img = cv2.imread('dataset/images/maksssksksss0.png')
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = gaussianBlur(name, 2)
        gray = np.array(gs(img), dtype="uint8")
        faces = face_cascade.detectMultiScale(gray, 1.5, 2)


        res = {}

        """
            {
                test/image1.jpg: [
                    {
                        face: (1,2,3,4),
                        eyes: [(1,2,3,4), (1,2,3,4)],
                        nose: (1,2,3,4)
                        mouth: (1,2,3,4)
                    }
                ]
            }
        """

        arr = []

        for face in faces:
            obj = {}
            (x, y, w, h) = face
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi = gray[y:y+h, x:x+w]
            obj["coord"] = face
            obj["eyes"] = eyes = self._get_eyes(face, roi)
            obj["nose"] = nose = self._get_nose(face, roi, eyes)
            obj["mouth"] = self._get_mouth(face, roi, nose)
            arr.append(obj)

        res[name] = arr
        return res

    def displayFaceData(self, obj):
        key = list(obj)[0]
        img = imgToNumpyarr(key)
        item = obj[key]

        for face in item:
            (x, y, w, h) = face["coord"]
            roi = img[y:y+h, x:x+w]
            
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

            if not face["eyes"] is None:
                for (x, y, w, h) in face['eyes']:
                    cv2.rectangle(roi,(x,y),(x+w,y+h),(0,255,0),2)

            if not face["nose"] is None:
                (x, y, w, h) = face["nose"]
                cv2.rectangle(roi,(x,y),(x+w,y+h),(0,0,255),2)

            if not face["mouth"] is None:
                (x, y, w, h) = face["mouth"]
                cv2.rectangle(roi,(x,y),(x+w,y+h),(0,0,0),2)

        displayImage(img)
    # private
    def _get_eyes(self, face, roi, threshold=5):
        (x, y, w, h) = face
        eyes = eye_cascade.detectMultiScale(roi ,1.1, threshold)

        if len(eyes) > 0:
            eyes = eyes[eyes[:,1].argsort()]
            best_eyes = [eyes[0]]

            if len(eyes) > 1:
                best_eyes.append(eyes[1])

            return best_eyes
        else:
            return None
    
    def _get_nose(self, face, roi, eyes=None, threshold=5):
        (x, y, w, h) = face
        best_nose = None
        nose = nose_cascade.detectMultiScale(roi, 1.1, threshold)
        if len(nose) > 0:
            eye_mid = eyes[1][1] + (eyes[1][3] / 2) if not eyes is None else (y + h) / 2
            nose_diff = 10000
            
            for i in nose:
                (ex,ey,ew,eh) = i
                diff = abs(ey - eye_mid)
                if diff < nose_diff:
                    best_nose = i
            
            return best_nose
    
    def _get_mouth(self, face, roi, nose=None, threshold=5):
        (x, y, w, h) = face
        best_mouth = None
        mouth = mouth_cascade.detectMultiScale(roi,1.1, threshold)
        if len(mouth) > 0:
            nose_mid = nose[1] + (nose[3] / 2) if not nose is None else (y + h) / 2
            mouth_diff = 10000
                
            for i in mouth:
                (ex,ey,ew,eh) = i
                if ey > nose_mid:
                    diff = abs(ey - nose_mid)
                    if diff < mouth_diff:
                        best_mouth = i
        
        return best_mouth
    

# test = Detector()
# data = test.getFaceData('dataset/images/maksssksksss250.png')
# print(data)
# test.displayFaceData(data)
