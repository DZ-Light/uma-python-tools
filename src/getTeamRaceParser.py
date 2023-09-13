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
                    msg = umsgpack.unpackb(msg)
                if "Q.msgpack" in name:
                    os.remove(os.path.join(root, name))
                else:
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
                    os.remove(os.path.join(root, name))


if __name__ == "__main__":
    print(color("程序开始运行", for_color=31))
    system_name = platform.system()
    if system_name == "Windows":
        msgpack_path_jp = os.path.expanduser('~') + "/DMMGAME/Umamusume/CarrotJuicer"
        msgpack_path_new = os.path.expanduser('~') + "/Documents/GitHub/AzusaHikari/uma-notify-analyzer/packets"
        msgpack_path_tw = os.path.expanduser('~') + "/AppData/Local/UmamusumeResponseAnalyzer/packets"
        while 1:
            try:
                move_race_data(msgpack_path_jp)
                move_race_data(msgpack_path_new)
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
