# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php

'''This handles all of the IRC events that are not messages.
'''
import irclib

class Event():
    '''This handles all of the IRC events that are not messages.
    '''
    def __init__(self, core, connection, event):
        '''This decides which event is being passed in and then runs
        the appropriate method.
        '''
        self.core       = core
        self.connection = connection
        self.event      = event
        self.nick       = irclib.nm_to_n(self.event.source())
        self.chan       = self.event.target()

        getattr(self, self.event.eventtype())()

    def privnotice(self):
        '''Logs and handles private notices.'''
        msg = self.event.arguments()[0]
        me  = self.connection.get_nickname()
        self.core.record('-%s- %s' % (self.nick, msg), self.chan)

        identified_msg = 'You are now identified for \x02%s\x02.' % me

        if self.nick == 'NickServ' and msg == identified_msg:
            self.core.identified(self.connection)

    def pubnotice(self):
        '''Logs and handles public notices.'''
        msg = self.event.arguments()[0]

        self.core.record('-%s:%s- %s' % (self.nick, self.chan, msg), self.chan)

    def join(self):
        '''Logs and handles channel joins.'''
        host = irclib.nm_to_uh(self.event.source())

        self.core.record('-!- %s [%s] has joined %s' % (self.nick, host, self.chan), self.chan)

    def part(self):
        '''Logs and handles channel parts.'''
        host = irclib.nm_to_uh(self.event.source())
        msg  = ''

        if len(self.event.arguments()) == 1:
            msg = self.event.arguments()[0]

        self.core.record('-!- %s [%s] has left %s [%s]' % (self.nick, host, self.chan, msg), self.chan)

    def quit(self):
        '''Logs and handles channel quits.'''
        host = irclib.nm_to_uh(self.event.source())
        msg  = self.event.arguments()[0]

        self.core.record('-!- %s [%s] has quit [%s]' % (self.nick, host, msg), self.chan)

    def kick(self):
        '''Logs and handles kicks.'''
        target = self.event.arguments()[0]
        msg    = self.event.arguments()[1]

        self.core.record('-!- %s was kicked from %s by %s [%s]' % (target, self.chan, self.nick, msg), self.chan)

    def mode(self):
        '''Logs and handles changes in channel modes.'''
        arg1 = self.event.arguments()[0]
        arg2 = ''

        if len(self.event.arguments()) == 2:
            arg2 = ' ' + self.event.arguments()[1]

        self.core.record('-!- mode/%s [%s%s] by %s' % (self.chan, arg1, arg2, self.nick), self.chan)

    #### TODO: Handle other CTCP events, including VERSION.
    def ctcp(self):
        '''Logs and handles various CTCP events, including 'ACTION',
        which what is actually sent by IRC clients when people use the
        /me command to describe some sort of action.'''
        arg = self.event.arguments()

        if arg[0] == 'ACTION':
            msg = arg[1]

            me_log = ' * %s %s'  % (self.nick, msg)

            if self.chan != 'AethBot':
                self.core.record(me_log, self.chan)

            else:
                self.core.record(me_log, self.nick)
