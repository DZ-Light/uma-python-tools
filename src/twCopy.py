from utils import *
jp_dbPath = "../master_jp/master.mdb"
tw_dbPath = "../master_tw/master.mdb"
move_file(os.path.expanduser('~') + "/AppData/LocalLow/Cygames/umamusume/master", "../master_jp/", "master.mdb")
move_file(os.path.expanduser('~') + "/Documents/leidian9/Pictures", "../master_tw/", "master.mdb")
jp_connect = sqlite3.connect(jp_dbPath)
tw_connect = sqlite3.connect(tw_dbPath)
print("JP数据库打开成功 === " + jp_dbPath)
print("TW数据库打开成功 === " + tw_dbPath)
jp_cursor = jp_connect.cursor()
tw_cursor = tw_connect.cursor()
jp_cur = jp_cursor.execute(
    """
            SELECT text, id, category, "index"
            FROM text_data;
        """
)
jp_rows = jp_cur.fetchall()
tw_cur = tw_cursor.execute(
    """
            SELECT text, id, category, "index"
            FROM text_data;
        """
)
tw_rows = tw_cur.fetchall()
i = 0
for tw_tuples in tw_rows:
    for jp_tuples in jp_rows:
        if tw_tuples[1] == jp_tuples[1] and tw_tuples[2] == jp_tuples[2] and tw_tuples[3] == jp_tuples[3] and tw_tuples[0] != jp_tuples[0]:
            sql = '''
                update text_data
                set text = ?
                where id = ? and category = ? and "index" = ?
            '''
            jp_cursor.execute(sql, tw_tuples)
            i += 1
            break

jp_cursor.close()
tw_cursor.close()
jp_connect.commit()
jp_connect.close()
tw_connect.close()
print("更新数据量 == ", i)
