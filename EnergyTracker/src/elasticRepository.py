#!/usr/bin/env python3
# Python 3

from datetime import datetime
from typing import Any, Dict, List
import configRepository
import logging
from elasticsearch import Elasticsearch

class ElasticRepository():
    _logger:logging.Logger=None
    _config:configRepository.ElasticConfig = None

    def __init__(self, config:configRepository.ElasticConfig):
        self._logger = logging.getLogger("elasticRepository")
        self._config=config
        if self._config.use_elastic and self._config.debug:
            # Configuration du logger en mode debug
            self._logger.setLevel(logging.DEBUG)
            es_logger = logging.getLogger("elasticsearch")
            es_logger.setLevel(logging.DEBUG)

    def WriteConso(self, obj: Dict[str, Any]) -> bool :
        if not self._config.use_elastic:
            return True
        
        self._logger.debug('WriteConsoToElastic : START', stacklevel=logging.DEBUG)

        # connection à la base
        client = Elasticsearch(self._config.url, api_key=self._config.api_key)
        
        try:
            dayIndex = f'{self._config.conso_index}-{datetime.today().strftime("%Y-%m-%d")}'
            self._logger.debug(f'useElastic index {dayIndex}')
            client.index(index=dayIndex,
                        id=obj["id"],
                        document=obj)
        except Exception as e:
            self._logger.error(f'Erreur :{e.message}', stacklevel=logging.ERROR)
            return False
        
        self._logger.debug('document created:{0}'.format(obj), stacklevel=logging.DEBUG)

        return True

    def WriteProd(self, intraday: List[Dict[str, Any]], summary: List[Dict[str, Any]]) -> bool :
        if not self._config.use_elastic:
            return True
        
        self._logger.debug('WriteProdToElastic : START', stacklevel=logging.DEBUG)

        # connection à la base
        client = Elasticsearch(self._config.url, api_key=self._config.api_key)
        
        try:
            intradayIndex = f'{self._config.prod_index}-intraday-{datetime.today().strftime("%Y-%m-%d")}'
            summaryIndex = f'{self._config.prod_index}-summary-{datetime.today().strftime("%Y-%m-%d")}'
            
            self._logger.debug(f'useElastic index {intradayIndex}', stacklevel=logging.DEBUG)

            client.options(ignore_status=[400,404]).indices.delete(index=intradayIndex)

            for entry in intraday:
                client.index(index=intradayIndex,
                            id=entry["id"],
                            document=entry)
            
            self._logger.debug(f'useElastic index {summaryIndex}', stacklevel=logging.DEBUG)

            for entry in summary:
                client.index(index=summaryIndex,
                            id=entry["id"],
                            document=entry)
        except Exception as e:
            self._logger.error(f'Erreur :{e.message}', stacklevel=logging.ERROR)
            return False
        
        self._logger.debug('document created:{0}'.format(intraday), stacklevel=logging.DEBUG)

        return True
