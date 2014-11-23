#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess


STREAMS = { 
    'rock':'http://83.102.39.40/Radiorock.mp3',
    'suomipop':'http://rstream2.nelonenmedia.fi/RadioSuomiPop.mp3',
    'city':'http://icelive0.43660-icelive0.cdn.qbrick.com/4916/43660_radio_city.mp3',
    'jyväskylä':'http://icelive0.43660-icelive0.cdn.qbrick.com/9883/43660_RadioJyvaskyla.mp3',
    'nova':'http://icelive0.41168-icelive0.cdn.qbrick.com/5050/41168_radionova1.mp3' }

PLAYLISTS = subprocess.check_output(['mpc', 'lsplaylists']).split('\n')

PLAYLISTS.pop()
starred = PLAYLISTS.pop()
PLAYLISTS.insert(0, starred)

with open('/dev/shm/ui_input.txt', 'w') as fd:
    fd.write("...Executing...")


def get_mpc_status():
    status = subprocess.check_output(['mpc', 'status']).split('\n')[0]
    if not status.startswith('volume:'):
        return status
    else: 
        return "NO AUDIO"

def get_stream_status():
    status = subprocess.check_output(['ps', 'aux']).split('\n')
    for line in status:
        if "mplayer" in line:
            return 'STREAM: ' + STREAMS.keys()[STREAMS.values().index(line.split(' ')[-1])]
    return "NO AUDIO"



def get_stream_uri(target):
    try:
        return STREAMS[target]
    except:
        return None

def main(mode, target, action=None):    
    if mode == 'spotify':
        os.system('pkill mplayer')
        if action == 'play':
            playlist = target
            try:
                playlist = PLAYLISTS[int(target) - 1]
            except ValueError:
                playlist = target
            except IndexError:
                playlist = PLAYLISTS[0]
            os.system('mpc clear')
            os.system('mpc load ' + '"' + playlist + '"') 
            os.system('mpc play')
        elif action == 'next':
            os.system('mpc next')
        elif action == 'prev':
            os.system('mpc prev')
        elif action == 'random':
            os.system('mpc random')
            os.system('mpc next')
        with open('/dev/shm/ui_input.txt', 'w') as fd:
            fd.write(get_mpc_status())
            fd.close()
    elif mode == 'stream':
        stream_uri = get_stream_uri(target)
        if stream_uri:
            os.system('pkill mplayer')
            os.system('mpc stop')
            os.system('mplayer ' + stream_uri + '< /dev/null >/dev/null 2>&1 &')
        with open('/dev/shm/ui_input.txt', 'w') as fd:
            fd.write(get_stream_status())
            fd.close()
            
    elif mode == 'general':
        if target == 'stop':
            os.system('pkill mplayer')
            os.system('mpc stop')
            with open('/dev/shm/ui_input.txt', 'w') as fd:
                fd.write("NO AUDIO")
                fd.close()

if __name__ == "__main__":
   import commandline
   commandline.run_as_main(main)
