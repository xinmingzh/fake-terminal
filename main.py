import argparse
import csv
import os
import random
from datetime import datetime, timedelta
import time

import pyautogui

DEFAULT_SEC = 3
DEFAULT_SPEED = 25
# DEFAULT_TIME = '2021-3-1 13:32:47'
DEFAULT_TIME = '2021-3-1 00:00:45'
DEFAULT_FRAMES = 25
DEFAULT_FILE = 'data/data4.csv'

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DATETIME_FORMAT1 = '%H:%M:%S'
DATETIME_LONG_FORMAT = '[%H:%M:%S.%f]'
DATETIME_FILE_NAME_FORMAT = '[%H:%M:%S.%f]'

DEFAULT_POS = '105,270,1110,850'

parser = argparse.ArgumentParser(description='Process some integers')
parser.add_argument('--sec', default=DEFAULT_SEC, type=float)
parser.add_argument('--speed', default=DEFAULT_SPEED, type=float)
parser.add_argument('--file', default=DEFAULT_FILE, type=str)
parser.add_argument('--time', default=DEFAULT_TIME, type=str)
parser.add_argument('--pos', default=DEFAULT_POS, type=str)
args = parser.parse_args()

save_folder = 'data/output/1'
if not os.path.exists(save_folder):
    os.makedirs(save_folder)


def main():
    zero_time = datetime(2021, 3, 1, 0, 0, 0)
    pos = tuple(args.pos.split(','))
    with open(args.file) as file:
        data = list(csv.reader(file))[1:]

    interval = 1 / args.speed
    end_time = time.time() + args.sec
    fake_time = datetime.strptime(args.time, DATETIME_FORMAT)
    msg_type = 'INFO'
    curr_data = 0

    start_time = time.time()
    curr_time = time.time()
    passed = -0.2 + 0.0000001

    while curr_time < end_time:
        sys_time = (fake_time + timedelta(seconds=passed)).strftime(DATETIME_LONG_FORMAT)
        curr_data = get_updated_curr(data, curr_data, passed)
        msg = data_tostring(data[curr_data])
        print_calculations()
        print('{} {}'.format(sys_time, msg))
        if random.randint(1, 10) == 1:
            print("Updating model")
        if random.randint(1, 5) == 1:
            print("Saving to local memory")
        if random.randint(1, 3) == 1:
            print("Reading info from horn")

        time.sleep(0.05)

        t = (zero_time + timedelta(seconds=passed)).strftime(DATETIME_FILE_NAME_FORMAT)
        my_screenshot = pyautogui.screenshot(region=pos)
        # print(sys_time[10:12])
        my_screenshot.save(os.path.join(save_folder, t[1:9] + '-' + str(int(int(t[10:12])/4)) + '.png'))

        passed += interval
        curr_time = start_time + passed


def print_calculations():
    init1 = random.randint(1, 9)
    init2 = init1 + random.randint(-1, 1)
    inf = random.randint(25, 45)
    result = random.randint(1, 3)
    print('a new image batch comes')
    print('batch size = 2')
    print('init1: {}'.format(init1))
    print('init2: {}'.format(init2))
    print('intf: {}'.format(inf))


def data_tostring(data: list) -> str:
    d1 = '' if int(data[2]) == 0 else '[' + data[2] + ' items] '
    d2 = '' if int(data[3]) == 0 else '[' + data[3] + ' logo] '
    d3 = '' if int(data[4]) == 0 else '[' + data[4] + ' text] '
    d4 = '' if int(data[5]) == 0 else '[' + data[5] + ' barcode] '
    return 'detected: {}{}{}{}'.format(d1, d2, d3, d4)


def get_seconds(data: list):
    s = datetime.strptime(data[0], DATETIME_FORMAT1).second + int(data[1]) / DEFAULT_FRAMES
    # print('frame time: ', s)
    return s


def get_updated_curr(data: list, curr: int, t: float) -> int:
    # print('curr time: ', t)
    return curr if curr + 1 >= len(data) or get_seconds(data[curr+1]) >= t else curr + 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
