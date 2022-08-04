import os

import cv2
import numpy

tw_original_1_path = "../tw_img/original/original_1.png"
tw_original_2_path = "../tw_img/original/original_2.png"
tw_template_path = "../tw_img/template"
chara1 = ["大和赤驥", "大樹快車", "櫻花驀進王", "小栗帽", "草上飛", "超級小溪", "優秀素質", "帝王光輝"]
chara2 = ["無聲鈴鹿", "氣槽", "春烏菈菈", "伏特加", "黃金船", "神鷹", "魯道夫象徵"]


def imgShowAndWrite(img_data: numpy.ndarray, img_name: str):
    cv2.imwrite("../tw_img/template/" + img_name + ".png", img_data)


if __name__ == '__main__':
    original_1_img = cv2.imread(tw_original_1_path)
    original_2_img = cv2.imread(tw_original_2_path)
    print(original_1_img.shape)
    print(original_2_img.shape)
    chara_interval = 238
    bottom_interval = 45
    for i in range(0, len(chara1)):
        top = 525 + (i * chara_interval)
        bottom = top + bottom_interval
        imgShowAndWrite(original_1_img[top:bottom, 320:550, :], chara1[i])
    for i in range(0, len(chara2)):
        top = 635 + (i * chara_interval)
        bottom = top + bottom_interval
        imgShowAndWrite(original_2_img[top:bottom, 320:550, :], chara2[i])
