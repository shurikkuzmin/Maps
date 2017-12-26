# coding: utf-8
import os
import pandas
import numpy
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model

class Fit(object):
    def __init__(self):
        print(os.getcwd())
        csv = pandas.read_excel("simple/data/table_clean.xlsx")
        model = Pipeline([('poly', PolynomialFeatures(degree = 1)), ('linear', linear_model.Ridge(normalize = True, alpha = 1.0))])
        model.fit(csv[["Salary","Years", "Position"]].values, csv["Delay"].values)
        self.model = model
        self.csv = csv

    def predict(self, data):
        return self.model.predict(data)
