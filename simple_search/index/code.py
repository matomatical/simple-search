"""
Encoding and decoding functions for various compression methods
"""
# 'do nothing' non-encoder/decoder
def do_nothing(numbers, **kwargs):
    return numbers

# TODO: implement VBYTE encoding/decoding
def encode_vbyte(numbers, gap=True):
    return numbers
def decode_vbyte(numbers, gap=True):
    return numbers

class Code:
    PLAIN = (do_nothing, do_nothing)
    VBYTE = (encode_vbyte, decode_vbyte)
