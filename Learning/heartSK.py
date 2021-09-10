# prepare data downloaded from UCL

import csv
import pandas as pd

# add header names
headers = [
    "age",
    "sex",
    "chest_pain",
    "resting_blood_pressure",
    "serum_cholestoral",
    "fasting_blood_sugar",
    "resting_ecg_results",
    "max_heart_rate_achieved",
    "exercise_induced_angina",
    "oldpeak",
    "slope of the peak",
    "num_of_major_vessels",
    "thal",
    "heart_disease",
]

heart_df = pd.read_csv("heart.dat", sep=" ", names=headers)

import numpy as np
import warnings

warnings.filterwarnings("ignore")  # suppress warnings
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# convert imput to numpy arrays
X = heart_df.drop(columns=["heart_disease"])

# replace target class with 0 and 1
# 1 means "have heart disease" and 0 means "do not have heart disease"
heart_df["heart_disease"] = heart_df["heart_disease"].replace(1, 0)
heart_df["heart_disease"] = heart_df["heart_disease"].replace(2, 1)

y_label = heart_df["heart_disease"].values.reshape(X.shape[0], 1)

# split data into train and test set
Xtrain, Xtest, ytrain, ytest = train_test_split(
    X, y_label, test_size=0.2, random_state=2
)

# standardize the dataset
sc = StandardScaler()
sc.fit(Xtrain)
Xtrain = sc.transform(Xtrain)
Xtest = sc.transform(Xtest)

print(f"Shape of train set is {Xtrain.shape}")
print(f"Shape of test set is {Xtest.shape}")
print(f"Shape of train label is {ytrain.shape}")
print(f"Shape of test labels is {ytest.shape}")
#########################################################
#########Creating the dataset above this line############
#########################################################
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

sknet = MLPClassifier(hidden_layer_sizes=(8), learning_rate_init=0.001, max_iter=100)

sknet.fit(Xtrain, ytrain)
preds_train = sknet.predict(Xtrain)
preds_test = sknet.predict(Xtest)

print(
    "Train accuracy of sklearn neural network: {}".format(
        round(accuracy_score(preds_train, ytrain), 2) * 100
    )
)
print(
    "Test accuracy of sklearn neural network: {}".format(
        round(accuracy_score(preds_test, ytest), 2) * 100
    )
)
