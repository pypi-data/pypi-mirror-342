"""
    @author Николай Витальевич Никоноров (Bitnik212)
    @date 02.02.2023 19:59
"""
from dataclasses import dataclass


@dataclass
class ReelPreview:
    width: int
    height: int
    url: str

