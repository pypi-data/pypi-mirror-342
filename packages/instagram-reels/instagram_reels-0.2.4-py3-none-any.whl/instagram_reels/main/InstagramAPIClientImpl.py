__author__ = "Николай Витальевич Никоноров (Bitnik212)"
__date__ = "14.01.2024 04:21"

from instagram_auth.service.WebLoginService import WebLoginService

from instagram_reels.api.private.client.ReelsClient import ReelsClient as AuthorizedReelsClient
from instagram_reels.api.public.client.ReelsClient import ReelsClient as NonAuthorizedReelsClient
from instagram_reels.common.IReelsClient import IReelsClient
from instagram_reels.main.InstagramAPIClient import InstagramAPIClient


class InstagramAPIClientImpl(InstagramAPIClient):

    def __init__(self):
        self.__login_service = WebLoginService()
        self.user_id: int | None = None
        self.sessionid: str | None = None

    async def login_with_credentials(self, username: str, password: str) -> InstagramAPIClient:
        user, sessionid = await self.__login_service.login(username, password)
        self.sessionid = sessionid
        self.user_id = user.userId
        return self

    async def login_with_sessionid(self, sessionid: str) -> InstagramAPIClient:
        self.sessionid = sessionid
        self.user_id = int(sessionid.split(":")[0])
        return self

    async def reels(self) -> IReelsClient:
        if self.sessionid is not None:
            return AuthorizedReelsClient(session_id=self.sessionid)
        else:
            return NonAuthorizedReelsClient()
