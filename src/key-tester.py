import urwid

t = urwid.Text('', align='center')

def on_keypress(key):
	t.set_text(repr(key))

filler = urwid.Filler(t, 'top')
loop = urwid.MainLoop(filler, unhandled_input=on_keypress)
loop.run()
