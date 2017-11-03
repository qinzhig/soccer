import sqlite3
import pandas as pd
from sklearn import svm
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn import linear_model
import numpy as np
from pandas import Series, DataFrame

from odds_data import getOddsDataForSpanish

def predictOdds():

    merged_data = getOddsDataForSpanish()
    #Shuffle and Slice Data for feeding the model
    merged_data = shuffle(merged_data)

    X = merged_data[['power','power_t']]
    y_win = merged_data[['mean_win']]
    y_draw = merged_data[['mean_draw']]
    y_lose = merged_data[['mean_lose']]

    X_train_win, X_test_win, y_train_win, y_test_win = train_test_split(X, y_win, test_size=0.2)
    X_train_draw, X_test_draw, y_train_draw, y_test_draw = train_test_split(X, y_draw, test_size=0.2)
    X_train_lose, X_test_lose, y_train_lose, y_test_lose = train_test_split(X, y_lose, test_size=0.2)

    #Predict using SVM model
    y_test_predict_win = predictBySVM(X_train_win,X_test_win,y_train_win)
    y_test_predict_draw = predictBySVM(X_train_draw,X_test_draw,y_train_draw)
    y_test_predict_lose = predictBySVM(X_train_lose,X_test_lose,y_train_lose)

    y_gap_win = predictGAP(y_test_predict_win,y_test_win)
    y_gap_draw = predictGAP(y_test_predict_draw,y_test_draw)
    y_gap_lose = predictGAP(y_test_predict_lose,y_test_lose)

    print("SVM Win Accuracy = %.3f" % result_accuracy(y_gap_win, 0.4))
    print("SVM Draw Accuracy = %.3f" % result_accuracy(y_gap_draw, 0.6))
    print("SVM Lose Accuracy = %.3f" % result_accuracy(y_gap_lose, 1.2))

#SVM build Model
def predictBySVM(x_train,x_test,y_train):

    clf = svm.SVR()
    clf.fit(x_train, y_train.values.ravel())
    y_predict = clf.predict(x_test)

    return y_predict

#SVM build Model
def predictByLR(x_train,x_test,y_train):

    model = linear_model.LinearRegression()
    model.fit(x_train,y_train.values.ravel())
    y_predict = model.predict(x_test)

    return y_predict

#Result gap caculation
def predictGAP(y_predict,y_actual):
    y_actual = y_actual.astype(float).fillna(0.000)
    y_gap = y_predict - y_actual.values.ravel()

    return y_gap

# Prediction accuracy caculation Function for the test dataset
def result_accuracy(result,var):
    count = 0
    len = 0
    for num in result:
        len = len + 1
        if abs(num) <= var:
            count = count +1

    count=round(count,3)
    len=round(len,3)

    return (count/len)

if __name__ == '__main__':
    predictOdds()




