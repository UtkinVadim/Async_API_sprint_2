from typing import Optional

from elasticsearch import AsyncElasticsearch

from services.searcher import ElasticSearcher

es: Optional[AsyncElasticsearch] = None


async def get_elastic() -> ElasticSearcher:
    return ElasticSearcher(es)
