#    AethBot Core Module
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


# Default Python modules.
import time, string

# python-irclib modules.
import irclib

# Other modules in this folder.
import botmath, commands, events

# Handles the core module to the IRC bot and calls all other custom modules.
class BotCore:
    def __init__(self, bot, ops, chans, about):
        self.operators = set(ops)
        self.bot       = bot
        self.math      = botmath.Math("postfix")
        self.channels  = chans
        self.about     = about

    # This is the default behavior for when identified.
    def identified(self, c):
        for channel in self.channels:
            self.join(c, channel)

    # This is the default return message when VERSION is requested via CTCP.
    def version(self):
        return self.about

    # Joins a channel.
    def join(self, c, chan):
        c.join(chan)
        date = self.date()
        time = self.time()

        self.record("Joined channel %s on %s at %s" % (chan, date, time))

    # Parts a channel.
    def part(self, c, chan, msg=''):
        c.part(chan, msg)
        date = self.date()
        time = self.time()

        self.record("Left channel %s on %s at %s" % (chan, date, time))

    # Sends and records a message to a user or channel.
    def outmsg(self, server, target, msg):
        self.record("(%s) <%s> %s" % (target, server.get_nickname(), msg))
        server.privmsg(target, msg)

    # Obtains the time for logging purposes.
    def time(self):
        return time.strftime("%H:%M:%S")

    # Obtains the date for logging purposes.
    def date(self):
        return time.strftime("%Y %m %d")

    # Reloads all AethBot modules.
    def reload(self):
        reload(botmath)
        reload(commands)
        reload(events)
        self.bot.reload_core(self.cmd.c, self.cmd.e, self.cmd.chan)

    # Records a line in the log.
    def record(self, message):
        # Timestamp logs are the default behavior.
        message = "%s %s" % (self.time(), message)

        # File i/o.
        logfile = open('irc.log', 'a')
        logfile.writelines(message + "\n")
        logfile.close()

    # Every notable and recorded IRC event except for messsages is handled here.
    # The event recording is designed to mimic the default irssi style.
    def handle_event(self, c, e):
        self.ev = events.Event(self, c, e)

    # Because messages can be commands, they're handled specially.
    def commands(self, c, e):
        self.cmd = commands.Command(self, c, e)
