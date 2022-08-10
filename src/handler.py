from utils import *


def ParseCommandInfo(msg):
    data = msg["data"]
    with open(supportCardPath, "r", encoding="utf-8") as load_f:
        support_card_dict = json.load(load_f)
    support_card = {}
    for support_card in data["chara_info"]["support_card_array"]:
        support_card[support_card["position"]] = support_card["support_card_id"]
    failure_rate = {}
    command_info = {}
    maxsize = 0
    for command in data["home_info"]["command_info_array"]:
        command_id = command["command_id"]
        if command_id == 101 or command_id == 601:
            command_id = 101
        elif command_id == 105 or command_id == 602:
            command_id = 105
        elif command_id == 102 or command_id == 603:
            command_id = 102
        elif command_id == 103 or command_id == 604:
            command_id = 103
        elif command_id == 106 or command_id == 605:
            command_id = 106
        else:
            continue
        failure_rate = (
            color(str(command["failure_rate"]), for_color=31)
            if command["failure_rate"] > 16
            else str(command["failure_rate"])
        )
        tips = set(command["tips_event_partner_array"]) & set(
            command["training_partner_array"])
        partner_name = []
        for_color = 38
        npc = {
            101: "骏川手纲",
            102: "理事长",
            103: "乙名史记者",
            104: "桐生院葵",
            106: "代理理事长",
        }
        for partner in command["training_partner_array"]:
            if partner in support_card:
                short_name = support_card_dict[str(
                    support_card[partner])]["short_name"]
                if 1 <= partner <= 7:
                    for evaluation in data["chara_info"]["evaluation_info_array"]:
                        if evaluation["target_id"] == partner and evaluation["evaluation"] < 80:
                            for_color = 33
                if support_card_dict[str(support_card[partner])]["command_id"] == 0:
                    for_color = 32
                if support_card_dict[str(support_card[partner])]["command_id"] == command_id:
                    for_color = 35
                short_name = color(short_name, for_color=for_color)
                if partner in tips:
                    short_name = color("!", for_color=31) + short_name
                partner_name.append(short_name)
            else:
                if partner in npc:
                    short_name = npc[partner]
                else:
                    with open(charaPath, "r", encoding="utf-8") as load_f:
                        chara_dict = json.load(load_f)
                    short_name = chara_dict[str(partner)]
                partner_name.append(short_name)
        if len(partner_name) > maxsize:
            maxsize = len(partner_name)
        if command_id == 101:
            failure_rate[101] = "速(" + failure_rate + "%)"
            command_info[101] = partner_name
        if command_id == 105:
            failure_rate[105] = "耐(" + failure_rate + "%)"
            command_info[105] = partner_name
        if command_id == 102:
            failure_rate[102] = "力(" + failure_rate + "%)"
            command_info[102] = partner_name
        if command_id == 103:
            failure_rate[103] = "根(" + failure_rate + "%)"
            command_info[103] = partner_name
        if command_id == 106:
            failure_rate[106] = "智(" + failure_rate + "%)"
            command_info[106] = partner_name
    for info in command_info:
        while len(command_info[info]) < maxsize:
            command_info[info].append("")
    table = PrettyTable()
    table.add_column(failure_rate[101], command_info[101])
    table.add_column(failure_rate[105], command_info[105])
    table.add_column(failure_rate[102], command_info[102])
    table.add_column(failure_rate[103], command_info[103])
    table.add_column(failure_rate[106], command_info[106])
    print(table)
    value = (msg["data_headers"]["viewer_id"], data["chara_info"]["single_mode_chara_id"], data["chara_info"]["turn"],
             data["chara_info"]["speed"],
             data["chara_info"]["stamina"], data["chara_info"]["power"], data["chara_info"]["guts"],
             data["chara_info"]["wiz"], data["chara_info"]["vital"], data["chara_info"]["max_vital"],
             data["chara_info"]["motivation"], data["chara_info"]["fans"], data["chara_info"]["skill_point"])
    insert_log(value)


def ParseSingleModeCheckEventResponse(msg):
    data = msg["data"]
    if (
            json_has_text(msg, "unchecked_event_array")
            and len(data["unchecked_event_array"]) > 0
    ):
        for item in data["unchecked_event_array"]:
            if len(item["event_contents_info"]["choice_array"]) > 1:
                print(color("storyId: " + str(item["story_id"])))
                with open(cjedbPath, "r", encoding="utf-8") as load_f:
                    cjedb_dict = json.load(load_f)
                for event in cjedb_dict["events"]:
                    if item["story_id"] == event["storyId"]:
                        print(color("storyName: " + event["storyName"]))
                        for choice in event["choices"]:
                            print(color("\nchoices: " + choice["title"]))
                            print(color(choice["text"]))
                for choice in item["event_contents_info"]["choice_array"]:
                    print(color("choice: " + str(choice["select_index"])))
                chara_info = PrettyTable(["スピ", "スタ", "パワ", "根性", "賢さ", "体力"])
                chara_info.add_row(
                    [
                        data["chara_info"]["speed"],
                        data["chara_info"]["stamina"],
                        data["chara_info"]["power"],
                        data["chara_info"]["wiz"],
                        data["chara_info"]["guts"],
                        str(data["chara_info"]["vital"])
                        + "/"
                        + str(data["chara_info"]["max_vital"]),
                    ]
                )
                print(chara_info)


def ParseSkillTipsResponse(msg):
    data = msg["data"]
    calc(data["chara_info"])


def ParseTrainedCharaLoadResponse(msg):
    with open(cardPath, "r", encoding="utf-8") as load_f:
        card_dict = json.load(load_f)
    data = msg["data"]
    stud = PrettyTable(
        ["stud_name", "win_saddle", "score", "icon_type", "memo", "factor"]
    )
    if (
            len(data["trained_chara_array"]) > 0
            and len(data["trained_chara_favorite_array"]) > 0
    ):
        for trained_chara in data["trained_chara_array"]:
            factor = ""
            factor_data = {
                "速": 0,
                "耐": 0,
                "力": 0,
                "根": 0,
                "智": 0,
                "芝": 0,
                "泥": 0,
                "短": 0,
                "英": 0,
                "中": 0,
                "长": 0,
                "逃": 0,
                "先": 0,
                "差": 0,
                "追": 0,
                "URA": 0,
                "青春杯": 0,
                "巅峰杯": 0,
                "地固": 0,
            }
            card_name = card_dict[str(trained_chara["card_id"])]["name_zh"]
            win_saddle = cale_win_saddle(trained_chara)
            score = trained_chara["rank_score"]
            factor_data = get_factor(
                factor_data, trained_chara["factor_id_array"])
            factor_data = get_factor(
                factor_data,
                trained_chara["succession_chara_array"][0]["factor_id_array"],
            )
            factor_data = get_factor(
                factor_data,
                trained_chara["succession_chara_array"][1]["factor_id_array"],
            )
            for key in factor_data:
                if factor_data[key] != 0:
                    factor += str(factor_data[key]) + key
            for trained_chara_favorite in data["trained_chara_favorite_array"]:
                if (
                        trained_chara["trained_chara_id"]
                        == trained_chara_favorite["trained_chara_id"]
                ):
                    icon_type = trained_chara_favorite["icon_type"]
                    memo = trained_chara_favorite["memo"]
                    if icon_type in [0, 1, 5]:
                        stud.add_row(
                            [card_name, win_saddle, score, icon_type, memo, factor]
                        )
                    break

    print(stud.get_string(sortby="win_saddle", reversesort=True))


def ParseFriendSearchResponse(msg):
    with open(cardPath, "r", encoding="utf-8") as load_f:
        card_dict = json.load(load_f)
    data = msg["data"]
    practice_partner_info = data["practice_partner_info"]
    card_name = card_dict[str(practice_partner_info["card_id"])]["name_zh"]
    win_saddle = cale_win_saddle(practice_partner_info)
    score = practice_partner_info["rank_score"]
    friend = PrettyTable(
        [
            "friend_name",
            "friend_id",
            "follower_number",
            "stud_name",
            "win_saddle",
            "score",
        ]
    )
    friend.add_row(
        [
            data["user_info_summary"]["name"],
            data["user_info_summary"]["viewer_id"],
            data["follower_num"],
            card_name,
            win_saddle,
            score,
        ]
    )
    print(friend)


def ParseTeamStadiumOpponentListResponse(msg):
    data = msg["data"]
    strength_dict = {1: "上", 2: "中", 3: "下"}
    proper_dict = {1: "G", 2: "F", 3: "E",
                   4: "D", 5: "C", 6: "B", 7: "A", 8: "S"}
    with open(cardPath, "r", encoding="utf-8") as load_f:
        card_dict = json.load(load_f)
    for i in data["opponent_info_array"]:
        strength_type = strength_dict.get(i["strength"])
        table = PrettyTable()
        table.title = strength_type
        field_names = ["马娘"]
        proper_type_line = ["类型"]
        proper_value_line = ["适性"]
        speed_line = ["速度"]
        stamina_line = ["耐力"]
        power_line = ["力量"]
        guts_line = ["根性"]
        wiz_line = ["智力"]
        rank_score_line = ["评价"]
        for team_data in i["team_data_array"]:
            if team_data["trained_chara_id"] == 0:
                break
            for trained_chara in i["trained_chara_array"]:
                if trained_chara["trained_chara_id"] == team_data["trained_chara_id"]:
                    field_names.append(
                        card_dict[str(trained_chara["card_id"])]["nickname"])
                    break
            proper_type = ""
            proper_value = ""
            if team_data["distance_type"] == 1:
                proper_type += "芝短"
                proper_value += " "
                proper_value += proper_dict.get(
                    trained_chara["proper_ground_turf"])
                proper_value += " "
                proper_value += proper_dict.get(
                    trained_chara["proper_distance_short"])
            elif team_data["distance_type"] == 2:
                proper_type += "芝英"
                proper_value += " "
                proper_value += proper_dict.get(
                    trained_chara["proper_ground_turf"])
                proper_value += " "
                proper_value += proper_dict.get(
                    trained_chara["proper_distance_mile"])
            elif team_data["distance_type"] == 3:
                proper_type += "芝中"
                proper_value += " "
                proper_value += proper_dict.get(
                    trained_chara["proper_ground_turf"])
                proper_value += " "
                proper_value += proper_dict.get(
                    trained_chara["proper_distance_middle"])
            elif team_data["distance_type"] == 4:
                proper_type += "芝长"
                proper_value += " "
                proper_value += proper_dict.get(
                    trained_chara["proper_ground_turf"])
                proper_value += " "
                proper_value += proper_dict.get(
                    trained_chara["proper_distance_long"])
            elif team_data["distance_type"] == 5:
                proper_type += "泥英"
                proper_value += " "
                proper_value += proper_dict.get(
                    trained_chara["proper_ground_dirt"])
                proper_value += " "
                proper_value += proper_dict.get(
                    trained_chara["proper_distance_mile"])
            if team_data["running_style"] == 1:
                proper_type += "逃"
                proper_value += " "
                proper_value += proper_dict.get(
                    trained_chara["proper_running_style_nige"]
                )
            elif team_data["running_style"] == 2:
                proper_type += "先"
                proper_value += " "
                proper_value += proper_dict.get(
                    trained_chara["proper_running_style_senko"]
                )
            elif team_data["running_style"] == 3:
                proper_type += "差"
                proper_value += " "
                proper_value += proper_dict.get(
                    trained_chara["proper_running_style_sashi"]
                )
            elif team_data["running_style"] == 4:
                proper_type += "追"
                proper_value += " "
                proper_value += proper_dict.get(
                    trained_chara["proper_running_style_oikomi"]
                )
            proper_type_line.append(proper_type)
            proper_value_line.append(proper_value)
            speed_line.append(trained_chara["speed"])
            stamina_line.append(trained_chara["stamina"])
            power_line.append(trained_chara["power"])
            guts_line.append(trained_chara["guts"])
            wiz_line.append(trained_chara["wiz"])
            rank_score_line.append(trained_chara["rank_score"])
        proper_type_line.append("平均")
        proper_value_line.append("/ / /")
        speed_line.append(int(round(sum(speed_line[1:]) / len(speed_line[1:]), 0)))
        stamina_line.append(int(round(sum(stamina_line[1:]) / len(stamina_line[1:]), 0)))
        power_line.append(int(round(sum(power_line[1:]) / len(power_line[1:]), 0)))
        guts_line.append(int(round(sum(guts_line[1:]) / len(guts_line[1:]), 0)))
        wiz_line.append(int(round(sum(wiz_line[1:]) / len(wiz_line[1:]), 0)))
        rank_score_line.append(int(round(sum(rank_score_line[1:]) / len(rank_score_line[1:]), 0)))
        field_names.append("综合")
        table.field_names = field_names
        table.add_row(proper_type_line)
        table.add_row(proper_value_line)
        table.add_row(speed_line)
        table.add_row(stamina_line)
        table.add_row(power_line)
        table.add_row(guts_line)
        table.add_row(wiz_line)
        table.add_row(rank_score_line)
        print(table)


def ParseChampionsRaceStartResponse(msg):
    data = msg["data"]
    print(data)
