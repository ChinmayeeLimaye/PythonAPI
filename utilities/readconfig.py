import configparser
import os
from pathlib import Path

config=configparser.ConfigParser()
config.read('/home/chinmayee/PycharmProjects/WeavAPI/utilities/properties.ini')



class ReadConfig:
    @staticmethod
    def getDataserviceURL():
        url=config.get('ServiceURL','Data_service_url')
        return url

    @staticmethod
    def getDataBrowser():
        url=config.get('ServiceURL','Data_browser_url')
        return url

    @staticmethod
    def getIngestion():
        url=config.get('ServiceURL','Ingestion_service_url')
        return url