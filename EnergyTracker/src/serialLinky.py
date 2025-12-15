#!/usr/bin/env python3
# Python 3

import time
import logging
import queue
import termios
import serial
import configRepository

class SerialLinky :
    
    START_FRAME = b'\x02'  # STX, Start of Text
    STOP_FRAME = b'\x03'   # ETX, End of Text

    _config: configRepository.SerialLinkyConfig = None
    _logger:logging.Logger=None

    def __init__(self, config:configRepository.SerialLinkyConfig):
        self._logger = logging.getLogger("serialLinky")
        self._config=config
        if self._config.read_data and self._config.debug:
            # Configuration du logger en mode debug
            self._logger.setLevel(logging.DEBUG)

    def _checksum(self, data, separator, checksum, linky_checksum_method) -> bool:
        """Vérifie la somme de contrôle du groupe d'information. Réf Enedis-NOI-CPT_02E, page 19."""
        if linky_checksum_method == 2:
            data += separator
        s = sum([ord(c) for c in data])
        s = (s & 0x3F) + 0x20
        return (checksum == chr(s))

    def _cast(self, key,val):
        if key == 'PREF' or key == 'EAST' or key == 'EASF02' or key == 'EASF01' or key == 'EAIT' or key == 'SINSTS':
            return int(val)
        else :
            return val
        
    def _read_values(self, line) -> dict:
        # Identification du séparateur en vigueur (espace ou tabulation)
        separator = line[-2]
        splitted = line.split(separator)
        count = len(splitted)

        values = dict()
        values["label"]=splitted[0]
        values["checksum"]=splitted[count-1]
        values["separator"]=separator
        # valeur horodatée ou pas
        if count>3:
            values["date"]=splitted[1]
            values["value"]=splitted[2]
        else:
            values["value"]=splitted[1]
        
        return values

    def linky(self, frame_queue:queue.Queue) -> bool:
        if not self._config.read_data:
            self._logger.debug('readData is false, bye.', stacklevel=logging.DEBUG)
            return True
        
        # Ouverture du port série
        try:
            baudrate = 1200 if self._config.linky_legacy_mode else 9600
            self._logger.info(f'Ouverture du port série {self._config.raspberry_stty_port} à {baudrate} Bd')
            with serial.Serial(port=self._config.raspberry_stty_port,
                            baudrate=baudrate,
                            parity=serial.PARITY_EVEN,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.SEVENBITS,
                            timeout=1) as ser:

                # Boucle pour partir sur un début de trame
                self._logger.info('Attente d\'une première trame...', stacklevel=logging.INFO)
                line = ser.readline()
                while self.START_FRAME not in line:  # Recherche du caractère de début de trame, c'est-à-dire STX 0x02
                    line = ser.readline()

                # Initialisation d'une trame vide
                frame = dict()

                # Boucle infinie
                while True:

                    try:
                        # Décodage ASCII et nettoyage du retour à la ligne
                        line_str = line.decode('ascii').rstrip()
                        self._logger.debug(f'Groupe d\'information brut : {line_str}', stacklevel=logging.DEBUG)

                        if len(line_str)>2:

                            #extraction des données
                            values = self._read_values(line_str)

                            if values["label"] in self._config.linky_keys:
                                
                                checksum_ok = False
                                if "date" in values:
                                    checksum_ok = self._checksum(f'{values["label"]}{values["separator"]}{values["date"]}{values["separator"]}{values["value"]}', values["separator"], values["checksum"], self._config.linky_checksum_method)
                                else:
                                    checksum_ok = self._checksum(f'{values["label"]}{values["separator"]}{values["value"]}', values["separator"], values["checksum"], self._config.linky_checksum_method)
                                
                                if checksum_ok:
                                    frame[values["label"]] = self._cast(values["label"],values["value"])
                                else:
                                    self._logger.debug(f'Somme de contrôle {values["checksum"]} erronée pour {values["label"]} {values["value"]}', stacklevel=logging.DEBUG)
                                    
                            # Si caractère de fin de trame dans la ligne, on écrit les données dans db
                            if self.STOP_FRAME in line:
                                num_keys = len(frame)
                                self._logger.info(f'Trame reçue ({num_keys} étiquettes traités)', stacklevel=logging.INFO)

                                if num_keys>0:
                                    frame_queue.put(frame)

                                # On réinitialise  une nouvelle trame
                                frame = dict()

                                time.sleep(self._config.interval)

                    except Exception as e:
                        self._logger.error(f'Une exception s\'est produite : {e}', exc_info=True, stacklevel=logging.ERROR)


                    # Lecture de la ligne suivante
                    line = ser.readline()

        except termios.error as err:
            self._logger.error('Erreur lors de la configuration du port série', stacklevel=logging.ERROR)
            if self._config.raspberry_stty_port == '/dev/ttyS0':
                self._logger.error('Essayez d\'utiliser /dev/ttyAMA0 plutôt que /dev/ttyS0', stacklevel=logging.ERROR)
            
            self._logger.error(f'{err}', stacklevel=logging.ERROR)
            raise SystemExit(1)

        except serial.SerialException as exc:
            if exc.errno == 13:
                self._logger.error('Erreur de permission sur le port série', stacklevel=logging.ERROR)
                self._logger.error('Avez-vous ajouté l\'utilisateur au groupe dialout ?', stacklevel=logging.ERROR)
                self._logger.error('  $ sudo usermod -G dialout $USER', stacklevel=logging.ERROR)
                self._logger.error(
                    'Vous devez vous déconnecter de votre session puis vous reconnecter pour que les droits prennent effet.', stacklevel=logging.ERROR)
            else:
                self._logger.error(f'Erreur lors de l\'ouverture du port série : {exc}', stacklevel=logging.ERROR)
            raise SystemExit(1)
