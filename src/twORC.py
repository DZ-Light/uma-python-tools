import os
import cv2
import numpy as np
from PIL import Image
import pytesseract

tw_orc_path = "../tw_img/orc/"
tw_template_path = "../tw_img/template/"


def ShowImage(name, image):
    cv2.imshow(name, image)
    cv2.waitKey(0)  # 等待时间，0表示任意键退出
    cv2.destroyAllWindows()


def template_match(img, template):
    temp = img.copy()
    template_h, template_w = template.shape[:2]
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val > 0.99:
        print("匹配成功")
        top_left = max_loc
        bottom_right = (top_left[0] + template_w, top_left[1] + template_h)
        cv2.rectangle(temp, top_left, bottom_right, (0, 0, 255), 2)
        pt_left = top_left[0] + 510
        pt_top = top_left[1] - 15
        pt_right = bottom_right[0] + 520
        pt_bottom = bottom_right[1] + 5
        cv2.rectangle(temp, (pt_left, pt_top), (pt_right, pt_bottom), (0, 0, 255), 2)
        # result = np.hstack((img, temp))
        pt = pytesseract.image_to_string(img[pt_top:pt_bottom, pt_left:pt_right])
        print(int(''.join(filter(str.isdigit, pt))))
        return int(''.join(filter(str.isdigit, pt)))
        # ShowImage('temp', result)
    else:
        print("匹配失敗")
        return None


if __name__ == '__main__':
    chara_pt = {}
    for orc_file in os.listdir(tw_orc_path):
        orc_path = tw_orc_path + orc_file.strip()
        orc_img = cv2.imread(orc_path, 0)
        for template_file in os.listdir(tw_template_path):
            template_path = tw_template_path + template_file.strip()
            template_img = cv2.imread(template_path, 0)
            pt = template_match(orc_img, template_img)
            if pt is not None:
                chara_pt[template_file.split('.')[0]] = pt
    print(chara_pt)
