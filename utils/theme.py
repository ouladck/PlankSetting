#!/usr/bin/env python3

from gi.repository import Gtk
from utils.writer import *
from utils.reader import *
from gettext import gettext as g
import os, zipfile

class Theme:
	def __init__(self, setting_path):
		self.theme_path = os.path.expanduser("~") + "/.local/share/plank/themes"
		self.setting = setting_path + "/settings"
		self.win = Gtk.Window()
		self.scroll = Gtk.ScrolledWindow()
		
		self.liststore = Gtk.ListStore(str)
		self.refresh(self.liststore)
		
		self.treeview = Gtk.TreeView(model=self.liststore)
		
		self.treeviewcolumn = Gtk.TreeViewColumn(g("Themes"))
		self.treeview.append_column(self.treeviewcolumn)
		self.cellrenderertext = Gtk.CellRendererText()
		self.treeviewcolumn.pack_start(self.cellrenderertext, True)
		self.treeviewcolumn.add_attribute(self.cellrenderertext, "text", 0)
		self.select = self.treeview.get_selection()
		self.read_file()
		self.select.connect("changed", self.on_tree_selection_changed)
		

		
		self.scroll.add(self.treeview)
		
		self.box = Gtk.VBox()
		self.box.pack_start(self.scroll, True, True, 15)
		
	def refresh(self, widget):
		for a in os.listdir(self.theme_path):
			widget.append([a])
	
	def addfunc(self, widget):
		pass
	
	def delfunc(self, widget):
		pass
	
		
	def on_tree_selection_changed(self, selection):
		model, treeiter = selection.get_selected()
		if treeiter != None:
			write_func(read_func(self.setting), self.setting, "Theme", model[treeiter][0])
			
	def read_file(self):
		self.lst = read_func(self.setting)
		for a in self.lst:
			if a[0:a.find("=")] == "Theme":
				for row in range(len(self.liststore)):
					if a[a.find("=")+1:-1] == self.liststore[row][0]:
						self.treeview.set_cursor(row)
						
		

