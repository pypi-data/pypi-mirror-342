__author__ = "Николай Витальевич Никоноров (Bitnik212)"
__date__ = "22.02.2024 20:25"

import json
import random

import aiohttp
import bs4
import math
from bs4 import PageElement

from instagram_reels.api.public.model.InstagramSettingDataClass import InstagramSettingDataClass
from instagram_reels.api.public.model.InstagramSettingsParamsDataClass import InstagramSettingsParamsDataClass
from instagram_reels.api.public.service.CrossSiteRequestTokenService import CrossSiteRequestTokenService
from instagram_reels.api.public.service.DynamicTokenService import DynamicTokenService


class InstagramApiParamsService:

    MAIN_PAGE = "https://www.instagram.com/"
    DEFAULT_REQUIRED_SETTINGS = ["SprinkleConfig", "RelayAPIConfigDefaults", "SiteData", "CookieCoreConfig", "LSD"]

    def __init__(self):
        self.csr_service = CrossSiteRequestTokenService()
        self.dyn_service = DynamicTokenService()
        self.__all_settings: dict[str, InstagramSettingDataClass] = {}

    async def params(
            self,
            required_settings: list[str] = None,
            page_url: str = MAIN_PAGE
    ) -> InstagramSettingsParamsDataClass:
        settings = await self.map_params(
            settings=await self.require_settings(
                page_url=page_url,
                required_setting_names=required_settings
            )
        )
        settings.body.update({
            "__csr": self.csr_service.generate(),
            "__dyn": self.dyn_service.generate(self.__all_settings)
        })
        return settings

    @classmethod
    async def map_params(
            cls,
            settings: dict[str, InstagramSettingDataClass]
    ) -> InstagramSettingsParamsDataClass:
        headers, body, cookies = [{}, {}, {}]
        sprinkle_config = settings.get("SprinkleConfig")
        relay_api_config_defaults_setting = settings.get("RelayAPIConfigDefaults")
        site_data_setting = settings.get("SiteData")
        csrf_token_setting = settings.get("CSRFToken")
        lsd_setting = settings.get("LSD")
        lsd: str | None = lsd_setting.content.get("token", None)
        headers.update(relay_api_config_defaults_setting.content.get("customHeaders"))
        headers.update({
            "X-Fb-Lsd": lsd,
            "X-Csrftoken": csrf_token_setting.content.get("value")
        })
        body.update({
            "jazoest": sprinkle_config.index,
            "__hs": site_data_setting.content.get("haste_session"),
            "__hsi": site_data_setting.content.get("hsi"),
            "__spin_r": site_data_setting.content.get("__spin_r"),
            "__spin_b": site_data_setting.content.get("__spin_b"),
            "__spin_t": site_data_setting.content.get("__spin_t"),
            "__rev": site_data_setting.content.get("server_revision"),
            "lsd": lsd,
            "__s": f"{cls.session_part}:{cls.session_part}:{cls.session_part}"
        })
        cookies.update({
            "csrftoken": csrf_token_setting.content.get("value")
        })
        return InstagramSettingsParamsDataClass(header=headers, cookie=cookies, body=body)

    async def require_settings(
            self,
            page_url: str,
            required_setting_names: list[str] = None
    ) -> dict[str, InstagramSettingDataClass]:
        """
        Получение конфигов из фронта

        :param page_url: Pape downloaded for settings
        :param required_setting_names: Setting names
        :return: dict[InstagramSettingName, InstagramSettingDict]
        """
        if required_setting_names is None:
            required_setting_names = self.DEFAULT_REQUIRED_SETTINGS
        settings: dict[str, InstagramSettingDataClass] = {}
        async with aiohttp.ClientSession() as session:
            async with session.get(url=page_url) as response:
                if response.status == 200 and response.content_type == "text/html":
                    csrf_token = response.cookies.get("csrftoken").value
                    parsed_settings: dict[str, InstagramSettingDataClass] = await self.parse_settings(
                        response_text=await response.text()
                    )
                    self.__all_settings = parsed_settings
                    for required_setting in required_setting_names:
                        parsed_required_setting = parsed_settings.get(required_setting, None)
                        if parsed_required_setting is not None:
                            settings.update({
                                required_setting: parsed_required_setting
                            })
                    settings.update({
                        "CSRFToken": InstagramSettingDataClass(content={"value": csrf_token}, index=0)
                    })
        return settings

    @classmethod
    async def parse_settings(cls, response_text: str) -> dict[str, InstagramSettingDataClass]:
        soup = bs4.BeautifulSoup(response_text, "html.parser")
        max_data_content_len = 0
        script_element: PageElement | None = None
        for element in soup.find_all("script", attrs={"type": "application/json"}):
            data_content_len, = element.get_attribute_list(key="data-content-len")
            if type(data_content_len) is str:
                data_content_len: int = int(data_content_len)
                if data_content_len > max_data_content_len:
                    max_data_content_len = data_content_len
                    script_element = element
        settings_json = json.loads(script_element.text)
        settings = {}
        for settings_item in settings_json["require"][0][3][0]["__bbox"]["define"]:
            settings_name, _, settings_dict, settings_value = settings_item
            settings.update({
                settings_name: InstagramSettingDataClass(content=settings_dict, index=settings_value)
            })
        return settings

    @property
    def session_part(self) -> str:
        i = 36
        j = 6
        k = math.pow(i, j)
        a = math.floor(random.random() * k)
        a = self.convert_base(a, i)  # Convert to base 36
        return ("0" * (j - len(a)) + a)[0:6].lower()

    @classmethod
    def convert_base(cls, num, to_base=10, from_base=10):
        # first convert to decimal number
        n = int(num, from_base) if isinstance(num, str) else num
        # now convert decimal to 'to_base' base
        alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        res = ""
        while n > 0:
            n, m = divmod(n, to_base)
            res += alphabet[m]
        return res[::-1]
