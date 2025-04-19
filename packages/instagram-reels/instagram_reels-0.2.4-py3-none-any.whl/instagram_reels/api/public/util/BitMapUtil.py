__author__ = "Николай Витальевич Никоноров (Bitnik212)"
__date__ = "24.02.2024 02:43"

import re


class BitMapUtil:

    @classmethod
    def convert_to_binary_string(cls, num):
        binary_string = format(num, 'b')
        padding = '0' * (len(binary_string) - 1)
        return padding + binary_string

    @classmethod
    def convert_to_base64_string(cls, binary_string):
        list_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_'
        six_bit_chunks = re.findall('.{1,6}', binary_string + '00000')
        base64_string = ''
        for chunk in six_bit_chunks:
            base64_string += list_chars[int(chunk, 2)]
        return base64_string

    @classmethod
    def to_compressed_string(cls, arr: list):
        bit_map = [0] * (max(arr) + 1)
        for item in arr:
            bit_map[item] = 1
        if len(bit_map) == 0:
            return ''
        compressed_bits = []
        count = 1
        current_bit = bit_map[0]
        current_bit_string = format(current_bit, 'b')
        for i in range(1, len(bit_map)):
            next_bit = bit_map[i]
            if next_bit == current_bit:
                count += 1
            else:
                compressed_bits.append(cls.convert_to_binary_string(count))
                current_bit = next_bit
                count = 1
        if count:
            compressed_bits.append(cls.convert_to_binary_string(count))
        return cls.convert_to_base64_string(current_bit_string + ''.join(compressed_bits))

