# !/usr/bin/python3
# coding: utf-8
import os
import struct
import sys
import base64

import gzip

import umsgpack

if __name__ == '__main__':
    msgpack_path = os.path.expanduser('~') + "/Documents/GitHub/AzusaHikari/uma-python-tools/MsgPack" \
                                             "/CarrotJuicer_team_race/134775491/"
    for root, dirs, files in os.walk(msgpack_path):
        for name in files:
            if ".msgpack" in name:  # 判断某一字符串是否具有某一字串，可以使用in语句
                with open(os.path.join(root, name), "rb") as load_f:
                    msg = load_f.read()
                    msg = umsgpack.unpackb(msg)
                for race_result in msg["data"]["race_result_array"]:
                    race_scenario = race_result["race_scenario"]
                    print(race_scenario)
                    base64_data = base64.b64decode(race_scenario.encode())
                    print(base64_data)
                    buffer = gzip.decompress(base64_data)
                    print(buffer)
                    [maxLength, version] = struct.unpack_from("<ii", buffer, 0)
                    offset = 4 + maxLength
                    [distanceDiffMax, horseNum, horseFrameSize, horseResultSize] = struct.unpack_from("<fiii", buffer, offset)
                    print(horseNum)
                    # str_unzip = bytes_decom.decode()
                    # print(str_unzip)
                    break
                break
    # race_scenario = msg["data"]["race_result_array"][0]["race_scenario"]
    # print(race_scenario)
    # base64_data = base64.b64decode(race_scenario.encode(encoding="unicode_escape"))
    # print(base64_data)
    # bytes_decom = gzip.decompress(base64_data)
    # print(bytes_decom)
    # str_unzip = bytes_decom.decode()
    # print(str_unzip)
