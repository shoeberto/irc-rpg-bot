from database import Database
from rpg_character import RpgCharacter

class Monster(RpgCharacter):
    def __init__(self, monster_name, xp):
        db = Database()
        cursor = db.query('SELECT * FROM rpg_characters WHERE character_name = ? AND username IS NULL', [monster_name])

        if db.fetchone(cursor) is None:
            self.lazy_create(monster_name)

        super(Monster, self).__init__(monster_name, xp)



    def lazy_create(self, monster_name):
        db = Database()
        db.query('INSERT INTO rpg_characters (character_name, username) VALUES (?, NULL)', [monster_name])
        db.commit()

