__author__ = "Николай Витальевич Никоноров (Bitnik212)"
__date__ = "24.02.2024 04:27"

import json
from json import JSONDecodeError

from instagram_reels.common.JsonParser import JsonParser
from instagram_reels.common.model.ReelAuthor import ReelAuthor
from instagram_reels.common.model.ReelModel import ReelModel
from instagram_reels.common.model.ReelPreview import ReelPreview
from instagram_reels.common.model.ReelVideo import ReelVideo


class MediaInfoParser(JsonParser):

    @staticmethod
    def parse(raw_json: str):
        try:
            content: dict = json.loads(raw_json).get("data").get("xdt_shortcode_media")
        except JSONDecodeError as e:
            raise Exception(f"Error on parse json from instagram web api. Exception: {e}")
        return ReelModel(
            media_id=content.get("id"),
            code=content.get("shortcode"),
            description="" if content.get("edge_media_to_caption", {}).get("edges", []) == [] else content.get("edge_media_to_caption", {}).get("edges", [])[0].get("node", {}).get("text", ""),
            duration=content.get("video_duration"),
            like_count=content["edge_media_preview_like"]["count"],
            view_count=content["video_view_count"],
            play_count=content["video_play_count"],
            author=ReelAuthor(
                user_id=content["owner"]["id"],
                username=content["owner"]["username"],
                full_name=content["owner"]["full_name"],
                profile_pic_url=content["owner"]["profile_pic_url"]
            ),
            previews=[
                ReelPreview(
                    url=preview["src"],
                    width=preview["config_width"],
                    height=preview["config_height"]
                )
                for preview in content["display_resources"]
            ],
            videos=[
                ReelVideo(
                    video_id="0",
                    width=content["dimensions"]["width"],
                    height=content["dimensions"]["height"],
                    url=content["video_url"]
                )
            ]
        )

