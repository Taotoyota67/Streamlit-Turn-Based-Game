MONSTERS = {
    "Swordman": {
        "health": 20,
        "damage": 5,
        "moves": {
            "attack": 75,
            "damage_buff": 25
        },
        "texts": {
            "do_attack": ["\"I will cut you down.\"", "\"You are no match for my blade.\""],
            "got_attack": ["\"Is that all you got?\"", "\"You think you can hurt me?\""],
            "do_damage_buff": ["\"Watch out, here I come.\"", "\"You will not be able to escape.\""]
        },
        "image": {
            "alive": "assets/monsters/swordman.png",
            "dead": "assets/monsters/swordman_dead.png"
        }
    },
    "Spearwoman": {
        "health": 16,
        "damage": 6,
        "moves": {
            "attack": 75,
            "damage_buff": 25
        },
        "texts": {
            "do_attack": ["\"You are too slow for my spear.\"", "\"I will pierce you through.\""],
            "got_attack": ["\"You think you can reach me?\"", "\"Is that all you got?\""],
            "do_damage_buff": ["\"Look out, here I go.\"", "\"You will not be able to resist.\""]
        },
        "image": {
            "alive": "assets/monsters/spearwomen.png",
            "dead": "assets/monsters/spearwomen_dead.png"
        }
    },
    "The Gatekeeper": {
        "health": 30,
        "damage": 5,
        "moves": {
            "attack": 60,
            "life_steal": 20,
            "damage_buff": 20
        },
        "texts": {
            "do_attack": ["\"I will stop you.\"", "\"You are trespassing on sacred ground.\""],
            "got_attack": [
                "\"You think you can break through my defense?\"",
                "\"You are mistaken.\""
            ],
            "do_damage_buff": ["\"Let's end this.\"", "\"You won't last long.\""],
            "do_life_steal": ["\"I will replenish from your souls.\"", "\"Let's keep it coming.\""]
        },
        "image": {
            "alive": "assets/monsters/ghost.png",
            "dead": "assets/monsters/ghost_dead.png"
        }
    },
    "The Soul Collector": {
        "health": 30,
        "damage": 6,
        "moves": {
            "attack": 45,
            "poison": 25,
            "mana_drain": 30
        },
        "texts": {
            "do_attack": ["\"You are a source of energy for me.\"", "\"You will feel the cold.\""],
            "got_attack": ["\"You will see my hunger.\"", "\"You think you can deplete me?\""],
            "do_poison": ["\"You won't escape this.\"", "\"You are wrong.\""],
            "do_mana_drain": ["\"I will drain you with my scythe.\"", "\"I will consume you.\""]
        },
        "image": {
            "alive": "assets/monsters/thresh.png",
            "dead": "assets/monsters/thresh_dead.png"
        }
    },
    "The Corrupted": {
        "health": 30,
        "damage": 5,
        "moves": {
            "attack": 45,
            "damage_buff": 30,
            "mana_drain": 25
        },
        "texts": {
            "do_attack": ["\"I will torture you.\"", "\"You are a toy for my amusement.\""],
            "got_attack": ["\"You are hilarious.\"", "\"I laugh at your attacks.\""],
            "do_damage_buff": [
                "\"You will scream from my madness.\"",
                "\"Let's see what you can do.\""
            ],
            "do_mana_drain": [
                "\"My curse will weaken you.\"",
                "\"You will not be able to cure it.\""
            ]
        },
        "image": {
            "alive": "assets/monsters/ghost_warrior.png",
            "dead": "assets/monsters/ghost_warrior_dead.png"
        }
    },
    "Arachne": {
        "health": 25,
        "damage": 3,
        "moves": {
            "attack": 75,
            "poison": 25
        },
        "texts": {
            "do_attack": ["\"You are prey for my stinger.\"", "\"You will suffer from my pain.\""],
            "got_attack": ["\"You think you can harm me?\"", "\"You are foolish.\""],
            "do_poison": [
                "\"I will poison you with venom.\"",
                "\"You will not be able to stand up.\""
            ]
        },
        "image": {
            "alive": "assets/monsters/arachne.png",
            "dead": "assets/monsters/arachne_dead.png"
        }
    },
    "Archer Elf": {
        "health": 20,
        "damage": 5,
        "moves": {
            "attack": 75,
            "damage_buff": 25
        },
        "texts": {
            "do_attack": ["\"I will shoot you with accuracy.\"", "\"Dodge this.\""],
            "got_attack": ["\"You are naive.\"", "\"You will see the grace of my steps.\""],
            "do_damage_buff": [
                "\"Arrows will rain on you.\"",
                "\"You are a target for my arrows.\""
            ]
        },
        "image": {
            "alive": "assets/monsters/huntress.png",
            "dead": "assets/monsters/huntress_dead.png"
        }
    },
    "Scarlet Witch": {
        "health": 20,
        "damage": 5,
        "moves": {
            "attack": 80,
            "stun": 20
        },
        "texts": {
            "do_attack": ["\"I will blast you with fire.\"", "\"You will burn from my power.\""],
            "got_attack": ["\"You are arrogant.\"", "\"You will see the horror of my spells.\""],
            "do_stun": ["\"You will not be able to escape it.\"", "\"Lay down.\""]
        },
        "image": {
            "alive": "assets/monsters/young_witch.png",
            "dead": "assets/monsters/young_witch_dead.png"
        }
    },
    "The Rhinoceros": {
        "health": 32,
        "damage": 5,
        "moves": {
            "attack": 55,
            "stun": 20,
            "heal": 25
        },
        "texts": {
            "do_attack": [
                "\"You are a nuisance for my territory.\"",
                "\"I will crush you with my weight.\""
            ],
            "got_attack": ["\"You are pathetic.\"", "\"I will shrug off your attacks.\""],
            "do_stun": ["\"Beware, here I ram.\"", "\"You will not be able to dodge it.\""],
            "do_heal": ["\"Such a shallow wound.\"", "\"Let's continue.\""]
        },
        "image": {
            "alive": "assets/monsters/rino.png",
            "dead": "assets/monsters/rino_dead.png"
        }
    },
    "The Gladiator": {
        "health": 20,
        "damage": 5,
        "moves": {
            "attack": 75,
            "damage_buff": 25
        },
        "texts": {
            "do_attack": [
                "\"You will witness the skill of the champion.\"",
                "\"You are a challenger for my glory.\""
            ],
            "got_attack": [
                "\"You are brave.\"",
                "\"I will respect your courage and fight with honor.\""
            ],
            "do_damage_buff": [
                "\"I will rush at you with full speed.\"",
                "\"You will not be able to withstand it.\""
            ]
        },
        "image": {
            "alive": "assets/monsters/golem.png",
            "dead": "assets/monsters/golem_dead.png"
        }
    },
    "Knight of Rosaria": {
        "health": 16,
        "damage": 6,
        "moves": {
            "attack": 80,
            "stun": 20
        },
        "texts": {
            "do_attack": [
                "\"You are a threat for my faith.\"",
                "\"You will feel the wrath of the holy.\""
            ],
            "got_attack": [
                "\"You are ignorant.\"",
                "\"I will trust in my belief and pray for strength.\""
            ],
            "do_stun": ["\"You will not be able to move.\"", "\"I'll bless you with death.\""]
        },
        "image": {
            "alive": "assets/monsters/woman_knight.png",
            "dead": "assets/monsters/woman_knight_dead.png"
        }
    },
    "Knight of The Dying Sun": {
        "health": 20,
        "damage": 5,
        "moves": {
            "attack": 75,
            "damage_buff": 25
        },
        "texts": {
            "do_attack": ["\"I will destroy you.\"", "\"You are a sacrifice for my cause.\""],
            "got_attack": ["\"You think you can stop me?\"", "\"You are foolish.\""],
            "do_damage_buff": [
                "\"You will not be able to survive it.\"",
                "\"I'll stop the nonsense.\""
            ]
        },
        "image": {
            "alive": "assets/monsters/black_knight.png",
            "dead": "assets/monsters/black_knight_dead.png"
        }
    },
    "Samurize": {
        "health": 14,
        "damage": 8,
        "moves": {
            "attack": 75,
            "damage_buff": 25
        },
        "texts": {
            "do_attack": [
                "\"I will cut you with my katana.\"",
                "\"You will feel the edge of the blade.\""
            ],
            "got_attack": ["\"You are unworthy.\"", "\"You will see the skill of the master.\""],
            "do_damage_buff": [
                "\"Watch out, here I slash\"",
                "\"You will not be able to block it.\""
            ]
        },
        "image": {
            "alive": "assets/monsters/wanderer.png",
            "dead": "assets/monsters/wanderer_dead.png"
        }
    },
    "Oni Kenshi": {
        "health": 20,
        "damage": 5,
        "moves": {
            "attack": 80,
            "life_steal": 20
        },
        "texts": {
            "do_attack": ["\"I will devour you.\"", "\"You are a snack for my hunger.\""],
            "got_attack": [
                "\"You are amusing.\"",
                "\"I will laugh at your attacks and rip you apart.\""
            ],
            "do_life_steal": ["\"Your blood excited me.\"", "\"I am having fun.\""]
        },
        "image": {
            "alive": "assets/monsters/samurai.png",
            "dead": "assets/monsters/samurai_dead.png"
        }
    },
    "Black": {
        "health": 15,
        "damage": 6,
        "moves": {
            "attack": 80,
            "life_steal": 20
        },
        "texts": {
            "do_attack": ["\"Chomp\"", "\"Ki kli\""],
            "got_attack": ["\"Screech\"", "\"Peep\""],
            "do_life_steal": ["\"Die!\"", "\"Blood!\""]
        },
        "image": {
            "alive": "assets/monsters/void_eye_ball.png",
            "dead": "assets/monsters/void_eye_ball_dead.png"
        }
    },
    "Reaper": {
        "health": 10,
        "damage": 9,
        "moves": {
            "attack": 60,
            "life_steal": 40
        },
        "texts": {
            "do_attack": ["\"Give me your soul.\"", "\"Your soul will be mine.\""],
            "got_attack": ["\"I will always come back.\"", "\"You can't stop me forever.\""],
            "do_life_steal": ["\"Mmm, delicious.\"", "\"This is just the beginning.\""]
        },
        "image": {
            "alive": "assets/monsters/reaper.png",
            "dead": "assets/monsters/reaper_dead.png"
        }
    },
    "The Celestial": {
        "health": 30,
        "damage": 3,
        "moves": {
            "attack": 60,
            "heal": 40
        },
        "texts": {
            "do_attack": ["\"Stop resisting.\"", "\"Stay down.\""],
            "got_attack": ["\"You won't pass me.\"", "\"Try your best.\""],
            "do_heal": ["\"Mmm\"", "\"Mmm\""]
        },
        "image": {
            "alive": "assets/monsters/void_human.png",
            "dead": "assets/monsters/void_human_dead.png"
        }
    },
    "Zombie": {
        "health": 20,
        "damage": 5,
        "moves": {
            "attack": 75,
            "heal": 25
        },
        "texts": {
            "do_attack": ["\"AUGHHH\"", "\"ARGHHH\""],
            "got_attack": ["\"Aughh\"", "\"Grrr\""],
            "do_heal": ["\"Brains!\"", "\"Meat!\""]
        },
        "image": {
            "alive": "assets/monsters/zombie.png",
            "dead": "assets/monsters/zombie_dead.png"
        }
    },
    "Undead Warrior": {
        "health": 15,
        "damage": 7,
        "moves": {
            "attack": 75,
            "heal": 25
        },
        "texts": {
            "do_attack": ["\"Taste my sword.\"", "\"I'm going to kill you!\""],
            "got_attack": ["\"Aughh\"", "\"Is that all you got.\""],
            "do_heal": ["\"It not over yet.\"", "\"Fight me.\""]
        },
        "image": {
            "alive": "assets/monsters/lich_warrior.png",
            "dead": "assets/monsters/lich_warrior_dead.png"
        }
    },
    "The Dark Wizard": {
        "health": 30,
        "damage": 5,
        "moves": {
            "attack": 25,
            "poison": 30,
            "stun": 25,
            "life_steal": 20
        },
        "texts": {
            "do_attack": ["\"You will feel my pain.\"", "\"I will give you a brutal death.\""],
            "got_attack": [
                "\"You will suffer for what you did.\"",
                "\"I definitely won't forgive you.\""
            ],
            "do_poison": ["\"You will feel my pain.\"", "\"You will continue to suffer.\""],
            "do_stun": ["\"You will be stuck here forever.\"", "\"Mwahahahahahahahaha!\""],
            "do_life_steal": ["\"I will suck your blood dry.\"", "\"Thank for a meal.\""]
        },
        "image": {
            "alive": "assets/monsters/wizard.png",
            "dead": "assets/monsters/wizard_dead.png"
        }
    },
    "Fireworm": {
        "health": 25,
        "damage": 3,
        "moves": {
            "attack": 75,
            "poison": 25
        },
        "texts": {
            "do_attack": ["\"Hiss\"", "\"Chomp\""],
            "got_attack": ["\"Arg\"", "\"Grrr\""],
            "do_poison": ["\"Ptooey\"", "\"BRUN!\""]
        },
        "image": {
            "alive": "assets/monsters/fire_worm.png",
            "dead": "assets/monsters/fire_worm_dead.png"
        }
    },
    "Ogre": {
        "health": 20,
        "damage": 5,
        "moves": {
            "attack": 80,
            "life_steal": 20
        },
        "texts": {
            "do_attack": ["\"I'm going to tear you to pieces.\"", "\"You will suffer.\""],
            "got_attack": ["\"You won't be able to escape from me.\"", "\"I will kill you!.\""],
            "do_life_steal": ["\"Need More..MORE\"", "\"I will eat you piece by piece.\""]
        },
        "image": {
            "alive": "assets/monsters/humungousaur.png",  # who tf name this.
            "dead": "assets/monsters/humungousaur_dead.png"
        }
    },
    "Demon": {
        "health": 16,
        "damage": 6,
        "moves": {
            "attack": 75,
            "damage_buff": 25
        },
        "texts": {
            "do_attack": [
                "\"I will punish you to a painful death.\"",
                "\"You will feel my fury through my spear.\""
            ],
            "got_attack": ["\"You will have to pay for this.\"", "\"Nice try for a human.\""],
            "do_damage_buff": ["\"You will die by my hand.\"", "\"I'm going to get serious now.\""]
        },
        "image": {
            "alive": "assets/monsters/guardian.png",
            "dead": "assets/monsters/guardian_dead.png"
        }
    },
    "The Inferno": {
        "health": 35,
        "damage": 3,
        "moves": {
            "attack": 55,
            "poison": 30,
            "heal": 15
        },
        "texts": {
            "do_attack": ["\"You will feel my fury.\"", "\"I will put you down\""],
            "got_attack": [
                "\"Have you attacked yet? I don't feel pain.\"",
                "\"You are a pathetic human being.\""
            ],
            "do_poison": ["\"You're going to be burn to death.\"", "\"Brun human BRUN!\""],
            "do_heal": [
                "\"Your attacks were pathetic.\"",
                "\"Your attacks were useless against me.\""
            ]
        },
        "image": {
            "alive": "assets/monsters/fire_demon.png",
            "dead": "assets/monsters/fire_demon_dead.png"
        }
    }
}

# Mana cost for every moves.
PLAYER_MOVE_COSTS = {
    "attack": 0,
    "damage_buff": 6,
    "heal": 8,
    "poison": 5,
    "life_steal": 8,
    "stun": 6,
}

MONSTER_HEAL_MULTIPLIER = 0.25  # 20% of max_hp
MONSTER_DAMAGE_MULTIPLIER = 2  # 2x
MONSTER_MANA_DRAIN_MULTIPLIER = 0.25  # 25% of player max_mana

PLAYER_BUFF_MULTIPLIER = 2  # 2x damage
PLAYER_BUFF_DURATION = 2  # 2 turns
PLAYER_HEAL_MULTIPLIER = 0.35  # 35% of max hp

POISON_MULTIPLIER = 0.1  # 10% of max hp per turn
POISON_DURATION = 4  # poison duration (turns)
