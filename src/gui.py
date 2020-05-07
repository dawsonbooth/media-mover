import logging
from enum import Enum

import PySimpleGUI as sg

from settings import CATEGORIES, HOME_DIRECTORY


class Log:
    def __init__(self, window, key):
        self.window = window
        self.key = key

    def write(self, s):
        self.window[self.key].print(s, end='')


class Stage(Enum):
    WAIT = 1
    COUNT = 2
    MOVE = 3


sg.theme('DarkBlue12')


category_frame_args = ((
    media,
    [[sg.CB(ext, default=True, enable_events=True,
            key=f"ext_{ext}") for ext in CATEGORIES[media]]]
) for media in CATEGORIES.keys())

category_frames = (
    [sg.Frame(media, layout, key=f"frame_{media}")]
    for media, layout in category_frame_args
)


source_input = [
    sg.Text('Source Folder'),
    sg.InputText(HOME_DIRECTORY, key='source_text'),
    sg.FolderBrowse('Browse', key='source_browse')
]
dest_input = [
    sg.Text('Destination Folder'),
    sg.InputText('', key='dest_text'),
    sg.FolderBrowse('Browse', key='dest_browse')
]
folder_section = [
    [sg.Text('Choose Source and Destination Folders')],
    [*source_input],
    [*dest_input],
]

output = sg.Multiline('', key='output', size=(80, 10)),

buttons = sg.Button('Cancel'), sg.Button('Start')

layout = [
    *category_frames,
    *folder_section,
    [*output],
    [*buttons],
]


window = sg.Window('Media Mover', layout, element_justification='center')

log = Log(window, 'output')

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(log)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(levelname)s] %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)
