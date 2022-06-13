import pytest
from pytest_bdd import scenarios, when, then, parsers, scenario, given

from utilities.BaseClass import BaseClass
from utilities.readconfig import ReadConfig
from utilities.resources import ApiResources

import os

import requests
import json
import jsonpath

scenarios('../features/getcolstats.feature')


@pytest.fixture
def logging():
    log = BaseClass.getLogger()
    return log

@given(parsers.parse('the user has datasetid and versionid through AddByPathAPI'),target_fixture='list')
def datasetid():

    logging = BaseClass.getLogger()



    #log.info("hi i am here")
    url = ReadConfig.getDataserviceURL() + ApiResources.AddByPathAPI
    file = open("/home/chinmayee/PycharmProjects/WeavAPI/JsonFiles/add_by_path.json", 'r')

    json_input = file.read()

    json_req = json.loads(json_input)

    logging.info(json_req)

    response = requests.post(url, json=json_req, headers={"Content-Type": "application/json"})

    logging.info(response.content)

    json_response = json.loads(response.text)

    datasetid = jsonpath.jsonpath(json_response, 'data.dataset_id')

    versionid = jsonpath.jsonpath(json_response, 'data.version_id')

    return [datasetid,versionid]


@when(parsers.parse('the user calls GetColStatsAPI using request payload "{JSONFile}"'),target_fixture='getcolstatsresponse')
def payload(JSONFile,list):
    logging = BaseClass.getLogger()

    url = ReadConfig.getDataBrowser() + ApiResources.GetColStatsAPI

    filepath="/home/chinmayee/PycharmProjects/WeavAPI/JsonFiles/"+ JSONFile

    #print(JSONFile)

    file = open(filepath, 'r')

    json_input = file.read()

    json_req = json.loads(json_input)

    if 'dataset_id' in json_req:
        json_req['dataset_id'] = list[0][0]
        json_req['version_id'] = list[1][0]

    logging.info(json_req)

    response = requests.post(url, json=json_req, headers={"Content-Type": "application/json"})

    #json_response = json.loads(response.text)

    logging.info(response.content)

    return [response,json_req]


@then(parsers.parse('user should get status code {status_code:d}'))
def status(getcolstatsresponse,status_code):
    logging = BaseClass.getLogger()
    logging.info("Asserting status code")
    assert getcolstatsresponse[0].status_code == status_code, "Status code not matched"
    logging.info(getcolstatsresponse[0].status_code)


@then('response body should not be null')
def resbody(getcolstatsresponse):
    logging = BaseClass.getLogger()
    logging.info("Asserting response body")
    assert getcolstatsresponse[0].content is not None


@then(parsers.parse('message in result should be "{message}"'))
def resmessage(getcolstatsresponse,message):
    logging = BaseClass.getLogger()
    logging.info("Asserting message in result")
    json_response = json.loads(getcolstatsresponse[0].text)
    status_message=jsonpath.jsonpath(json_response, 'status.result')
    assert status_message[0]==message,"Status message not matched"
    logging.info(status_message[0])


@then('column names in API response data should be equal to column names given in input file')
def colname(getcolstatsresponse):
    logging = BaseClass.getLogger()
    logging.info("Asserting column names in response body")
    json_response = json.loads(getcolstatsresponse[0].text)
    if 'col_names' in getcolstatsresponse[1]:
        col_name = getcolstatsresponse[1]['col_names']

        req_col_name=set(col_name)

        column_name = jsonpath.jsonpath(json_response, 'data.')

        key_list = list(column_name[0].keys())

        res_col_name=set(key_list)

        #print(getcolstatsresponse[0])
        #print(getcolstatsresponse[1])

        assert req_col_name == res_col_name