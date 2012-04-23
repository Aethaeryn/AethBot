# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php

from aethbot import AethBot
import yaml

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

def main():
    irc = BotRun()

if __name__ == '__main__':
    main()
