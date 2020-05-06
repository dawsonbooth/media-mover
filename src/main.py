import PySimpleGUI as sg
from utils import HOME_DIRECTORY, CATEGORIES, copy_files, count_files

sg.theme('Default1')

source_input = sg.Text('Source'), sg.InputText(
    HOME_DIRECTORY, key='source_text'), sg.FolderBrowse('Browse', key='source_browse')
dest_input = sg.Text('Destination'), sg.InputText(
    '', key='dest_text'), sg.FolderBrowse('Browse', key='dest_browse')


layout = [
    [*source_input],
    [*dest_input],
    [sg.Button('Cancel'), sg.Button('Start')],
]

window = sg.Window('Media Mover', layout)

# Event Loop to process "events" and get the "values" of the inputs
moving_media = False
while True:
    event, values = window.read()

    if event in (None, 'Cancel'):  # if user closes window or clicks cancel
        break
    elif event in ('Start') and not moving_media:
        num_files = count_files(values['source_text'])
        for n in copy_files(values['source_text'], values['dest_text'], CATEGORIES):
            if not sg.OneLineProgressMeter('Total Progress', n, num_files, 'progress', orientation='h'):
                break

window.close()
