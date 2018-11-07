import requests
import configparser
from bs4 import BeautifulSoup
import logging
from logging.handlers  import SMTPHandler
from buffered_smtp_handler import BufferedSMTPHandler
import re

def createLogger(config):
    levels = { 'debug': logging.DEBUG,
               'info': logging.INFO,
               'warning': logging.WARNING,
               'error': logging.ERROR,
               'critical': logging.CRITICAL}

    logger = logging.getLogger('monitor')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(config['general']['logfile'])
    fh.setLevel(levels[config.get('general', 'loglevel', fallback='warning')])
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create an email handler with high log level
    smtph = BufferedSMTPHandler(
            mailhost = (config.get('general','smtp_server'),int(config.get('general','smtp_port'))),
            fromaddr = config.get('general','from'),
            toaddrs = [config.get('general','email')],
            subject = config.get('general','subject'),
            credentials = (config.get('general','username'), config.get('general','password')),
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
    return logger

def getRegexes(config, url, logger):
    logger.info("Compilation des expressions régulières pour l'URL %s" % url)
    regexes = []
    for k in config.get(url,'patterns').split(','):
        k = k.strip()
        regexes.append(re.compile(k))
        logger.debug("Expression compilée : %s" % k)
    return regexes

def parsePage(config, url, content, logger):
    logger.info("Analyse de la page %s" % url)
    soup = BeautifulSoup(content, 'html.parser')
    regexes = getRegexes(config, url, logger)
    for item in soup.find_all('p'):
        for r in regexes:
            m = r.search(item.get_text())
            if m:
                logger.error("Expression %s trouvée sur la page %s" % (m.group(), url))

def analyzeURL(config, url, logger):
    logger.info("Téléchargement de la page %s" % url)
    page = requests.get(url)
    logger.debug("Status code %s" % str(page.status_code))
    if not page.status_code == 200:
        logger.critical("Erreur lors de la vérification de la page %s, code d'erreur %s" % (url, str(page.status_code)))
    else:
        parsePage(config, url, page.content, logger)


def analyzeURLs(config,logger):
    for section in config.sections():
        if not section == "general":
            analyzeURL(config, section, logger)

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.cfg')
    logger = createLogger(config)
    analyzeURLs(config,logger)

