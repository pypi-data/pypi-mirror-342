# coding=utf-8

from dataclasses import dataclass
from pathlib import Path
from typing import List, Literal, Optional

Language = Literal["zh", "en", "jp"]


@dataclass
class Title:
    zh: Optional[str] = None
    en: Optional[str] = None
    jp: Optional[str] = None


@dataclass
class Source:
    name: str


@dataclass
class RawOtakuMediaInfo:
    raw_path: Path
    raw_name: str
    raw_size: int
    raw_mtime: float
    raw_ctime: float
    raw_title: Title
    raw_author: str


@dataclass
class OtakuMediaInfo:
    raw: RawOtakuMediaInfo
    title: str
    author: str
    type: str
    page: Optional[int]
    total: Optional[int]
    language: Language
    categories: List[str]


@dataclass
class RawBangumiMediaInfo(RawOtakuMediaInfo):
    raw_season: str


@dataclass
class BangumiMediaInfo(OtakuMediaInfo):
    raw: RawBangumiMediaInfo
    season: int
    sub: str
    sub_group: str
    resolution: str
    capture_source: str
