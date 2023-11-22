import requests
import time
from requests.auth import HTTPBasicAuth
import json
import sys
import datetime

time_list_method = []
time_list_elastic = []

for i in range(100):
    time_sta = time.perf_counter()
    response = requests.post("http://ono-http-server.a910.tak-cslab.org:8000/search_abnormally")
    time_end = time.perf_counter()
    time_method = time_end - time_sta
    #print(response.json())
    time_list_method.append(str(time_method)[2:11])



    time.sleep(1)
#
    time_sta = time.perf_counter()
    elastic_url = 'http://ono-workplace.a910.tak-cslab.org:9200/koyama/_search'
    # Basic Authentication
    # https://requests.readthedocs.io/en/latest/user/authentication/
    basic = HTTPBasicAuth('elastic', 'L4iievuw=Ij8lBr6F*-X')
    headers = {
        'Content-Type': 'application/json',
    }
    json_data = {
        "query": {
            "range": {
                "ResponseCode": {
                    "gte": 500
                }
            }
        },
        "size": 300
    }
    response = requests.get(elastic_url, auth=basic, headers=headers, json=json_data)
    #print(json.dumps(response.json(), indent=4))
    time_end = time.perf_counter()
    time_elasticsearch = time_end - time_sta
    #print(response.json())
    #time_list_elastic.extend(time_elasticsearch)
    time_list_elastic.append(str(time_elasticsearch)[2:11])

results_method = "\n".join(time_list_method)
resutls_elastic = "\n".join(time_list_elastic)

dt_now = datetime.datetime.now()
file_time = dt_now.strftime('%Y_%m_%d_%H_%M')
with open('method_'+file_time+'.txt', 'w') as f:
    f.write(results_method)
with open('elastic_'+file_time+'.txt', 'w') as f:
    f.write(resutls_elastic)
