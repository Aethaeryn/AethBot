# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://opensource.org/licenses/MIT

'''This handles all of the messages that AethBot receives.
'''
import sys
import irclib

class Command():
    '''This handles all of the messages. The messages that are also
    commands are then treated appropriately.
    '''
    def __init__(self, core, connection, event):
        '''Logs messages, handles common information, and then calls
        the appropriate method if it detects a command.
        '''
        self.calc_words = set(['~', 'calc', 'math'])

        self.core       = core
        self.connection = connection
        self.event      = event
        self.me         = self.connection.get_nickname()

        self.msg        = self.event.arguments()[0]
        self.msg_args   = self.msg.split()
        self.sender     = irclib.nm_to_n(self.event.source())
        self.chan       = self.event.target()

        # If the target of the message has the bot's name, it was a query.
        if irclib.nm_to_n(self.chan) == self.connection.get_nickname():
            self.chan = self.sender

        # Records the messages themselves.
        self.core.record('<%s> %s' % (self.sender, self.msg), self.chan)

        # Skips over blank lines so it doesn't crash.
        if len(self.msg_args) == 0:
            pass

        # Messaging the bot's name directly will cause the bot to check for commands.
        elif (self.msg_args[0] == self.me + ':' and self.chan != self.sender):
            # We want the bot to ignore its name when handling the commands.
            self.msg_args.pop(0)
            self.commands()

        # Querying it will work, too.
        elif self.chan == self.sender:
            self.commands()

    def commands(self):
        '''Determines what kind of command it is and sends it to the
        right location.
        '''
        # Handles the core commands.
        if self.msg_args[0] == ',' and len(self.msg_args) > 1 and self.sender in self.core.operators:
            self.msg_args.pop(0)
            self.msg_args[0] = self.msg_args[0].lower()

            self.core_commands()
 
        # Hands the math over to calc.py
        elif self.msg_args[0] in self.calc_words:
            pos = self.msg.find(self.msg_args[0])
            self.speak(self.core.math.command(self.msg[(pos + len(self.msg_args[0]) + 1):]))

        # Using the restricted prefix without being an operator gives an error.
        elif self.msg_args[0] == ',':
            self.speak('I\'m sorry, you are not authorized.')

        else:
            self.public_commands()

    def public_commands(self):
        '''These are harmless, public commands that anyone is allowed
        to use with the bot.
        '''
        # Displays a help string.
        if self.msg_args[0] == 'help':
            self.speak('I am AethBot, a basic IRC bot created in Python by Aethaeryn. '\
                           'For commands you can use, say "commands".')

        # Lists public commands.
        elif self.msg_args[0] == 'commands':
            commands = 'The following public commands are available: '\
                'help commands time version ops'

            for word in self.calc_words:
                commands += ' %s' % word

            self.speak(commands)

        # Prints the current operators.
        elif self.msg_args[0] == 'ops':
            op_msg = 'My current operators are:'

            for op in self.core.operators:
                op_msg += ' %s' % op

            self.speak(op_msg)

        # Prints the version string.
        elif self.msg_args[0] == 'version':
            self.speak(self.core.version)

        # Displays the current local time.
        elif self.msg_args[0] == 'time':
            time = self.core.time()

            self.speak('My current local time is %s' % time)

    def core_commands(self):
        '''The main commands, not part of another module, are handled here.
        '''
        # Sends a message in the current channel or query.
        # syntax: , msg <message>
        if self.msg_args[0] == 'msg':
            pos = self.msg.find(self.msg_args[0])
            self.speak(self.msg[(pos + len(self.msg_args[0]) + 1):])

        # Sends a message to a given destination.
        # syntax: , <destination> msg <message>
        elif len(self.msg_args) > 1 and self.msg_args[1] == 'msg':
            pos = self.msg.find(self.msg_args[1])
            self.core.outmsg(self.connection, self.msg_args[0],
                             self.msg[(pos + len(self.msg_args[1]) + 1):])

        # Orders the bot to join a channel.
        elif self.msg_args[0] == 'join':
            if len(self.msg_args) == 2:
                self.core.join(self.connection, self.msg_args[1])

            else:
                self.speak('I need to be given a channel to join!')

        # Orders the bot to part a channel.
        elif self.msg_args[0] == 'part':
            if len(self.msg_args) == 2:
                self.core.part(self.connection, self.msg_args[1])

            else:
                self.speak('I need to be given a channel to leave!')

        # Reloads this module without restarting the bot.
        # syntax: , reload
        elif self.msg_args[0] == 'reload':
            self.core.reload(self.connection, self.chan)

        # Orders the bot to quit from IRC.
        # syntax: , quit
        elif self.msg_args[0] == 'quit':
            self.core.bot.connection.disconnect(self.core.version)
            sys.exit(0)

        # The proper prefix without a recognized command gets an error.
        else:
            self.speak('I\'m sorry, I don\'t know that command.')

    def speak(self, msg):
        '''This is how the bot speaks.
        '''
        self.core.outmsg(self.connection, self.chan, msg)
