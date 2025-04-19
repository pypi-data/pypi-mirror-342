__author__ = "Николай Витальевич Никоноров (Bitnik212)"
__date__ = "24.02.2024 02:45"

from instagram_reels.api.public.model.InstagramSettingDataClass import InstagramSettingDataClass
from instagram_reels.api.public.util.BitMapUtil import BitMapUtil


class DynamicTokenService:

    @classmethod
    def generate(cls, all_settings: dict[str, InstagramSettingDataClass]) -> str:
        settings_indexes = [setting.index for setting_name, setting in all_settings.items()]
        return BitMapUtil.to_compressed_string(settings_indexes)
