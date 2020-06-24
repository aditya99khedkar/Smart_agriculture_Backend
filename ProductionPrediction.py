import matplotlib.pyplot as plt
import pandas as pd
import csv
from matplotlib import style
style.use('ggplot')
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from google.cloud import storage
from CropCluster import *
probable_list = []

client = storage.Client(project="python").from_service_account_json("key.json")
bucket = client.get_bucket("crop-data")
blob = bucket.get_blob("Crops_MIR.csv")
blob.download_to_filename("Crops_MIR.csv")
data = pd.read_csv(r'Crops_MIR.csv', names = cols)
for row in data:
    if row[1] == cluster_number:
        probable_list.append(row[0])
        
for row in probable_list:
    blob = bucket.get_blob(str(row)+".csv")
    blob.download_to_filename(str(row)+".csv")
    cols = ['Water Require','Temp','Moisture','Production']
    data = pd.read_csv(r'str(row).csv', names = cols)
#print(data)
    X = pd.DataFrame(data.iloc[:,:-1])
    y = pd.DataFrame(data.iloc[:,-1])
#print(X)
    X_train, X_test, y_train, y_test = train_test_split(X,y,random_state = 5)
    print(X_train)
    print(X_test)
    print(y_train)
    print(y_test)
    regressor = LinearRegression()
    regressor.fit(X_train,y_train)
    v = pd.DataFrame(regressor.coef_,index=['Co-efficient']).transpose()
    w = pd.DataFrame(X.columns, columns=['Attribute'])
    coef_df = pd.concat([w,v], axis=1, join='inner')
    print(coef_df)
    y_pred = regressor.predict(X_test)
    y_pred = pd.DataFrame(y_pred, columns=['Predicted'])
    print(y_pred)  

accuracy = regressor.score(X_train,y_train)
print(accuracy*100,'%')                                                                                                                                                      
