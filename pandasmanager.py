import os
import datetime
import numpy as np
import pandas as pd
from sklearn import preprocessing


class PandasManager():
    def __init__(self, nCluster=30):
        """
        Init Dataframe
        :param nCluster: number of minutes to take in mind
        """

        self.fullFile = self.readXLSX()
        # replace DateTime with Timestamp
        self.df = self.readLastNCluster(self.fullFile, nCluster)
        #self.printTest()

    def normalizeData(self, df):
        min_max_scaler = preprocessing.MinMaxScaler()
        np_scaled = min_max_scaler.fit_transform(df)
        df_normalized = pd.DataFrame(np_scaled)
        return df_normalized

    def readXLSX(self, path=''):
        fullFile = pd.read_excel('DAT_XLSX_EURUSD_M1_201708.xlsx')

        return fullFile

    def replaceTimeWithTimestamp(self):
        # ToDo # maybe not used, pandas autoconvert datetime
        print self.fullFile['DateTime']

        for row in self.fullFile['DateTime']:
            row = self.getTimestampFromString(row.values)
            print row[0]

        #print self.fullFile['DateTime']

    def readAllDataframe(self):
        return self.fullFile

    def readLastNCluster(self, dataFrame, nCluster):
        """
        Read the latest N row
        :param dataFrame:
        :param nCluster:
        :return:
        """
        #return dataFrame.head(nCluster)
        return dataFrame.tail(nCluster)

    def appendIQCandleRow(self, candle):
        timestamp = candle[-2][0]

        result = 0
        if (candle[-2][2]/1000000) < (candle[-3][2]/1000000):
            result = 0
        else:
            result = 1

        candlesDF = {
            'DateTime': timestamp,
            'Open': candle[-2][1]/1000000,
            'Close': candle[-2][2]/1000000,
            'High': candle[-2][3]/1000000,
            'Low': candle[-2][4]/1000000,
            'Result': result
        }

        self.fullFile.append(candlesDF)

    def getTimeFromTimestamp(self, timestamp):
        """
        Return time as a String
        :param timestamp: string or int
        :return: String
        """
        # datetime.datetime.fromtimestamp(int(candles[-1][0])).strftime('%Y-%m-%d %H:%M:%S')
        return datetime.datetime.fromtimestamp(int(timestamp).strftime('%Y-%m-%d %H:%M:%S'))

    def getTimestampFromString(self, timeString):
        """
        Return timestamp from string with format: Y-%m-%d %H:%M:%S
        :param timeString: string
        :return: int
        """
        return datetime.time.mktime(datetime.datetime.strptime(timeString, '%Y-%m-%d %H:%M:%S').timetuple())


    def printTest(self):
        #print self.df.head()
        #print self.df.shape
        #print self.df.ix[:,:-1] # tutto tranne la colonna result
        print self.df.as_matrix() # return ndarray, Numpy-array
        self.replaceTimeWithTimestamp()


if __name__ == "__main__":
    test = PandasManager()

    import neuralnetwork as nn

    mNN = nn.IqNeuralNetwork()
    matrix = test.readAllDataframe()
    matrix = matrix.drop('DateTime', axis=1)
    x_train, y_train, x_test, y_test = mNN.load_data(matrix, 30)
    #print x_train
    mNN.train(x_train, y_train)