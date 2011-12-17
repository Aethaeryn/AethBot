#    AethBot Events Module
#    Copyright (C) 2011 Michael Babich
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


# python-irclib modules.
import irclib

class Event():
    def __init__(self, core, c, e):
        # Common information across all event types.
        self.core = core
        self.c    = c
        self.e    = e
        self.nick = irclib.nm_to_n(self.e.source())
        self.chan = self.e.target()

        # Runs the method that matches the event type name.
        getattr(self, self.e.eventtype())()

    # Logs and handles private notices.
    def privnotice(self):
        msg = self.e.arguments()[0]
        me  = self.c.get_nickname()
        self.core.record("-%s- %s" % (self.nick, msg))

        identified_msg = "You are now identified for \x02%s\x02." % me

        if self.nick == "NickServ" and msg == identified_msg:
            self.core.identified(self.c)

    # Logs and handles public notices.
    def pubnotice(self):
        msg = self.e.arguments()[0]

        self.core.record("-%s:%s- %s" % (self.nick, self.chan, msg))

    # Logs and handles channel joins.
    def join(self):
        host = irclib.nm_to_uh(self.e.source())

        self.core.record("-!- %s [%s] has joined %s" % (self.nick, host, self.chan))

    # Logs and handles channel parts.
    def part(self):
        host = irclib.nm_to_uh(self.e.source())
        msg  = ""

        if len(self.e.arguments()) == 1:
            msg = self.e.arguments()[0]

        self.core.record("-!- %s [%s] has left %s [%s]" % (self.nick, host, self.chan, msg))

    # Logs and handles channel quits.
    def quit(self):
        host = irclib.nm_to_uh(self.e.source())
        msg  = self.e.arguments()[0]

        self.core.record("-!- %s [%s] has quit [%s]" % (self.nick, host, msg))

    # Logs and handles kicks.
    def kick(self):
        target = self.e.arguments()[0]
        msg    = self.e.arguments()[1]

        self.core.record("-!- %s was kicked from %s by %s [%s]" % (target, self.chan, self.nick, msg))

    # Logs and handles channel modes.
    def mode(self):
        arg1 = self.e.arguments()[0]
        arg2 = ""

        if len(self.e.arguments()) == 2:
            arg2 = " " + self.e.arguments()[1]

        self.core.record("-!- mode/%s [%s%s] by %s" % (self.chan, arg1, arg2, self.nick))
