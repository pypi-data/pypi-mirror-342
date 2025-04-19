import logging
from typing import List, Optional

import requests
from cachetools.func import ttl_cache

from otaku_media_info.models.bangumi import Bangumi, BangumiEpisode

logger = logging.getLogger(__name__)


# see: https://bangumi.github.io/api
@ttl_cache(maxsize=32, ttl=3600)
def query_bangumi(keyword: str) -> Bangumi:
    with requests.Session() as session:
        session.headers.update({"User-Agent": "jloeve/otaku_media_info"})

        res = session.get(
            f"https://api.bgm.tv/search/subject/{keyword}", params={"type": 2}
        )

        if res.status_code != 200:
            raise Exception(f"Error fetching data from Bangumi API: {res.status_code}")

        data = res.json()

        if data["results"] > 1:
            logger.warning(
                f"Multiple results found for '{keyword}'. Returning the first result."
            )

        data = data["list"][0]

        subject_id = data["id"]

        res = session.get(f"https://api.bgm.tv/v0/subjects/{subject_id}")

        if res.status_code != 200:
            raise Exception(f"Error fetching data from Bangumi API: {res.status_code}")

        return Bangumi(**res.json())


@ttl_cache(maxsize=32, ttl=3600)
def query_episodes(
    subject_id: int, *, type: Optional[int] = None, limit=100, offset=0
) -> List[BangumiEpisode]:
    with requests.Session() as session:
        session.headers.update({"User-Agent": "jloeve/otaku_media_info"})

        res = session.get(
            "https://api.bgm.tv/v0/episodes",
            params={
                "subject_id": subject_id,
                "type": type,
                "limit": limit,
                "offset": offset,
            },
        )
        if res.status_code != 200:
            raise Exception(f"Error fetching data from Bangumi API: {res.status_code}")

        result = res.json()

        return [BangumiEpisode(**item) for item in result["data"]]


@ttl_cache(maxsize=32, ttl=3600)
def query_episode(subject_id: int, ep: int) -> Optional[BangumiEpisode]:
    # 循环查询，直到找到对应的ep
    offset = 0
    limit = 100
    while True:
        episodes = query_episodes(subject_id, limit=limit, offset=offset)

        for episode in episodes:
            if episode.ep == ep:
                return episode

        # 如果没有更多的结果，退出循环
        if len(episodes) < limit:
            break

        offset += limit
    return None
