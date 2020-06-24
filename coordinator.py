#import serial
from google.cloud import storage
import csv

def addtoCloud():
    client = storage.Client(project="Python").from_service_account_json("key.json")
    bucket = client.get_bucket("crop-data")
    blob = bucket.get_blob("Current_Data.csv")
    blob.download_to_filename("currentcropdata.csv")
    cols = ['Humidity','Temperature','Distance','Moisture']
    with open('currentcropdata.csv','r') as csv_file:
        csv_reader = csv.reader(csv_file)
        new_rows_list = []
        for row in csv_reader:
            new_rows_list.append(row)
#temp = ['95','27','234','4']
#new_rows_list.append(temp)
    ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=5
    )
#while 1:
    x = ser.readline().strip()
    split_string = str(x).split()
    print(split_string)
    data_to_append = [split_string[3],split_string[7],split_string[11],split_string[14]]
    print(data_to_append)
    new_rows_list.append(data_to_append)
    with open('currentcropdata.csv','w',newline='') as write_csv:
        csv_writer = csv.writer(write_csv)
        csv_writer.writerows(new_rows_list)
    blob_upload = storage.Blob("Current_Data.csv", bucket)
    blob_upload.upload_from_filename("currentcropdata.csv")
    return data_to_append

import requests
import pandas as pd
def watercontrol(moisture_value, water_level, rainfall_prediction):
    total_water_tank_capacity = 500
    rainfall_prediction = bool(rainfall_prediction)
    if moisture_value <= 15 and water_level >= 0.4*total_water_tank_capacity and not rainfall_prediction:
        while moisture_value != 45:
            print("1.Turn Water Channel On till value become 45")
            moisture_value += 1
    elif moisture_value <=15 and water_level >=0.4*total_water_tank_capacity and rainfall_prediction:
        while moisture_value != 45:
            print("2.Turn Water Sprinkler On till value become 45")
            moisture_value += 1
    elif moisture_value <=15 and water_level <0.4*total_water_tank_capacity and not rainfall_prediction:
        while moisture_value != 45:
            print("3.Turn Water Sprinkler On till value become 45")
            moisture_value += 1
    elif moisture_value <=15 and water_level <0.4*total_water_tank_capacity and rainfall_prediction:
        while moisture_value != 15:
            print("4.Turn Water Sprinkler On till value become 15")
            moisture_value += 1
    elif 15 < moisture_value <=45 and water_level >=0.4*total_water_tank_capacity and not rainfall_prediction:
        while moisture_value != 45:
            print("5.Turn Water Sprinkler On till value become 45")  
            moisture_value += 1
    else:
        print("6.Turn Water Supply Off")
        

        
def getMoistureValue():
    moisture_value = split_string[3]
    return moisture_value

def getAvailableWater():
    water_level = split_string[11]
    return water_level
        
        
def main():
    moisture_value = getMoistureValue()
    #rainfall_prediction = rainfall_prediction()
    api_address='http://api.openweathermap.org/data/2.5/weather?appid=f0b2823efc49a3f2d44fef7b2a0642e7&q='
    city = input('City Name :')
    url = api_address + city
    json_data = requests.get(url).json()
    format_add = json_data['weather'][0]['main']
    print(format_add)
    if format_add == "Clear":
        format_add = 0
    else:
        format_add = 1
    addtoCloud()
    water_level = getAvailableWater()
    watercontrol(moisture_value, water_level, format_add)
    
    
if __name__== "__main__":
    main() 
