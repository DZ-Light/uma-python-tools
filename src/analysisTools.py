import platform
import time

from handler import *
from utils import *


def move_race_data(path):
    # （使用 os.walk ,这个方法返回的是一个三元tuple(dir_path(string), dir_names(list), filenames(list)), 其中第一个为起始路径， 第二个为起始路径下的文件夹,
    # 第三个是起始路径下的文件.）
    for root, dirs, files in os.walk(path):
        for name in files:
            if ".msgpack" in name:  # 判断某一字符串是否具有某一字串，可以使用in语句
                # os.remove(os.path.join(root, name))  # os.move语句为删除文件语句
                with open(os.path.join(root, name), "rb") as load_f:
                    msg = load_f.read()
                    if "Q.msgpack" in name:
                        offset = struct.unpack_from("<i", msg, 0)[0]
                        msg = msg[4 + offset:]
                    msg = msgpack.loads(msg, strict_map_key=False)

                if "Q.msgpack" in name:
                    os.remove(os.path.join(root, name))
                else:
                    if (
                            json_has_text(msg, "chara_info")
                            and json_has_text(msg, "home_info")
                            and json_has_text(msg, "command_info_array")
                            and not json_has_text(msg, "race_reward_info")
                    ):
                        print_file_name(name, "ParseCommandInfo")
                        ParseCommandInfo(msg)
                        deal_path(root, "ParseCommandInfo", name, 5)
                    if (
                            json_has_text(msg, "chara_info")
                            and json_has_text(msg, "race_condition_array")
                    ) or json_has_text(msg, "unchecked_event_array"):
                        print_file_name(
                            name, "ParseSingleModeCheckEventResponse")
                        ParseSingleModeCheckEventResponse(msg)
                        deal_path(
                            root, "ParseSingleModeCheckEventResponse", name, 5)
                        if (
                                json_has_text(msg, "chara_info")
                                and (msg["data"]["chara_info"]["state"] == 2
                                     or msg["data"]["chara_info"]["state"] == 3)
                                and len(msg["data"]["unchecked_event_array"]) == 0
                        ):
                            print_file_name(name, "ParseSkillTipsResponse")
                            ParseSkillTipsResponse(msg)
                            deal_path(root, "ParseSkillTipsResponse", name, 5)
                    if (
                            json_has_text(msg, "trained_chara_array")
                            and json_has_text(msg, "trained_chara_favorite_array")
                            and json_has_text(msg, "room_match_entry_chara_id_array")
                    ):
                        print_file_name(name, "ParseTrainedCharaLoadResponse")
                        ParseTrainedCharaLoadResponse(msg)
                        deal_path(
                            root, "ParseTrainedCharaLoadResponse", name, 1)
                    if (
                            json_has_text(msg, "user_info_summary")
                            and json_has_text(msg, "practice_partner_info")
                            and json_has_text(msg, "directory_card_array")
                            and json_has_text(msg, "support_card_data")
                            and json_has_text(msg, "follower_num")
                            and json_has_text(msg, "own_follow_num")
                    ):
                        print_file_name(name, "ParseFriendSearchResponse")
                        ParseFriendSearchResponse(msg)
                        deal_path(root, "ParseFriendSearchResponse", name, 1)
                    if json_has_text(msg, "opponent_info_array") and "opponent_info_array" in msg["data"]:
                        print_file_name(name, "ParseTeamStadiumOpponentListResponse")
                        ParseTeamStadiumOpponentListResponse(msg)
                        deal_path(
                            root, "ParseTeamStadiumOpponentListResponse", name, 1)
                    if (
                            json_has_text(msg, "room_info")
                            and json_has_text(msg, "room_user_array")
                            and json_has_text(msg, "race_horse_data_array")
                            and json_has_text(msg, "trained_chara_array")
                    ):
                        print_file_name(name, "ParseChampionsRaceStartResponse")
                        ParseChampionsRaceStartResponse(msg)
                        deal_path(root, "ParseChampionsRaceStartResponse", name, 1)
                    if json_has_text(msg, "race_start_params_array"):
                        print_file_name(name, "CarrotJuicer_team_race")
                        viewer_id = msg["data_headers"]["viewer_id"]
                        move_file(root, "../MsgPack/CarrotJuicer_team_race/" + str(viewer_id), name)
                    elif json_has_text(msg, "trained_chara_array") and json_has_text(
                            msg, "race_scenario"
                    ):
                        print_file_name(name, "CarrotJuicer_train_race")
                        move_file(
                            root, "../MsgPack/CarrotJuicer_train_race", name)
                    elif (
                            json_has_text(msg, "race_horse_data")
                            or json_has_text(msg, "race_horse_data_array")
                            or json_has_text(msg, "race_scenario")
                            or json_has_text(msg, "race_result_array")
                    ):
                        print_file_name(name, "CarrotJuicer_other_race")
                        deal_path(root, "CarrotJuicer_other_race", name, 1)
                    elif json_has_text(msg, "card_list") and json_has_text(
                            msg, "support_card_list"
                    ):

                        print_file_name(name, "CarrotJuicer_info")
                        clear_path("../MsgPack/CarrotJuicer_info", 0)
                        clear_path("../Json/CarrotJuicer_info", 0)
                        move_file(root, "../MsgPack/CarrotJuicer_info", name)
                        convert_msgpack_json("CarrotJuicer_info", name)
                    os.remove(os.path.join(root, name))


if __name__ == "__main__":
    print(color("程序开始运行", for_color=31))
    system_name = platform.system()
    if system_name == "Windows":
        msgpack_path_jp = os.path.expanduser('~') + "/DMMGAME/Umamusume/CarrotJuicer"
        msgpack_path_tw = os.path.expanduser('~') + "/AppData/Local/UmamusumeResponseAnalyzer/packets"
        while 1:
            try:
                move_race_data(msgpack_path_jp)
                move_race_data(msgpack_path_tw)
            except Exception as ex:
                print(color("出现如下异常%s" % ex, for_color=31))
                init_data()
                continue
            time.sleep(1)
    else:
        print(color(system_name))
        msgpack_path = "/Users/dingzg/Documents/GitHub/AzusaHikari/uma-python-tools/CarrotJuicer"
        move_race_data(msgpack_path)
