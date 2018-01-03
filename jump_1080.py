import numpy
import uiautomator2 as u2
import time
import scipy.misc


# 根据颜色得到棋子底部位置
def get_chess(img, chess_height):
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            if 78 >= img[i][j][0] >= 68 and 66 >= img[i][j][1] >= 56 and 103 >= img[i][j][2] >= 93:
                return i + chess_height, j
    return 0, 0


# 根据色差得到要跳的方格位置
def get_des(img, y1, block_height):
    for i in range(1, img.shape[0]):
        for j in range(1, img.shape[1]):
            # 不扫描棋子所在列，避免棋子比方格高的情况
            if y1 - 60 <= j <= y1 + 60:
                continue
            if numpy.abs(int(img[i][j][2]) - int(img[i][j - 1][2])) > 5 or numpy.abs(
                            int(img[i][j][1]) - int(img[i][j - 1][1])) > 5 or numpy.abs(
                        int(img[i][j][0]) - int(img[i][j - 1][0])) > 5:
                return i + block_height, j
            if numpy.abs(int(img[i][j][2]) - int(img[i - 1][j][2])) > 5 or numpy.abs(
                            int(img[i][j][1]) - int(img[i - 1][j][1])) > 5 or numpy.abs(
                        int(img[i][j][0]) - int(img[i - 1][j][0])) > 5:
                return i + block_height, j

# 可调节参数
chess_height = 180
block_height = 50
right_ratio = 740
left_ratio = 755
min_step = 0.2
view_right = 15
view_left = 10
# 自己设备的序列号
d = u2.connect('WTKDU16A17017621')
dis_list = []
time_list = []

while True:
    # 截屏
    d.screenshot('test.png')
    img = scipy.misc.imread('test.png')
    img = img[300:, :]
    x1, y1 = get_chess(img, chess_height)
    x2, y2 = get_des(img, y1, block_height)
    # 区分向左还是向右跳，由于视角问题，力度会有不同
    if (y2 - y1) > 0:
        distance = numpy.sqrt((x2 - x1) ** 2 + (y2 - y1 + view_right) ** 2)
        t = max(distance / right_ratio, min_step)
        d.long_click(400, 400, t)
    else:
        distance = numpy.sqrt((x2 - x1 + 5) ** 2 + (y2 - y1 + view_left) ** 2)
        t = max(distance / left_ratio, min_step)
        d.long_click(400, 400, t)
    # 确保截图时已跳完
    time.sleep(2)
