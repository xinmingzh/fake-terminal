import argparse
import csv
import os
from datetime import datetime, timedelta
import time

import pyautogui

DEFAULT_SEC = 15
DEFAULT_SPEED = 30
DEFAULT_FRAMES = 30
# DEFAULT_TIME = '13:33:17'
DEFAULT_TIME = '13:00:00'
DEFAULT_FILE = 'data/slow2.csv'

DATETIME_FORMAT = '%H:%M:%S'
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

save_folder = 'data/output/2'
if not os.path.exists(save_folder):
    os.makedirs(save_folder)


def main():
    zero_time = datetime(2021, 3, 1, 0, 0, 0)
    pos = tuple(args.pos.split(','))
    with open(args.file) as file:
        data = list(csv.reader(file))[1:]
        print(data)

    interval = 1 / args.speed
    end_time = time.time() + args.sec
    fake_time = datetime.strptime(args.time, DATETIME_FORMAT)
    msg_type = 'INFO'
    curr_data = 0

    start_time = time.time()
    curr_time = time.time()
    passed = -0.8 + 0.0000001

    while curr_time < end_time:
        sys_time = (fake_time + timedelta(seconds=passed)).strftime(DATETIME_LONG_FORMAT)
        curr_data = get_updated_curr(data, curr_data, passed)
        msg = data_tostring(data[curr_data])
        print('{} {}'.format(sys_time, msg))

        time.sleep(0.05)
        t = (zero_time + timedelta(seconds=passed - 0.0000001)).strftime(DATETIME_FILE_NAME_FORMAT)
        my_screenshot = pyautogui.screenshot(region=pos)
        # print(sys_time[10:12])
        my_screenshot.save(
            os.path.join(save_folder, t[1:9] + '-' + str(round(int(t[10:12]) * DEFAULT_FRAMES / 100)) + '.png'))

        passed += interval
        curr_time = start_time + passed


def data_tostring(data: list) -> str:
    d1 = '' if data[2].strip() == '0' else '[Item name: ' + data[2] + '] '
    d2 = '' if data[3].strip() == '0' else '[Logo: ' + data[3] + '] '
    d3 = '' if data[4].strip() == '0' else '[Text: ' + data[4] + '] '
    d4 = '' if data[5].strip() == '0' else '[Barcode: ' + data[5] + '] '
    return 'detected: {}{}{}{}'.format(d1, d2, d3, d4)


def get_seconds(data: list):
    s = datetime.strptime(data[0], DATETIME_FORMAT).second + int(data[1]) / DEFAULT_FRAMES
    # print(data)
    # print('frame time: ', s)
    return s


def get_updated_curr(data: list, curr: int, t: float) -> int:
    # print('curr time: ', t)
    return curr if curr + 1 >= len(data) or get_seconds(data[curr+1]) >= t else curr + 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
