import argparse
import os

import pyautogui

DEFAULT_POS = '105,270,1110,850'

parser = argparse.ArgumentParser(description='Process some integers')
parser.add_argument('--pos', default=DEFAULT_POS, type=str)
args = parser.parse_args()

save_folder = 'data/folder'
if not os.path.exists(save_folder):
    os.mkdir(save_folder)

pos = tuple(args.pos.split(','))

myScreenshot = pyautogui.screenshot(region=pos)
myScreenshot.save(os.path.join(save_folder, '1.png'))
