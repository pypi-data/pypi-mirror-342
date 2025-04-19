__author__ = "Николай Витальевич Никоноров (Bitnik212)"
__date__ = "29.02.2024 08:14"

from instagram_reels.common.IReelsClient import IReelsClient


class InstagramAPIClient:

    async def reels(self) -> IReelsClient: ...

