from irc.irclib import nm_to_n

class PlayerSessionManager(object):
    registry = {}

    @staticmethod
    def on_login(username, nick):
        PlayerSessionManager.registry[username] = nick


    @staticmethod
    def nick_changed(c, e):
        before = nm_to_n(e.source())
        after = e.target()
        for cached_username, cached_nick in PlayerSessionManager.registry.iteritems():
            if cached_nick == before:
                PlayerSessionManager.registry[cached_username] = after


    @staticmethod
    def remove_stale():
        return


    @staticmethod
    def validate_session(nick):
        for cached_username, cached_nick in PlayerSessionManager.registry.iteritems():
            if cached_nick == nick:
                return cached_username

        return None
