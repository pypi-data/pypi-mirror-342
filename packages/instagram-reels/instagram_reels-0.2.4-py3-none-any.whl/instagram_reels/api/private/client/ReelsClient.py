from asyncio import sleep

import aiohttp as aiohttp
import requests
from bs4 import BeautifulSoup

from instagram_reels.api.private.client.MediaInfoClient import MediaInfoClient
from instagram_reels.api.private.service.MediaInfoService import MediaInfoService
from instagram_reels.common.IReelsClient import IReelsClient
from instagram_reels.common.model.ReelModel import ReelModel


class ReelsClient(IReelsClient):

    def __init__(self, session_id: str):
        self.__session_id = session_id
        self.media_info = MediaInfoService(MediaInfoClient(session_id=session_id))

    async def get(self, reel_id: str) -> ReelModel | None:
        cookies = {
            "sessionid": self.__session_id
        }
        # Иногда куки мешают получить рилс. TODO переделать получение media_id через meta тэг
        reel = await self.__process(await self.__try_one(reel_id))
        if reel is None:
            await sleep(1)
            reel = await self.__process(await self.__try_one(reel_id, cookies))
            if reel is None:
                await sleep(1)
                reel = await self.__process(self.__try_two(reel_id))
                if reel is None:
                    await sleep(1)
                    reel = await self.__process(self.__try_two(reel_id, cookies))
                    if reel is None:
                        return None
        return reel

    async def __process(self, raw_html: str) -> ReelModel | None:
        parser = BeautifulSoup(raw_html, "html.parser")
        all_scripts = parser.find_all("script")
        for script in all_scripts:
            find_index = str(script.text).find("media_id")
            if find_index != -1:
                raw_media_id = script.text[find_index:find_index + 50]
                media_id = self.__parse_media_id(raw_media_id)
                if media_id is not None:
                    return await self.media_info.get_info(media_id)

    @classmethod
    async def __try_one(cls, reel_id: str, cookies: dict | None = None) -> str | None:
        async with aiohttp.ClientSession(cookies=cookies) as session:
            async with session.get(f"https://www.instagram.com/reel/{reel_id}/") as response:
                if response.status == 200:
                    return await response.text()

    @classmethod
    def __try_two(cls, reel_id: str, cookies: dict | None = None) -> str | None:
        response = requests.get(f"https://www.instagram.com/reel/{reel_id}/", cookies=cookies)
        if response.status_code == 200:
            return response.text

    @classmethod
    def __parse_media_id(cls, raw_media_id: str) -> str | None:
        try:
            media_id = raw_media_id.split('"')[2]
            return media_id
        except Exception as e:
            return None
