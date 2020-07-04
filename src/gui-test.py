import urwid
import gui


selector = gui.Selector
main_screen = gui.MainScreen()
gui.UserInputHandler.set_screen(main_screen)

text_entry = main_screen.child.main_window.text_entry
selector.select(text_entry.corresponding_widget())

loop = urwid.MainLoop(main_screen.corresponding_widget(), gui.PALETTE)
loop.run()
