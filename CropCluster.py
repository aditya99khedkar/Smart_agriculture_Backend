import matplotlib.pyplot as plt
import pandas as pd
import csv
from matplotlib import style
style.use('ggplot')
import numpy as np
from sklearn.cluster import KMeans
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.preprocessing import StandardScaler
from google.cloud import storage
client = storage.Client(project="python").from_service_account_json("key.json")
bucket = client.get_bucket("crop-data")
blob = bucket.get_blob("Crops_MIR.csv")
blob.download_to_filename("Crops_MIR.csv")
cols = ['Name','Labels','Water Require','Temp','Moisture','Production']
data = pd.read_csv(r'Crops_MIR.csv', names = cols)
colors = ['r', 'g', 'b', 'y', 'c', 'm']
X = data.loc[:,'Water Require':'Production']
k =3
colmap = {0: 'r', 1: 'g', 2: 'b'}

X = StandardScaler().fit_transform(X)
kmeans = KMeans(n_clusters=3)
kmeans = kmeans.fit(X)
labels = kmeans.predict(X)
print(labels)
centroids = kmeans.cluster_centers_
print("Shape of cluster:", kmeans.cluster_centers_.shape)
plt.scatter(X[:,0],X[:,2],c =kmeans.labels_ ,cmap = "rainbow")
plt.show()
i = 0    
with open('Crops_MIR.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    new_rows_list = []
    for row in csv_reader:
        row[1]=labels[i]
        i = i+1
        new_rows_list.append(row)
#for data in new_rows_list:
  #  data[i][1]=''.join(labels[i])
   # i = i+1
print(new_rows_list)
with open('Crops_MIR.csv', 'w',newline='') as write_csv:
    csv_writer = csv.writer(write_csv)
    csv_writer.writerows(new_rows_list)
cols = ['Name','Labels','Water Require','Temp','Moisture','Production']
data = pd.read_csv(r'Crops_MIR.csv', names = cols)
y = data['Labels']
X_norm = (X-X.min())/(X.max()-X.min())
lda = LDA(n_components = 1)
lda_transformed = pd.DataFrame(lda.fit_transform(X_norm,y))
#print(lda_transformed)
for i in range(3):
    plt.scatter(lda_transformed[y==i], data[y==i]['Water Require'], color=colmap[i])
plt.show()
#min_required = min(data[y==2]['Water Require'])

#Get Current Data from Farm to predict list of next possible crops
blob = bucket.get_blob("Current_Data.csv")
blob.download_to_filename("currentcropdata.csv")
cols1 = ['Humidity','Temperature','Distance','Moisture']
current_data = pd.read_csv(r'Crops_MIR.csv', names = cols1)
last_value = pd.DataFrame(current_data.iloc[-1:,:].values)   #Get Values of Latest field Data
cluster_number = kmeans.predict(last_value)