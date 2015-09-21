__author__ = 'pknox-kennedy'

#!/usr/bin/env python
import os

from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf, InterpType

gladefile = os.path.join(os.path.dirname(__file__), "glade/item.glade")
ledfile = os.path.join(os.path.dirname(__file__), "images/green_led.png")


class Item(object):

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(gladefile)
        self.view = Gtk.ListBoxRow()
        self.view.add(self.builder.get_object("itemBox"))
        self.mainhandlers = {
            #"on_cancel_clicked": Gtk.main_quit,
            #"on_cancelBtn_clicked": Gtk.main_quit,
            #"on_mainWindow_delete_event": Gtk.main_quit,
        }
        self.builder.connect_signals(self.mainhandlers)
        pixbuf = Pixbuf.new_from_file(ledfile)
        pixbuf = pixbuf.scale_simple(32, 32, InterpType.BILINEAR)
        self.builder.get_object("image1").set_from_pixbuf(pixbuf)

        #self.window.show_all()
        #Gtk.main()

    def get_filename(self):
        fname = self.builder.get_object("filechooserbutton1").get_filename()
        print(fname)
        return fname