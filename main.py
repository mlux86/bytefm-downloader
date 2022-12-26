import argparse
import logging
import os
from os.path import isdir
from urllib.parse import quote

import yaml
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from byte_fm import ByteFm
from download import file_name_from_url, download_file
from downloads_db import DownloadsDatabase

DEFAULT_CONFIG_FILE = 'config.yml'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/84.0.4147.125 ' \
             'Safari/537.36'

# parse arguments

parser = argparse.ArgumentParser(description='Fetches the latest MP3s from your favorite byte.fm programs.')
parser.add_argument('-c', '--config', dest='config', help='Configuration file', type=str)
args = parser.parse_args()

config_file = None
if args.config is not None:
    config_file = args.config

# base directory

abspath = os.path.abspath(__file__)
base_dir = os.path.dirname(abspath)

# configure logging

logging.basicConfig(filename=f'{base_dir}/run.log', level=logging.INFO)

# load config

if config_file is None:
    config_file = f'{base_dir}/{DEFAULT_CONFIG_FILE}'

if not os.path.exists(config_file):
    parser.error(f'The file {config_file} does not exist.')

with open(config_file, 'r') as stream:
    config = yaml.safe_load(stream)

if 'username' not in config or 'password' not in config:
    raise Exception('Cannot find credentials in config file.')

if 'shows' not in config:
    raise Exception('Cannot find shows in config file.')

if 'directory' not in config:
    raise Exception('Cannot find target directory in config file.')
if not isdir(config['directory']):
    raise Exception(f'Cannot find directory {config["directory"]}')

# configure webdriver

opts = Options()
opts.add_argument('--window-size=1920,1080')
opts.add_argument('--headless')
opts.add_argument(f'user-agent={USER_AGENT}')
driver = webdriver.Firefox(options=opts)
driver.implicitly_wait(5)

try:
    byteFm = ByteFm(driver) \
        .login(config['username'], config['password'])

    # configure downloads db

    db = DownloadsDatabase(base_dir)

    # start crawling

    for show in config['shows']:
        logging.info('crawling: %s', show)
        mp3_urls = byteFm\
            .go_to_program(show)\
            .go_to_latest_episode()\
            .get_mp3_urls()

        logging.info('found mp3s: %s', mp3_urls)
        for url in mp3_urls:
            count = db.get_count(show, url)
            if count > 0:
                logging.info('already downloaded: %s', url)
                continue

            logging.info('downloading: %s', url)
            file_name = file_name_from_url(url)
            mp3_path = f'{config["directory"]}/{file_name}'
            download_file(quote(url, safe='.:/'), mp3_path, driver.get_cookies())
            db.log_download(show, url)
except Exception as e:
    logging.exception('An error occurred.', exc_info=e)
finally:
    driver.close()
