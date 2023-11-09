from .entity import Entity  # pylint: disable=E0402
from .text import Text  # pylint: disable=E0402


class Slime(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.text.set(
            "got_hit",
            Text().add(
                "AAAAAA!!!"
            ).add(
                "Please spare me."
            ).add(
                "I'm not delicious."
            ).add(
                "O U C H ! ! !"
            )
        )

        self.text.set(
            "do_hit",
            Text().add(
                "I gotta go..."
            ).add(
                "This should buy time."
            ).add(
                "T...Take this!"
            )
        )

        self.text.set(
            "do_heal",
            Text().add(
                "I'm still alive?"
            ).add(
                "Still luckly enough."
            ).add(
                "I feel back to normal."
            )
        )

        self._image["alive"] = "assets/monsters/slime_test.png"
        self._image["dead"] = "assets/monsters/slime_test_dead.png"


class Monsters:
    def __init__(self) -> None:
        self._monsters = {
            "slime": Slime
        }

    def get(self, monster: str, **kwargs) -> Entity:
        return self._monsters[monster](**kwargs)
