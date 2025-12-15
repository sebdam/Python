
#!/usr/bin/env python3
# Python 3, pré-requis : pip install PyYAML pySerial azure-cosmos RPi.GPIO elasticsearch

import logging
import queue
import signal
import threading
from datetime import datetime, timezone
import time
import uuid

from beemRepository import BeemRepository
from configRepository import ConfigRepository
from elasticRepository import ElasticRepository
from serialLinky import SerialLinky

_configRepo = ConfigRepository()
_elasticRepo = ElasticRepository(_configRepo.elasticConfig)
_beemRepo = BeemRepository(_configRepo.beemConfig)

def _handler(signum, frame):
    logging.getLogger("linky").info('Programme interrompu par CTRL+C', stacklevel=logging.DEBUG)
    raise SystemExit(0)

def _send_frames_to_db():
    logging.getLogger("linky").info(f'Thread d\'envoi vers DB démarré', stacklevel=logging.INFO)
    while True:
        # Récupère une trame dans la file d'attente
        frame = frame_queue.get()
        
        # Horodatage de la trame reçue
        frame['date'] = datetime.today().strftime("%Y-%m-%d")
        frame['ts'] = datetime.now(timezone.utc)
        # Id de la trame
        frame['id']=str(uuid.uuid4())

        _elasticRepo.WriteConso(frame)

        frame_queue.task_done()

def _read_prod():
    logging.getLogger("linky").info(f'Thread de lecture de la production démarré', stacklevel=logging.INFO)
    while True:
        intraday = []
        if not _beemRepo.ReadIntraDay(intraday):
            continue
        
        summary = []
        if not _beemRepo.ReadSummary(summary):
            continue

        for entry in intraday:
            entry['id']=str(uuid.uuid4())
        
        for entry in summary:
            entry['id']=str(uuid.uuid4())

        _elasticRepo.WriteProd(intraday,summary)

        time.sleep(_configRepo.beemConfig.interval)

if __name__ == '__main__':

    # Creation du logger
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    logger = logging.getLogger("linky")
    
    # Capture élégamment une interruption par CTRL+C
    signal.signal(signal.SIGINT, _handler)

    logger.info('Démarrage Linky Téléinfo', stacklevel=logging.INFO)

    # Création d'une queue FIFO pour stocker les données
    frame_queue = queue.Queue()

    if _configRepo.elasticConfig.use_elastic:
        # Démarrage du thread d'envoi vers Elastic
        logging.getLogger("linky").debug(f'Démarrage du thread d\'envoi vers db', stacklevel=logging.DEBUG)
        send_thread = threading.Thread(target=_send_frames_to_db, daemon=True)
        send_thread.start()

    if _configRepo.beemConfig.read_prod :
        # Démarrage du thread de lecture de la production
        logging.getLogger("linky").debug(f'Démarrage du thread de lecture de la production', stacklevel=logging.DEBUG)
        read_thread = threading.Thread(target=_read_prod, daemon=True)
        read_thread.start()

    # Démarrage de la lecture du port série
    linky = SerialLinky(_configRepo.serialLinkyConfig)
    linky.linky(frame_queue)

    while True:
        time.sleep(0)
