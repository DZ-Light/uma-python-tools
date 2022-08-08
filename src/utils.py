import json
import os
import shutil
import sqlite3
import struct
from decimal import *

import msgpack
from prettytable import PrettyTable
from pykakasi import kakasi

dbPath = "../master_jp/master.mdb"
umdbPath = "../data/umdb.json"
charaPath = "../data/chara_data.json"
cardPath = "../data/card_data.json"
supportCardPath = "../data/support_card_data.json"
skillPath = "../data/skill_data.json"
racePath = "../data/race_data.json"
eventPath = "../data/event_data.json"
factorPath = "../data/factor_data.json"
itemPath = "../data/item_data.json"
translatePath = "../data/translate.json"
cjedbPath = "../data/cjedb.json"
basicPoint = [
    0,
    1,
    1,
    2,
    2,
    3,
    3,
    4,
    4,
    5,
    5,
    6,
    6,
    7,
    7,
    8,
    8,
    9,
    9,
    10,
    10,
    11,
    11,
    12,
    12,
    13,
    13,
    14,
    14,
    15,
    15,
    16,
    16,
    17,
    17,
    18,
    18,
    19,
    19,
    20,
    20,
    21,
    21,
    22,
    22,
    23,
    23,
    24,
    24,
    25,
    25,
    26,
    27,
    28,
    29,
    29,
    30,
    31,
    32,
    33,
    33,
    34,
    35,
    36,
    37,
    37,
    38,
    39,
    40,
    41,
    41,
    42,
    43,
    44,
    45,
    45,
    46,
    47,
    48,
    49,
    49,
    50,
    51,
    52,
    53,
    53,
    54,
    55,
    56,
    57,
    57,
    58,
    59,
    60,
    61,
    61,
    62,
    63,
    64,
    65,
    66,
    67,
    68,
    69,
    70,
    71,
    72,
    73,
    74,
    75,
    76,
    77,
    78,
    79,
    80,
    81,
    82,
    83,
    84,
    85,
    86,
    87,
    88,
    89,
    90,
    91,
    92,
    93,
    94,
    95,
    96,
    97,
    98,
    99,
    100,
    101,
    102,
    103,
    104,
    105,
    106,
    107,
    108,
    109,
    110,
    111,
    112,
    113,
    114,
    115,
    116,
    117,
    118,
    120,
    121,
    122,
    124,
    125,
    126,
    128,
    129,
    130,
    131,
    133,
    134,
    135,
    137,
    138,
    139,
    141,
    142,
    143,
    144,
    146,
    147,
    148,
    150,
    151,
    152,
    154,
    155,
    156,
    157,
    159,
    160,
    161,
    163,
    164,
    165,
    167,
    168,
    169,
    170,
    172,
    173,
    174,
    176,
    177,
    178,
    180,
    181,
    183,
    184,
    186,
    188,
    189,
    191,
    192,
    194,
    196,
    197,
    199,
    200,
    202,
    204,
    205,
    207,
    208,
    210,
    212,
    213,
    215,
    216,
    218,
    220,
    221,
    223,
    224,
    226,
    228,
    229,
    231,
    232,
    234,
    236,
    237,
    239,
    240,
    242,
    244,
    245,
    247,
    248,
    250,
    252,
    253,
    255,
    256,
    258,
    260,
    261,
    263,
    265,
    267,
    269,
    270,
    272,
    274,
    276,
    278,
    279,
    281,
    283,
    285,
    287,
    288,
    290,
    292,
    294,
    296,
    297,
    299,
    301,
    303,
    305,
    306,
    308,
    310,
    312,
    314,
    315,
    317,
    319,
    321,
    323,
    324,
    326,
    328,
    330,
    332,
    333,
    335,
    337,
    339,
    341,
    342,
    344,
    346,
    348,
    350,
    352,
    354,
    356,
    358,
    360,
    362,
    364,
    366,
    368,
    371,
    373,
    375,
    377,
    379,
    381,
    383,
    385,
    387,
    389,
    392,
    394,
    396,
    398,
    400,
    402,
    404,
    406,
    408,
    410,
    413,
    415,
    417,
    419,
    412,
    423,
    425,
    427,
    429,
    431,
    434,
    436,
    438,
    440,
    442,
    444,
    446,
    448,
    450,
    452,
    455,
    457,
    459,
    462,
    464,
    467,
    469,
    471,
    474,
    476,
    479,
    481,
    483,
    486,
    488,
    491,
    493,
    495,
    498,
    500,
    503,
    505,
    507,
    510,
    512,
    515,
    517,
    519,
    522,
    524,
    527,
    529,
    531,
    534,
    536,
    539,
    541,
    543,
    546,
    548,
    551,
    553,
    555,
    558,
    560,
    563,
    565,
    567,
    570,
    572,
    575,
    577,
    580,
    582,
    585,
    588,
    590,
    593,
    595,
    598,
    601,
    603,
    606,
    608,
    611,
    614,
    616,
    619,
    621,
    624,
    627,
    629,
    632,
    634,
    637,
    640,
    642,
    645,
    647,
    650,
    653,
    655,
    658,
    660,
    663,
    666,
    668,
    671,
    673,
    676,
    679,
    681,
    684,
    686,
    689,
    692,
    694,
    697,
    699,
    702,
    705,
    707,
    710,
    713,
    716,
    719,
    721,
    724,
    727,
    730,
    733,
    735,
    738,
    741,
    744,
    747,
    749,
    752,
    755,
    758,
    761,
    763,
    766,
    769,
    772,
    775,
    777,
    780,
    783,
    786,
    789,
    791,
    794,
    797,
    800,
    803,
    805,
    808,
    811,
    814,
    817,
    819,
    822,
    825,
    828,
    831,
    833,
    836,
    839,
    842,
    845,
    847,
    850,
    853,
    856,
    859,
    862,
    865,
    868,
    871,
    874,
    876,
    879,
    882,
    885,
    888,
    891,
    894,
    897,
    900,
    903,
    905,
    908,
    911,
    914,
    917,
    920,
    923,
    926,
    929,
    931,
    934,
    937,
    940,
    943,
    946,
    949,
    952,
    955,
    958,
    961,
    963,
    966,
    969,
    972,
    975,
    978,
    981,
    984,
    987,
    990,
    993,
    996,
    999,
    1002,
    1005,
    1008,
    1011,
    1014,
    1017,
    1020,
    1023,
    1026,
    1029,
    1032,
    1035,
    1038,
    1041,
    1044,
    1047,
    1050,
    1053,
    1056,
    1059,
    1062,
    1065,
    1068,
    1071,
    1074,
    1077,
    1080,
    1083,
    1086,
    1089,
    1092,
    1095,
    1098,
    1101,
    1104,
    1107,
    1110,
    1113,
    1116,
    1119,
    1122,
    1125,
    1128,
    1131,
    1134,
    1137,
    1140,
    1143,
    1146,
    1149,
    1152,
    1155,
    1158,
    1161,
    1164,
    1167,
    1171,
    1174,
    1177,
    1180,
    1183,
    1186,
    1189,
    1192,
    1195,
    1198,
    1202,
    1205,
    1208,
    1211,
    1214,
    1217,
    1220,
    1223,
    1226,
    1229,
    1233,
    1236,
    1239,
    1242,
    1245,
    1248,
    1251,
    1254,
    1257,
    1260,
    1264,
    1267,
    1270,
    1273,
    1276,
    1279,
    1282,
    1285,
    1288,
    1291,
    1295,
    1298,
    1301,
    1304,
    1308,
    1311,
    1314,
    1318,
    1321,
    1324,
    1328,
    1331,
    1334,
    1337,
    1341,
    1344,
    1347,
    1351,
    1354,
    1357,
    1361,
    1364,
    1367,
    1370,
    1374,
    1377,
    1380,
    1384,
    1387,
    1390,
    1394,
    1397,
    1400,
    1403,
    1407,
    1410,
    1413,
    1417,
    1420,
    1423,
    1427,
    1430,
    1433,
    1436,
    1440,
    1443,
    1446,
    1450,
    1453,
    1456,
    1460,
    1463,
    1466,
    1470,
    1473,
    1477,
    1480,
    1483,
    1487,
    1490,
    1494,
    1497,
    1500,
    1504,
    1507,
    1511,
    1514,
    1517,
    1521,
    1524,
    1528,
    1531,
    1534,
    1538,
    1541,
    1545,
    1548,
    1551,
    1555,
    1558,
    1562,
    1565,
    1568,
    1572,
    1575,
    1579,
    1582,
    1585,
    1589,
    1592,
    1596,
    1596,
    1602,
    1606,
    1609,
    1613,
    1616,
    1619,
    1623,
    1626,
    1630,
    1633,
    1637,
    1640,
    1644,
    1647,
    1651,
    1654,
    1658,
    1661,
    1665,
    1668,
    1672,
    1675,
    1679,
    1682,
    1686,
    1689,
    1693,
    1696,
    1700,
    1703,
    1707,
    1710,
    1714,
    1717,
    1721,
    1724,
    1728,
    1731,
    1735,
    1738,
    1742,
    1745,
    1749,
    1752,
    1756,
    1759,
    1763,
    1766,
    1770,
    1773,
    1777,
    1780,
    1784,
    1787,
    1791,
    1794,
    1798,
    1801,
    1805,
    1808,
    1812,
    1816,
    1820,
    1824,
    1828,
    1832,
    1836,
    1840,
    1844,
    1847,
    1851,
    1855,
    1859,
    1863,
    1867,
    1871,
    1875,
    1879,
    1883,
    1886,
    1890,
    1894,
    1898,
    1902,
    1906,
    1910,
    1914,
    1918,
    1922,
    1925,
    1929,
    1933,
    1937,
    1941,
    1945,
    1949,
    1953,
    1957,
    1961,
    1964,
    1968,
    1972,
    1976,
    1980,
    1984,
    1988,
    1992,
    1996,
    2000,
    2004,
    2008,
    2012,
    2016,
    2020,
    2024,
    2028,
    2032,
    2036,
    2041,
    2045,
    2049,
    2053,
    2057,
    2061,
    2065,
    2069,
    2073,
    2077,
    2082,
    2086,
    2090,
    2094,
    2098,
    2102,
    2106,
    2110,
    2114,
    2118,
    2123,
    2127,
    2131,
    2135,
    2139,
    2143,
    2147,
    2151,
    2155,
    2159,
    2164,
    2168,
    2172,
    2176,
    2180,
    2184,
    2188,
    2192,
    2196,
    2200,
    2205,
    2209,
    2213,
    2217,
    2221,
    2226,
    2230,
    2234,
    2238,
    2242,
    2247,
    2251,
    2255,
    2259,
    2263,
    2268,
    2272,
    2276,
    2280,
    2284,
    2289,
    2293,
    2297,
    2301,
    2305,
    2310,
    2314,
    2318,
    2322,
    2326,
    2331,
    2335,
    2339,
    2343,
    2347,
    2352,
    2356,
    2360,
    2364,
    2368,
    2373,
    2377,
    2381,
    2385,
    2389,
    2394,
    2398,
    2402,
    2406,
    2410,
    2415,
    2419,
    2423,
    2427,
    2432,
    2436,
    2440,
    2445,
    2449,
    2453,
    2458,
    2462,
    2466,
    2470,
    2475,
    2479,
    2483,
    2488,
    2492,
    2496,
    2501,
    2505,
    2509,
    2513,
    2518,
    2522,
    2526,
    2531,
    2535,
    2539,
    2544,
    2548,
    2552,
    2556,
    2561,
    2565,
    2569,
    2574,
    2578,
    2582,
    2587,
    2591,
    2595,
    2599,
    2604,
    2608,
    2612,
    2617,
    2621,
    2625,
    2630,
    2635,
    2640,
    2645,
    2650,
    2656,
    2661,
    2666,
    2671,
    2676,
    2682,
    2687,
    2692,
    2697,
    2702,
    2708,
    2713,
    2718,
    2723,
    2728,
    2734,
    2739,
    2744,
    2749,
    2754,
    2760,
    2765,
    2770,
    2775,
    2780,
    2786,
    2791,
    2796,
    2801,
    2806,
    2812,
    2817,
    2822,
    2827,
    2832,
    2838,
    2843,
    2848,
    2853,
    2858,
    2864,
    2869,
    2874,
    2879,
    2884,
    2890,
    2895,
    2901,
    2906,
    2912,
    2917,
    2923,
    2928,
    2934,
    2939,
    2945,
    2950,
    2956,
    2961,
    2967,
    2972,
    2978,
    2983,
    2989,
    2994,
    3000,
    3005,
    3011,
    3016,
    3022,
    3027,
    3033,
    3038,
    3044,
    3049,
    3055,
    3060,
    3066,
    3071,
    3077,
    3082,
    3088,
    3093,
    3099,
    3104,
    3110,
    3115,
    3121,
    3126,
    3132,
    3137,
    3143,
    3148,
    3154,
    3159,
    3165,
    3171,
    3178,
    3184,
    3191,
    3198,
    3204,
    3211,
    3217,
    3224,
    3231,
    3237,
    3244,
    3250,
    3257,
    3264,
    3283,
    3277,
    3283,
    3290,
    3297,
    3303,
    3310,
    3316,
    3323,
    3330,
    3336,
    3343,
    3349,
    3356,
    3363,
    3369,
    3376,
    3382,
    3389,
    3396,
    3402,
    3409,
    3415,
    3422,
    3429,
    3435,
    3442,
    3448,
    3455,
    3462,
    3468,
    3475,
    3481,
    3488,
    3495,
    3501,
    3508,
    3515,
    3522,
    3529,
    3535,
    3542,
    3549,
    3556,
    3563,
    3569,
    3576,
    3583,
    3590,
    3597,
    3603,
    3610,
    3617,
    3624,
    3631,
    3637,
    3644,
    3651,
    3658,
    3665,
    3671,
    3678,
    3685,
    3692,
    3699,
    3705,
    3712,
    3719,
    3726,
    3733,
    3739,
    3746,
    3753,
    3760,
    3767,
    3773,
    3780,
    3787,
    3794,
    3801,
    3807,
    3814,
    3821,
    3828,
    3835,
    3841,
]


def print_file_name(name, file_type):
    print("filename: " + color(name, for_color=34), end="\t")
    print("type: " + color(file_type, for_color=34))


def skill_condition_find(condition, string):
    pos = condition.find(string)
    if pos != -1:
        pos += len(string)
        if condition[pos: pos + 1] >= "0" or condition[pos: pos + 1] <= "9":
            return int(condition[pos: pos + 1])
    return -1


def cale_win_saddle(info):
    win_saddle = len(
        [
            val
            for val in info["win_saddle_id_array"]
            if val
               in info["succession_chara_array"][0]["win_saddle_id_array"]
        ]
    ) + len(
        [
            val
            for val in info["win_saddle_id_array"]
            if val
               in info["succession_chara_array"][1]["win_saddle_id_array"]
        ]
    )
    return win_saddle


def prop_coefficient(p):
    # S,A
    if p == 8 or p == 7:
        return 1.1
    # B,C
    if p == 6 or p == 5:
        return 0.9
    # D,E,F
    if p == 4 or p == 3 or p == 2:
        return 0.8
    # G
    if p == 1:
        return 0.7
    return 1


def color(target, mode=0, for_color=38, bg_color=48):
    """
    It takes a string, and returns the same string, but with ANSI color codes added to it

    :param target: The string you want to color
    :param mode: 0 = normal, 1 = bold, 4 = underline, 7 = negative, defaults to 0 (optional)
    :param for_color: 30-37, defaults to 38 (optional)
    :param bg_color: The background color, defaults to 48 (optional)
    :return: A string with the target text in the specified color.
    """
    return (
            "\033["
            + str(mode)
            + ";"
            + str(for_color)
            + ";"
            + str(bg_color)
            + "m"
            + str(target)
            + "\033[0m"
    )


def calc(chara_info):
    # 技能数据
    with open(skillPath, "r", encoding="utf-8") as load_f:
        skill_dict = json.load(load_f)
    # 已有技能
    skill_array = chara_info["skill_array"]
    # 可选技能
    skill_tips_array = chara_info["skill_tips_array"]
    skill_point = chara_info["skill_point"]
    hint_array = [0, 10, 20, 30, 35, 40]
    max_rank_point = 0
    max_rank_point += basicPoint[chara_info["speed"]]
    max_rank_point += basicPoint[chara_info["stamina"]]
    max_rank_point += basicPoint[chara_info["power"]]
    max_rank_point += basicPoint[chara_info["wiz"]]
    max_rank_point += basicPoint[chara_info["guts"]]
    max_rank_point += chara_info["skill_array"][0]["level"] * (
        170 if chara_info["rarity"] > 2 else 120
    )
    skill_tips_map = {}
    for skill in skill_array:
        skill_id_out = str(skill["skill_id"])
        if skill_dict[skill_id_out]["rarity"] >= 3:
            max_rank_point += chara_info["skill_array"][0]["level"] * (
                170 if chara_info["rarity"] > 2 else 120
            )
        else:
            temp_out = skill_dict[skill_id_out]
            grade_value_out = get_grade_value(chara_info, temp_out)
            need_skill_point = 0 if temp_out["group_rate"] > 0 else temp_out["need_skill_point"]
            skill_tips_out = {"id": temp_out["id"], "group_id": temp_out["group_id"],
                              "rarity": temp_out["rarity"], "group_rate": temp_out["group_rate"],
                              "grade_value": grade_value_out, "need_skill_point": need_skill_point,
                              "disp_order": temp_out["disp_order"],
                              "name": temp_out["name_jp"]}
            if temp_out["group_rate"] > 1:
                for skill_id_in in skill_dict:
                    if temp_out["group_id"] == skill_dict[skill_id_in]["group_id"] and skill_dict[skill_id_in][
                        "rarity"] < temp_out["rarity"] and skill_id_in not in skill_tips_map:
                        temp_in = skill_dict[skill_id_in]
                        grade_value_in = get_grade_value(chara_info, temp_in)
                        skill_tips_int = {"id": temp_in["id"], "group_id": temp_in["group_id"],
                                          "rarity": temp_in["rarity"], "group_rate": temp_in["group_rate"],
                                          "grade_value": grade_value_in, "need_skill_point": 0,
                                          "disp_order": temp_in["disp_order"],
                                          "name": temp_in["name_jp"]}
                        skill_tips_map[skill_id_in] = skill_tips_int
            max_rank_point += grade_value_out
            skill_tips_map[str(skill["skill_id"])] = skill_tips_out

    if 7 in chara_info["chara_effect_id_array"]:
        if_global_discount = True
    else:
        if_global_discount = False
    print("当前分数：" + color(str(max_rank_point), for_color=31), end="\t")
    for skill_tips in skill_tips_array:
        for skill_id in skill_dict:
            if skill_tips["group_id"] == skill_dict[skill_id]["group_id"] and skill_dict[skill_id]["rarity"] <= \
                    skill_tips["rarity"] and skill_dict[skill_id]["group_rate"] > 0 and skill_id not in skill_tips_map:
                temp = skill_dict[skill_id]
                grade_value = get_grade_value(chara_info, temp)
                need_skill_point = Decimal(temp["need_skill_point"] * (
                        (1 - 0.01 * hint_array[skill_tips["level"]] - 0.00001) - 0.1 * (
                    1 if if_global_discount else 0))).quantize(Decimal("1"), ROUND_HALF_UP)
                skill_temp = {"id": temp["id"], "group_id": temp["group_id"],
                              "rarity": temp["rarity"], "group_rate": temp["group_rate"],
                              "grade_value": grade_value, "need_skill_point": int(need_skill_point),
                              "disp_order": temp["disp_order"],
                              "name": temp["name_jp"]}
                skill_tips_map[skill_id] = skill_temp
    skill_table = PrettyTable(
        ["name", "id", "group_id", "rarity", "group_rate", "point_rate", "grade_value", "need_skill_point",
         "disp_order"])
    skill_final_map = {}
    for skill_id_out in skill_tips_map:
        skill_out = skill_tips_map[skill_id_out]
        grade_value = skill_out["grade_value"]
        if skill_out["group_rate"] > 1 and skill_out["need_skill_point"] != 0:
            for skill_id_in in skill_tips_map:
                if skill_out["group_id"] == skill_tips_map[skill_id_in]["group_id"] and skill_tips_map[skill_id_in][
                    "group_rate"] < skill_out["group_rate"] and skill_tips_map[skill_id_in]["group_rate"] > 0:
                    skill_in = skill_tips_map[skill_id_in]
                    grade_value -= skill_in["grade_value"]
            skill_out["grade_value"] = grade_value
        if skill_out["need_skill_point"] != 0:
            point_rate = Decimal(skill_out["grade_value"] / skill_out["need_skill_point"]).quantize(Decimal("0.01"),
                                                                                                    ROUND_HALF_UP)
            skill_final_map[skill_id_out] = point_rate
    skill_final_list = sorted(skill_final_map.items(),
                              key=lambda x: x[1], reverse=True)
    for skill_final in skill_final_list:
        skill = skill_tips_map[str(skill_final[0])]
        if skill_point > skill["need_skill_point"]:
            skill_point -= skill["need_skill_point"]
            max_rank_point += skill["grade_value"]
    print("预估分数：" + color(str(max_rank_point), for_color=31))
    for skill_final in skill_final_list:
        skill = skill_tips_map[str(skill_final[0])]
        skill_table.add_row(
            [skill["name"], str(skill["id"]), str(skill["group_id"]), str(skill["rarity"]),
             str(skill["group_rate"]), skill_final[1], str(
                skill["grade_value"]),
             str(skill["need_skill_point"]), str(skill["disp_order"])])
    print(skill_table)


def get_grade_value(chara_info, skill):
    condition = skill["condition_1"]
    value = skill["grade_value"]
    t = skill_condition_find(condition, "ground_type==")
    if t == 1:
        value = Decimal(
            value *
            prop_coefficient(chara_info["proper_ground_turf"])
        ).quantize(Decimal("1"), ROUND_HALF_UP)
    if t == 2:
        value = Decimal(
            value *
            prop_coefficient(chara_info["proper_ground_dirt"])
        ).quantize(Decimal("1"), ROUND_HALF_UP)
    t = skill_condition_find(condition, "distance_type==")
    if t == 1:
        value = Decimal(
            value *
            prop_coefficient(chara_info["proper_distance_short"])
        ).quantize(Decimal("1"), ROUND_HALF_UP)
    if t == 2:
        value = Decimal(
            value *
            prop_coefficient(chara_info["proper_distance_mile"])
        ).quantize(Decimal("1"), ROUND_HALF_UP)
    if t == 3:
        value = Decimal(
            value *
            prop_coefficient(chara_info["proper_distance_middle"])
        ).quantize(Decimal("1"), ROUND_HALF_UP)
    if t == 4:
        value = Decimal(
            value *
            prop_coefficient(chara_info["proper_distance_long"])
        ).quantize(Decimal("1"), ROUND_HALF_UP)
    t = skill_condition_find(condition, "running_style==")
    if t == 1:
        value = Decimal(
            value
            * prop_coefficient(chara_info["proper_running_style_nige"])
        ).quantize(Decimal("1"), ROUND_HALF_UP)
    if t == 2:
        value = Decimal(
            value
            * prop_coefficient(chara_info["proper_running_style_senko"])
        ).quantize(Decimal("1"), ROUND_HALF_UP)
    if t == 3:
        value = Decimal(
            value
            * prop_coefficient(chara_info["proper_running_style_sashi"])
        ).quantize(Decimal("1"), ROUND_HALF_UP)
    if t == 4:
        value = Decimal(
            value
            * prop_coefficient(chara_info["proper_running_style_oikomi"])
        ).quantize(Decimal("1"), ROUND_HALF_UP)
    return int(value)


def deal_path(old_path, new_path, name, num):
    clear_path("../MsgPack/" + new_path, num)
    clear_path("../Json/" + new_path, num)
    move_file(old_path, "../MsgPack/" + new_path, name)
    convert_msgpack_json(new_path, name)


def convert_msgpack_json(new_path, name):
    with open(os.path.join("../MsgPack/" + new_path, name), "rb") as load_f:
        msg = load_f.read()
        if "Q.msgpack" in name:
            offset = struct.unpack_from("<i", msg, 0)[0]
            msg = msg[4 + offset:]
        msg = msgpack.loads(msg, strict_map_key=False)
    if not os.path.exists("../Json/" + new_path):
        os.makedirs("../Json/" + new_path)
    with open(
            os.path.join(
                "../Json/" + new_path, name.replace(".msgpack", ".json")
            ),
            "w",
            encoding="utf-8",
    ) as dump_f:
        json.dump(msg, dump_f, ensure_ascii=False, indent=2)


def json_has_text(dic_json, text):
    if isinstance(dic_json, dict):  # 判断是否是字典类型isinstance 返回True false
        for key in dic_json:
            if text == key:
                return True
            if isinstance(dic_json[key], dict):  # 如果dic_json[key]依旧是字典类型
                if json_has_text(dic_json[key], text):
                    return True


def move_file(old_path, new_path, name):
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    shutil.copy(
        os.path.join(old_path, name),
        os.path.join(new_path, name),
    )


def clear_path(path, num):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        file_list = os.listdir(path)
        file_list.sort(reverse=True)
        i = 0
        for name in file_list:
            i += 1
            if i > num:
                os.remove(os.path.join(path, name))


def get_factor(factor_data, factor_id_array):
    if 101 in factor_id_array:
        factor_data["速"] += 1
    if 102 in factor_id_array:
        factor_data["速"] += 2
    if 103 in factor_id_array:
        factor_data["速"] += 3
    if 201 in factor_id_array:
        factor_data["耐"] += 1
    if 202 in factor_id_array:
        factor_data["耐"] += 2
    if 203 in factor_id_array:
        factor_data["耐"] += 3
    if 301 in factor_id_array:
        factor_data["力"] += 1
    if 302 in factor_id_array:
        factor_data["力"] += 2
    if 303 in factor_id_array:
        factor_data["力"] += 3
    if 401 in factor_id_array:
        factor_data["根"] += 1
    if 402 in factor_id_array:
        factor_data["根"] += 2
    if 403 in factor_id_array:
        factor_data["根"] += 3
    if 501 in factor_id_array:
        factor_data["智"] += 1
    if 502 in factor_id_array:
        factor_data["智"] += 2
    if 503 in factor_id_array:
        factor_data["智"] += 3
    if 1101 in factor_id_array:
        factor_data["芝"] += 1
    if 1102 in factor_id_array:
        factor_data["芝"] += 2
    if 1103 in factor_id_array:
        factor_data["芝"] += 3
    if 1201 in factor_id_array:
        factor_data["泥"] += 1
    if 1202 in factor_id_array:
        factor_data["泥"] += 2
    if 1203 in factor_id_array:
        factor_data["泥"] += 3
    if 3101 in factor_id_array:
        factor_data["短"] += 1
    if 3102 in factor_id_array:
        factor_data["短"] += 2
    if 3103 in factor_id_array:
        factor_data["短"] += 3
    if 3201 in factor_id_array:
        factor_data["英"] += 1
    if 3202 in factor_id_array:
        factor_data["英"] += 2
    if 3203 in factor_id_array:
        factor_data["英"] += 3
    if 3301 in factor_id_array:
        factor_data["中"] += 1
    if 3302 in factor_id_array:
        factor_data["中"] += 2
    if 3303 in factor_id_array:
        factor_data["中"] += 3
    if 3401 in factor_id_array:
        factor_data["长"] += 1
    if 3402 in factor_id_array:
        factor_data["长"] += 2
    if 3403 in factor_id_array:
        factor_data["长"] += 3
    if 2101 in factor_id_array:
        factor_data["逃"] += 1
    if 2102 in factor_id_array:
        factor_data["逃"] += 2
    if 2103 in factor_id_array:
        factor_data["逃"] += 3
    if 2201 in factor_id_array:
        factor_data["先"] += 1
    if 2202 in factor_id_array:
        factor_data["先"] += 2
    if 2203 in factor_id_array:
        factor_data["先"] += 3
    if 2301 in factor_id_array:
        factor_data["差"] += 1
    if 2302 in factor_id_array:
        factor_data["差"] += 2
    if 2303 in factor_id_array:
        factor_data["差"] += 3
    if 2401 in factor_id_array:
        factor_data["追"] += 1
    if 2402 in factor_id_array:
        factor_data["追"] += 2
    if 2403 in factor_id_array:
        factor_data["追"] += 3
    if 3000101 in factor_id_array:
        factor_data["URA"] += 1
    if 3000102 in factor_id_array:
        factor_data["URA"] += 2
    if 3000103 in factor_id_array:
        factor_data["URA"] += 3
    if 3000201 in factor_id_array:
        factor_data["青春杯"] += 1
    if 3000202 in factor_id_array:
        factor_data["青春杯"] += 2
    if 3000203 in factor_id_array:
        factor_data["青春杯"] += 3
    if 3000101 in factor_id_array:
        factor_data["巅峰杯"] += 1
    if 3000302 in factor_id_array:
        factor_data["巅峰杯"] += 2
    if 3000303 in factor_id_array:
        factor_data["巅峰杯"] += 3
    if 2016001 in factor_id_array:
        factor_data["地固"] += 1
    if 2016002 in factor_id_array:
        factor_data["地固"] += 2
    if 2016003 in factor_id_array:
        factor_data["地固"] += 3
    return factor_data


def get_roman(text):
    temp = ""
    kks = kakasi()
    result = kks.convert(text)
    for item in result:
        temp = temp + ("{} ".format(item['hepburn'].capitalize()))
    return temp


def select_card_data(cur, old_card_data, translate_dict):
    cur = cur.execute(
        """
            SELECT cd.id,
                   td1.text AS name_jp,
                   td2.text AS chara,
                   cd.talent_speed,
                   cd.talent_stamina,
                   cd.talent_pow,
                   cd.talent_guts,
                   cd.talent_wiz,
                   CASE cd.running_style
                       WHEN 1 THEN '逃'
                       WHEN 2 THEN '先'
                       WHEN 3 THEN '差'
                       WHEN 4 THEN '追'
                       END  AS running_style,
                   cd.available_skill_set_id
            FROM card_data cd
                     LEFT JOIN text_data td1 ON cd.id = td1.[index]
                     LEFT JOIN text_data td2 ON cd.chara_id = td2.[index]
            WHERE td1.category = '5'
              AND td2.category = '6';
        """
    )
    rows = cur.fetchall()
    new_card_data = {}
    for tuples in rows:
        if tuples[1] not in translate_dict:
            translate_dict[tuples[1]] = tuples[1]
        if tuples[2] not in translate_dict:
            translate_dict[tuples[2]] = tuples[2]
        card = {"id": tuples[0], "name_jp": tuples[1] + tuples[2],
                "name_zh": translate_dict[tuples[1]] + translate_dict[tuples[2]], "nickname": translate_dict[tuples[2]],
                "talent_speed": tuples[3], "talent_stamina": tuples[4], "talent_pow": tuples[5],
                "talent_guts": tuples[6], "talent_wiz": tuples[7], "running_style": tuples[8],
                "available_skill_set_id": tuples[9]}
        if card["id"] in old_card_data and card["nickname"] != old_card_data[card["id"]]["nickname"]:
            card["nickname"] = old_card_data[card["id"]]["nickname"]
        new_card_data[card["id"]] = card
    return new_card_data, translate_dict


def select_umdb(cur, old_umdb, translate_dict):
    cur = cur.execute(
        """
            SELECT cd.id,
                td1.text AS name,
                td2.text AS castName
            FROM chara_data cd
                LEFT JOIN
                text_data td1 ON cd.id = td1.[index]
                LEFT JOIN
                text_data td2 ON cd.id = td2.[index]
            WHERE td1.category = '6' AND 
                td2.category = '7';
        """
    )
    rows = cur.fetchall()
    chara_data = old_umdb["chara"]
    for tuples in rows:
        if tuples[1] not in translate_dict:
            translate_dict[tuples[1]] = tuples[1]
        new_chara = {
            "id": tuples[0],
            "name": translate_dict[tuples[1]],
            "castName": tuples[2]
        }
        for old_chara in chara_data:
            if old_chara["id"] == new_chara["id"]:
                old_chara["name"] = new_chara["name"]
    old_umdb["chara"] = chara_data
    return old_umdb, translate_dict


def select_chara_data(cur, old_chara_data, translate_dict):
    cur = cur.execute(
        """
            SELECT cd.id,
                td1.text AS name_jp,
                cd.birth_year,
                cd.birth_month,
                cd.birth_day
            FROM chara_data cd
                LEFT JOIN
                text_data td1 ON cd.id = td1.[index]
            WHERE td1.category = '6';
        """
    )
    rows = cur.fetchall()
    new_chara_data = {}
    for tuples in rows:
        if tuples[1] not in translate_dict:
            translate_dict[tuples[1]] = tuples[1]
        new_chara_data[tuples[0]] = translate_dict[tuples[1]]
    return new_chara_data, translate_dict


def select_support_card_data(cur, old_support_card_data, translate_dict):
    cur = cur.execute(
        """
            SELECT scd.id,
                   td1.text                  AS name_jp,
                   td2.text                  AS chara,
                   CASE scd.rarity
                       WHEN 1 THEN 'R'
                       WHEN 2 THEN 'SR'
                       WHEN 3 THEN 'SSR' END AS rarity,
                   CASE scd.command_id
                       WHEN 0 THEN '友'
                       WHEN 101 THEN '速'
                       WHEN 102 THEN '力'
                       WHEN 103 THEN '根'
                       WHEN 104 THEN ''
                       WHEN 105 THEN '耐'
                       WHEN 106 THEN '智' END AS type,
                   scd.unique_effect_id,
                   scd.effect_table_id,
                   scd.command_id
            FROM support_card_data scd
                     LEFT JOIN
                 text_data td1 ON scd.id = td1.[index]
                     LEFT JOIN
                 text_data td2 ON scd.chara_id = td2.[index]
            WHERE td1.category = '76'
              AND td2.category = '6';
        """
    )
    rows = cur.fetchall()
    new_support_card_data = {}
    for tuples in rows:
        if tuples[1] not in translate_dict:
            translate_dict[tuples[1]] = tuples[1]
        if tuples[2] not in translate_dict:
            translate_dict[tuples[2]] = tuples[2]
        supportCard = {"id": tuples[0], "name_jp": tuples[1] + tuples[2],
                       "name_zh": translate_dict[tuples[1]] + translate_dict[tuples[2]],
                       "short_name": "[" + tuples[4] + "]" + translate_dict[tuples[2]], "rarity": tuples[3],
                       "type": tuples[4], "unique_effect_id": tuples[5], "effect_table_id": tuples[6],
                       "command_id": tuples[7]}
        new_support_card_data[supportCard["id"]] = supportCard
    return new_support_card_data, translate_dict


def select_event_data(cur, old_event_data, translate_dict):
    with open(cjedbPath, "r", encoding="utf-8") as load_f:
        old_cjedb_dict = json.load(load_f)
    cur = cur.execute(
        """
        SELECT "index",
            text
        FROM text_data
        WHERE category = '181';
    """
    )
    rows = cur.fetchall()
    new_event_data = {}
    new_cjedb_dict = {"events": []}
    for tuples in rows:
        event = {"storyId": tuples[0], "storyName": tuples[1], "choices": [
            {"title": "", "text": ""}]}
        if str(event["storyId"]) in old_event_data:
            event["choices"] = old_event_data[str(event["storyId"])]["choices"]
        for item in old_cjedb_dict["events"]:
            if tuples[0] == item["storyId"]:
                event["choices"] = item["choices"]
                break
        if len(event["choices"]) >= 2:
            new_cjedb_dict["events"].append(event)
        new_event_data[event["storyId"]] = event
    with open(cjedbPath, "w", encoding="utf-8") as dump_f:
        json.dump(new_cjedb_dict, dump_f, ensure_ascii=False, indent=2)
    return new_event_data, translate_dict


def select_skill_data(cur, old_skill_data, translate_dict):
    cur = cur.execute(
        """
        SELECT sd.id,
            td1.text,
            CASE WHEN smsnp.need_skill_point IS NULL THEN 200 ELSE smsnp.need_skill_point END AS need_skill_point,
            sd.grade_value,
            sd.rarity,
            sd.disp_order,
            sd.condition_1,
            sd.condition_2,
            td2.text,
            sd.icon_id,
            sd.group_id,
            sd.group_rate
        FROM skill_data sd
            LEFT JOIN
            single_mode_skill_need_point AS smsnp ON sd.id = smsnp.id
            LEFT JOIN
            text_data AS td1 ON sd.id = td1.[index] AND 
                                td1.category = 47
            LEFT JOIN
            text_data AS td2 ON sd.id = td2.[index] AND 
                                td2.category = 48;

        """
    )
    skill_rarity = ["ノーマル", "レア", "固有★", "固有★★", "固有★★★"]
    rows = cur.fetchall()
    new_skill_data = {}
    for tuples in rows:
        if tuples[6] == "":
            continue
        if tuples[1] not in translate_dict:
            translate_dict[tuples[1]] = tuples[1]
        if tuples[8] not in translate_dict:
            translate_dict[tuples[8]] = tuples[8]
        skill = {"id": tuples[0], "name_jp": tuples[1], "name_zh": translate_dict[tuples[1]],
                 "need_skill_point": tuples[2], "grade_value": tuples[3], "rare": skill_rarity[tuples[4] - 1],
                 "rarity": tuples[4], "disp_order": tuples[5], "condition_1": tuples[6], "condition_2": tuples[7],
                 "describe": translate_dict[tuples[8]], "icon_id": tuples[9], "group_id": tuples[10],
                 "group_rate": tuples[11]}
        new_skill_data[skill["id"]] = skill
    return new_skill_data, translate_dict


def select_factor_data(cur, old_factor_data, translate_dict):
    cur = cur.execute(
        """
            SELECT "index",
                text
            FROM text_data
            WHERE category = '147';
        """
    )
    rows = cur.fetchall()
    new_factor_data = {}
    for tuples in rows:
        if tuples[0] not in old_factor_data:
            new_factor_data[tuples[0]] = tuples[1]
        else:
            new_factor_data[tuples[0]] = old_factor_data[tuples[0]]
    return new_factor_data, translate_dict


def select_item_data(cur, old_item_data, translate_dict):
    cur = cur.execute(
        """
            SELECT td1.[index],
                td1.text,
                td2.text,
                td3.text
            FROM text_data td1
                LEFT JOIN
                text_data td2 ON td1.[index] = td2.[index]
                left join
                text_data td3 ON td2.[index] = td3.[index]
            WHERE td1.category = '225' AND 
                td2.category = '238' AND 
                td3.category = '226';
        """
    )
    rows = cur.fetchall()
    new_item_data = {}
    for tuples in rows:
        if tuples[1] not in translate_dict:
            translate_dict[tuples[1]] = tuples[1]
        if tuples[2] not in translate_dict:
            translate_dict[tuples[2]] = tuples[2]
        if tuples[3] not in translate_dict:
            translate_dict[tuples[3]] = tuples[3]
        item = {"item_id": tuples[0], "name_jp": tuples[1], "name_zh": translate_dict[tuples[1]],
                "effect": translate_dict[tuples[2]], "detail": translate_dict[tuples[3]]}
        new_item_data[item["item_id"]] = item
    return new_item_data, translate_dict


def select_from_mdb(cur, path, fun):
    with open(path, "r", encoding="utf-8") as load_f:
        old_dict = json.load(load_f)
    with open(translatePath, "r", encoding="utf-8") as load_f:
        translate_dict = json.load(load_f)
    new_dict, translate_dict = fun(cur, old_dict, translate_dict)
    with open(path, "w", encoding="utf-8") as dump_f:
        json.dump(new_dict, dump_f, ensure_ascii=False, indent=2)
    with open(translatePath, "w", encoding="utf-8") as dump_f:
        json.dump(translate_dict, dump_f, ensure_ascii=False,
                  indent=2, sort_keys=True)


def init_data():
    move_file(os.path.expanduser('~') + "/AppData/LocalLow/Cygames/umamusume/master", "../master_jp", "master.mdb")
    connection = sqlite3.connect(dbPath)
    print("数据库打开成功 === " + dbPath)
    cursor = connection.cursor()
    select_from_mdb(cursor, umdbPath, select_umdb)
    select_from_mdb(cursor, charaPath, select_chara_data)
    select_from_mdb(
        cursor, cardPath, select_card_data)
    select_from_mdb(cursor, supportCardPath, select_support_card_data)
    select_from_mdb(cursor, skillPath, select_skill_data)
    # select_from_mdb(cursor, racePath, select_race_data)
    select_from_mdb(cursor, eventPath, select_event_data)
    select_from_mdb(cursor, factorPath, select_factor_data)
    select_from_mdb(
        cursor, itemPath, select_item_data)
    print("数据操作成功")
    connection.close()
    move_file("../data", os.path.expanduser('~') + "/DMMGAME/Umamusume", "cjedb.json")


def insert_log(value):
    cx = sqlite3.connect("../data/uma.sqlite")
    cu = cx.cursor()
    ins = "REPLACE INTO single_mode_log( id, turn, speed, stamina, power, guts, wiz, vital, max_vital, motivation, fans, skill_point, viewer_id) VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
    cu.execute(ins, value)
    cx.commit()
    cx.close()
