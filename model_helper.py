import sqlite3
import pandas as pd
from sklearn import svm
from sklearn import linear_model

#@Author:   Qin Zhi Guo
#@Version:  1.0

#SVM build Model
def predictBySVM(x_train,x_test,y_train):

    clf = svm.SVR()
    clf.fit(x_train, y_train.values.ravel())
    y_predict = clf.predict(x_test)

    return y_predict


#Linear Regression build Model
def predictByARDRegression(x_train,x_test,y_train):

    model = linear_model.ARDRegression()
    model.fit(x_train,y_train.values.ravel())
    y_predict = model.predict(x_test)

    return y_predict

#Linear Regression build Model
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
def setBettingStrategy(y1,y2,y3):
    if y2 - y3 > y2 -y1:
        y1 = y1 * 1.8
        y2 = y2 * 1.2
        if y3 > 1.5:
            y3 = y3 * 0.8
    elif y2 > (y2 - y1)*1.2:
        y2 = y2*1.8
        y3 = y3*2.5
        if y1 > 1.5:
            y1 = y1*0.8

    return y1,y2,y3

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
