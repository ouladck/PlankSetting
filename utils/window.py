#!/usr/bin/env python3

from gi.repository import Gtk
from utils.serialize import *
from gettext import gettext as g


class Window:
    def __init__(self, setting_path, folder):
        self.win = Gtk.Window()
        self.setting = setting_path + folder + "/settings"
        self.scroll = Gtk.ScrolledWindow()

        #Whether to show only windows of the current workspace.
        self.label1 = Gtk.Label(g("Show windows"))
        self.label1.set_tooltip_text(
            g("Show only windows of the current workspace."))
        self.switch = Gtk.Switch()
        self.switch.connect("notify::active", self.switched)

        #The size of dock icons (in pixels).
        self.label2 = Gtk.Label(g("Dock size"))
        self.label2.set_tooltip_text(g("The size of dock icons (in pixels)."))
        self.adjustment = Gtk.Adjustment(32, 16, 48, 1, 5, 0)
        self.spinbutton = Gtk.SpinButton(adjustment=self.adjustment)
        self.spinbutton.connect("value-changed", self.spinb_chenged)

        #If 0, the dock won't hide.  If 1,
        #the dock intelligently hides.  If 2, the dock auto-hides.
        #If 3, the dock dodges active maximized windows.
        self.label3 = Gtk.Label(g("Display mode"))
        self.label3.set_tooltip_text(g("The display of the dock."))
        self.display = self.radios(
            g("Don't hide"), g("Intelligently hide"),
            g("Auto hide"), g("Dodge"), 1)

        #Time (in ms) to wait before unhiding the dock.
        self.label4 = Gtk.Label(g("Waiting time"))
        self.label4.set_tooltip_text(
            g("Time (in ms) to wait before unhiding the dock."))
        self.adj = Gtk.Adjustment(0, 0, 60, 1, 5, 0)
        self.spintime = Gtk.SpinButton(adjustment=self.adj)
        self.spintime.connect("value-changed", self.spint_chenged)

        #The monitor number for the dock. Use -1 to keep on the primary monitor.
        self.label5 = Gtk.Label(g("The monitor number for the dock."))

        #The position for the dock on the monitor.
        #If 0, left.  If 1, right.  If 2, top.  If 3, bottom.
        self.label6 = Gtk.Label(g("Position"))
        self.label6.set_tooltip_text(
            g("The position for the dock on the monitor."))
        self.pos = self.radios(g("Left"), g("Right"), g("Top"), g("Bottom"), 2)

        #The dock's position offset from center (in percent).
        self.label7 = Gtk.Label(g("Offset"))
        self.label7.set_tooltip_text(
            g("The dock's position offset from center (in percent)."))
        self.adj1 = Gtk.Adjustment(0, 0, 100, 1, 5, 0)
        self.offset = Gtk.SpinButton(adjustment=self.adj1)
        self.offset.connect("value-changed", self.offset_chenged)

        #The alignment for the dock on the monitor's edge.
        #If 0, panel-mode.  If 1, right-aligned.
        #If 2, left-aligned.  If 3, centered.
        self.label8 = Gtk.Label(g("Alignment"))
        self.label8.set_tooltip_text(
            g("The alignment for the dock on the monitor's edge."))
        self.alignment = self.radios(
            g("Panel mode"), g("Right aligned"),
            g("Left aligned"), g("Centered"), 3)

        #The alignment of the items in this dock if panel-mode is used.
        #If 1, right-aligned.  If 2, left-aligned.  If 3, centered.
        self.label9 = Gtk.Label(g("Item alignment"))
        self.label9.set_tooltip_text(
            g("The alignment of the items in this dock."))
        self.itemalig = self.radios(
            g("Panel mode"), g("Right aligned"),
            g("Left aligned"), g("Centered"), 4)

        #Whether to prevent drag'n'drop actions and lock items on the dock.
        self.label10 = Gtk.Label(g("Drag'n'drop"))
        self.label10.set_tooltip_text(
            g("Prevent drag'n'drop actions and lock items on the dock."))
        self.drag = Gtk.Switch()
        self.drag.connect("notify::active", self.switched1)

        #################
        self.read_file()
        #################

        self.table = Gtk.VBox()

        self.table.pack_start(self.fbox(self.label1, self.switch),
            False, False, 5)
        self.table.pack_start(self.fbox(self.label2, self.spinbutton),
            False, False, 5)
        self.table.pack_start(self.fbox(self.label3, self.display[0]),
            False, False, 5)
        self.table.pack_start(self.fbox(self.label4, self.spintime),
            False, False, 5)
        self.table.pack_start(self.fbox(self.label5),
            False, False, 5)
        self.table.pack_start(self.fbox(self.label6, self.pos[0]),
            False, False, 5)
        self.table.pack_start(self.fbox(self.label7, self.offset),
            False, False, 5)
        self.table.pack_start(self.fbox(self.label8, self.alignment[0]),
            False, False, 5)
        self.table.pack_start(self.fbox(self.label9, self.itemalig[0]),
            False, False, 5)
        self.table.pack_start(self.fbox(self.label10, self.drag),
            False, False, 5)

        self.scroll.add(self.table)

    """Methods"""
    #Views
    def fbox(self, widget1, widget2=Gtk.Label("Not Available now!")):
        h = Gtk.HBox()
        h.pack_start(widget1, False, False, 5)
        h.pack_end(widget2, False, False, 15)
        return h

    def radios(self, arg1, arg2, arg3, arg4, nmbr):
        def toggled(widget):
            value = 0
            if widget.get_active():
                if widget.get_label() == g("Hide")or widget.get_label()== g("Left") or widget.get_label() == g("Panel mode"):
                    value = 0
                elif widget.get_label() == g("Intelligently hide") or widget.get_label() == g("Right") or widget.get_label() == g("Right aligned"):
                    value = 1
                elif widget.get_label() == g("Auto hide") or widget.get_label() == g("Top") or widget.get_label() == g("Left aligned"):
                    value = 2
                elif widget.get_label() == g("Dodge") or widget.get_label() == g("Bottom") or widget.get_label() == g("Centered"):
                    value = 3
            if nmbr == 1:
                write_func(read_func(self.setting), self.setting, "HideMode", value)
            elif nmbr == 2:
                write_func(read_func(self.setting), self.setting, "Position", value)
            elif nmbr == 3:
                write_func(read_func(self.setting), self.setting, "Alignment", value)
            elif nmbr == 4:
                write_func(read_func(self.setting), self.setting, "ItemsAlignment", value)
        self.box = Gtk.HBox()
        self.hide = Gtk.RadioButton(arg1)
        self.hide.connect("toggled", toggled)
        self.ihide = Gtk.RadioButton(arg2, group=self.hide)
        self.ihide.connect("toggled", toggled)
        self.ahide = Gtk.RadioButton(arg3, group=self.hide)
        self.ahide.connect("toggled", toggled)
        self.maxw = Gtk.RadioButton(arg4, group=self.hide)
        self.maxw.connect("toggled", toggled)
        self.box.pack_start(self.hide, 0, 0, False)
        self.box.pack_start(self.ihide, 0, 0, False)
        self.box.pack_start(self.ahide, 0, 0, False)
        self.box.pack_start(self.maxw, 0, 0, False)
        return self.box, self.hide, self.ihide, self.ahide, self.maxw

    def read_file(self):
        self.lst = read_func(self.setting)
        for a in self.lst:
            #1
            if a[0:a.find("=")] == "CurrentWorkspaceOnly":
                if a[a.find("=")+1:-1] == "true":
                    self.switch.set_active(True)
                else:
                    self.switch.set_active(False)
            #2
            if a[0:a.find("=")] == "IconSize":
                self.spinbutton.set_value(int(a[a.find("=")+1:-1]))
            #3
            if a[0:a.find("=")] == "HideMode":
                self.display[int(a[a.find("=")+1:-1])+1].set_active(True)
            #4
            if a[0:a.find("=")] == "UnhideDelay":
                self.spintime.set_value(int(a[a.find("=")+1:-1]))
            #5
            if a[0:a.find("=")] == "Position":
                self.pos[int(a[a.find("=")+1:-1])+1].set_active(True)
            #6
            if a[0:a.find("=")] == "Offset":
                self.offset.set_value(int(a[a.find("=")+1:-1]))
            #7
            if a[0:a.find("=")] == "Alignment":
                self.alignment[int(a[a.find("=")+1:-1])+1].set_active(True)
            #8
            if a[0:a.find("=")] == "ItemsAlignment":
                self.itemalig[int(a[a.find("=")+1:-1])+1].set_active(True)
            #9
            if a[0:a.find("=")] == "LockItems":
                if a[a.find("=")+1:-1] == "true":
                    self.drag.set_active(True)
                else:
                    self.drag.set_active(False)

            #end   a[a.find("=")+1:-1] #start  a[0:a.find("=")]

    #Helpers
    #1
    def switched(self, widget, state):
        write_func(read_func(self.setting), self.setting, "CurrentWorkspaceOnly", widget.get_active())
    #2
    def spinb_chenged(self, widget):
        write_func(read_func(self.setting), self.setting, "IconSize", widget.get_value_as_int())
    #4
    def spint_chenged(self, widget):
        write_func(read_func(self.setting), self.setting, "UnhideDelay", widget.get_value_as_int())
    #6
    def offset_chenged(self, widget):
        write_func(read_func(self.setting), self.setting, "Offset", widget.get_value_as_int())
    #9
    def switched1(self, widget, state):
        write_func(read_func(self.setting), self.setting, "LockItems", widget.get_active())


    def main(self):
        Gtk.main()
