#!/usr/bin/env python3

from gi.repository import Gtk
from utils.writer import *
from utils.reader import *
from gettext import gettext as g
import os, zipfile, tarfile, shutil
from utils.rarfile import *

class Theme:
	def __init__(self, setting_path):
		self.theme_path = os.path.expanduser("~") + "/.local/share/plank/themes"
		self.sys_theme_path = "/usr/share/plank/themes"
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
		
		self.button = Gtk.ButtonBox()
		self.button.set_spacing(15)
		self.b = Gtk.FileChooserButton()
		self.b.set_tooltip_text(g("Add a theme"))
		self.b.connect('file-set', self.addfunc)
		self.button.add(self.b)
		self.b1 = Gtk.Button(stock=Gtk.STOCK_REMOVE)
		self.b1.set_tooltip_text(g("Remove a theme"))
		self.b1.connect('clicked', self.delfunc)
		self.button.add(self.b1)
		
		self.scroll.add(self.treeview)
		
		self.box = Gtk.VBox()
		self.box.pack_start(self.scroll, True, True, 15)
		self.box.pack_start(self.button, False, False, 15)
		
	def refresh(self, widget):
		self.liststore.clear()
		for a in os.listdir(self.theme_path):
			widget.append([a])
		for b in os.listdir(self.sys_theme_path):
			if(b not in os.listdir(self.theme_path)):
				widget.append([b])
	
	def addfunc(self, widget):
		f = widget.get_filename()
		bn = os.path.basename(f)
		name = bn[:bn.find(".")+1]
		path = self.theme_path + '/' + name
		newpath = self.theme_path + '/' + name[:name.find('_')].capitalize()
		if f.find('.') != -1:
			if f[f.find('.')+1:] == 'rar':
				try:
					with RarFile(f, 'r') as fi:
							if (len(fi.namelist()) == 2) and ('dock.theme' in fi.namelist()) and ('hover.theme' in fi.namelist()):
								fi.extractall(self.theme_path+'/'+name[:name.find('_')].capitalize(), fi.namelist())
					os.system("unrar x {0} {1}".format(f, self.theme_path))
				except:
					msg = Gtk.MessageDialog(message_type = Gtk.MessageType.WARNING, message_format = g("You dont have a UNRAR program\nPlease make sure to install it before!"))
					msg.run()
					msg.destroy()
			elif f[f.find('.')+1:] == 'tar':
				with tarfile.TarFile(f, 'r') as fi:
					if (len(fi.getnames()) == 2) and ('dock.theme' in fi.getnames()) and ('hover.theme' in fi.getnames()):
						fi.extractall(self.theme_path+'/'+name[:name.find('_')].capitalize(), fi.namelist())
			elif f[f.find('.')+1:] == 'tar.bz2':
				with tarfile.open(f, 'r') as fi:
					i = 0
					for a in fi.getmembers():
						if (name+'/'+a.name == 'dock.theme') or (name+'/'+a.name == 'hover.theme'):
							i += 1
					fi.extractall(self.theme_path, fi.getmembers())
			elif f[f.find('.')+1:] == 'tar.gz':
				with tarfile.open(f, 'r') as fi:
					i = 0
					for a in fi.getmembers():
						if (name+'/'+a.name == 'dock.theme') or (name+'/'+a.name == 'hover.theme'):
							i += 1
					fi.extractall(self.theme_path, fi.getmembers())
			
			elif f[f.find('.')+1:] == 'zip':
					try:
						with zipfile.ZipFile(f, 'r') as fi:
							if (len(fi.namelist()) == 2) and ('dock.theme' in fi.namelist()) and ('hover.theme' in fi.namelist()):
								fi.extractall(self.theme_path+'/'+name[:name.find('_')].capitalize(), fi.namelist())
					except:
						msg = Gtk.MessageDialog(message_type = Gtk.MessageType.WARNING, message_format = g("You dont have a UNZIP program\nPlease make sure to install it before!"))
						msg.run()
						msg.destroy()
					
		else:
			msg = Gtk.MessageDialog(message_type = Gtk.MessageType.WARNING, message_format = g("The theme format is not supported!"))
			msg.run()
			msg.destroy()
		try:
			os.rename(path, newpath)
		except:
			pass
		self.refresh(self.liststore)
	
	def delfunc(self, widget):
		model, treeiter = self.select.get_selected()
		sys = False
		try:
			if model[treeiter][0] in os.listdir(self.theme_path):
				rmtheme = self.theme_path+'/'+model[treeiter][0]
			else:
				rmtheme = self.sys_theme_path+'/'+model[treeiter][0]
				sys = True
			msg = Gtk.MessageDialog(None, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, g("Do you really wanna remove the theme {} ?").format(model[treeiter][0]))
			resp = msg.run()
			if resp == Gtk.ResponseType.OK:
				if sys:
					os.system("gksu 'rm -r {0}'".format(rmtheme))
				else:
					shutil.rmtree(rmtheme)
			msg.destroy()
		except:
			pass
		self.refresh(self.liststore)

		
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
						
		

