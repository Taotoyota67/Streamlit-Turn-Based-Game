class Good_Boy():
	def __init__(self,
			hp=100,
			max_hp=100,
			hit=10,
			got_hit=["Tsk...", "So annoying",
				"Is that all you got", "AH..."],
			do_hit=["W E A K",
				"let me show you.", "I'm not holding back."],
			do_heal=["Did you think it will end that easily.", "Not yet",
				"Come Onnnn"],
			skill=["heal", "charge"],
			do_charge=["You will regret this.", "PEASANT!!!", "Rot in hell"]):
		self.hp = hp
		self.max_hp = max_hp
		self.hit = hit
		self.got_hit = got_hit
		self.do_hit = do_hit
		self.do_heal = do_heal
		self.skill = skill
		self.do_charge = do_charge

	def heal(self) :
		if self.hp + 15 <= 100 :
			self.hp += 15
		else :
			self.hp = 100
			
	def charge(self) :
		self.hit += 10

	def lose_hp(self, player_damage) :
		if self.hp - player_damage >= 0 :
			self.hp -= player_damage
		else :
			self.hp = 0
