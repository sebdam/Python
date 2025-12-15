#!/usr/bin/env python3
# Python 3

from typing import Any, Dict, List
from datetime import datetime, timedelta, timezone
import configRepository
import logging
import requests

class BeemRepository :
    _config: configRepository.BeemConfig = None
    _logger:logging.Logger=None
    _token = ""

    def __init__(self, config:configRepository.BeemConfig) :
        self._logger = logging.getLogger("elasticRepository")
        self._config=config
        if self._config.read_prod and self._config.debug:
            # Configuration du logger en mode debug
            self._logger.setLevel(logging.DEBUG)
            req_log = logging.getLogger('requests.packages.urllib3')
            req_log.setLevel(logging.DEBUG)
            req_log.propagate = True

    def __getBearerToken(self) -> bool :
        url = f'{self._config.url}user/login'
        body = dict()
        body['email']=self._config.user
        body['password']=self._config.pwd

        try:
            response = requests.post(url=url,json=body)
            if response.ok:
                self._token = response.json()["accessToken"]
                return True
            else :
                self._logger.error(f'getBearerToken Error : status={response.status_code} - reason={response.reason}', stacklevel=logging.ERROR)
        except Exception as e:
            self._logger.error(f'ERROR :{e}', stacklevel=logging.ERROR)

        return False

    def ReadIntraDay(self, obj: List[Dict[str, Any]]) -> bool :
        if not self._config.read_prod :
            self._logger.debug('readProd is false, bye.', stacklevel=logging.DEBUG)
            return True
        
        self._logger.debug('BeemRepository.ReadIntraDay : START', stacklevel=logging.DEBUG)

        if len(self._token) == 0:
            if not self.__getBearerToken():
                self._logger.debug('BeemRepository.ReadIntraDay : Unable to get token', stacklevel=logging.DEBUG)
                return False

        headers = {'Authorization': f'Bearer {self._token}'}
        url = f'{self._config.url}production/energy/intraday'
        params = dict()
        params['from']=datetime.today().strftime("%Y-%m-%dT00:00:00Z")
        params['to']= (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%dT00:00:00Z")
        params['scale']='PT5M'

        try:
            response = requests.get(url=url, params=params,headers=headers)

            if response.status_code == 401:
                if not self.__getBearerToken():
                    self._logger.debug('BeemRepository.ReadIntraDay : Unable to get token', stacklevel=logging.DEBUG)
                    return False
                
                headers = {'Authorization': f'Bearer {self._token}'}
                url = f'{self._config.url}production/energy/intraday'
                params = dict()
                params['from']=datetime.today().strftime("%Y-%m-%dT00:00:00Z")
                params['to']= (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%dT00:00:00Z")
                params['scale']='PT5M'
                
                response = requests.get(url=url, params=params,headers=headers)

            if response.ok :
                for device in response.json()["devices"]:
                    deviceId=f'{device["deviceType"]}-{device["deviceId"]}'
                    for measure in device["measures"]:
                        frameDict=dict()
                        frameDict["device"]=deviceId
                        frameDict["ts"]=measure["endDate"]
                        frameDict["value"]=measure["value"]
                        obj.append(frameDict)

                return True
            else :
                self._logger.error(f'ReadIntraDay Error : status={response.status_code} - reason={response.reason}', stacklevel=logging.ERROR)
        except Exception as e:
            self._logger.error(f'ERROR :{e}', stacklevel=logging.ERROR)

        return False

    def ReadSummary(self, obj: List[Dict[str, Any]]) -> bool :
        if not self._config.read_prod :
            self._logger.debug('readProd is false, bye.', stacklevel=logging.DEBUG)
            return True
        
        self._logger.debug('BeemRepository.ReadIntraDay : START', stacklevel=logging.DEBUG)

        if len(self._token) == 0:
            if not self.__getBearerToken():
                self._logger.debug('BeemRepository.ReadIntraDay : Unable to get token', stacklevel=logging.DEBUG)
                return False

        headers = {'Authorization': f'Bearer {self._token}'}
        url = f'{self._config.url}box/summary'
        body = dict()
        body['year']=int(datetime.today().strftime("%Y"))
        body['month']= int(datetime.today().strftime("%m"))

        try:
            response = requests.post(url=url,json=body,headers=headers)

            if response.status_code == 401:
                if not self.__getBearerToken():
                    self._logger.debug('BeemRepository.ReadIntraDay : Unable to get token', stacklevel=logging.DEBUG)
                    return False
                
                headers = {'Authorization': f'Bearer {self._token}'}
                url = f'{self._config.url}box/summary'
                body = dict()
                body['year']=int(datetime.today().strftime("%Y"))
                body['month']= int(datetime.today().strftime("%m"))

                response = requests.post(url=url,json=body,headers=headers)
            
            if response.ok:
                for device in response.json():
                    deviceId=f'box-{device["boxId"]}'
                    frameDict = dict()
                    frameDict["SINSTS"]=device["wattHour"]
                    frameDict["PDAY"]=device["totalDay"]
                    frameDict["device"]=deviceId
                    frameDict["ts"]=datetime.now(timezone.utc).isoformat()
                    obj.append(frameDict)

                return True
            else :
                self._logger.error(f'ReadSummary Error : status={response.status_code} - reason={response.reason}', stacklevel=logging.ERROR)
        except Exception as e:
            self._logger.error(f'ERROR :{e}', stacklevel=logging.ERROR)

        return False
