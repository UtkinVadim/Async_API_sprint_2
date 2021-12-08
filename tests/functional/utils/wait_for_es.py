import asyncio
import logging
import sys

import backoff
import elasticsearch
from functional.settings import ELASTIC_HOST, ELASTIC_PORT

logger = logging.getLogger(__name__)
log_format = "%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s"
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=log_format)

bold_green = "\x1b[32;1m"
reset = "\x1b[0m"


def backoff_handler(_details):
    logger.exception("Waiting for elastic...", exc_info=False)


@backoff.on_exception(backoff.expo, ConnectionError, max_time=300, max_tries=15, on_backoff=backoff_handler)
async def main():
    elastic = elasticsearch.AsyncElasticsearch(hosts=[f"{ELASTIC_HOST}:{ELASTIC_PORT}"])
    elastic_answer = await elastic.ping(error_trace=False)
    if elastic_answer:
        logger.info("Elastic reporting!".join([bold_green, reset]))
        await elastic.close()
    else:
        raise ConnectionError


if __name__ == "__main__":
    asyncio.run(main())
