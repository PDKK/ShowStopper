#!/usr/bin/env python
import os

from gi.repository import Gtk
import item
import model
import player


gladefile = os.path.join(os.path.dirname(__file__), "glade/main.glade")


class mainWindow(object):
    items = []
    currentItem = 0;
    player1 = player.player()

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
        self.items.append(item.Item())
        self.leftPanel.add(self.items[len(self.items) - 1].view)
	self.items[len(self.items) - 1].connect("my_signal", self.on_item_signal)
        self.items.append(item.Item())
        self.leftPanel.add(self.items[len(self.items) - 1].view)
        self.items.append(item.Item())
        self.leftPanel.add(self.items[len(self.items) - 1].view)
        self.leftPanel.select_row(self.items[2].view)
        self.window.show_all()

    def on_btn_next(self, obj):
        print("Next")
        self.currentItem += 1
        print(self.currentItem)
        self.leftPanel.select_row(self.items[self.currentItem].view)

    def on_btn_prev(self, obj):
        print("Prev")
        self.currentItem -= 1
        print(self.currentItem)
        self.leftPanel.select_row(self.items[self.currentItem].view)

    def on_btn_play(self, obj):
        print("Play" + self.items[self.currentItem].get_filename())
        self.player1.set_source(self.items[self.currentItem].get_filename())
        self.player1.play()

    def on_item_signal(self, orig, pos):
        print("on_item_signal", pos)

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

