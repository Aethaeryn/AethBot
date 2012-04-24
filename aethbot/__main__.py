# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php

'''This directly launches AethBot and reads in configuration values
from default.yml or config.yml if the latter exists.

To run this file, use the command ``python -m aethbot``
'''
from aethbot import AethBot
from yaml import load

def load_config():
    '''This turns the YAML file(s) into a configuration dictionary
    that AethBot recognizes. First, it loads the defaults. Then it
    tries to read config.yml and update the Connection entry,
    overriding any defaults with custom values.
    '''
    default_file = open('default.yml', 'r')
    config       = load(default_file)
    default_file.close()         

    try:
        config_file = open('config.yml', 'r')
        config['Connection'].update(load(config_file)['Connection'])
        config_file.close()

    except IOError:
        pass

    return config

def main():
    '''This directly launches AethBot with a given configuration.
    '''
    bot = AethBot(load_config())
    bot.start()

if __name__ == '__main__':
    main()
