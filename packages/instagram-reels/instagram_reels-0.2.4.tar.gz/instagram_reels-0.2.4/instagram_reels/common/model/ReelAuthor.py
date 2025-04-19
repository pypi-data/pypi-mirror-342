"""
    @author Николай Витальевич Никоноров (Bitnik212)
    @date 02.02.2023 19:38
"""
from dataclasses import dataclass


@dataclass
class ReelAuthor:
    user_id: str
    username: str
    full_name: str
    profile_pic_url: str
