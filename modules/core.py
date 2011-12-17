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
    def __init__(self, args, bot):
        self.operators = set(["Aethaeryn", "Aeth", "MikeJB"]) #### TODO: Put in config.
        self.bot       = bot
        self.math      = botmath.Math("postfix")

        self.args      = args # Currently does nothing.

    # This is the default behavior for when identified.
    def identified(self, c):
        self.join(c, "##aeth") #### TODO: Put in config.

    # This is the default return message when VERSION is requested via CTCP.
    def version(self):
        return "AethBot Alpha 1, based on Python's irclib" #### TODO: Put in config.

    #### TODO: Make sure only successful attempts are logged!
    def join(self, c, chan):
        c.join(chan)
        self.record("Joined channel " + chan + " on " + time.strftime("%Y %m %d") + " at " + self.logTime())

    #### TODO: Make sure only successful attempts are logged!
    def part(self, c, chan, msg=''):
        c.part(chan, msg)
        self.record("Left channel " + chan + " on " + time.strftime("%Y %m %d") + " at " + self.logTime() + " [" + msg + "]")

    # Sends and records a message to a user or channel.
    def outmsg(self, server, target, msg):
        self.record("(" + target + ") <" + server.get_nickname() + "> " + msg)
        server.privmsg(target, msg)

    # Obtains the time for logging purposes.
    def logTime(self):
        return time.strftime("%H:%M:%S")

    # Reloads all AethBot modules.
    def reload(self):
        reload(botmath)
        reload(commands)
        reload(events)
        self.bot.reload_core(c, e, cmd.chan)

    # Records a line in the log.
    def record(self, message):
        # Timestamp logs are the default behavior.
        message = self.logTime() + " " + message

        # File i/o.
        logfile = open('irc.log', 'a')
        logfile.writelines(message + "\n")
        logfile.close()

    # Every notable and recorded IRC event except for messsages is handled here.
    # The event recording is designed to mimic the default irssi style.
    def handle_event(self, c, e):
        ev = events.Event(self, c, e)

    # Because messages can be commands, they're handled specially.
    def commands(self, c, e):
        cmd = commands.Command(self, c, e)
