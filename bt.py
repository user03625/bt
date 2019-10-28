import pandas as pd
import math
import argparse

def createSeparatedDF():
    def mergeData():
        df1 = pd.read_csv("data.csv",index_col=0)
        df2 = pd.read_csv("data2.csv",index_col=0)
        df3 = pd.read_csv("data3.csv",index_col=0)

        #df1.reset_index(inplace=True,drop=True)
        #df2.reset_index(inplace=True,drop=True)
        #df3.reset_index(inplace=True,drop=True)
        print(df1)
        print(df2)
        print(df3)

        bigDF = pd.concat([df1,df2,df3])

        #bigDF.reset_index(inplace=True)

        bigDF.to_csv("bigData.csv")

    def joinLists(row,features):
            l=[]
            for column in  features:
                l+=row[column]
            return l

    def splitNumber(number,maxSize):
        numberList = list(str(number))
        remainderSize = maxSize - len(numberList)
        l=[0]*remainderSize
        return l+numberList

    def getNumberLength(number):
        return len(list(str(number)))

    df = pd.read_csv("bigData.csv")
    #columns = ["version","prev","merkle","timestamp","utc","bits","nonce","difficulty","hash"]
    columns = ["version","prev","merkle","timestamp","bits","nonce"]
    df = df[columns]

    print(df)

    PREV_SIZE = 64
    MERKLE_SIZE = 64
    VERSION_SIZE = getNumberLength(df.version.max())
    TIMESTAMP_SIZE = getNumberLength(df.timestamp.max())
    BITS_SIZE = getNumberLength(df.bits.max())
    #NONCE_SIZE = getNumberLength(df.nonce.max())
    NONCE_SIZE = 1 
    TOTAL_SIZE = VERSION_SIZE + PREV_SIZE + MERKLE_SIZE + TIMESTAMP_SIZE + BITS_SIZE + NONCE_SIZE


    print("{}_SIZE = {}".format("VERSION",VERSION_SIZE)) 
    print("{}_SIZE = {}".format("TIMESTAMP",TIMESTAMP_SIZE)) 
    print("{}_SIZE = {}".format("BITS",BITS_SIZE)) 
    print("{}_SIZE = {}".format("NONCE",NONCE_SIZE)) 
    fileV = open("vars.txt","w")
    fileV.write(str(TOTAL_SIZE)+"\n")
    fileV.write(str(NONCE_SIZE)+"\n")
    fileV.close()


    dictSize = {
            "version":VERSION_SIZE,
            "prev":PREV_SIZE,
            "merkle":MERKLE_SIZE,
            "timestamp":TIMESTAMP_SIZE,
            "bits":BITS_SIZE,
            "nonce":NONCE_SIZE
            }


    columnsToTransform = ["version","prev","merkle","timestamp","bits"]

    def getSignificantDigit(digitList):
        return [digitList[0]]

    MAX_NONCE_SIZE  =  10

    for column in columnsToTransform:
        print("Split Number for column {}".format(column))
        df[column]=df[column].map(lambda x: splitNumber(x,dictSize[column]))
    #df["nonce"] = df["nonce"].map(lambda x: [math.log(x)])
    df["nonce"] = df["nonce"].map(lambda x: getSignificantDigit(splitNumber(x,MAX_NONCE_SIZE)))

    print("Join lists")
    df['joined_list'] = df.apply(lambda row: joinLists(row,columns), axis = 1)

    separatedFeatures = []
    for i in range(TOTAL_SIZE):
        separatedFeatures.append(str(i))
    print("Create separated data frame")
    separatedDF = pd.DataFrame(df.joined_list.tolist(),columns=separatedFeatures)
    separatedDF.replace(['a','b','c','d','e','f'],['10','11','12','13','14','15'],inplace  = True)

    
    separatedDF = separatedDF.sample(frac=1).reset_index(drop=True)

    separatedDF.to_csv("separatedDF.csv")


#=======================================================================================================
def createOneShotDF():
    separatedDF = pd.read_csv("separatedDF.csv")
    fileV = open('vars.txt','r')
    TOTAL_SIZE = int(fileV.readline())
    fileV.close()

    separatedFeatures = []
    for i in range(TOTAL_SIZE):
        separatedFeatures.append(str(i))

    parser = argparse.ArgumentParser()
    parser.add_argument("index")
    args = parser.parse_args()

    index = int(args.index)


    if index == 1:
        separatedDF=separatedDF[:100000]
    elif index == 2:
        separatedDF=separatedDF[100000:200000]
    elif index == 3:
        separatedDF=separatedDF[200000:300000]
    elif index == 4:
        separatedDF=separatedDF[300000:400000]
    elif index == 5:
        separatedDF=separatedDF[400000:500000]
    elif index == 6:
        separatedDF=separatedDF[500000:]

    def numberToOneShot(number,size):
        l = [0]*size
        l[number]=1
        return l
     
    def joinLists(row,features):
        l=[]
        for column in  features:
            l+=row[column]
        return l

    print("Apply oneShot")
    ONE_SHOT_SIZE = 16
    for column in  separatedFeatures:
        separatedDF[column] = separatedDF[column].map(lambda x:numberToOneShot(x,ONE_SHOT_SIZE))

    oneShotFeatures = []
    for i in range(TOTAL_SIZE * 16):
        oneShotFeatures.append(str(i))

    print("join oneShot lists")
    separatedDF['joined_list'] = separatedDF.apply(lambda row: joinLists(row,separatedFeatures),axis =1)
    print("Create oneShot DataFrame")
    oneShotDF = pd.DataFrame(separatedDF.joined_list.tolist(),columns=oneShotFeatures)

    print("Write data frame to csv file")
    oneShotDF.to_csv("oneShotBigData{}.csv".format(index))


#createSeparatedDF()
createOneShotDF()

