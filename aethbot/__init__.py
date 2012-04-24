# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php

from aethbot import core
from irclib import SimpleIRCClient

# Handles the actual IRC bot, inherited from ircbot.py from the irclib package.
# This file contains the bare minimum necessary to get it to run. The fancier
# features are handled in individual modules, centered around core.py, so that
# they can be reloaded while the bot is still running.
class AethBot(SimpleIRCClient):
    def __init__(self, config):
        # Instantiates from ircbot.py
        bot = config["Connection"]

        SimpleIRCClient.__init__(self)
        self.connect(bot["server"], bot["port"], bot["nick"], bot["pw"], bot["name"])

        # Sets up the core.py main bot code.
        self.ops   = bot["ops"]
        self.chans = bot["chans"]
        self.about = bot["about"]

        self.core   = core.BotCore(self, self.ops, self.chans, self.about)

    def start(self):
        SimpleIRCClient.start(self)

    # ** Reads various events, sending them to core.py to be handled. ** #
    def on_privmsg(self, connection, event):
        self.core.commands(connection, event)

    def on_pubmsg(self, connection, event):
        self.core.commands(connection, event)

    def on_privnotice(self, connection, event):
        self.core.handle_event(connection, event)

    def on_pubnotice(self, connection, event):
        self.core.handle_event(connection, event)

    def on_join(self, connection, event):
        self.core.handle_event(connection, event)

    def on_part(self, connection, event):
        self.core.handle_event(connection, event)

    def on_quit(self, connection, event):
        self.core.handle_event(connection, event)

    def on_kick(self, connection, event):
        self.core.handle_event(connection, event)

    def on_mode(self, connection, event):
        self.core.handle_event(connection, event)

    def on_ctcp(self, connection, event):
        self.core.handle_event(connection, event)

    def get_version(self):
        return self.core.version

    # Reloads the core.py if the new code isn't buggy.
    def reload_core(self, connection, target):
        try:
            reload(core)
            self.core = core.BotCore(self, self.ops, self.chans, self.about)
            self.core.outmsg(connection, target, "All modules have been reloaded.")

        except:
            self.core.outmsg(connection, target, "Error in reloading modules.")
