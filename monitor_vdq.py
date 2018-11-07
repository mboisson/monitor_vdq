import requests
import configparser
from bs4 import BeautifulSoup
import logging
from logging.handlers  import SMTPHandler

logger = None
config = None

def createLogger():
    levels = { 'debug': logging.DEBUG,
               'info': logging.INFO,
               'warning': logging.WARNING,
               'error': logging.ERROR,
               'critical': logging.CRITICAL}

    logger = logging.getLogger('monitor')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(config['DEFAULT']['logfile'])
    fh.setLevel(levels[config.get('DEFAULT', 'loglevel', fallback='warning')])
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create an email handler with high log level
    smtph = SMTPHandler(
            mailhost = (config.get('DEFAULT','smtp_server'),config.get('DEFAULT','smtp_port')),
            fromaddr = config.get('DEFAULT','from'),
            toaddrs = config.get('DEFAULT','email'),
            subject = config.get('DEFAULT','subject'),
            credentials = (config.get('DEFAULT','username'), config.get('DEFAULT','password')),
            secure = ()
            )
    smtph._timeout=30
    smtph.setLevel(logging.ERROR)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    smtph.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.addHandler(smtph)
    logger.info('logger created')

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.cfg')
    createLogger()

