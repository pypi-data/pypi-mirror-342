from __future__ import annotations

from datetime import date
from typing import Dict, List, Union

from pydantic import BaseModel, Field


class Images(BaseModel):
    """Model for the 'images' object."""

    small: str
    grid: str
    large: str
    medium: str
    common: str


class Tag(BaseModel):
    """Model for individual tags in the 'tags' list."""

    name: str
    count: int
    total_cont: int


class InfoboxValueItem(BaseModel):
    """Model for the objects within the value list in 'infobox'."""

    v: str


class InfoboxItem(BaseModel):
    """
    Model for individual items in the 'infobox' list.
    The 'value' can be a string or a list of InfoboxValueItem.
    """

    key: str
    value: Union[str, List[InfoboxValueItem]]


class Rating(BaseModel):
    """Model for the 'rating' object."""

    rank: int
    total: int
    # The 'count' is a dictionary where keys are score strings ("1" to "10")
    # and values are counts (integers).
    count: Dict[str, int]
    score: float  # Using float as scores can potentially be non-integers


class Collection(BaseModel):
    """Model for the 'collection' object."""

    on_hold: int = Field(
        alias="on_hold"
    )  # Explicitly using Field for clarity, though not strictly needed here
    dropped: int
    wish: int
    collect: int
    doing: int


# Main model for the entire JSON structure
class Bangumi(BaseModel):
    """Main model representing the anime data structure."""

    date: (
        date  # Pydantic can automatically parse "YYYY-MM-DD" strings into datetime.date
    )
    platform: str
    images: Images
    summary: str
    name: str
    name_cn: str = Field(
        alias="name_cn"
    )  # Explicitly using Field for clarity, though not strictly needed here
    tags: List[Tag]
    infobox: List[InfoboxItem]
    rating: Rating
    total_episodes: int = Field(
        alias="total_episodes"
    )  # Explicitly using Field for clarity
    collection: Collection
    id: int
    eps: int  # Appears to be a duplicate of total_episodes based on data, but modeled as provided
    meta_tags: List[str] = Field(
        alias="meta_tags"
    )  # Explicitly using Field for clarity
    volumes: int
    series: bool
    locked: bool
    nsfw: bool
    type: int  # Note: 'type' is a Python built-in name, but valid as a field name in Pydantic


class BangumiEpisode(BaseModel):
    """
    Represents information about an anime episode.
    """

    airdate: date = Field(..., description="The air date of the episode.")
    name: str = Field(..., description="The Japanese title of the episode.")
    name_cn: str = Field(..., description="The Chinese title of the episode.")
    duration: str = Field(
        ..., description="The duration of the episode in HH:MM:SS format."
    )
    desc: str = Field(
        ...,
        description="The description of the episode, containing both Japanese and Chinese text.",
    )
    ep: int = Field(..., description="The episode number.")
    sort: int = Field(
        ..., description="The sorting order of the episode (often the same as ep)."
    )
    id: int = Field(..., description="The unique ID of the episode.")
    subject_id: int = Field(
        ..., description="The ID of the subject (anime) this episode belongs to."
    )
    comment: int = Field(..., description="The number of comments for the episode.")
    type: int = Field(
        ..., description="The type of episode (e.g., main episode, special)."
    )
    disc: int = Field(
        ..., description="The disc number the episode is on (if applicable)."
    )
    duration_seconds: int = Field(
        ..., description="The duration of the episode in seconds."
    )


__all__ = ["Bangumi", "BangumiEpisode"]
