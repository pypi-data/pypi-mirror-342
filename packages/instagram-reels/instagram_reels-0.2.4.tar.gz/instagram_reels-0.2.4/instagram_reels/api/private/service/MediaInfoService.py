__author__ = "Николай Витальевич Никоноров (Bitnik212)"
__date__ = "14.01.2024 02:55"

from instagram_auth.common.exception.web.InstagramSessionExpiredException import InstagramSessionExpiredException

from instagram_reels.api.private.client.MediaInfoClient import MediaInfoClient
from instagram_reels.api.private.parser.MediaInfoParser import MediaInfoParser
from instagram_reels.common.model.ReelModel import ReelModel


class MediaInfoService:

    def __init__(self, client: MediaInfoClient, parser: MediaInfoParser = MediaInfoParser()):
        self.__client = client
        self.__parser = parser

    async def get_info(self, media_id: str) -> ReelModel | None:
        response_text = await self.__client.get(media_id)
        if response_text is not None:
            return self.__parser.parse(response_text)
        else:
            raise InstagramSessionExpiredException("Maybe your sessionid is expired or invalid")
