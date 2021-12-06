import asyncio
import logging
import sys
import time

import elasticsearch
from settings import ELASTIC_HOST, ELASTIC_PORT

logger = logging.getLogger(__name__)
log_format = "%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s"
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=log_format)

bold_green = "\x1b[32;1m"
reset = "\x1b[0m"


async def main():
    elastic_online = False
    while not elastic_online:
        time.sleep(2)
        try:
            elastic = elasticsearch.AsyncElasticsearch(hosts=[f"{ELASTIC_HOST}:{ELASTIC_PORT}"])
            elastic_answer = await elastic.ping()
            if elastic_answer:
                elastic_online = True
                logger.info("Elastic reporting!".join([bold_green, reset]))
                await elastic.close()
        except ConnectionRefusedError:
            logger.exception("Waiting for elastic...", exc_info=False)


if __name__ == "__main__":
    asyncio.run(main())
