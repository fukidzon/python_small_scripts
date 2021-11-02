# aws lambda function to get current data from API of shmu.sk and return it as json for specified city
# added in https://console.aws.amazon.com/lambda
# Configuration - API HTTP Gateway  - accessible at https://006arcb5i4.execute-api.us-east-1.amazonaws.com/default/shmu?cccc=ASBB


import urllib.request

def get_csv(time):
   
    timestring = "{:02d}.{:02d}.{:d}:{:02d}".format(time.day, time.month, time.year, time.hour)
    shmu_address = 'http://meteo.shmu.sk/customer/home/opendata/?observations;date='+timestring
    (filename, headers) = urllib.request.urlretrieve(shmu_address)
    return filename

import json
from datetime import datetime

def lambda_handler(event, context):
  
    if 'queryStringParameters' in event and 'cccc' in event['queryStringParameters']:
        cccc=event['queryStringParameters']['cccc']
    else:
        cccc='ASBB'
    time = datetime.utcnow()
    filename = get_csv(time) 
    file1 = open(filename, "r")
    lines = file1.readlines()
    file1.close()
    for i,line in enumerate(lines):
        if i==0:
            columns = []
            for col in line.split(";"):
                col=col.strip()
                columns.append(col)
            continue
        data = {}
        for col, element in zip(columns, line.split(';')):
            data[col] = element.strip()
        if data['cccc'] == cccc:
            break
            