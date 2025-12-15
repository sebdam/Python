import yaml
import logging

class ElasticConfig:
    use_elastic = False
    debug = False
    url = ""
    api_key = ""
    conso_index = ""
    prod_index = ""

    def __init__(self, use_elastic, debug, url, api_key, conso_index, prod_index):
        self.use_elastic=use_elastic
        self.debug=debug
        self.url=url
        self.api_key=api_key
        self.conso_index=conso_index
        self.prod_index=prod_index

class BeemConfig:
    read_prod = False
    debug = False
    url = ""
    interval = 0
    user = ""
    pwd = ""

    def __init__(self, read_prod, debug, url, interval, user, pwd):
        self.read_prod=read_prod
        self.debug=debug
        self.url=url
        self.interval=interval
        self.user=user
        self.pwd=pwd

class SerialLinkyConfig:
    read_data = False
    debug = False
    interval = 0
    linky_legacy_mode = 0
    linky_checksum_method = 0
    linky_keys = []
    raspberry_stty_port=""

    def __init__(self, read_data, debug, interval, linky_legacy_mode, linky_checksum_method, linky_keys, raspberry_stty_port):
        self.read_data=read_data
        self.debug=debug
        self.interval=interval
        self.linky_legacy_mode=linky_legacy_mode
        self.linky_checksum_method=linky_checksum_method
        self.linky_keys=linky_keys
        self.raspberry_stty_port=raspberry_stty_port

class ConfigRepository:
    _cfg = None
    _logger:logging.Logger = None

    elasticConfig: ElasticConfig = None
    beemConfig: BeemConfig = None
    serialLinkyConfig: SerialLinkyConfig = None

    def __init__(self):
        # Creation du logger
        logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

        # Ouverture du fichier de configuration
        try:
            with open("./config.yml", "r") as f:
                self._cfg = yaml.load(f, Loader=yaml.SafeLoader)
        except FileNotFoundError:
            logging.error('Il manque le fichier de configuration config.yml', stacklevel=logging.ERROR)
            raise SystemExit(1)
        except yaml.YAMLError as exc:
            if hasattr(exc, 'problem_mark'):
                mark = exc.problem_mark
                logging.error('Le fichier de configuration comporte une erreur de syntaxe', stacklevel=logging.ERROR)
                logging.error(f'La position de l\'erreur semble être en ligne {mark.line+1} colonne {mark.column+1}', stacklevel=logging.ERROR)
                raise SystemExit(1)
        except (OSError, IOError):
            logging.error('Erreur de lecture du fichier config.yml. Vérifiez les permissions ?', stacklevel=logging.ERROR)
            raise SystemExit(1)
        except Exception:
            logging.critical('Erreur lors de la lecture du fichier de configuration', exc_info=True, stacklevel=logging.CRITICAL)
            raise SystemExit(1)
        
        #Configuration Elastic Search
        try:
            self.elasticConfig = ElasticConfig(self._cfg['elastic']['sendData'],
                                               self._cfg['elastic'].get('debug', False),
                                               self._cfg['elastic'].get('url',""),
                                               self._cfg['elastic'].get('api_key',""),
                                               self._cfg['elastic'].get('conso-index',""),
                                               self._cfg['elastic'].get('prod-index',""))
        except KeyError as exc:
            self._logger.error(f'Erreur : il manque la clé {exc} dans le fichier de configuration', stacklevel=logging.ERROR)
            raise SystemExit(1)
        except Exception:
            self._logger.critical('Erreur lors de la lecture du fichier de configuration', exc_info=True, stacklevel=logging.CRITICAL)
            raise SystemExit(1)
        
        #Configuration Beem
        try:
            self.beemConfig = BeemConfig(self._cfg['beem']['readData'],
                                        self._cfg['beem'].get('debug', False),
                                        self._cfg['beem'].get('url',""),
                                        self._cfg['beem'].get('interval',60),
                                        self._cfg['beem'].get('user',""),
                                        self._cfg['beem'].get('pwd',""))
        except KeyError as exc:
            self._logger.error(f'Erreur : il manque la clé {exc} dans le fichier de configuration', stacklevel=logging.ERROR)
            raise SystemExit(1)
        except Exception:
            self._logger.critical('Erreur lors de la lecture du fichier de configuration', exc_info=True, stacklevel=logging.CRITICAL)
            raise SystemExit(1)
        
        #Configuration Serial Linky
        try:
            self.serialLinkyConfig = SerialLinkyConfig(self._cfg['linky']['readData'],
                                                       self._cfg['linky'].get('debug', False),
                                                       self._cfg['linky'].get('interval', 5*60),
                                                       self._cfg['linky'].get('legacy_mode',1),
                                                       self._cfg['linky'].get('checksum_method', 1),
                                                       self._cfg['linky'].get('keys', ('PRM', 'PREF', 'EAST', 'EAIT', 'SINSTS')),
                                                       self._cfg['raspberry'].get('stty_port',""))
        except KeyError as exc:
            logging.getLogger("serialLinky").error(f'Erreur : il manque la clé {exc} dans le fichier de configuration', stacklevel=logging.ERROR)
            raise SystemExit(1)
        except Exception:
            logging.getLogger("serialLinky").critical('Erreur lors de la lecture du fichier de configuration', exc_info=True, stacklevel=logging.CRITICAL)
            raise SystemExit(1)
