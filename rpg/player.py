from rpg_character import RpgCharacter
from database import Database
from player_session_manager import PlayerSessionManager

import hashlib
import time
import config

class Player(RpgCharacter):
    user = None

    def __init__(self, user, username):
        db = Database()
        cursor = db.query('SELECT username, xp FROM rpg_users WHERE username = ?', [username])

        res = db.fetchone(cursor)

        self.user = user
        super(Player, self).__init__(res['username'], res['xp'])


    def get_name(self):
        return self.user.nick


    @staticmethod
    def login(bot, user, username, password):
        db = Database()

        m = hashlib.sha256()
        m.update(password + config.pw_salt)
        cursor = db.query('''SELECT ru.xp, rc.character_name
                FROM rpg_users ru
                JOIN rpg_characters rc ON rc.username = ru.username
                WHERE ru.username = ? and ru.password = ?''', [username, m.hexdigest()])

        account_deets = db.fetchone(cursor)
        if account_deets is None:
            bot.say_private(user.nick, 'Sorry, your username or password was not correct.')
            return None

        player = Player(user, account_deets['character_name'])
        db.query('UPDATE rpg_users SET auth_hostmask = ?, auth_timestamp = ? WHERE username = ?', [user.hostmask, '%d' % round(time.time() * 100), username])
        db.commit()

        PlayerSessionManager.on_login(username, user.nick)
        bot.say_private(user.nick, "Welcome back, %s. You are now logged in." % username)
        return player


    @staticmethod
    def create(bot, user, username, password):
        db = Database()

        cursor = db.query('SELECT * FROM rpg_users WHERE username = ?', [username])
        if len(cursor.fetchall()) > 0:
            bot.say_private(user.nick, 'Sorry, but that username is already in use.')
            return

        m = hashlib.sha256()
        m.update(password + config.pw_salt)

        db.query('INSERT INTO rpg_users (username, password, auth_hostmask, auth_timestamp) VALUES (?, ?, ?, ?)', [username, m.hexdigest(), user.hostmask, '%d' % round(time.time() * 100)])
        db.query('INSERT INTO rpg_characters (character_name, username) VALUES (?, ?)', [username, username])
        db.commit()

        bot.say_private(user.nick, "Success. Created account '%s'. You are now logged in. Have fun!" % username)

        return Player(user, username)


    @staticmethod
    def route(bot, user, args):
        if len(args) == 0:
            bot.say_private(user.nick, "No such command.")
            return

        if args[0] == 'register':
            if len(args) < 3:
                bot.say_private(user.nick, "Too few arguments for register command. Please use the form: .account register [username] [password]")
                return

            return Player.create(bot, user, args[1], args[2])
        elif args[0] == 'login':
            if len(args) < 3:
                bot.say_private(nick, "Too few arguments for login command. Please use the form: .account login [username] [password]")
                return

            return Player.login(bot, user, args[1], args[2])
