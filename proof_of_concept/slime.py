class Slime():
    def __init__(self,
                 hp=50,
                 max_hp=50,
                 hit=10,
                 got_hit=["AAAAAA !!!", "Please spare me.",
                          "I'm not delicious.", "O U C H !!!"],
                 do_hit=["I'm gotta go.",
                         "This should by time.", "T...Take this~~~"],
                 do_heal=["I'm still alive?", "Still lucky enough.",
                          "I feel back to normal."],
                 skill=["heal"]):
        self.hp = hp
        self.max_hp = max_hp
        self.hit = hit
        self.got_hit = got_hit
        self.do_hit = do_hit
        self.do_heal = do_heal
        self.skill = skill

    def heal(self):
        if self.hp + 5 <= 50:
            self.hp += 5
        else:
            self.hp = 50

    def lose_hp(self, player_damage):
        if self.hp - player_damage >= 0:
            self.hp -= player_damage
        else:
            self.hp = 0
