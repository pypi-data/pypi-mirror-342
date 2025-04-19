"""
    @author Николай Витальевич Никоноров (Bitnik212)
    @date 02.02.2023 19:37
"""
from dataclasses import dataclass

from .ReelAuthor import ReelAuthor
from .ReelPreview import ReelPreview
from .ReelVideo import ReelVideo


@dataclass
class ReelModel:
    media_id: str
    code: str
    description: str
    duration: float
    like_count: int
    view_count: int
    play_count: int
    author: ReelAuthor
    previews: list[ReelPreview]
    videos: list[ReelVideo]
