#!/usr/bin/env python3
import os,sys
import PySimpleGUI as sg
import glob
import argparse
import time
import threading
import ipdb
from os.path import join, dirname, abspath
scripts_path = '.'
abs_path=dirname(abspath(__file__))
scripts_path = abs_path + ''
cmd_fmt = 'bash -c "source ~/.bashrc && cd '+scripts_path+' && {} ; sleep 2"&'
def run(cmd):
    os.system('xfce4-terminal -x '+cmd_fmt.format(cmd))

command_pairs = [
        ('pre_work','./pre_work.sh'),
        ('roscore','./roscore.sh'),
        ('launch','./launch.sh'),
        ('teleop','./teleop.sh'),
]

buttons = [a for a,b in command_pairs]
sg.theme('DarkAmber') 
layout = [[sg.Button(a)] for a in buttons]
window = sg.Window('Run All', layout)

while True:
    event, values = window.read(timeout=None)
    if event == sg.WIN_CLOSED:      # if user closes window or clicks cancel
        break

    if event in buttons:
        cmd = command_pairs[buttons.index(event)][1]
        #if event == 'set-profile':
        #    print('sync files...')
        #    set_profile(values[0],values[1],values[2])
        #else:
        run(cmd)
    #if values[0] is not None:
    #        print('----',values[0])

window.close()




