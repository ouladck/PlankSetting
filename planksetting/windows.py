#!/usr/bin/env python3

import webbrowser

from planksetting import Gtk, GdkPixbuf
from planksetting import g
from planksetting.apps import *
from planksetting.general import *
from planksetting.themes import *


class windows():
    def destroy(self, widget):
        Gtk.main_quit()

    def translation(self, widget):
        webbrowser.open("https://www.transifex.com/projects/p/planksetting")

    def report(self, widget):
        webbrowser.open("https://github.com/karim88/PlankSetting/issues")

    def about(self, widget):
        about = Gtk.AboutDialog()
        about.set_program_name(g("PlankSetting"))
        about.set_logo(
            GdkPixbuf
            .Pixbuf.new_from_file("/usr/share/pixmaps/planksetting.png"))
        about.set_icon(
            GdkPixbuf.Pixbuf
            .new_from_file("/usr/share/pixmaps/planksetting_logo.png"))
        about.set_version("0.1.4.1")
        about.set_comments(
            g("A stupid application to customize plank dock easily."))
        about.set_copyright("Copyright (c) 2014-2017 Karim Oulad Chalha")
        about.set_website("http://karim88.github.io/PlankSetting/")
        about.set_website_label(g("PlankSetting website"))
        about.set_authors(["Karim Oulad Chalha"])
        about.set_license(g("GPL v3"))
        about.set_translator_credits(g("translator-credits"))

        about.run()
        about.destroy()

    def __init__(self, folder):
        self.win = Gtk.Window()
        self.win.set_default_size(1000, 600)

        #HeadBar
        self.head = Gtk.HeaderBar()
        self.head.props.show_close_button = True
        self.head.props.title = g("PlankSetting")
        self.win.set_titlebar(self.head)

        #instance
        self.general = general(folder)
        self.themes = themes(folder)
        self.adda = apps(folder)

        self.box = Gtk.VBox()
        self.menu = Gtk.MenuBar()
        self.menu.set_hexpand(True)

        self.plankmenu = Gtk.MenuItem(g("Menu"))
        self.menu.append(self.plankmenu)
        self.m = Gtk.Menu()
        self.plankmenu.set_submenu(self.m)
        """ Translate """
        self.tra = Gtk.MenuItem(g("Translate this Application"))
        self.tra.connect('activate', self.translation)
        self.m.append(self.tra)
        """ Report a bug """
        self.bug = Gtk.MenuItem(g("Report a bug"))
        self.bug.connect('activate', self.report)
        self.m.append(self.bug)
        """ About """
        self.abt = Gtk.MenuItem(g("About"))
        self.abt.connect('activate', self.about)
        self.m.append(self.abt)
        """ Exit """
        self.xit = Gtk.MenuItem(g("Exit"))
        self.xit.connect('activate', self.destroy)
        self.m.append(self.xit)

        """ Tabs """
        self.tab = Gtk.Notebook()
        self.tab.append_page(self.general.scroll, Gtk.Label(g("General")))
        self.tab.append_page(self.themes.box, Gtk.Label(g("Themes")))
        self.tab.append_page(self.adda.box, Gtk.Label(g("Group Apps")))

        self.head.pack_start(self.menu)
        self.box.pack_end(self.tab, True, True, 25)

        #self.win = HeaderBarWindow()
        self.win.add(self.box)
        self.win.show_all()
        self.win.connect("destroy", self.destroy)

    """Methods"""

    def main(self):
        Gtk.main()

