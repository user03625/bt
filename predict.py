from keras.models import load_model
import pandas as pd
import numpy as np
import math
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("index")
args = parser.parse_args()
index = int(args.index)

model = load_model("model.h5")

df = pd.read_csv("oneShotBigData{}.csv".format(index))

SIZE = 50

fileV = open("vars.txt","r")
TOTAL_SIZE = int(fileV.readline())*16
NONCE_SIZE = int(fileV.readline())*16
fileV.close()
INPUT_SIZE = TOTAL_SIZE - NONCE_SIZE
X = df.values[:SIZE,1:INPUT_SIZE+1]
Y = df.values[:SIZE,INPUT_SIZE+1:]


prediction = model.predict(X)
#prediction = prediction.astype(int)

f = np.vectorize(lambda x: round(x,2))
prediction = f(prediction)


for i in  range(SIZE):
    print("(prediction,label) -> ({},{})".format(prediction[i],Y[i]))

