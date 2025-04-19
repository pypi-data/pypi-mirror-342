__author__ = "Николай Витальевич Никоноров (Bitnik212)"
__date__ = "24.02.2024 04:09"

from instagram_reels.api.public.client.MediaInfoClient import MediaInfoClient
from instagram_reels.api.public.parser.MediaInfoParser import MediaInfoParser
from instagram_reels.common.IReelsClient import IReelsClient
from instagram_reels.common.model.ReelModel import ReelModel


class ReelsClient(IReelsClient):

    def __init__(self):
        self.client = MediaInfoClient()
        self.parser = MediaInfoParser()

    async def get(self, reel_id: str) -> ReelModel | None:
        return self.parser.parse(await self.client.request_info(reel_id))
