__author__ = "Николай Витальевич Никоноров (Bitnik212)"
__date__ = "13.01.2024 09:00"

from dataclasses import dataclass


@dataclass
class InstagramShortUser:
    user: bool
    userId: str
    authenticated: bool
    oneTapPrompt: bool
    has_onboarded_to_text_post_app: bool
    status: str
    reactivated: bool = False

