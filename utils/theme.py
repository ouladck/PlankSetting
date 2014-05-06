#!/usr/bin/env python3

from gi.repository import Gtk
from utils.writer import *
from utils.reader import *
from gettext import gettext as g
import os

class Theme:
	def __init__(self, setting_path):
		self.theme_path = os.path.expanduser("~") + "/.local/share/plank/themes"
		self.setting = setting_path + "/settings"
		self.win = Gtk.Window()
		self.scroll = Gtk.ScrolledWindow()
		
		self.liststore = Gtk.ListStore(str)
		for a in os.listdir(self.theme_path):
			self.liststore.append([a])
		
		self.treeview = Gtk.TreeView(model=self.liststore)
		
		self.treeviewcolumn = Gtk.TreeViewColumn(g("Themes"))
		self.treeview.append_column(self.treeviewcolumn)
		self.cellrenderertext = Gtk.CellRendererText()
		self.treeviewcolumn.pack_start(self.cellrenderertext, True)
		self.treeviewcolumn.add_attribute(self.cellrenderertext, "text", 0)
		self.select = self.treeview.get_selection()
		self.select.connect("changed", self.on_tree_selection_changed)
		
		
		self.scroll.add(self.treeview)
		
		self.box = Gtk.VBox()
		self.box.pack_start(self.scroll, True, True, 15)
		
	
	def addfunc(self, widget):
		pass
	
	def delfunc(self, widget):
		pass
	
		
	def on_tree_selection_changed(self, selection):
		model, treeiter = selection.get_selected()
		if treeiter != None:
			write_func(read_func(self.setting), self.setting, "Theme", model[treeiter][0])

