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
		about.set_version(g("0.1.2"))
		about.set_comments(g("A stupid application to customize plank dock easily."))
		about.set_copyright("Copyright (c) 2014 Karim Oulad Chalha")
		about.set_website("http://karim88.github.io/PlankSetting/")
		about.set_website_label(g("PlankSetting website"))
		about.set_authors(["Karim Oulad Chalha"])
		about.set_license(g("GPL v3"))
		about.set_translator_credits(g("translator-credits"))
		
		about.run()
		about.destroy()
		
	def add_dock(self, parent):
		Gtk.Dialog.__init__(self, "Add a new Dock", parent, 0,
							(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
							Gtk.STOCK_OK, Gtk.ResponseType.OK))
		self.set_default_size(150, 150)
		
		label = Gtk.Label("Entry the name of the new dock:")
		entry = Gtk.Entry()
		
		box = self.get_content_area()
		box.add(label)
		box.add(entry)
		box.show_all()
		
		response = self.run()
		if response == Gtk.ResponseType.OK:
			
			Gtk.MessageDialog('Dock added successfuly!')
		self.destroy()
		
		
	
	def __init__(self, setting_path):
		self.win = Gtk.Window()
		self.win.set_default_size(800,500)
		
		#HeadBar
		self.head = Gtk.HeaderBar()
		self.head.props.show_close_button = True
		self.head.props.title = g("PlankSetting")
		self.win.set_titlebar(self.head)
		
		
		#instance
		self.ins = Window(setting_path)
		self.themes = Theme(setting_path)
		
		self.box = Gtk.VBox()
		self.menu = Gtk.MenuBar()
		self.menu.set_hexpand(True)
		
		self.plankmenu = Gtk.MenuItem(g("Menu"))
		self.menu.append(self.plankmenu)
		self.m = Gtk.Menu()
		self.plankmenu.set_submenu(self.m)
		""" About """
		self.abt = Gtk.MenuItem(g("About"))
		self.abt.connect('activate', self.about)
		self.m.append(self.abt)
		""" Add a new Dock """
		self.adk = Gtk.MenuItem(g("Add a new Dock")
		self.adk.connect('activate', self.add_dock)
		self.m.append(self.adk)
		""" Exit """
		self.xit = Gtk.MenuItem(g("Exit"))
		self.xit.connect('activate', self.destroy)
		self.m.append(self.xit)
		
		""" Tabs """
		self.tab = Gtk.Notebook()
		self.tab.append_page(self.ins.scroll, Gtk.Label(g("General")))
		self.tab.append_page(self.themes.box, Gtk.Label(g("Themes")))
		
		self.head.pack_start(self.menu)
		self.box.pack_end(self.tab, True, True, 25)
		
		#self.win = HeaderBarWindow()
		self.win.add(self.box)
		self.win.show_all()
		self.win.connect("destroy", self.destroy)
		
	
	"""Methods"""
	
	def main(self):
		Gtk.main()

