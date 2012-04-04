#    AethBot
#    Copyright (C) 2011, 2012 Michael Babich
#
#    This program is free software. It comes without any warranty, to
#    the extent permitted by applicable law. You can redistribute it
#    and/or modify it under the terms of the Do What The Fuck You Want
#    To Public License, Version 2, as published by Sam Hocevar. See
#    http://sam.zoy.org/wtfpl/COPYING for more details.


# Python modules.
import irclib, yaml

# Handles the AethBot modules.
from modules import core

# Handles the actual IRC bot, inherited from ircbot.py from the irclib package.
# This file contains the bare minimum necessary to get it to run. The fancier
# features are handled in individual modules, centered around core.py, so that
# they can be reloaded while the bot is still running.
class AethBot(irclib.SimpleIRCClient):
    def __init__(self, config):
        # Instantiates from ircbot.py
        bot = config["Connection"]

        irclib.SimpleIRCClient.__init__(self)
        self.connect(bot["server"], bot["port"], bot["nick"], bot["pw"], bot["name"])

        # Sets up the core.py main bot code.
        self.ops   = bot["ops"]
        self.chans = bot["chans"]
        self.about = bot["about"]

        self.core   = core.BotCore(self, self.ops, self.chans, self.about)
        irclib.SimpleIRCClient.start(self)

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

    def on_ctcp(self, c, e):
        self.core.handle_event(c, e)

    def get_version(self):
        return self.core.version

    # Reloads the core.py if the new code isn't buggy.
    def reload_core(self, c, e, target):
        try:
            reload(core)
            self.core = core.BotCore(self, self.ops, self.chans, self.about)
            self.core.outmsg(c, target, "All modules have been reloaded.")

        except:
            self.core.outmsg(c, target, "Error in reloading modules.")

# Runs the AethBot application.
class BotRun:
    def __init__(self):
        config = self.loadConfig()

        self.bot = AethBot(config)

    def loadConfig(self):
        # Loads the defaults.
        default_file = open('default.yml', 'r')
        default      = yaml.load(default_file)
        default_file.close()         

        # Loads the custom options, if they exist.
        try:
            config_file  = open('config.yml', 'r')
            config       = yaml.load(config_file)
            config_file.close()

        except IOError:
            config = default

        # Anything missing from the config file is overriden by the defaults.
        for main_section in default:
            if main_section not in config:
                config[main_section] = default[main_section]
            else:
                for subsection in default[main_section]:
                    if subsection not in config[main_section]:
                        config[main_section][subsection] = default[main_section][subsection]

        return config

# Launches the bot.
def main():
    irc = BotRun()

main()
