# coding=utf8
"""
IRC RPG bot.
"""
from __future__ import unicode_literals

# rpgbot stuff
from rpg.battle import Battle
from rpg.player_session_manager import PlayerSessionManager
from rpg.player import Player
from irc.user import User
from router import Router

import sys
import re
import threading
import random
from irc.ircbot import SingleServerIRCBot
from irc.irclib import nm_to_n, nm_to_h, irc_lower
import irc.botcommon


class RpgBot(SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.connection.add_global_handler('nick', PlayerSessionManager.nick_changed)

        Battle.precache()
        self.channel = channel
        self.nickname = nickname

        self.queue = irc.botcommon.OutputManager(self.connection)
        self.queue.start()

        self.start()


    def on_nicknameinuse(self, c, e):
        self.nickname = c.get_nickname() + "_"
        c.nick(self.nickname)


    def on_welcome(self, c, e):
      c.join(self.channel)


    def get_hostmask(self, source):
        split = source.split('!', 1)

        assert len(split) > 1

        return split[1]


    def on_privmsg(self, c, e):
      user = User(nm_to_n(e.source()), self.get_hostmask(e.source()))
      router = Router(self)
      router.route_private(user, e.arguments()[0])


    def on_pubmsg(self, c, e):
      user = User(nm_to_n(e.source()), self.get_hostmask(e.source()))
      router = Router(self)
      router.route_public(user, e.target(), e.arguments()[0])


    def say_public(self, text):
      self.queue.send(text, self.channel)


    def say_private(self, nick, text):
      self.queue.send(text,nick)


    def reply(self, text, to_private=None):
      if to_private is not None:
        self.say_private(to_private, text)
      else:
        self.say_public(text)


    def do_command(self, e, cmd, from_private):
        if None == re.search(r"^(\.attack).*", cmd):
            return


if __name__ == "__main__":
  try:
    irc.botcommon.trivial_bot_main(RpgBot)
  except KeyboardInterrupt:
    print("Shutting down.")

