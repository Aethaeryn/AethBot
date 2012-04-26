# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://opensource.org/licenses/MIT

'''This core file acts as an intermediate step between the basic bot
defined in __init__.py and the advanced features that are handled in
individual, modular files.
'''
from time import strftime
from os import mkdir, listdir
from aethbot import calc, commands, events

class BotCore:
    '''This core module interfaces directly with the IRC bot and calls
    all of the custom modules.
    '''
    def __init__(self, bot, ops, chans, about):
        self.operators = set(ops)
        self.bot       = bot
        self.math      = calc.Math()
        self.channels  = chans
        self.version   = about

    def identified(self, connection):
        '''Once the bot is identified, it does this action.'''
        for channel in self.channels:
            self.join(connection, channel)

    def join(self, connection, chan):
        '''This is how AethBot tries to join a channel.'''
        connection.join(chan)

    def part(self, connection, chan, msg=''):
        '''This is how AethBot tries to part a channel.'''
        connection.part(chan, msg)

    def outmsg(self, server, target, msg):
        '''This gets AethBot to send and record messages to a user or
        a channel.
        '''
        self.record('<%s> %s' % (server.get_nickname(), msg), target)
        server.privmsg(target, msg)

    def time(self):
        '''Obtains the time for the logs.'''
        return strftime('%H:%M:%S')

    def date(self):
        '''Obtains the date for the logs.'''
        return strftime('%Y %m %d')

    def reload(self, connection, chan):
        '''Reloads all of the AethBot modules.'''
        reload(calc)
        reload(commands)
        reload(events)
        self.bot.reload_core(connection, chan)


    def record(self, message, name):
        '''Records a line in a log file. If no name (i.e. the location
        of events) is given, then the log that is used is the default
        log. It also logs to as any channels that the person who
        triggered the event is or was located in. This is used for
        actions such as quitting.
        '''
        directory = 'logs'

        if directory not in listdir('.'):
            mkdir(directory)

        if name:
            name = name.lower()

        else:
            name = 'irc'

            #### TODO: This has been broken ever since the switch from
            #### ircbot to irclib. This causes the bot to crash when,
            #### for instance, someone quits.
            for channel in self.bot.channels:
                nick = message.split()[1]

                if nick in self.bot.channels[channel].userdict:
                    self.record(message, channel)

        # If there is no channel or nick, the name should be 'irc.log'
        if name == '*':
            name = 'irc'

        # Handles the timestamps.
        message = '%s %s' % (self.time(), message)

        logfile = open('%s/%s.log' % (directory, name), 'a')
        logfile.writelines(message + '\n')
        logfile.close()

    def handle_event(self, connection, event):
        '''Every notable and recorded IRC event except for messages is
        handled here.
        '''
        events.Event(self, connection, event)

    def commands(self, connection, event):
        '''Messages are handled separately because they may or may not
        be commands for AethBot.
        '''
        commands.Command(self, connection, event)
