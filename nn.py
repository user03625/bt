import pandas as pd
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, LSTM, Dropout
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from keras import regularizers
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("index")
args = parser.parse_args()
index = int(args.index)

NUMBER_OF_EPOCHS = 100 
BATCH_SIZE = 256 

df = pd.read_csv('oneShotBigData{}.csv'.format(index))
df = df.sample(frac=1).reset_index(drop=True)

fileV = open('vars.txt','r')
TOTAL_SIZE = int(fileV.readline())*16
NONCE_SIZE = int(fileV.readline())*16
fileV.close()
INPUT_SIZE = TOTAL_SIZE-NONCE_SIZE

X = df.values[:,1:INPUT_SIZE+1]
Y = df.values[:,INPUT_SIZE+1:]

#minMaxScaler = preprocessing.MinMaxScaler()
#X  = minMaxScaler.fit_transform(X)
def fooBar():
    def numberToOneShot(number):
        size =  10
        l = [0]*size
        l[number]=1
        return l

    Y2  = np.zeros(shape  = (Y.size,10))

    for i in range(Y.size):
        oneShot = numberToOneShot(Y[i])
        for j in range(10):
            Y2[i][j] =  oneShot[j] 
    Y=Y2



X_train, X_val_and_test, Y_train, Y_val_and_test = train_test_split(X,Y,test_size=0.3)
X_val, X_test, Y_val, Y_test = train_test_split(X_val_and_test, Y_val_and_test, test_size=0.1)


#print(Y2[:50])
#exit()

def createModel():
    activationType = 'selu'
    model = Sequential()
    model.add(Dense(512,activation = activationType, input_shape=(INPUT_SIZE,)))
    model.add(Dropout(0.2))
    model.add(Dense(512,activation = activationType))
    model.add(Dropout(0.2))
    model.add(Dense(512,activation = activationType))
    model.add(Dropout(0.2))

    #model.add(LSTM(200,dropout = 0.2,recurrent_dropout = 0.2,input_shape=(1,INPUT_SIZE),return_sequences=True))
    #model.add(LSTM(200,dropout = 0.2,recurrent_dropout = 0.2))
    model.add(Dense(16, activation = 'softmax'))
    model.compile(optimizer='adam',loss='categorical_crossentropy',metrics = ['accuracy'])
    return model


#model = createModel()
model = load_model("model.h5")

history = model.fit(X_train, Y_train, epochs = NUMBER_OF_EPOCHS, batch_size = BATCH_SIZE, verbose=1,validation_data = (X_val,Y_val))
model.save('model.h5')

print(model.metrics_names)
print(model.evaluate(X_test, Y_test))
