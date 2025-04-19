__author__ = "Николай Витальевич Никоноров (Bitnik212)"
__date__ = "22.02.2024 20:27"

from dataclasses import dataclass


@dataclass
class InstagramSettingDataClass:
    content: dict
    index: int | None
