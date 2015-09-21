
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
gi.require_version('GstController', '1.0')
# from gi.repository import GObject,Gtk
from gi.repository import Gst as gst
from gi.repository import GstController
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

        self.cs = GstController.InterpolationControlSource.new()
        self.cs.set_property('mode', GstController.InterpolationMode.LINEAR)
        self.cb = GstController.DirectControlBinding.new(self.volume, 'volume', self.cs)
        self.volume.add_control_binding(self.cb)


    def set_source(self, source):
        self.audio_source.set_property('location', source)

    def play(self):
        self.pipeline.set_state(gst.State.PLAYING)

    def stop(self):
        self.pipeline.set_state(gst.State.READY)

    def fade_out(self):
        current = self.pipeline.get_clock().get_time()
        self.cs.set(current, 0.15)
        self.cs.set(current + 3 * gst.SECOND, 0.0)

    def unused_bus_code(self):
        # Wait until error or EOS.
        bus = self.pipeline.get_bus()
        msg = bus.timed_pop_filtered(gst.CLOCK_TIME_NONE,gst.MessageType.ERROR | gst.MessageType.EOS)
        print (msg)

        # Free resources.
        self.pipeline.set_state(gst.State.NULL)

if __name__=="__main__":
    p1 = player()
    p1.set_source("1.mp3")
    p1.play()
    time.sleep(5)
    p1.fade_out()
    time.sleep(4)

