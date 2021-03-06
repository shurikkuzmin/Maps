# coding: utf-8
import os
import pandas
import numpy
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor

class Fit(object):
    def __init__(self):
        print(os.getcwd())
        csv = pandas.read_excel("simple/data/table_clean.xlsx")
        model = RandomForestRegressor(max_depth=4, random_state=42)
        
        #print("Years = ", csv["Years"].values)
        #print("Salary = ", csv["Salary"].values)
        #print("Age = ", csv["Age"].values)
        
        model.fit(csv[["Years", "Salary", "Age"]].values, csv["Delay"].values)
        self.model = model
        self.csv = csv

    def predict(self, service, age, min_salary, max_salary):
        val1 = self.model.predict([[service, min_salary, age]])
        val2 = self.model.predict([[service, max_salary, age]])
        return min(val1[0], val2[0]), max(val1[0], val2[0])
