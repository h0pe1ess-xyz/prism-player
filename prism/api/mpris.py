import pydbus
from gi.repository import GLib
import threading
import os
import re

import collections

# We will export commands back to main
mpris_command_queue = collections.deque()

class PrismMprisPlayer:
    dbus = """<node>
      <interface name="org.mpris.MediaPlayer2">
        <property name="CanQuit" type="b" access="read"/>
        <property name="CanRaise" type="b" access="read"/>
        <property name="HasTrackList" type="b" access="read"/>
        <property name="Identity" type="s" access="read"/>
        <property name="DesktopEntry" type="s" access="read"/>
        <property name="SupportedUriSchemes" type="as" access="read"/>
        <property name="SupportedMimeTypes" type="as" access="read"/>
        <method name="Quit"/>
        <method name="Raise"/>
      </interface>
      <interface name="org.mpris.MediaPlayer2.Player">
        <property name="PlaybackStatus" type="s" access="read"/>
        <property name="LoopStatus" type="s" access="readwrite"/>
        <property name="Rate" type="d" access="readwrite"/>
        <property name="Shuffle" type="b" access="readwrite"/>
        <property name="Metadata" type="a{sv}" access="read"/>
        <property name="Volume" type="d" access="readwrite"/>
        <property name="Position" type="x" access="read"/>
        <property name="MinimumRate" type="d" access="read"/>
        <property name="MaximumRate" type="d" access="read"/>
        <property name="CanGoNext" type="b" access="read"/>
        <property name="CanGoPrevious" type="b" access="read"/>
        <property name="CanPlay" type="b" access="read"/>
        <property name="CanPause" type="b" access="read"/>
        <property name="CanSeek" type="b" access="read"/>
        <property name="CanControl" type="b" access="read"/>
        <method name="Next"/>
        <method name="Previous"/>
        <method name="Pause"/>
        <method name="PlayPause"/>
        <method name="Stop"/>
        <method name="Play"/>
        <method name="Seek">
          <arg direction="in" name="Offset" type="x"/>
        </method>
        <method name="SetPosition">
          <arg direction="in" name="TrackId" type="o"/>
          <arg direction="in" name="Position" type="x"/>
        </method>
        <method name="OpenUri">
          <arg direction="in" name="Uri" type="s"/>
        </method>
      </interface>
    </node>"""

    def __init__(self, get_state_func):
        self.get_state_func = get_state_func

    # --- org.mpris.MediaPlayer2 ---
    @property
    def CanQuit(self): return False
    @property
    def CanRaise(self): return False
    @property
    def HasTrackList(self): return False
    @property
    def Identity(self): return "Prism Player"
    @property
    def DesktopEntry(self): return "prismplayer"
    @property
    def SupportedUriSchemes(self): return []
    @property
    def SupportedMimeTypes(self): return []
    def Quit(self): pass
    def Raise(self): pass

    # --- org.mpris.MediaPlayer2.Player ---
    @property
    def PlaybackStatus(self):
        state = self.get_state_func()
        if not state.get("is_playing"): return "Stopped"
        return "Paused" if state.get("is_paused") else "Playing"

    @property
    def LoopStatus(self): return "None"
    @LoopStatus.setter
    def LoopStatus(self, val): pass

    @property
    def Rate(self): return 1.0
    @Rate.setter
    def Rate(self, val): pass

    @property
    def Shuffle(self): return False
    @Shuffle.setter
    def Shuffle(self, val): pass

    @property
    def Metadata(self):
        state = self.get_state_func()
        if not state.get("is_playing"):
            return {
                "mpris:trackid": GLib.Variant('o', "/org/mpris/MediaPlayer2/TrackList/NoTrack"),
                "xesam:title": GLib.Variant('s', "No Track Loaded")
            }
        
        safe_vid = re.sub(r'[^a-zA-Z0-9_]', '_', str(state.get("video_id", "0")))
        return {
            "mpris:trackid": GLib.Variant('o', f"/org/mpris/MediaPlayer2/TrackList/{safe_vid}"),
            "xesam:title": GLib.Variant('s', state.get("title", "Unknown")),
            "xesam:artist": GLib.Variant('as', [state.get("artist", "Unknown")]),
            "mpris:length": GLib.Variant('x', int(state.get("duration", 0) * 1000000))
        }

    @property
    def Volume(self): return 1.0
    @Volume.setter
    def Volume(self, val): pass

    @property
    def Position(self):
        return int(self.get_state_func().get("elapsed", 0) * 1000000)

    @property
    def MinimumRate(self): return 1.0
    @property
    def MaximumRate(self): return 1.0
    @property
    def CanGoNext(self): return True
    @property
    def CanGoPrevious(self): return True
    @property
    def CanPlay(self): return True
    @property
    def CanPause(self): return True
    @property
    def CanSeek(self): return False
    @property
    def CanControl(self): return True

    # Methods
    def Next(self): mpris_command_queue.append("next")
    def Previous(self): mpris_command_queue.append("previous")
    def Pause(self): mpris_command_queue.append("pause")
    def PlayPause(self): mpris_command_queue.append("play")
    def Stop(self): mpris_command_queue.append("pause")
    def Play(self): mpris_command_queue.append("play")
    def Seek(self, offset): pass
    def SetPosition(self, trackId, pos): pass
    def OpenUri(self, uri): pass


def start_mpris_server(get_state_func):
    try:
        bus = pydbus.SessionBus()
        player = PrismMprisPlayer(get_state_func)
        bus_name = f"org.mpris.MediaPlayer2.PrismPlayer.instance{os.getpid()}"
        bus.publish(bus_name, ("/org/mpris/MediaPlayer2", player))
        loop = GLib.MainLoop()
        loop.run()
    except Exception as e:
        import traceback
        with open("mpris_error.log", "w") as f:
            f.write(traceback.format_exc())

def run_mpris_background(get_state_func):
    t = threading.Thread(target=start_mpris_server, args=(get_state_func,), daemon=True)
    t.start()
