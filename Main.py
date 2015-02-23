#!/usr/bin/env python3

from gi.repository import Gtk
from utils.mainwin import Mainwin
import os
import gettext
from gettext import gettext as g

APP_NAME = "planksetting"
APP_DIR = "/usr/share/locale"
gettext.bindtextdomain(APP_NAME, APP_DIR)
gettext.textdomain(APP_NAME)
g = gettext.gettext

setting_path = os.listdir(os.path.expanduser("~") + "/.config/plank")
folder = ""


def choosed(widget):
    folder = widget.get_label()
    win.hide()
    main = Mainwin(os.path.expanduser("~") + "/.config/plank/", folder)
    main.main()

if __name__ == "__main__":
    if len(setting_path) > 1:
        win = Gtk.Window()
        label = Gtk.Label(g("Choose the dock:"))
        box = Gtk.VBox()
        box.pack_start(label, False, False, 5)
        for a in setting_path:
            button = Gtk.Button(a)
            button.connect('clicked', choosed)
            box.pack_start(button, False, False, 5)
        win.add(box)
        win.show_all()
        Gtk.main()

    else:
        for a in setting_path:
            folder = a
            main = Mainwin(os.path.expanduser("~") + "/.config/plank/", folder)
            main.main()
