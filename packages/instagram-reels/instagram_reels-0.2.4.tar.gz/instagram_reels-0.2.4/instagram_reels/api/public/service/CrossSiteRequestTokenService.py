__author__ = "Николай Витальевич Никоноров (Bitnik212)"
__date__ = "22.02.2024 22:18"

import random

from instagram_reels.api.public.util.BitMapUtil import BitMapUtil


class CrossSiteRequestTokenService:

    def generate(self) -> str:
        arr = []
        count = random.randint(100, 270)
        all_numbers = list(range(1, 43095))
        for i in range(count):
            random_index = random.randint(0, len(all_numbers) - 1)
            random_number = all_numbers.pop(random_index)
            arr.append(random_number)
        return BitMapUtil.to_compressed_string(arr)

