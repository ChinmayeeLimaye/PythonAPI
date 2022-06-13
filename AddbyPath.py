import requests
import json
import jsonpath

import os

#from utilities.BaseClass import getConfig
from utilities.readconfig import ReadConfig
from utilities.resources import ApiResources

from pathlib import Path

print(Path.home())



url = ReadConfig.getDataserviceURL() +ApiResources.AddByPathAPI
#url=ReadConfig.getDataserviceURL()

print(url)

file=open(os.getcwd()+"/JsonFiles/add_by_path.json",'r')
json_input=file.read()

json_req=json.loads(json_input)

print(json_req)

response=requests.post(url, json=json_req,headers={"Content-Type": "application/json"})

print(os.path.expanduser('~'))

#print(response.content)

json_response=json.loads(response.text)

print(json_response)

#json_response = response.json()

datasetid=jsonpath.jsonpath(json_response,'data.dataset_id')

versionid=jsonpath.jsonpath(json_response,'data.version_id')

url = ReadConfig.getDataBrowser() +ApiResources.GetRowsAPI

print(url)

file=open(os.getcwd()+"/JsonFiles/get_rows.json",'r')
json_input=file.read()

json_req=json.loads(json_input)

#print(type(json_req))

if 'dataset_id' in json_req:
    json_req['dataset_id'] =datasetid[0]
    json_req['version_id'] =versionid[0]

print(json_req)

response=requests.post(url, json=json_req,headers={"Content-Type": "application/json"})

#print(response)

#print(response.reason)

#print(response)

json_response=json.loads(response.text)

print(json_response)

if 'show_cols' in json_req:
    col_name=json_req['show_cols']

    #print(req_col_name)

    req_col_name = set(col_name)

    #filename=json_req['file_name']

    #print(filename)

    #req_col_name = set(req_col_name)

    #print(json_response)

    sort_obj = json_req['sort_obj']

    oper_obj=json_req['operations']

    print(oper_obj)

    print(type(oper_obj))

    sort_col = sort_obj.get('col_name')



    res_column_name = jsonpath.jsonpath(json_response, "$..data[0]")

    count=jsonpath.jsonpath(json_response, "$.data..data[*]")

    particular_column_name = jsonpath.jsonpath(json_response, "$..data[*]["+sort_col+"]")

    print(particular_column_name)

    particular_column_name1 = particular_column_name[:]
    particular_column_name1.sort()
    if (particular_column_name1 == particular_column_name):
        flag = 1

    # printing result
    if (flag):
        assert True
    else:
        assert False

    #print(type(count))

    res_row_count=len(count)

    req_row_count = json_req['row_count']

    #l=res_column_name

    #print(l[0])
   #print(type(l[0]))

    key_list = list(res_column_name[0].keys())
    res_col_name = set(key_list)
    print(req_col_name)
    print(res_col_name)
    print(req_row_count)
    print(res_row_count)



    assert req_col_name == res_col_name
    assert req_row_count==res_row_count

#print(len(column_name))

#print(column_name[0])

#print(type(column_name[0]))



#print(key_list)



#print(type(column_name))



#print(col_name)

#print(type(col_name))

#json_response = response.json()

#datasetid=jsonpath.jsonpath(json_response,'data.dataset_id')



#print(datasetid[0])

#assert datasetid[0]== 9

assert response.status_code ==200

