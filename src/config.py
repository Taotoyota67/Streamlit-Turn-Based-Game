MONSTERS = {
    "Slime": {
        "health": 20,
        "damage": 5,
        "moves": {
            "attack": 75,
            "heal": 25
        },
        "texts": {
            "do_attack": ["Ya!", "Boom!"],
            "got_attack": ["AAAAA", "That hurt!"],
            "do_heal": ["That feels good..."]
        },
        "image": {
            "alive": "assets/monster/slime_test.png",
            "dead": "assets/monster/slime_test.png"
        }
    },
    "Goblin": {
        "health": 20,
        "damage": 5,
        "moves": {
            "attack": 75,
            "damage_buff": 25
        },
        "texts": {},
        "image": {
            "alive": "assets/monster/slime_test.png",
            "dead": "assets/monster/slime_test.png"
        }
    },
    "Sharkman": {
        "health": 20,
        "damage": 5,
        "moves": {
            "attack": 50,
            "poison": 25,
            "mana_drain": 25
        },
        "texts": {},
        "image": {
            "alive": "assets/monster/slime_test.png",
            "dead": "assets/monster/slime_test.png"
        }
    },
    "The Dragon": {
        "health": 40,
        "damage": 10,
        "moves": {
            "attack": 50,
            "stun": 25,
            "mana_drain": 25
        },
        "texts": {},
        "image": {
            "alive": "assets/monster/slime_test.png",
            "dead": "assets/monster/slime_test.png"  # Please add a real path, ty
        }
    }
}

PLAYER_DEFAULT_STATS = {
    "damage": 10,
    "health": 100,
    "mana": 100
}

MONSTER_HEAL_MULTIPLIER = 0.2  # 20% of max_hp
MONSTER_DAMAGE_MULTIPLIER = 2  # 2x
MONSTER_MANA_DRAIN_MULTIPLIER = 0.25  # 25% of player max_mana

PLAYER_BUFF_MULTIPLIER = 2  # 2x damage
PLAYER_BUFF_DURATION = 2  # 2 turns
PLAYER_POISON_MULTIPLIER = 2
PLAYER_POISON_DURATION = 2
