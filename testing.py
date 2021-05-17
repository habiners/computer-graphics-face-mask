import pandas as pd
import numpy as np
import pickle
from detect import Detector



with open('FaceMaskModel', 'rb') as f:
    model = pickle.load(f)

testimage = 'testdata/testdata5.jpg'
dt = Detector()
pp = dt.get_face_data(testimage, False)

scores = []
for face in pp:
    score = np.fromiter(pp[0].values(), dtype=float)
    scores.append(score)

scores = np.array(scores)
print(scores)

result = False
for x in scores:
    pred = model.predict(x)
    print(pred)
    if pred == 1:
        result = True

print(result)

def mask_detector(filename):
    # testimage = 'testdata/testdata1.jpg'
    dt = Detector()
    pp = dt.get_face_data(filename, False)

    scores = []
    for face in pp:
        score = np.fromiter(pp[0].values(), dtype=float)
        scores.append(score)

    scores = np.array(scores)
    print(scores)

    result = False

    for x in scores:
        pred = model.predict(x)
        if pred == 1: # if naay isa ka 1, then true
            result = True

    return result



