# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php

import irclib

class Event():
    def __init__(self, core, connection, event):
        # Common information across all event types.
        self.core       = core
        self.connection = connection
        self.event      = event
        self.nick       = irclib.nm_to_n(self.event.source())
        self.chan       = self.event.target()

        # Runs the method that matches the event type name.
        getattr(self, self.event.eventtype())()

    # Logs and handles private notices.
    def privnotice(self):
        msg = self.event.arguments()[0]
        me  = self.connection.get_nickname()
        self.core.record("-%s- %s" % (self.nick, msg), self.chan)

        identified_msg = "You are now identified for \x02%s\x02." % me

        if self.nick == "NickServ" and msg == identified_msg:
            self.core.identified(self.connection)

    # Logs and handles public notices.
    def pubnotice(self):
        msg = self.event.arguments()[0]

        self.core.record("-%s:%s- %s" % (self.nick, self.chan, msg), self.chan)

    # Logs and handles channel joins.
    def join(self):
        host = irclib.nm_to_uh(self.event.source())

        self.core.record("-!- %s [%s] has joined %s" % (self.nick, host, self.chan), self.chan)

    # Logs and handles channel parts.
    def part(self):
        host = irclib.nm_to_uh(self.event.source())
        msg  = ""

        if len(self.event.arguments()) == 1:
            msg = self.event.arguments()[0]

        self.core.record("-!- %s [%s] has left %s [%s]" % (self.nick, host, self.chan, msg), self.chan)

    # Logs and handles channel quits.
    def quit(self):
        host = irclib.nm_to_uh(self.event.source())
        msg  = self.event.arguments()[0]

        self.core.record("-!- %s [%s] has quit [%s]" % (self.nick, host, msg), self.chan)

    # Logs and handles kicks.
    def kick(self):
        target = self.event.arguments()[0]
        msg    = self.event.arguments()[1]

        self.core.record("-!- %s was kicked from %s by %s [%s]" % (target, self.chan, self.nick, msg), self.chan)

    # Logs and handles channel modes.
    def mode(self):
        arg1 = self.event.arguments()[0]
        arg2 = ""

        if len(self.event.arguments()) == 2:
            arg2 = " " + self.event.arguments()[1]

        self.core.record("-!- mode/%s [%s%s] by %s" % (self.chan, arg1, arg2, self.nick), self.chan)

    # Handles ctcp.
    def ctcp(self):
        arg = self.event.arguments()

        if arg[0] == "ACTION":
            msg = arg[1]

            me_log = " * %s %s"  % (self.nick, msg)

            if self.chan != "AethBot":
                self.core.record(me_log, self.chan)

            else:
                self.core.record(me_log, self.nick)
