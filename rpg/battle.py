import random
import threading
from rpg.player import Player
from rpg.player_session_manager import PlayerSessionManager
from rpg.monster import Monster
from irc.user import User

class Battle(object):
    monsters = None
    items = None
    modifiers = None
    battles = []

    bot = None
    attacker = None
    monster = None


    def __init__(self, bot, attacker, monster):
        self.bot = bot
        self.attacker = attacker
        self.monster = monster


    def has(self, character):
        if (self.attacker.get_name() == character.get_name() or self.monster.get_name() == character.get_name()):
            return True

        return False


    def attack(self):
        # TODO: this was just a straight copy-paste of my prototype code from the Sopel plugin
        # it "worked" before, but was not very clean, and would need to be refactored to use player stats, etc
        gob_atk = random.randint(0,9)
        bat_atk = random.randint(0,9)

        gob_init = random.randint(0, 20)
        bat_init = random.randint(0, 20)

        if (gob_init > bat_init):
            if (self.attacker.dmg(gob_atk) is False):
                self.bot.say_public("Oh no! " + self.attacker.get_name() + " has been bested by " + self.monster.get_name() + "!")
                self.bot.say_public(self.monster.get_name() + " receives a %s %s" % (random.choice(self.modifiers), random.choice(self.items)))
                Battle.battles.remove(self)
                return
            elif (self.monster.dmg(bat_atk) is False):
                self.bot.say_public("Victory! " + self.attacker.get_name() + " has slain " + self.monster.get_name() + "!")
                self.bot.say_public(self.attacker.get_name() + " receives a %s %s" % (random.choice(self.modifiers), random.choice(self.items)))
                Battle.battles.remove(self)
                return
            else:
                self.bot.say_public(self.monster.get_name() + " hits for " + str(gob_atk) + " damage! " + self.attacker.get_name() + " responds with an attack for " + str(bat_atk) + " damage!")
        else:
            if (self.monster.dmg(bat_atk) is False):
                self.bot.say_public("Victory! " + self.attacker.get_name() + " has slain " + self.monster.get_name() + "!")
                self.bot.say_public(self.attacker.get_name() + " receives a %s %s" % (random.choice(self.modifiers), random.choice(self.items)))
                Battle.battles.remove(self)
                return
            elif (self.attacker.dmg(gob_atk) is False):
                self.bot.say_public("Oh no! " + self.attacker.get_name() + " has been bested by " + self.monster.get_name() + "!")
                self.bot.say_public(self.monster.get_name() + " receives a %s %s" % (random.choice(self.modifiers), random.choice(self.items)))
                Battle.battles.remove(self)
                return
            else:
                self.bot.say_public(self.attacker.get_name() + " attacks fiercely for " + str(bat_atk) + " damage! " + self.monster.get_name() + " responds for " + str(gob_atk) + " damage! ")

        t = threading.Timer(3.0, self.attack)
        t.start()


    @staticmethod
    def precache():
        Battle.monsters = Battle.parse_flat_file('res/monsters.txt')
        Battle.items = Battle.parse_flat_file('res/items.txt')
        Battle.modifiers = Battle.parse_flat_file('res/modifiers.txt')


    @staticmethod
    def parse_flat_file(filename):
        fh = None
        try:
            fh = open('./' + filename, 'r')
        except IOError:
            return None

        contents = [line.strip() for line in fh.readlines()]
        return contents


    @staticmethod
    def route(bot, channel, player, args):
        for b in Battle.battles:
            if b.has(player):
             bot.say_public("You're already in combat!")
             return

        target = 'monster'
        users = None
        if len(args) >= 1:
            users = [w.replace('~', '').replace('+', '').replace('@', '') for w in bot.channels[channel].users()]

            if bot.nickname in users: users.remove(bot.nickname)
            if player.user.nick in users: users.remove(player.user.nick)

            if not users:
                return

            if args[0] in users:
                target = args[0]
            elif ' '.join(args[0:]) in Battle.monsters:
                target = ' '.join(args[0:])
            elif args[0] == 'monster':
                target = 'monster'
            else:
                bot.say_public(args[0] + " is not a valid target!")
                return

        if target == 'monster':
            target = Monster(random.choice(Battle.monsters), 0)
        else:
            target_user = PlayerSessionManager.validate_session(target)
            if target_user is None:
                bot.say_public(target + " is not a player! Tell them to sign up!")
                return

            target = Player(User(target, bot.connection.userhost(target)), target_user)


        msg = random.choice((
            '%s attacks %s!'
            # TODO: add more flavor text
        ))

        battle = Battle(bot, player, target)
        Battle.battles.append(battle)

        bot.say_public(msg % (player.get_name(), target.get_name()))

        battle.attack()
