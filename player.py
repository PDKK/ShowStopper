
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import GObject,Gtk
from gi.repository import Gst as gst
import time
import threading

# Globally call gst init
gst.init(None)


class player(object):

    def __init__(self):

        # Create the pipeline for our elements.
        self.pipeline = gst.Pipeline()
        # Create the elements for our project.

        self.audio_source = gst.ElementFactory.make('filesrc', 'audio_source')
        self.decode = gst.ElementFactory.make('mad', 'decode')
        self.volume = gst.ElementFactory.make('volume', 'volume')
        self.audio_sink = gst.ElementFactory.make('autoaudiosink', 'audio_sink')

        # Ensure all elements were created successfully.
        if (not self.pipeline or not self.audio_source or not self.decode or not self.audio_sink or not self.volume):
            print('Not all elements could be created.')
            exit(-1)

        # Add our elements to the pipeline.
        self.pipeline.add(self.audio_source)
        self.pipeline.add(self.decode)
        self.pipeline.add(self.volume)
        self.pipeline.add(self.audio_sink)

        # Link our elements together.
        self.audio_source.link(self.decode)
        self.decode.link(self.volume)
        self.volume.link(self.audio_sink)
        self.volume.set_property('volume', 1.0)
        self.current_volume = 100

    def set_source(self, source):
        self.audio_source.set_property('location', source)

    def play(self):
        self.pipeline.set_state(gst.State.PLAYING)

    def stop(self):
        self.pipeline.set_state(gst.State.READY)

    def fade_out_work(self):
        while (self.current_volume > 0):
            self.current_volume -= 10
            self.volume.set_property('volume', self.current_volume / 100.0)
            time.sleep(0.1)

    def fade_out(self):
        threading.Thread(target=self.fade_out_work).start()

    def unused_bus_code(self):
        # Wait until error or EOS.
        bus = pipeline.get_bus()
        msg = bus.timed_pop_filtered(gst.CLOCK_TIME_NONE,gst.MessageType.ERROR | gst.MessageType.EOS)
        print (msg)

        # Free resources.
        pipeline.set_state(gst.State.NULL)

if __name__=="__main__":
    p1 = player()
    p1.set_source("knight.mp3")
    p1.play()
    time.sleep(5)
    p1.fade_out()
    time.sleep(2)

