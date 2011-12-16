#    AethBot
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
import sys, collections, time

# python-irclib modules.
import irclib, ircbot

# Handles the AethBot modules.
from modules import core

# Handles the actual IRC bot, inherited from ircbot.py from the irclib package.
# This file contains the bare minimum necessary to get it to run. The fancier
# features are handled in individual modules, centered around core.py, so that
# they can be reloaded while the bot is still running.
class AethBot(ircbot.SingleServerIRCBot):
    def __init__(self,
                 nick   = 'AethBot',
                 name   = 'AethBot',
                 server = 'irc.freenode.net',
                 port   = 6667,
                 pw     = '',
                 args   = ''):
        # Instantiates from ircbot.py
        ircbot.SingleServerIRCBot.__init__(self, [(server, port, pw)], nick, name)

        # Sets up the core.py main bot code.
        self.args   = args
        self.core   = core.BotCore(self.args, self)

    # ** Reads various events, sending them to core.py to be handled. ** #
    def on_privmsg(self, c, e):
        self.core.commands(c, e)

    def on_pubmsg(self, c, e):
        self.core.commands(c, e)

    def on_privnotice(self, c, e):
        self.core.handle_event(c, e)

    def on_pubnotice(self, c, e):
        self.core.handle_event(c, e)

    def on_join(self, c, e):
        self.core.handle_event(c, e)

    def on_part(self, c, e):
        self.core.handle_event(c, e)

    def on_quit(self, c, e):
        self.core.handle_event(c, e)

    def on_kick(self, c, e):
        self.core.handle_event(c, e)

    def on_mode(self, c, e):
        self.core.handle_event(c, e)

    def get_version(self):
        return self.core.version

    # Reloads the core.py if the new code isn't buggy.
    def reload_core(self, c, e, target):
        try:
            reload(core)
            self.core = core.BotCore(self.args, self)
            self.core.outmsg(c, target, "All modules have been reloaded.")
        except:
            self.core.outmsg(c, target, "Error in reloading modules.")

# Runs the AethBot application.
class BotRun:
    def __init__(self, args):
        self.get_config()

        # Creates the bot with the command line and config preferences.
        self.bot = AethBot(nick = self.config['nick'],
                           name = self.config['name'],
                           pw   = self.config['pw'],
                           args = args)

        self.bot.start()

    # Loads the nick and password from the configuration file into a dictionary.
    # The only elements it recognizes are 'nick', 'name' (optional), and 'pw'.
    def get_config(self):
        self.config = {}

        config_file = open("config", "r")

        for line in config_file:
            line = line.split("=")
            self.config[line[0].strip()] = line[1].strip()

        if 'name' not in self.config:
            self.config['name'] = self.config['nick']

# Launches the bot.
def main():
    irc = BotRun(sys.argv)

main()
