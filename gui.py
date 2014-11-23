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
    if txt.get_text != text:
        txt.set_text(('banner',' ' + text + ' '))

pipe = loop.watch_pipe(draw_ui)

def myfunc(pipe):
    count = 0
    last = ""
    while loop.running:
        time.sleep(1.5)
        fd = open('/dev/shm/ui_input.txt', 'r')
        text = fd.read().strip()
        fd.close()
        os.write(int(pipe), text)
        if text == 'ERROR' or text.startswith('...'):
            count = count + 1
        else:
            last = text
        if count >= 3:
            count = 0
            text = last
            with open('/dev/shm/ui_input.txt', 'w') as fd:
                fd.write(text)

t = Thread(target=myfunc, args=(str(pipe)))
t.start()
loop.run()
