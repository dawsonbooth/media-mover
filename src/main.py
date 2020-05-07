import logging

import PySimpleGUI as sg

import utils

sg.theme('DarkBlue12')

source_input = [
    sg.Text('Source Folder'),
    sg.InputText(utils.HOME_DIRECTORY, key='source_text'),
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
    *folder_section,
    [*output],
    [*buttons],
]


window = sg.Window('Media Mover', layout, element_justification='center')

log = utils.Log(window, 'output')

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(log)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '[%(levelname)s] %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

moving_media = False
while True:
    event, values = window.read()

    if event in (None, 'Cancel'):
        break
    elif event in ('Start') and not moving_media:
        logging.info('Starting...')
        num_files = utils.count_files(values['source_text'])
        for n in utils.copy_files(values['source_text'], values['dest_text'], utils.CATEGORIES):
            if not sg.OneLineProgressMeter('Total Progress', n, num_files, 'progress', orientation='h'):
                break
        logging.info('Finished!')

window.close()
