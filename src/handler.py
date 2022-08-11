from utils import *

def ParseCommandInfo(msg):
    data = msg["data"]
    with open(supportCardPath, "r", encoding="utf-8") as load_f:
        support_card_dict = json.load(load_f)
    supportCard = {}
    for support_card in data["chara_info"]["support_card_array"]:
        supportCard[support_card["position"]] = support_card["support_card_id"]
    failureRate = {}
    commandInfo = {}
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
        forColor = 38
        npc = {
            101: "骏川手纲",
            102: "理事长",
            103: "乙名史记者",
            104: "桐生院葵",
            106: "代理理事长",
        }
        for partner in command["training_partner_array"]:
            if partner in supportCard:
                short_name = support_card_dict[str(
                    supportCard[partner])]["short_name"]
                if 1 <= partner <= 7:
                    for evaluation in data["chara_info"]["evaluation_info_array"]:
                        if evaluation["target_id"] == partner and evaluation["evaluation"] < 80:
                            forColor = 33
                if support_card_dict[str(supportCard[partner])]["command_id"] == 0:
                    forColor = 32
                if support_card_dict[str(supportCard[partner])]["command_id"] == command_id:
                    forColor = 35
                short_name = color(short_name, for_color=forColor)
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
            failureRate[101] = "速(" + failure_rate + "%)"
            commandInfo[101] = partner_name
        if command_id == 105:
            failureRate[105] = "耐(" + failure_rate + "%)"
            commandInfo[105] = partner_name
        if command_id == 102:
            failureRate[102] = "力(" + failure_rate + "%)"
            commandInfo[102] = partner_name
        if command_id == 103:
            failureRate[103] = "根(" + failure_rate + "%)"
            commandInfo[103] = partner_name
        if command_id == 106:
            failureRate[106] = "智(" + failure_rate + "%)"
            commandInfo[106] = partner_name
    for info in commandInfo:
        while len(commandInfo[info]) < maxsize:
            commandInfo[info].append("")
    table = PrettyTable()
    table.add_column(failureRate[101], commandInfo[101])
    table.add_column(failureRate[105], commandInfo[105])
    table.add_column(failureRate[102], commandInfo[102])
    table.add_column(failureRate[103], commandInfo[103])
    table.add_column(failureRate[106], commandInfo[106])
    print(table)
    value = (msg["data_headers"]["viewer_id"], data["chara_info"]["single_mode_chara_id"], data["chara_info"]["turn"],
             data["chara_info"]["speed"], data["chara_info"]["stamina"], data["chara_info"]["power"], data["chara_info"]["guts"],
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
        properTypeLine = ["类型"]
        properValueLine = ["适性"]
        speedLine = ["速度"]
        staminaLine = ["耐力"]
        powerLine = ["力量"]
        gutsLine = ["根性"]
        wizLine = ["智力"]
        rankScoreLine = ["评价"]
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
            properTypeLine.append(proper_type)
            properValueLine.append(proper_value)
            speedLine.append(trained_chara["speed"])
            staminaLine.append(trained_chara["stamina"])
            powerLine.append(trained_chara["power"])
            gutsLine.append(trained_chara["guts"])
            wizLine.append(trained_chara["wiz"])
            rankScoreLine.append(trained_chara["rank_score"])
        properTypeLine.append("平均")
        properValueLine.append("/ / /")
        speedLine.append(
            int(round(sum(speedLine[1:]) / len(speedLine[1:]), 0)))
        staminaLine.append(
            int(round(sum(staminaLine[1:]) / len(staminaLine[1:]), 0)))
        powerLine.append(
            int(round(sum(powerLine[1:]) / len(powerLine[1:]), 0)))
        gutsLine.append(int(round(sum(gutsLine[1:]) / len(gutsLine[1:]), 0)))
        wizLine.append(int(round(sum(wizLine[1:]) / len(wizLine[1:]), 0)))
        rankScoreLine.append(
            int(round(sum(rankScoreLine[1:]) / len(rankScoreLine[1:]), 0))
        )
        field_names.append("综合")
        table.field_names = field_names
        table.add_row(properTypeLine)
        table.add_row(properValueLine)
        table.add_row(speedLine)
        table.add_row(staminaLine)
        table.add_row(powerLine)
        table.add_row(gutsLine)
        table.add_row(wizLine)
        table.add_row(rankScoreLine)
        print(table)



def ParseChampionsRaceStartResponse(msg):
    data = msg["data"]
    print(data)
