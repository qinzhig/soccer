import sqlite3
import pandas as pd
from sklearn import svm
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

from odds_data import getOddsDataForSpanish
from model_helper import predictBySVM,predictByLR,predictGAP,result_accuracy

def predictOdds():

    merged_data = getOddsDataForSpanish()
    #Shuffle and Slice Data for feeding the model
    merged_data = shuffle(merged_data)

    X = merged_data[['power','power_t']]
    y_win = merged_data[['mean_win']]
    y_draw = merged_data[['mean_draw']]
    y_lose = merged_data[['mean_lose']]

    X_train_win, X_test_win, y_train_win, y_test_win = train_test_split(X, y_win, test_size=0.4)
    X_train_draw, X_test_draw, y_train_draw, y_test_draw = train_test_split(X, y_draw, test_size=0.4)
    X_train_lose, X_test_lose, y_train_lose, y_test_lose = train_test_split(X, y_lose, test_size=0.4)

    #Predict using SVM model
    y_test_predict_win = predictBySVM(X_train_win,X_test_win,y_train_win)
    y_test_predict_draw = predictBySVM(X_train_draw,X_test_draw,y_train_draw)
    y_test_predict_lose = predictBySVM(X_train_lose,X_test_lose,y_train_lose)

    y_gap_win = predictGAP(y_test_predict_win,y_test_win)
    y_gap_draw = predictGAP(y_test_predict_draw,y_test_draw)
    y_gap_lose = predictGAP(y_test_predict_lose,y_test_lose)

    print("SVM Win  Accuracy = %.3f" % result_accuracy(y_gap_win, 0.4))
    print("SVM Draw Accuracy = %.3f" % result_accuracy(y_gap_draw, 0.6))
    print("SVM Lose Accuracy = %.3f" % result_accuracy(y_gap_lose, 1.2))

if __name__ == '__main__':
    predictOdds()




