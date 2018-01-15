class RpgCharacter(object):
    character_name = None
    xp = 0
    hp = 30


    def __init__(self, character_name, xp):
        self.xp = xp
        self.character_name = character_name


    def dmg(self, dmg):
        self.hp = self.hp - dmg

        return self.hp > 0


    def get_name(self):
        return self.character_name
