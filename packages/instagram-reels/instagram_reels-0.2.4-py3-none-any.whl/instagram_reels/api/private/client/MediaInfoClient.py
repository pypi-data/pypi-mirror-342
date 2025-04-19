"""
    @author Николай Витальевич Никоноров (Bitnik212)
    @date 02.02.2023 19:06
"""

import aiohttp

from instagram_reels.common import USER_AGENT


class MediaInfoClient:

    def __init__(
            self,
            session_id: str,
            instagram_app_id_header: str = "936619743392459"
    ):
        self.__headers = {
            "x-ig-app-id": instagram_app_id_header,
            "user-agent": USER_AGENT,
            "cookie": f"sessionid={session_id};"
        }

    async def get(self, media_id: str) -> str | None:
        async with aiohttp.ClientSession(headers=self.__headers) as session:
            async with session.get(f"https://www.instagram.com/api/v1/media/{media_id}/info/") as response:
                if response.status == 200 and response.content_type == "application/json":
                    return await response.text()
                else:
                    return None

