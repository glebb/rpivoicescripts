import urwid
import os
import time
from threading import Thread

palette = [
    ('banner', 'black,bold,standout', 'light gray'),
    ('streak', 'black', 'dark red'),
    ('bg', 'black', 'dark blue'),]

txt = urwid.Text(('banner', u''), align='center')
map1 = urwid.AttrMap(txt, 'streak')
fill = urwid.Filler(map1)
map2 = urwid.AttrMap(fill, 'bg')

def exit_on_q(key):
    if key in ('q', 'Q'):
        loop.running = False
        raise urwid.ExitMainLoop()

loop = urwid.MainLoop(map2, palette, unhandled_input=exit_on_q)
loop.running = True

def draw_ui(text):
    txt.set_text(('banner',' ' + text + ' '))

pipe = loop.watch_pipe(draw_ui)

def myfunc(pipe, loop):
    while loop.running:
        fd = open('ui_input.txt', 'r')
        text = fd.read().strip()
        fd.close()
        os.write(int(pipe), text)
        time.sleep(1)

t = Thread(target=myfunc, args=(str(pipe), loop))
t.start()
time.sleep(1)
loop.run()
