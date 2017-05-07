#!/usr/bin/env python3

from planksetting import Gio
from planksetting import Gtk
from planksetting import g


class general:
    def __init__(self, folder):
        self.win = Gtk.Window()
        self.setting = Gio.Settings.new_with_path("net.launchpad.plank.dock.settings",
                                                  "/net/launchpad/plank/docks/{}/".format(folder))
        self.scroll = Gtk.ScrolledWindow()

        # Whether to show only windows of the current workspace.
        self.label1 = Gtk.Label(g("Show windows"))
        self.label1.set_tooltip_text(g("Show only windows of the current workspace."))
        self.switch = Gtk.Switch()
        # Get value
        value = self.setting.get_boolean("current-workspace-only")
        self.switch.set_active(value)
        self.switch.connect("notify::active", self.switched, "current-workspace-only")

        # The size of dock icons (in pixels).
        self.label2 = Gtk.Label(g("Icon size"))
        self.label2.set_tooltip_text(g("The size of dock icons (in pixels)."))
        self.adjustment = Gtk.Adjustment(48, 24, 128, 1, 5, 0)
        self.spinbutton = Gtk.SpinButton(adjustment=self.adjustment)
        # Get value
        value = self.setting.get_int("icon-size")
        self.spinbutton.set_value(value)
        self.spinbutton.connect("value-changed", self.set_value, "icon-size")

        # If 0, the dock won't hide.  If 1,
        # the dock intelligently hides.  If 2, the dock auto-hides.
        # If 3, the dock dodges active maximized windows.
        self.label3 = Gtk.Label(g("Display mode"))
        self.label3.set_tooltip_text(g("The display of the dock."))
        self.display = self.radios(g("Don't hide"), g("Intelligently hide"),
                                   g("Auto hide"), g("Dodge active"), g("Dodge maximized"), g("Dodge window"),
                                   "hide-mode")

        # Time (in ms) to wait before unhiding the dock.
        self.label4 = Gtk.Label(g("Waiting time"))
        self.label4.set_tooltip_text(
            g("Time (in ms) to wait before unhiding the dock."))
        self.adj = Gtk.Adjustment(0, 0, 60, 1, 5, 0)
        self.spintime = Gtk.SpinButton(adjustment=self.adj)
        # Get value
        value = self.setting.get_int("unhide-delay")
        self.spintime.set_value(value)
        self.spintime.connect("value-changed", self.set_value, "unhide-delay")

        # Time (in ms) to wait before unhiding the dock.
        self.label12 = Gtk.Label(g("Dock hide delay"))
        self.label12.set_tooltip_text(
            g("Length of the delay before hiding the dock, in milliseconds."))
        self.adj2 = Gtk.Adjustment(0, 0, 60, 1, 5, 0)
        self.spintime2 = Gtk.SpinButton(adjustment=self.adj2)
        # Get value
        value = self.setting.get_int("hide-delay")
        self.spintime2.set_value(value)
        self.spintime2.connect("value-changed", self.set_value, "hide-delay")

        # The monitor number for the dock. Use -1 to keep on the primary monitor.
        self.label5 = Gtk.Label(g("The monitor number for the dock."))
        self.label5.set_tooltip_text(
            "The plug-name of the monitor for the dock to show on (e.g. DVI-I-1, HDMI1, LVDS1). Leave this empty to keep on the primary monitor.")
        self.monitor = Gtk.Entry()
        # Get value
        value = self.setting.get_string("monitor")
        self.monitor.set_text(value)
        self.monitor.connect("focus-out-event", self.set_value, "monitor")

        # The position for the dock on the monitor.
        # If 0, left.  If 1, right.  If 2, top.  If 3, bottom.
        self.label6 = Gtk.Label(g("Position"))
        self.label6.set_tooltip_text(
            g("The position for the dock on the monitor."))
        self.pos = self.radios(g("Left"), g("Right"), g("Top"), g("Bottom"), None, None, "position")

        # The dock's position offset from center (in percent).
        self.label7 = Gtk.Label(g("Offset"))
        self.label7.set_tooltip_text(
            g("The dock's position offset from center (in percent)."))
        self.adj1 = Gtk.Adjustment(0, -100, 100, 1, 5, 0)
        self.offset = Gtk.SpinButton(adjustment=self.adj1)
        # Get value
        value = self.setting.get_int("offset")
        self.offset.set_value(value)
        self.offset.connect("value-changed", self.set_value, "offset")

        # The alignment for the dock on the monitor's edge.
        # If 0, panel-mode.  If 1, right-aligned.
        # If 2, left-aligned.  If 3, centered.
        self.label8 = Gtk.Label(g("Alignment"))
        self.label8.set_tooltip_text(
            g("The alignment for the dock on the monitor's edge."))
        self.alignment = self.radios(
            g("Panel mode"), g("Right aligned"),
            g("Left aligned"), g("Centered"), None, None, "alignment")

        # The alignment of the items in this dock if panel-mode is used.
        # If 1, right-aligned.  If 2, left-aligned.  If 3, centered.
        self.label9 = Gtk.Label(g("Item alignment"))
        self.label9.set_tooltip_text(
            g("The alignment of the items in this dock."))
        self.itemalig = self.radios(
            g("Panel mode"), g("Right aligned"),
            g("Left aligned"), g("Centered"), None, None, "items-alignment")

        # Whether to prevent drag'n'drop actions and lock items on the dock.
        self.label10 = Gtk.Label(g("Disable Drag'N'Drop"))
        self.label10.set_tooltip_text(
            g("Prevent drag'n'drop actions and lock items on the dock."))
        self.drag = Gtk.Switch()
        # Get value
        value = self.setting.get_boolean("lock-items")
        self.drag.set_active(value)
        self.drag.connect("notify::active", self.switched, "lock-items")

        # Automatically pin an application if it seems useful to do
        self.label11 = Gtk.Label(g("Auto pin"))
        self.label11.set_tooltip_text(g("Automatically pin an application if it seems useful to do"))
        self.pin = Gtk.Switch()
        # Get value
        value = self.setting.get_boolean("auto-pinning")
        self.pin.set_active(value)
        self.pin.connect("notify::active", self.switched, "auto-pinning")

        # If true, only show pinned applications. Useful for running more than one dock.
        self.label12n = Gtk.Label(g("Only show pinned applications"))
        self.label12n.set_tooltip_text(
            g("If true, only show pinned applications. Useful for running more than one dock."))
        self.pin1 = Gtk.Switch()
        # Get value
        value = self.setting.get_boolean("pinned-only")
        self.pin1.set_active(value)
        self.pin1.connect("notify::active", self.switched, "pinned-only")

        # If true, use pressure-based revealing of the dock if the input device supports it.
        self.label13 = Gtk.Label(g("Pressure Reveal"))
        self.label13.set_tooltip_text(
            g("If true, use pressure-based revealing of the dock if the input device supports it."))
        self.press = Gtk.Switch()
        # Get value
        value = self.setting.get_boolean("pressure-reveal")
        self.press.set_active(value)
        self.press.connect("notify::active", self.switched, "pressure-reveal")

        # If true, show the Plank dock item.
        self.label14 = Gtk.Label(g("Show the item for the dock itself"))
        self.label14.set_tooltip_text(g("If true, show the Plank dock item."))
        self.show_item = Gtk.Switch()
        # Get value
        value = self.setting.get_boolean("show-dock-item")
        self.show_item.set_active(value)
        self.show_item.connect("notify::active", self.switched, "show-dock-item")

        # If true, tooltips will be shown when dock items are hovered with the cursor.
        self.label15 = Gtk.Label(g("Show tooltips when items are hovered"))
        self.label15.set_tooltip_text(g("If true, tooltips will be shown when dock items are hovered with the cursor."))
        self.tooltps = Gtk.Switch()
        # Get value
        value = self.setting.get_boolean("tooltips-enabled")
        self.tooltps.set_active(value)
        self.tooltps.connect("notify::active", self.switched, "tooltips-enabled")

        # If true, zoom dock items when hovered with the cursor.
        self.label16 = Gtk.Label(g("Zoom dock items when hovered"))
        self.label16.set_tooltip_text(g("If true, zoom dock items when hovered with the cursor."))
        self.zoom = Gtk.Switch()
        # Get value
        value = self.setting.get_boolean("zoom-enabled")
        display = value
        self.zoom.set_active(value)
        self.zoom.connect("notify::active", self.switched, "zoom-enabled")

        # The amount to zoom dock items, in percent.
        self.label17 = Gtk.Label(g("Icon zoom percentage"))
        self.label17.set_tooltip_text(g("The amount to zoom dock items, in percent."))
        self.adj3 = Gtk.Adjustment(150, 100, 200, 1, 5, 0)
        self.zoom_val = Gtk.SpinButton(adjustment=self.adj3)
        # Get value
        value = self.setting.get_int("zoom-percent")
        self.zoom_val.set_value(value)
        self.zoom_val.set_editable(display)
        self.zoom_val.connect("value-changed", self.set_value, "zoom-percent")

        self.table = Gtk.VBox()

        self.table.pack_start(self.fbox(self.label1, self.switch),
                              False, False, 5)
        self.table.pack_start(self.fbox(self.label2, self.spinbutton),
                              False, False, 5)
        self.table.pack_start(self.fbox(self.label3, self.display[0]),
                              False, False, 5)
        self.table.pack_start(self.fbox(self.label4, self.spintime),
                              False, False, 5)
        self.table.pack_start(self.fbox(self.label12, self.spintime2),
                              False, False, 5)
        self.table.pack_start(self.fbox(self.label5, self.monitor),
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
        self.table.pack_start(self.fbox(self.label11, self.pin),
                              False, False, 5)
        self.table.pack_start(self.fbox(self.label12n, self.pin1),
                              False, False, 5)
        self.table.pack_start(self.fbox(self.label13, self.press),
                              False, False, 5)
        self.table.pack_start(self.fbox(self.label14, self.show_item),
                              False, False, 5)
        self.table.pack_start(self.fbox(self.label15, self.tooltps),
                              False, False, 5)
        self.table.pack_start(self.fbox(self.label16, self.zoom),
                              False, False, 5)
        self.table.pack_start(self.fbox(self.label17, self.zoom_val),
                              False, False, 5)

        self.scroll.add(self.table)

    """Methods"""

    # Views
    def fbox(self, widget1, widget2=Gtk.Label("Not Available yet!")):
        h = Gtk.HBox()
        h.pack_start(widget1, False, False, 5)
        h.pack_end(widget2, False, False, 15)
        return h

    def radios(self, arg1, arg2, arg3, arg4, arg5, arg6, val):
        self.box = Gtk.HBox()
        self.hide = Gtk.RadioButton(arg1)
        # Get value
        value = str(self.setting.get_string(val))
        if (value == 'none' or value == 'left' or value == 'fill'):
            self.hide.set_active(True)
        self.hide.connect("toggled", self.toggled, val)
        self.ihide = Gtk.RadioButton(arg2, group=self.hide)
        # Get value
        value1 = str(self.setting.get_string(val))
        if (value1 == 'intelligent' or value1 == 'right' or value1 == 'end'):
            self.ihide.set_active(True)
        self.ihide.connect("toggled", self.toggled, val)
        self.ahide = Gtk.RadioButton(arg3, group=self.hide)
        # Get value
        value2 = str(self.setting.get_string(val))
        if (value2 == 'auto' or value2 == 'top' or value2 == 'start'):
            self.ahide.set_active(True)
        self.ahide.connect("toggled", self.toggled, val)
        self.maxw = Gtk.RadioButton(arg4, group=self.hide)
        # Get value
        value3 = str(self.setting.get_string(val))
        if (value3 == 'dodge-active' or value3 == 'bottom' or value3 == 'center'):
            self.maxw.set_active(True)
        self.maxw.connect("toggled", self.toggled, val)
        self.d5, self.d6 = None, None
        if (arg5 != None):
            self.d5 = Gtk.RadioButton(arg5, group=self.hide)
            # Get value
            value4 = str(self.setting.get_string(val))
            if (value4 == 'dodge-maximized'):
                self.d5.set_active(True)
            self.d5.connect("toggled", self.toggled, val)
        if (arg6 != None):
            self.d6 = Gtk.RadioButton(arg6, group=self.hide)
            # Get value
            value5 = str(self.setting.get_string(val))
            if (value5 == 'window-dodge'):
                self.d6.set_active(True)
            self.d6.connect("toggled", self.toggled, val)

        self.box.pack_start(self.hide, 0, 0, False)
        self.box.pack_start(self.ihide, 0, 0, False)
        self.box.pack_start(self.ahide, 0, 0, False)
        self.box.pack_start(self.maxw, 0, 0, False)
        if (arg5 != None):
            self.box.pack_start(self.d5, 0, 0, False)
        if (arg6 != None):
            self.box.pack_start(self.d6, 0, 0, False)
        return self.box, self.hide, self.ihide, self.ahide, self.maxw, self.d5, self.d6

    # Helpers
    # 1

    def toggled(self, widget, init_value):
        value = ''
        if widget.get_active():
            if (init_value == "hide-mode"):
                if widget.get_label() == g("Don't Hide"):
                    value = 'none'
                elif widget.get_label() == g("Intelligently hide"):
                    value = 'intelligent'
                elif widget.get_label() == g("Auto hide"):
                    value = 'auto'
                elif widget.get_label() == g("Dodge"):
                    value = 'dodge-active'
                elif widget.get_label() == g("Dodge maximized"):
                    value = 'dodge-maximized'
                elif widget.get_label() == g("Dodge window"):
                    value = 'window-dodge'

            if (init_value == "position"):
                if widget.get_label() == g("Left"):
                    value = 'left'
                elif widget.get_label() == g("Right"):
                    value = 'right'
                elif widget.get_label() == g("Top"):
                    value = 'top'
                elif widget.get_label() == g("Bottom"):
                    value = 'bottom'

            if (init_value == "alignment" or init_value == "items-alignment"):
                if widget.get_label() == g("Panel mode"):
                    value = 'fill'
                elif widget.get_label() == g("Right aligned"):
                    value = 'end'
                elif widget.get_label() == g("Left aligned"):
                    value = 'start'
                elif widget.get_label() == g("Centered"):
                    value = 'center'

        self.setting.set_string(init_value, value)
        self.setting.apply()

    # 2
    def set_value(self, widget, name):
        if (name == 'monitor'):
            value = widget.get_value()
            self.setting.set_string(name, str(value))
        else:
            value = widget.get_value_as_int()
            self.setting.set_int(name, value)
        self.setting.apply()

    # 9

    def switched(self, widget, state, name):
        value = True if widget.get_active() else False
        if (name == 'zoom-enabled' and not value):
            self.zoom_val.set_editable(False)
        else:
            self.zoom_val.set_editable(True)
        self.setting.set_boolean(name, value)
        self.setting.apply()

    def main(self):
        Gtk.main()
