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


# python-irclib modules.
import irclib

class Command():
    def __init__(self, core, c, e):
        # Reads in all the relevant information for the commands.
        self.core     = core
        self.c        = c
        self.e        = e

        self.msg      = e.arguments()[0]
        self.msg_args = self.msg.split()
        self.sender   = irclib.nm_to_n(e.source())
        self.chan     = e.target()

        # If the target of the message has the bot's name, it was a query.
        if irclib.nm_to_n(self.chan) == c.get_nickname():
            self.chan = self.sender

        # Outputs the messages.
        core.record("(%s) <%s> %s" % (self.chan, self.sender, self.msg))

        # Handles the commands.
        if self.msg_args[0] == "," and len(self.msg_args) > 1 and self.sender in core.operators:
            self.msg_args[1] = self.msg_args[1].lower()

            # ** MESSGING COMMANDS ** #
            # Sends a message in the current channel or query.
            # syntax: , msg <message>
            if self.msg_args[1] == "msg":
                core.outmsg(c, self.chan, self.msg[6:])

            # Sends a message to a given destination.
            # syntax: , <destination> msg <message>
            elif len(self.msg_args) > 2 and self.msg_args[2] == "msg":
                core.outmsg(c, self.msg_args[1], self.msg[7 + len(self.msg_args[1]):])

            # ** BASIC COMMANDS ** #
            elif self.msg_args[1] == "time":
                time = core.time()

                core.outmsg(c, self.chan, "My current local time is %s" % time)

            # ** CONNECTION AND SYSTEM COMMANDS ** #
            # Orders the bot to join a channel.
            elif self.msg_args[1] == "join":
                if len(msg_args) == 3:
                    core.join(c, self.msg_args[2])

                else:
                    core.outmsg(c, self.chan, "I need to be given a channel to join!")

            # Orders the bot to part a channel.
            elif self.msg_args[1] == "part":
                if len(msg_args) == 3:
                    core.part(c, self.msg_args[2])

                else:
                    core.outmsg(c, self.chan, "I need to be given a channel to leave!")

            #### fixme: This breaks sometimes.
            # Reloads this module without restarting the bot.
            # syntax: , reload
            elif self.msg_args[1] == "reload":
                core.reload()

            # Orders the bot to disconnect from the server.
            # It will automatically attempt to reconnect.
            # syntax: , reconnect
            elif self.msg_args[1] == "reconnect":
                core.bot.disconnect()

            #### fixme: No quit message is displayed.
            # Orders the bot to quit from IRC.
            # syntax: , quit
            elif self.msg_args[1] == "quit":
                core.bot.die(core.version())

            # The proper prefix without a recognized command gets an error.
            else:
                core.outmsg(c, self.chan, "I'm sorry, I don't know that command.")

        # Anything with this prefix is handled in botmath.py
        elif self.msg_args[0] == "~":
            core.outmsg(c, self.chan, core.math.command(msg[2:]))

        # Using the restricted prefix without being an operator gives an error.
        elif self.msg_args[0] == ",":
            core.outmsg(c, self.chan, "I'm sorry, you are not authorized.")

