#!/usr/bin/env python
import os

from gi.repository import Gtk
import item
import model

gladefile = os.path.join(os.path.dirname(__file__), "main.glade")


class mainWindow(object):

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(gladefile)
        self.window = self.builder.get_object("mainWindow")
        self.leftPanel = self.builder.get_object("listbox1")
        self.mainhandlers = {
            "on_btn_next_clicked": self.on_btn_next,
            "on_btn_prev_clicked": self.on_btn_prev,
            "on_btn_play_clicked": self.on_btn_play,
            "on_file_open": self.on_file_open,
            #"on_cancelBtn_clicked": Gtk.main_quit,
            "on_mainWindow_delete_event": Gtk.main_quit,
        }
        self.builder.connect_signals(self.mainhandlers)
        item1 = item.Item()
        self.leftPanel.add(item1.view)
        item2 = item.Item()
        self.leftPanel.add(item2.view)
        item3 = item.Item()
        self.leftPanel.add(item3.view)
        self.leftPanel.select_row(item3.view)
        self.window.show_all()
        Gtk.main()

    def on_btn_next(self, obj):
        print("Next")
        self.leftPanel.select_row(self.leftPanel.get_selected_row()+1)

    def on_btn_prev(self, obj):
        print("Prev")

    def on_btn_play(self, obj):
        print("Play")

    def on_file_open(self, obj):
        print("Open")
        dialog = Gtk.FileChooserDialog("Please choose a file", self.window,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Chose:" + dialog.get_filename())
            self.model = model.show()
            self.model.load(dialog.get_filename())
        else:
            print("Cancelled")
        dialog.destroy()

mainWindow()