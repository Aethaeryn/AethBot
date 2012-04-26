# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://opensource.org/licenses/MIT

'''AethBot is a simple IRC bot with a modular design, intended for use
in Aethaeryn's IRC channels on the Freenode IRC network. Because of
its modular nature, it will have tight integration with his other
projects, including the game Federation.
'''
from aethbot import core
from irclib import SimpleIRCClient

class AethBot(SimpleIRCClient):
    '''AethBot handles the actual IRC bot, inherited from irclib's
    SimpleIRCClient. This class contains the minimum functionality
    necessary to get the bot to run. All of the other features are
    handled by individual files. This is managed by core.py, allowing
    almost every file to be modified and reloaded while the bot is
    still running.
    '''

    def __init__(self, config):
        '''Sets up two things from the configuration file: the
        connection information that is used by the SimpleIRCClient
        parent class and the information needed by the core class that
        adds interactive functionality to the bot.
        '''
        bot = config['Connection']

        SimpleIRCClient.__init__(self)
        self.connect(bot['server'], bot['port'], bot['nick'],
                     bot['pw'], bot['name'])

        self.ops   = bot['ops']
        self.chans = bot['chans']
        self.about = bot['about']

        self.core   = core.BotCore(self, self.ops, self.chans, self.about)

    def start(self):
        '''Starts the IRC bot, which gets it to connect to the server
        that has been specified.
        '''
        SimpleIRCClient.start(self)

    # ** Reads various events, sending them to core.py to be handled. ** #
    def on_privmsg(self, connection, event):
        '''Sends private messages to the core to be handled there.'''
        self.core.commands(connection, event)

    def on_pubmsg(self, connection, event):
        '''Sends public messages to the core to be handled there.'''
        self.core.commands(connection, event)

    def on_privnotice(self, connection, event):
        '''Sends notices to the core to be handled there.'''
        self.core.handle_event(connection, event)

    def on_pubnotice(self, connection, event):
        '''Sends notices to the core to be handled there.'''
        self.core.handle_event(connection, event)

    def on_join(self, connection, event):
        '''Sends joins to the core to be handled there.'''
        self.core.handle_event(connection, event)

    def on_part(self, connection, event):
        '''Sends parts to the core to be handled there.'''
        self.core.handle_event(connection, event)

    def on_quit(self, connection, event):
        '''Sends quits to the core to be handled there.'''
        self.core.handle_event(connection, event)

    def on_kick(self, connection, event):
        '''Sends kicks to the core to be handled there.'''
        self.core.handle_event(connection, event)

    def on_mode(self, connection, event):
        '''Sends modes to the core to be handled there.'''
        self.core.handle_event(connection, event)

    def on_ctcp(self, connection, event):
        '''Sends CTCP to the core to be handled there.'''
        self.core.handle_event(connection, event)

    def get_version(self):
        '''Gets the version number.'''
        #### TODO: Check to see if this is still used anywhere.
        return self.core.version

    def reload_core(self, connection, target):
        '''Reloads core.py unless there is some bug in the new code.
        '''
        try:
            reload(core)
            self.core = core.BotCore(self, self.ops, self.chans, self.about)
            self.core.outmsg(connection, target,
                             'All modules have been reloaded.')

        except:
            self.core.outmsg(connection, target, 'Error in reloading modules.')
