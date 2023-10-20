class Good_Boy() :
    def __init__(self, hp = 30, hp2 = 100, hit = 5, hit2 = 10) :
        self.hp = hp
        self.hp2 = hp2
        self.hit = hit
        self.hit2 = hit2

    def heal(self) :
        self.hp += 10

    def charge_at(self) :
        self.hit2 = 20