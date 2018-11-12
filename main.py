#!/usr/bin/python3.5


# imports
import os
import logging
import speedtest
import configparser


# constants
ROOT = os.path.dirname(os.path.abspath(__file__)) + '/'
CONFIG_FILE = ROOT + 'config'
LOGGING_FILE = ROOT + 'log'
LOGGING_LEVEL = logging.DEBUG


# logging
logging.basicConfig(filename=LOGGING_FILE, format='%(asctime)-15s %(levelname)-8s %(message)s', level=LOGGING_LEVEL)


# config file
logging.info('Read config file')
config = configparser.ConfigParser()
config.read(CONFIG_FILE)
EXPORT_FILE_PATH = config['EXPORT']['FILE_PATH']


# write file header
if not os.path.isfile(EXPORT_FILE_PATH):
    logging.info('New file is created')
    with open(EXPORT_FILE_PATH, 'w') as file:
        logging.info('Write file header')
        file.write('Date\tTime\tPing (ms)\tDownload (Mbit/s)\tUpload (Mbit/s)\n')


# speedtest
logging.info('Start speedtest')
s = speedtest.Speedtest()
server = s.get_best_server()
logging.info('Best Server: {} in {} ({})'.format(server['sponsor'], server['name'], server['country']))
download = s.download()
logging.info('Download: {} Bit/s'.format(download))
upload = s.upload()
logging.info('Upload: {} Bit/s'.format(upload))

results = s.results.dict()
timestamp = results['timestamp'][:-8]
date, time = timestamp.split('T')
ping = results['ping']
download = results['download'] / 1E6
upload = results['upload'] / 1E6


# write results
with open(EXPORT_FILE_PATH, 'a') as file:
    logging.info('Write results to file')
    file.write('{}\t{}\t{}\t{}\t{}\n'.format(date, time, ping, download, upload))
