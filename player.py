
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import GObject,Gtk
from gi.repository import Gst as gst
import time

# Globally call gst init
gst.init(None)


class player(object):

    def __init__(self):

        # Create the pipeline for our elements.
        self.pipeline = gst.Pipeline()
        # Create the elements for our project.

        self.audio_source = gst.ElementFactory.make('filesrc', 'audio_source')
        self.decode = gst.ElementFactory.make('mad', 'decode')
        self.audio_sink = gst.ElementFactory.make('autoaudiosink', 'audio_sink')

        # Ensure all elements were created successfully.
        if (not self.pipeline or not self.audio_source or not self.decode or not self.audio_sink):
            print('Not all elements could be created.')
            exit(-1)

        # Add our elements to the pipeline.
        self.pipeline.add(self.audio_source)
        self.pipeline.add(self.decode)
        self.pipeline.add(self.audio_sink)

        # Link our elements together.
        self.audio_source.link(self.decode)
        self.decode.link(self.audio_sink)

    def set_source(self, source):

        # Configure our elements.
        self.audio_source.set_property('location', source)


    def play(self):
        # Set our pipelines state to Playing.
        '''
        gst.STATE_PLAYING => gst.State.PLAYING

        Just a hint:
        check the following documentation whenever you get
        some AttributeError.
        link: http://lazka.github.io/pgi-docs/#Gst-1.0/flags.html

        '''
        self.pipeline.set_state(gst.State.PLAYING)

    def stop(self):
        self.pipeline.set_state(gst.State.READY)

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
    p1.stop()

