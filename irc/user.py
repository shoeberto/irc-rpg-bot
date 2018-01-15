class User(object):
    nick = None
    hostmask = None

    def __init__(self, nick, hostmask):
        self.nick = nick
        self.hostmask = hostmask
