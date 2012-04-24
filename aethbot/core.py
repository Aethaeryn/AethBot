# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php

from time import strftime
from os import mkdir, listdir
from aethbot import calc, commands, events

# Handles the core module to the IRC bot and calls all other custom modules.
class BotCore:
    def __init__(self, bot, ops, chans, about):
        self.operators = set(ops)
        self.bot       = bot
        self.math      = calc.Math()
        self.channels  = chans
        self.version   = about

    # This is the default behavior for when identified.
    def identified(self, connection):
        for channel in self.channels:
            self.join(connection, channel)

    # Tries to join a channel.
    def join(self, connection, chan):
        connection.join(chan)

    # Tries to parts a channel.
    def part(self, connection, chan, msg=''):
        connection.part(chan, msg)

    # Sends and records a message to a user or channel.
    def outmsg(self, server, target, msg):
        self.record('<%s> %s' % (server.get_nickname(), msg), target)
        server.privmsg(target, msg)

    # Obtains the time for logging purposes.
    def time(self):
        return strftime('%H:%M:%S')

    # Obtains the date for logging purposes.
    def date(self):
        return strftime('%Y %m %d')

    # Reloads all AethBot modules.
    def reload(self, connection, chan):
        reload(calc)
        reload(commands)
        reload(events)
        self.bot.reload_core(connection, chan)

    # Records a line in the log.
    def record(self, message, name):
        # Records logs in the log directory.
        directory = 'logs'

        if directory not in listdir('.'):
            mkdir(directory)

        # Prevents crash if name is not given.
        if name:
            name = name.lower()

        # If no name (i.e. location of events) is given, it's logged in the
        # default log and then also in any channels the person who triggered
        # the event (such as a quit) is in.
        else:
            name = 'irc'

            for channel in self.bot.channels:
                nick = message.split()[1]

                if nick in self.bot.channels[channel].userdict:
                    self.record(message, channel)

        # If there is no channel or nick, the name should be 'irc.log'
        if name == '*':
            name = 'irc'

        # Timestamp logs are the default behavior.
        message = '%s %s' % (self.time(), message)

        # File i/o.
        logfile = open('%s/%s.log' % (directory, name), 'a')
        logfile.writelines(message + '\n')
        logfile.close()

    # Every notable and recorded IRC event except for messsages is handled here.
    # The event recording is designed to mimic the default irssi style.
    def handle_event(self, connection, event):
        self.event = events.Event(self, connection, event)

    # Because messages can be commands, they're handled specially.
    def commands(self, connection, event):
        commands.Command(self, connection, event)
