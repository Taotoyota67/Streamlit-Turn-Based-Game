class Slime():
    def __init__(self,
                 hp=50,
                 hit=10,
                 got_hit=["AAAAAA !!!", "Please spare me.",
                          "I'm not delicious.", "O U C H !!!"],
                 do_hit=["I'm gotta go.",
                         "This should by time.", "T...Take this~~~"],
                 do_heal=["I'm still alive?", "Still lucky enough.",
                          "I feel back to normal."],
                 skill=["heal"],
                 heal=5):
        self.hp = hp
        self.hit = hit
        self.got_hit = got_hit
        self.do_hit = do_hit
        self.do_heal = do_heal
        self.skill = skill
        self.heal = heal
