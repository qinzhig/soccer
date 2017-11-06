from pandas.core.frame import DataFrame
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn import tree
from sklearn import metrics
from sklearn.naive_bayes import GaussianNB

from gap_data import getMatchHistory
from classifier_helper import getAccuracy, getMatrix, getReport

def predictGap(ps):
    '''
    xs = getMatchHistory()
    
    #write list to the csv
    output = open("match_data.csv","wb")
    import csv
    writer = csv.writer(output)
    #writer.writerows(xs)
    '''
    #read csv as training data
    fd = pd.read_csv('match_data.csv',header = None)
    test_set = fd.iloc[:-1,0:1]
    train_set = fd.iloc[:-1,23:]

    #trainset
    from sklearn.model_selection import train_test_split
    x_train,x_test, y_train, y_test = train_test_split(train_set, test_set, test_size=0.33, random_state=12)

    #DecisionTree build Model
    print("######DecisionTree######")
    clf_decisionTree = tree.DecisionTreeClassifier().fit(x_train, y_train)
    predicted = clf_decisionTree.predict(x_test)
    print(getMatrix(y_test, predicted))
    print(getAccuracy(y_test,predicted))

    #MultinomialNB build Model
    print("######MultinomialNB######")
    clf_multiNB = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True).fit(x_train, y_train)
    predicted = clf_multiNB.predict(x_test)
    print(getMatrix(y_test, predicted))
    print(getAccuracy(y_test,predicted))

    #SGD classification
    print("######SGDClassifier######")
    clf_sgd = SGDClassifier().fit(x_train, y_train)
    predicted = clf_sgd.predict(x_test)
    print(getMatrix(y_test, predicted))
    print(getAccuracy(y_test,predicted))

    #GaussianNB model
    print("######GaussianNB######")
    clf_gaussianNB = GaussianNB().fit(x_train, y_train)
    predicted = clf_gaussianNB.predict(x_test)
    print(getMatrix(y_test, predicted))
    print(getAccuracy(y_test,predicted))
 
    #use the model
    print("----------------------&Predict_data&-----------------------")
    print(ps)
    predict_data = DataFrame(ps)
    predict_data = predict_data.T
    print(predict_data)

    predicted = predict_data

    predicted_result = clf_multiNB.predict(predicted)

    print predicted_result
        
    return predicted_result.tolist()
if __name__ == '__main__':
    #[gap, H, D, A, HGK1, HP2, HP3, HP4, HP5, HP6, HP7, HP8, HP9, HP10, HP11, AGK1, AP2, AP3, AP4, AP5, AP6, AP7, AP8, AP9, AP10, AP11]
    ps = [2.5,4.5,1.5,50,60,70,80,90,100,90,80,70,60,50,50,60,70,80,90,100,90,80,70,60,50]

    predictGap(ps)