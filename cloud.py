from google.cloud import storage
import csv
from coordinator import addtoCloud
client = storage.Client(project="Python").from_service_account_json("key.json")
bucket = client.get_bucket("crop-data")
print(bucket)
blob = bucket.get_blob("str(crop_name).csv")

#blob = storage.Blob("Crops_MIR.csv", bucket)
#blob.upload_from_string("my secret message.")
#with open("/tmp/my-secure-file", "wb") as file_obj:
       # blob.download_to_file(file_obj)
blob.download_to_filename("cropdata.csv")
with open('cropdata.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    new_rows_list = []
    for row in csv_reader:
        new_rows_list.append(row)
#temp = ['0','0','0','1','1','1']
Latest_crop_data = addtoCloud()
new_rows_list.append(Latest_crop_data)
print(new_rows_list)  
with open('cropdata.csv', 'w',newline='') as write_csv:
    csv_writer = csv.writer(write_csv)
    csv_writer.writerows(new_rows_list) 
blob_upload = storage.Blob("str(crop_name).csv", bucket)
blob_upload.upload_from_filename("cropdata.csv")

