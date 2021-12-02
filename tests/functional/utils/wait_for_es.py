import os
import sys

import elasticsearch

sys.path.insert(1, os.path.realpath(os.path.pardir))
from settings import ELASTIC_HOST, ELASTIC_PORT

import time

import logging

logger = logging.getLogger(__name__)
log_format = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format)

bold_green = "\x1b[32;1m"
reset = "\x1b[0m"


def main():
    elastic_online = False
    while not elastic_online:
        try:
            elastic = elasticsearch.Elasticsearch(hosts=[f"{ELASTIC_HOST}:{ELASTIC_PORT}"])
            elastic_answer = elastic.ping()
            if elastic_answer:
                elastic_online = True
                logger.debug('Elastic reporting!'.join([bold_green, reset]))
        except:
            logger.exception('Waiting for elastic...', exc_info=False)
            time.sleep(1)


if __name__ == '__main__':
    main()
