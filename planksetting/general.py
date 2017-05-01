#!/usr/bin/env python3

from planksetting import Gtk
from planksetting import Gio
from planksetting import g


class general:
    def __init__(self, folder):
        self.win = Gtk.Window()
        self.setting = Gio.Settings.new_with_path("net.launchpad.plank.dock.settings", "/net/launchpad/plank/docks/{}/".format(folder))
        self.scroll = Gtk.ScrolledWindow()

        #Whether to show only windows of the current workspace.
        self.label1 = Gtk.Label(g("Show windows"))
        self.label1.set_tooltip_text(g("Show only windows of the current workspace."))
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
        self.box = Gtk.HBox()
        self.hide = Gtk.RadioButton(arg1)
        self.hide.connect("toggled", self.toggled, nmbr)
        self.ihide = Gtk.RadioButton(arg2, group=self.hide)
        self.ihide.connect("toggled", self.toggled, nmbr)
        self.ahide = Gtk.RadioButton(arg3, group=self.hide)
        self.ahide.connect("toggled", self.toggled, nmbr)
        self.maxw = Gtk.RadioButton(arg4, group=self.hide)
        self.maxw.connect("toggled", self.toggled, nmbr)

        self.box.pack_start(self.hide, 0, 0, False)
        self.box.pack_start(self.ihide, 0, 0, False)
        self.box.pack_start(self.ahide, 0, 0, False)
        self.box.pack_start(self.maxw, 0, 0, False)
        return self.box, self.hide, self.ihide, self.ahide, self.maxw


    #Helpers
    #1

    def toggled(self, widget, init_value):
        value = 0
        print(init_value)
        print(widget)
        if widget.get_active():
            if(init_value == 1):
                if widget.get_label() == g("Don't Hide"):
                    value = 'left'
                elif widget.get_label() == g("Intelligently hide"):
                    value = 'right'
                elif widget.get_label() == g("Auto hide"):
                    value = 'top'
                elif widget.get_label() == g("Dodge"):
                    value = 'bottom'

            if(init_value == 2):
                if widget.get_label() == g("Left"):
                    value = 'left'
                elif widget.get_label() == g("Right"):
                    value = 'right'
                elif widget.get_label() == g("Top"):
                    value = 'top'
                elif widget.get_label() == g("Bottom"):
                    value = 'bottom'

            if(init_value == 3 or init_value == 4):
                if widget.get_label() == g("Panel mode"):
                    value = 'panel'
                elif widget.get_label() == g("Right aligned"):
                    value = 'right'
                elif widget.get_label() == g("Left aligned"):
                    value = 'left'
                elif widget.get_label() == g("Centered"):
                    value = 'conter'

        if init_value == 1:
            self.setting.set_string("hide-mode", str(value))
        elif init_value == 2:
            self.setting.set_string("position", str(value))
        elif init_value == 3:
            self.setting.set_string("alignment", str(value))
        elif init_value == 4:
            self.setting.set_string("items-alignment", str(value))
        self.setting.apply()

    def switched(self, widget, state):
        self.setting.set_string("current-workspace-only", str(widget.get_active()))
        self.setting.apply()
    #2
    def spinb_chenged(self, widget):
        self.setting.set_string("icon-size", str(widget.get_value_as_int()))
        self.setting.apply()
    #4
    def spint_chenged(self, widget):
        self.setting.set_string("unhide-delay", str(widget.get_value_as_int()))
        self.setting.apply()
    #6
    def offset_chenged(self, widget):
        self.setting.set_string("offset", str(widget.get_value_as_int()))
        self.setting.apply()
    #9
    def switched1(self, widget, state):
        self.setting.set_string("lock-items", str(widget.get_active()))
        self.setting.apply()


    def main(self):
        Gtk.main()
