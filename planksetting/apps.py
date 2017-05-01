#!/usr/bin/env python3

from planksetting import Gtk
from planksetting import g
import os
import shutil

class apps:

    def makedire(self, f):
        if not os.path.exists(f):
            os.makedirs(f)

    def groupsel(self, widget, listbox):
        print(listbox.get_text())

    def appchooser(self, widget):
        app = Gtk.AppChooserDialog(content_type='image/png')
        response = app.run()
        if response == Gtk.ResponseType.OK:
            app_info = app.get_app_info()
            self.appname = app_info.get_filename()
            shutil.copy2(app_info.get_filename(), self.groupdir + self.selectedgroup)
        app.destroy()
        self.refresh(self.store, self.groupdir + self.selectedgroup)

    def on_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        self.selectedgroup = model[treeiter][0]
        self.refresh(self.store, self.groupdir + self.selectedgroup)
        self.delg.set_sensitive(True)
        self.addapp.set_sensitive(True)
        self.delapp.set_sensitive(True)

    def on_tree_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        self.appnom = model[treeiter][0]
        self.selectedapp = self.getinfo(self.appnom)

    def getinfo(self, name):
        for b in os.listdir(self.groupdir + self.selectedgroup):
            with open(self.groupdir + self.selectedgroup + '/' + b, 'r') as rf:
                li = rf.readlines()
            for a in li:
                if a[a.find("=") + 1:-1] == name:
                    return self.groupdir + self.selectedgroup + '/' + b

    def xtract(self, name):
        i = int()
        Name, Icon = str(), str()
        with open(self.groupdir + self.selectedgroup + '/' + name, 'r') as rf:
            li = rf.readlines()
        for a in li:
            if a[0:a.find("=")] == "Name" and i == 0:
                Name = a[a.find("=") + 1:-1]
                i += 1
            if a[0:a.find("=")] == "Icon":
                Icon = a[a.find("=") + 1:-1]
        return Name, Icon

    def refresh(self, widget, f):
        widget.clear()
        for a in os.listdir(f):
            if a.endswith('.desktop'):
                a = self.xtract(a)[0]
            widget.append([a])

    def delgroup(self, widget):
        if len(self.selectedgroup) > 0:
            this = self.dockitems + self.selectedgroup + ".dockitem"
            os.remove(this)
            shutil.rmtree(self.groupdir + self.selectedgroup)
            print(this)
        self.refresh(self.liststore, self.groupdir)

    def delapplication(self, widget):
        if len(self.selectedgroup) > 0:
            os.remove(self.selectedapp)
        self.refresh(self.store, self.groupdir + self.selectedgroup)

    def addgroup(self, widget):
        self.dialog = Gtk.Dialog(title=g("New Group"), buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))

        label = Gtk.Label(g("Enter the Group name"))
        entry = Gtk.Entry()

        box = self.dialog.get_content_area()
        box.add(label)
        box.add(entry)
        box.show_all()
        response = self.dialog.run()
        if response == Gtk.ResponseType.OK:
            if len(entry.get_text()) > 0:
                with open(self.dockitems + entry.get_text() + ".dockitem", 'w') as rf:
                    rf.write("[PlankItemsDockItemPreferences]\nLauncher=file://" + self.groupdir + entry.get_text())
                self.makedire(self.groupdir + entry.get_text())
        self.refresh(self.liststore, self.groupdir)
        self.dialog.destroy()

    def __init__(self, folder):
        self.selectedgroup, self.selectedapp = str(), str()
        self.appname, self.appnom = str(), str()
        self.groupdir = os.path.expanduser("~") + "/.config/plank/" + folder + "/groupapps/"
        self.dockitems = os.path.expanduser("~") + "/.config/plank/" + folder + "/launchers/"
        self.makedire(self.groupdir)

        self.win = Gtk.Window()
        #self.scroll = Gtk.ScrolledWindow()
        self.box = Gtk.VBox()
        self.hb1 = Gtk.HBox()
        self.hb2 = Gtk.HBox()

        ### Listview

        self.liststore = Gtk.ListStore(str)
        self.refresh(self.liststore, self.groupdir)

        self.treeview = Gtk.TreeView(model=self.liststore)

        self.treeviewcolumn = Gtk.TreeViewColumn(g("Group of Apps"))
        self.treeview.append_column(self.treeviewcolumn)
        self.cellrenderertext = Gtk.CellRendererText()
        self.treeviewcolumn.pack_start(self.cellrenderertext, True)
        self.treeviewcolumn.add_attribute(self.cellrenderertext, "text", 0)
        self.select = self.treeview.get_selection()
        self.select.connect("changed", self.on_selection_changed)

        self.store = Gtk.ListStore(str)

        self.view = Gtk.TreeView(model=self.store)

        self.viewcolumn = Gtk.TreeViewColumn(g("Application"))
        self.view.append_column(self.viewcolumn)
        self.cellrenderertext = Gtk.CellRendererText()
        self.viewcolumn.pack_start(self.cellrenderertext, True)
        self.viewcolumn.add_attribute(self.cellrenderertext, "text", 0)
        self.select1 = self.view.get_selection()
        self.select1.connect("changed", self.on_tree_selection_changed)

#        self.listbox = Gtk.ListBox()
#        for g in os.listdir(self.groupdir):
#            self.listbox.add(Gtk.Label(g))
#        self.listbox.connect("row-activated", self.groupsel)

        self.hb1.pack_start(self.treeview, True, True, 5)
        self.hb1.pack_end(self.view, True, True, 5)

        ### Button

        self.addg = Gtk.Button(stock=Gtk.STOCK_ADD)
        self.addg.connect('clicked', self.addgroup)
        self.addg.set_tooltip_text(g("Add a Group"))
        #
        self.delg = Gtk.Button(stock=Gtk.STOCK_REMOVE)
        self.delg.set_sensitive(False)
        self.delg.connect('clicked', self.delgroup)
        self.delg.set_tooltip_text(g("Delete a Group"))
        #
        self.addapp = Gtk.Button(stock=Gtk.STOCK_ADD)
        self.addapp.set_sensitive(False)
        self.addapp.connect('clicked', self.appchooser)
        self.addapp.set_tooltip_text(g("Add a Application"))
        #
        self.delapp = Gtk.Button(stock=Gtk.STOCK_REMOVE)
        self.delapp.set_sensitive(False)
        self.delapp.connect('clicked', self.delapplication)
        self.delapp.set_tooltip_text(g("Delete a Application"))

        self.hb2.pack_start(self.addg, False, False, 5)
        self.hb2.pack_start(self.delg, False, False, 5)
        self.hb2.pack_end(self.delapp, False, False, 5)
        self.hb2.pack_end(self.addapp, False, False, 5)

        self.box.pack_start(self.hb1, True, True, 15)
        self.box.pack_start(self.hb2, False, False, 15)
