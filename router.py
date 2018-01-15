from rpg.battle import Battle
from rpg.player import Player
from rpg.monster import Monster
from rpg.player_session_manager import PlayerSessionManager

class Router(object):
    bot = None

    private_cmds = ['.help', '.account']
    public_cmds = ['.help', '.attack']

    def __init__(self, bot):
        self.bot = bot


    def route_private(self, user, command):
        text = command.split()

        if len(text) < 1:
            self.bot.say_private("Internal error. Could not parse command.")
            return

        if text[0] not in set(self.private_cmds + self.public_cmds):
            return

        if text[0] not in self.private_cmds:
            self.bot.say_private(user.nick, "'%s' is not a valid command in private chat. Type .help for more options." % text[0])
            return

        args = []
        if len(text) > 1:
            args = text[1:]

        return self.route(user, text[0], args)



    def route_public(self, user, channel, command):
        text = command.split()

        if len(text) < 1:
            self.bot.say_public("Internal error. Could not parse command.")

        if text[0] not in set(self.private_cmds + self.public_cmds):
            return

        if text[0] not in self.public_cmds:
            self.bot.say_public("'%s' is not a valid command in public chat. Type .help for more options." % text[0])
            return

        args = []
        if len(text) > 1:
            args = text[1:]

        return self.route(user, text[0], args, channel = channel)


    def route(self, user, command, args, channel = None):
        if (command == '.account'):
            return Player.route(self.bot, user, args)

        username = self.get_username(user)

        if username is None:
            return

        if (command == '.attack'):
            Battle.route(self.bot, channel, Player(user, username), args)


    def get_username(self, user):
        username = PlayerSessionManager.validate_session(user.nick)

        if (username is None):
            if (user.nick is None):
                self.bot.say_public("Sorry, you are not logged in.")
            else:
                self.bot.say_private(user.nick, "Sorry, you are not logged in")

        return username
