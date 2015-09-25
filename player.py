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


def getAudioLength(name):
    # Simple gstreamer pipeline going to fakesink
    d = gst.parse_launch("filesrc name=source ! decodebin name=decode ! fakesink")
    source = d.get_by_name("source")
    source.set_property("location", name)
    d.set_state(gst.State.PLAYING)
    # Set state will give us an async return. Get state with timeout
    # waits until we reach the playing state. Note that this timeout
    # is in nanoseconds
    d.get_state(1 * gst.SECOND)
    success, duration = d.query_duration(gst.Format.TIME)
    d.set_state(gst.State.NULL)
    return duration / gst.SECOND

class Player(object):
    def __init__(self):

        # Create the pipeline for our elements.
        self._pipeline = gst.Pipeline()
        # Create the elements for our project.

        self._audio_source = gst.ElementFactory.make('filesrc', 'audio_source')
        self._decode = gst.ElementFactory.make('decodebin', 'decode')
        self._decode.connect("pad-added", self.on_dynamic_pad)
        self._volume = gst.ElementFactory.make('volume', 'volume')
        self._convert = gst.ElementFactory.make('audioconvert', 'convert')
        self._pan = gst.ElementFactory.make('audiopanorama', 'pan')
        self._audio_sink = gst.ElementFactory.make('autoaudiosink', 'audio_sink')

        # Ensure all elements were created successfully.
        if (not self._pipeline
            or not self._audio_source
            or not self._decode
            or not self._pan
            or not self._convert
            or not self._audio_sink
            or not self._volume):
            print('Not all elements could be created.')
            exit(-1)

        # Add our elements to the pipeline.
        self._pipeline.add(self._audio_source)
        self._pipeline.add(self._decode)
        self._pipeline.add(self._volume)
        self._pipeline.add(self._convert)
        self._pipeline.add(self._pan)
        self._pipeline.add(self._audio_sink)

        # Link our elements together.
        self._audio_source.link(self._decode)

        # self._decode.link(self._volume)
        self._volume.link(self._convert)
        self._convert.link(self._pan)
        self._pan.link(self._audio_sink)

        self._volume_control_source = GstController.InterpolationControlSource.new()
        self._volume_control_source.set_property('mode', GstController.InterpolationMode.LINEAR)
        self._volume_control_binding = GstController.DirectControlBinding.new(self._volume, 'volume',
                                                                              self._volume_control_source)
        self._volume.add_control_binding(self._volume_control_binding)

        self._pan_control_source = GstController.InterpolationControlSource.new()
        self._pan_control_source.set_property('mode', GstController.InterpolationMode.LINEAR)
        self._pan_control_binding = GstController.DirectControlBinding.new(self._pan, 'panorama',
                                                                           self._pan_control_source)
        self._pan.add_control_binding(self._pan_control_binding)

    def set_source(self, source):
        self._audio_source.set_property('location', source)

    def play(self):
        self._pipeline.set_state(gst.State.PLAYING)

    def stop(self):
        self._pipeline.set_state(gst.State.READY)

    def fade_out(self):
        current = self._pipeline.get_clock().get_time()
        self._volume_control_source.set(current, 0.15)
        self._volume_control_source.set(current + 8 * gst.SECOND, 0.0)

    def pan(self, start, end, duration):
        current = self._pipeline.get_clock().get_time()
        self._pan_control_source.set(current, start)
        self._pan_control_source.set(current + duration * gst.SECOND, end)

    def unused_bus_code(self):
        # Wait until error or EOS.
        bus = self._pipeline.get_bus()
        msg = bus.timed_pop_filtered(gst.CLOCK_TIME_NONE, gst.MessageType.ERROR | gst.MessageType.EOS)
        print(msg)

        # Free resources.
        self._pipeline.set_state(gst.State.NULL)

    def on_dynamic_pad(self, element, pad):
        print("OnDynamicPad Called!")
        pad.link(self._volume.get_static_pad("sink"))
        print(self.get_duration())

    def get_duration(self):
        success, duration = self._decode.query_duration(gst.Format.TIME)
        if not success:
            duration = -1
        else:
            duration /= gst.SECOND
        return duration

    def get_position(self):
        success, position = self._decode.query_position(gst.Format.TIME)
        if not success:
            position = -1
        else:
            position /= gst.SECOND
        return position


if __name__ == "__main__":
    print("File 1.mp3, duration",getAudioLength("1.mp3"))
    p1 = Player()
    p2 = Player()
    p1.set_source("1.mp3")
    p2.set_source("chime.wav")
    p1.play()
    time.sleep(15)
    print("position", p1.get_position(), "duration", p1.get_duration())
    print("Pan to -1")
    p1.pan(0.5, 0, 5)
    time.sleep(5)
    print("Pan to 1")
    p1.pan(0, 1, 5)
    p2.play()
    time.sleep(5)
    print("Pan to 0")
    p1.pan(1, 0.5, 5)
    time.sleep(5)
    print("Fade out")
    p1.fade_out()
    time.sleep(9)
    getAudioLength("1.mp3")

