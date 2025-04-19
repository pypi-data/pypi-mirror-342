"""
    @author Николай Витальевич Никоноров (Bitnik212)
    @date 02.02.2023 20:02
"""
from dataclasses import dataclass


@dataclass
class ReelVideo:
    video_id: str
    width: int
    height: int
    url: str

