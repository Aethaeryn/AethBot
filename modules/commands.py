#    AethBot Commands Module
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


# Default Python modules
import string

# python-irclib modules.
import irclib

# Handles all messages. The ones that are commands are then treated appropriately.
class Command():
    def __init__(self, core, c, e):
        # Reads in all the relevant information for the commands.
        self.core     = core
        self.c        = c
        self.e        = e
        self.me       = self.c.get_nickname()

        self.msg      = self.e.arguments()[0]
        self.msg_args = self.msg.split()
        self.sender   = irclib.nm_to_n(self.e.source())
        self.chan     = self.e.target()

        # If the target of the message has the bot's name, it was a query.
        if irclib.nm_to_n(self.chan) == self.c.get_nickname():
            self.chan = self.sender

        # Records the messages themselves.
        self.core.record("<%s> %s" % (self.sender, self.msg), self.chan)

        # Skips over blank lines so it doesn't crash.
        if len(self.msg_args) == 0:
            pass

        # Messaging the bot's name directly will cause the bot to check for commands.
        elif (self.msg_args[0] == self.me + ":" and self.chan != self.sender):
            # We want the bot to ignore its name when handling the commands.
            self.msg_args.pop(0)
            self.commands()

        # Querying it will work, too.
        elif self.chan == self.sender:
            self.commands()

    # Determines what kind of command it is and sends it to the right location.
    def commands(self):
        self.calc_words = set(["~", "calc", "math"])

        # Handles the core commands.
        if self.msg_args[0] == "," and len(self.msg_args) > 1 and self.sender in self.core.operators:
            self.msg_args.pop(0)
            self.msg_args[0] = self.msg_args[0].lower()

            self.core_commands()
 
        # Hands the math over to calc.py
        elif self.msg_args[0] in self.calc_words:
            pos = string.find(self.msg, self.msg_args[0])
            self.speak(self.core.math.command(self.msg[(pos + len(self.msg_args[0]) + 1):]))

        # Using the restricted prefix without being an operator gives an error.
        elif self.msg_args[0] == ",":
            self.speak("I'm sorry, you are not authorized.")

        else:
            self.public_commands()

    # These are harmless, public commands that anyone can use.
    def public_commands(self):
        # Displays a help string.
        if self.msg_args[0] == "help":
            self.speak("I am AethBot, a basic IRC bot created in Python by Aethaeryn. For commands you can use, say 'commands'.")

        # Lists public commands.
        elif self.msg_args[0] == "commands":
            commands = "The following public commands are available: help commands time version ops"

            for word in self.calc_words:
                commands += " %s" % word

            self.speak(commands)

        # Prints the current operators.
        elif self.msg_args[0] == "ops":
            op_msg = "My current operators are:"

            for op in self.core.operators:
                op_msg += " %s" % op

            self.speak(op_msg)

        # Prints the version string.
        elif self.msg_args[0] == "version":
            self.speak(self.core.version)

        # Displays the current local time.
        elif self.msg_args[0] == "time":
            time = self.core.time()

            self.speak("My current local time is %s" % time)

    # The main commands, not part of another module, are handled here.
    def core_commands(self):
        # Sends a message in the current channel or query.
        # syntax: , msg <message>
        if self.msg_args[0] == "msg":
            pos = string.find(self.msg, self.msg_args[0])
            self.speak(self.msg[(pos + len(self.msg_args[0]) + 1):])

        # Sends a message to a given destination.
        # syntax: , <destination> msg <message>
        elif len(self.msg_args) > 2 and self.msg_args[1] == "msg":
            pos = string.find(self.msg, self.msg_args[1])
            self.core.outmsg(self.c, self.msg_args[0], self.msg[(pos + len(self.msg_args[1]) + 1):])

        # Orders the bot to join a channel.
        elif self.msg_args[0] == "join":
            if len(self.msg_args) == 3:
                self.core.join(self.c, self.msg_args[1])

            else:
                self.speak("I need to be given a channel to join!")

        # Orders the bot to part a channel.
        elif self.msg_args[0] == "part":
            if len(self.msg_args) == 3:
                self.core.part(self.c, self.msg_args[1])

            else:
                self.speak("I need to be given a channel to leave!")

        # Reloads this module without restarting the bot.
        # syntax: , reload
        elif self.msg_args[0] == "reload":
            self.core.reload()

        # Orders the bot to disconnect from the server.
        # It will automatically attempt to reconnect.
        # syntax: , reconnect
        elif self.msg_args[0] == "reconnect":
            self.core.bot.disconnect()

        # Orders the bot to quit from IRC.
        # syntax: , quit
        elif self.msg_args[0] == "quit":
            self.core.bot.die(self.core.version)

        # The proper prefix without a recognized command gets an error.
        else:
            self.speak("I'm sorry, I don't know that command.")

    # This is how the bot speaks.
    def speak(self, msg):
        self.core.outmsg(self.c, self.chan, msg)
