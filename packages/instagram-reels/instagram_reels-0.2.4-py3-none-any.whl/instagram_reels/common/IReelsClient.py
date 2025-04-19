__author__ = "Николай Витальевич Никоноров (Bitnik212)"
__date__ = "28.01.2024 03:18"

from instagram_reels.common.model.ReelModel import ReelModel


class IReelsClient:

    async def get(self, reel_id: str) -> ReelModel | None: ...

