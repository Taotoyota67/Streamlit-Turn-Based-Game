class Player():
    def __init__(self, hp=100, hit=10, mana=100):
        self.hp = hp
        self.hit = hit
        self.mana = mana

    def lose_hp(self, monster_damage):
        if self.hp - monster_damage >= 0:
            self.hp -= monster_damage
        else:
            self.hp = 0

    def lose_mana(self):
        if self.mana - 10 >= 0:
            self.mana -= 10
        else:
            self.mana = 0

    def heal(self):
        if self.hp + 10 <= 100:
            self.hp += 10
        else:
            self.hp = 100
