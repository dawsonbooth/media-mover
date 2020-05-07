import logging
from copy import deepcopy

import PySimpleGUI as sg

import futil
from gui import Stage, window
from settings import CATEGORIES

categories = deepcopy(CATEGORIES)
stage = Stage.WAIT
while True:

    if stage == Stage.WAIT:
        event, values = window.read()

        if event.startswith('ext_'):
            ext = event[4:]
            media = None
            for k, v in CATEGORIES.items():
                if ext in v:
                    media = k
                    break
            if values[event]:
                categories[media].append(ext)
            else:
                categories[media].remove(ext)
        elif event == 'Start':
            stage = Stage.COUNT
            logging.info('Counting files...')
            logging.warning('Window may block!')
        elif event in (None, 'Cancel'):
            break

    elif stage == Stage.COUNT:
        num_files = futil.count_files(values['source_text'])
        logging.info('Finished counting.')
        stage = Stage.MOVE

    elif stage == Stage.MOVE:
        logging.info('Starting...')
        for n in futil.copy_files(values['source_text'], values['dest_text'], categories):
            if not sg.OneLineProgressMeter('Total Progress', n, num_files, 'progress', orientation='h'):
                break
        sg.OneLineProgressMeterCancel('progress')
        logging.info('Finished!')
        stage = Stage.WAIT

window.close()
