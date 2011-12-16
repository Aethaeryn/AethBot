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
import botmath

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
        # Common information across all event types.
        nick = irclib.nm_to_n(e.source())
        chan = e.target()

        # Logs and handles private notices.
        if e.eventtype() == "privnotice":
            msg    = e.arguments()[0]

            self.record("-" + nick + "- " + msg)

            if nick == "NickServ" and msg == "You are now identified for \x02" + c.get_nickname() + "\x02.":
                self.identified(c)

        # Logs and handles public notices.
        elif e.eventtype() == "pubnotice":
            msg  = e.arguments()[0]
            
            self.record("-" + nick + ":" + chan + "- " + msg)

        # Logs and handles channel joins.
        elif e.eventtype() == "join":
            host = irclib.nm_to_uh(e.source())

            self.record("-!- " + nick + " [" + host + "] has joined " + chan)

        # Logs and handles channel parts.
        elif e.eventtype() == "part":
            host = irclib.nm_to_uh(e.source())
            msg  = ""

            if len(e.arguments()) == 1:
                msg = e.arguments()[0]

            self.record("-!- " + nick + " [" + host + "] has left " +
                        chan + " [" + msg + "]")

        # Logs and handles channel quits.
        elif e.eventtype() == "quit":
            host = irclib.nm_to_uh(e.source())
            msg  = e.arguments()[0]

            self.record("-!- " + nick + " [" + host + "] has quit [" + msg + "]")

        # Logs and handles channel kicks.
        elif e.eventtype() == "kick":
            target = e.arguments()[0]
            msg    = e.arguments()[1]

            self.record("-!- " + target + " was kicked from " + chan +
                        " by " + nick + " [" + msg + "]")

        # Logs and handles channel modes.
        elif e.eventtype() == "mode":
            arg1 = e.arguments()[0]
            arg2 = ""

            if len(e.arguments()) == 2:
                arg2 = " " + e.arguments()[1]

            self.record("-!- mode/" + chan + " [" + arg1 + arg2 + "] by " + nick)

    # Because messages can be commands, they're handled specially.
    def commands(self, c, e):
        # Reads in all the relevant information for the commands.
        msg      = e.arguments()[0]
        msg_args = msg.split()
        sender   = irclib.nm_to_n(e.source())
        chan     = e.target()

        # If the target of the message has the bot's name, it was a query.
        if irclib.nm_to_n(chan) == c.get_nickname():
            chan = sender

        # Outputs the messages.
        self.record("(" + chan + ") <" + sender + "> " + msg)

        # Handles the commands.
        if msg_args[0] == "," and len(msg_args) > 1 and sender in self.operators:
            msg_args[1] = msg_args[1].lower()

            # ** MESSGING COMMANDS ** #
            # Sends a message in the current channel or query.
            # syntax: , msg <message>
            if msg_args[1] == "msg":
                self.outmsg(c, chan, msg[6:])

            # Sends a message to a given destination.
            # syntax: , <destination> msg <message>
            elif len(msg_args) > 2 and msg_args[2] == "msg":
                self.outmsg(c, msg_args[1], msg[7 + len(msg_args[1]):])

            # ** BASIC COMMANDS ** #
            elif msg_args[1] == "time":
                self.outmsg(c, chan, "My current local time is " + self.logTime())

            # ** CONNECTION AND SYSTEM COMMANDS ** #
            # Orders the bot to join a channel.
            elif msg_args[1] == "join":
                self.join(c, msg_args[2])

            # Orders the bot to part a channel.
            elif msg_args[1] == "part":
                self.part(c, msg_args[2])

            # Reloads this module without restarting the bot.
            # syntax: , reload
            elif msg_args[1] == "reload":
                reload(botmath)
                self.bot.reload_core(c, e, chan)

            # Orders the bot to disconnect from the server.
            # It will automatically attempt to reconnect.
            # syntax: , reconnect
            elif msg_args[1] == "reconnect":
                self.bot.disconnect()

            # Orders the bot to quit from IRC.
            # syntax: , quit
            elif msg_args[1] == "quit":
                self.bot.die(self.version())

            # The proper prefix without a recognized command gets an error.
            else:
                self.outmsg(c, chan, "I'm sorry, I don't know that command.")

        # Anything with this prefix is handled in botmath.py
        elif msg_args[0] == "~":
            self.outmsg(c, chan, self.math.command(msg[2:]))

        # Using the restricted prefix without being an operator gives an error.
        elif msg_args[0] == ",":
            self.outmsg(c, chan, "I'm sorry, you are not authorized.")
