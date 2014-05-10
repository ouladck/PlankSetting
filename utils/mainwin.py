#!/usr/bin/env python3

from gi.repository import Gtk, GdkPixbuf
from utils.window import Window
from utils.theme import Theme
from gettext import gettext as g

class Mainwin():
	def destroy(self, widget):
		Gtk.main_quit()
	
	def about(self, widget):
		about = Gtk.AboutDialog()
		about.set_program_name(g("PlankSetting"))
		about.set_logo(GdkPixbuf.Pixbuf.new_from_file("/usr/share/pixmaps/planksetting.png"))
		about.set_icon(GdkPixbuf.Pixbuf.new_from_file("/usr/share/pixmaps/planksetting_logo.png"))
		about.set_version(g("0.1.1"))
		about.set_comments(g("A stupid application to customize plank dock easily."))
		about.set_copyright("Copyright © 2014 Karim Oulad Chalha")
		about.set_website("http://karim88.github.io/PlankSetting/")
		about.set_website_label(g("PlankSetting website"))
		about.set_authors(["Karim Oluad Chalha"])
		about.set_license(g("GPL v3"))
		about.set_translator_credits(g("translator-credits"))
		
		about.run()
		about.destroy()
		
	
	def __init__(self, setting_path):
		self.win = Gtk.Window()
		self.win.set_title(g("PlankSetting"))
		self.win.set_default_size(800,500)
		
		
		#instance
		self.ins = Window(setting_path)
		self.themes = Theme(setting_path)
		
		self.box = Gtk.VBox()
		self.menu = Gtk.MenuBar()
		self.menu.set_hexpand(True)
		
		self.plankmenu = Gtk.MenuItem(g("PlankSetting"))
		self.menu.append(self.plankmenu)
		self.m = Gtk.Menu()
		self.plankmenu.set_submenu(self.m)
		self.abt = Gtk.MenuItem(g("About"))
		self.abt.connect('activate', self.about)
		self.m.append(self.abt)
		self.xit = Gtk.MenuItem(g("Exit"))
		self.xit.connect('activate', self.destroy)
		self.m.append(self.xit)
		
		self.tab = Gtk.Notebook()
		self.tab.append_page(self.ins.scroll, Gtk.Label(g("General")))
		self.tab.append_page(self.themes.box, Gtk.Label(g("Themes")))
		
		self.box.pack_start(self.menu, False, False, 0)
		self.box.pack_end(self.tab, True, True, 5)
		
		self.win.add(self.box)
		self.win.show_all()
		self.win.connect("destroy", self.destroy)
		
	
	"""Methods"""
	
	def main(self):
		Gtk.main()

