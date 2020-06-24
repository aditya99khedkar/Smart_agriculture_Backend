import csv
import pandas as pd
from google.cloud import storage
flag = 0
client = storage.Client(project="python")
bucket = client.get_bucket("crop-data")
blob = storage.Blob("Crops_MIR.csv", bucket)
blob.download_to_filename("Crops_MIR.csv")

crop_name = input('Enter Crop Name: ')
with open('Crops_MIR.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for data in csv_reader:
        if data[0]==crop_name:
            flag = 1
            break
if flag==1:
    new_rows_list = []
    blob1 = storage.Blob("str(crop_name).csv", bucket)
    blob1.download_to_filename("str(crop_name).csv")
    with open('str(crop_name).csv','r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for data in csv_reader:
            new_rows_list.append(data)
        data = pd.DataFrame(new_rows_list)
        print(data)
        for i in range(4):
            data[i] = data[i].astype(int)
        sum1 = data.mean(axis=0)
        print(sum1[1])
        i = 0
        with open('Crops_MIR.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            new_rows_list = []
            for row in csv_reader:
                if row[0]==crop_name:
                    for i in range(4):
                        row[i+2] = sum1[i]
                new_rows_list.append(row)
        print(new_rows_list) 
        with open('Crops_MIR.csv', 'w',newline='') as write_csv:
            csv_writer = csv.writer(write_csv)
            csv_writer.writerows(new_rows_list)

else:
    df = pd.DataFrame(list())
    df.to_csv('str(crop_name).csv')
    blob.upload_to_filename("str(crop_name).csv")
    
    

