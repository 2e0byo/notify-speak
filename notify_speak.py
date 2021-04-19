import html
import re
from subprocess import run

import dbus
import gi.repository.GLib
from dbus.mainloop.glib import DBusGMainLoop


def speak(msg: str):
    """Call text-to-speak on a particular message."""
    run(["mimic", "-t", msg])


def speak_notifications(bus, msg):
    summary = msg.get_args_list()[3]
    msg = msg.get_args_list()[4]
    if not msg:
        msg = summary
    msg = html.unescape(msg)
    # remove urls as they're annoying
    msg = " ".join(x for x in msg.split(" ") if not re.match("https*://", x))
    speak(msg[:80])


def debug_notifications(bus, msg):
    """Show detail on notifications for testing."""
    from devtools import debug

    debug(msg.get_args_list())


DBusGMainLoop(set_as_default=True)

bus = dbus.SessionBus()
bus.add_match_string_non_blocking(
    "eavesdrop=true, interface='org.freedesktop.Notifications', member='Notify'"
)
bus.add_message_filter(speak_notifications)

mainloop = gi.repository.GLib.MainLoop()
mainloop.run()
