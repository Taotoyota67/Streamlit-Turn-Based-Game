from io import BytesIO
import random
from typing import Any, Optional, TypeVar


T = TypeVar("T", bound="EntityStats")


class Text:
    def __init__(self, texts: Optional[list[str]] = None) -> None:
        if not texts:
            texts = []

        self.texts = texts

    def add(self, txt: str) -> "Text":
        self.texts.append(txt)
        return self

    def adds(self, list_txt: list[str]) -> None:
        self.texts += list_txt

    def choice(self) -> str:
        return random.choice(self.texts)


class EntityStats:
    def __init__(self, max_hp: int, damage: int, heal: int = 0, mana: int = 0) -> None:
        self.current_hp = max_hp
        self.max_hp = max_hp
        self.damage = damage
        self.current_mana = mana
        self.max_mana = mana
        self.heal_amount = heal
        self.name = None

    @property
    def is_alive(self) -> bool:
        return self.current_hp > 0

    def set_name(self: T, name: str) -> T:
        self.name = name
        return self

    def add_health(self, amount: int) -> None:
        self.current_hp = min(self.current_hp + amount, self.max_hp)

    def reduce_health(self, amount: int) -> None:
        self.current_hp = max(self.current_hp - amount, 0)

    def heal(self) -> None:
        self.current_hp = min(self.current_hp + self.heal_amount, self.max_hp)

    def add_mana(self, amount: int) -> None:
        self.current_mana = min(self.current_mana + amount, self.max_mana)

    def reduce_mana(self, amount: int) -> None:
        self.current_mana = max(self.current_mana - amount, 0)


class EntityText:
    def __init__(self) -> None:
        self.texts: dict[str, Text] = {}

    def set(self, key: str, value: Text) -> None:
        self.texts[key] = value

    def get(self, key: str) -> str:
        if key not in self.texts:
            raise KeyError(f"Unknown EntityText key: {key}")

        return self.texts[key].choice()


class Image:
    def __init__(self) -> None:
        self._images = {}
        self._bimages = {}

    def __getitem__(self, __name: str) -> BytesIO:
        if __name not in self._images:
            raise KeyError(f"Image named {__name}; not found")

        if __name in self._bimages:
            return self._bimages[__name]

        with open(self._images[__name], "rb") as file:
            self._bimages[__name] = file.read()

        return self._bimages[__name]

    def __setitem__(self, __name: str, __value: Any) -> None:
        self._images[__name] = __value


class Slime(EntityStats):
    def __init__(self, max_hp: int, damage: int, heal: int = 0, mana: int = 0) -> None:
        super().__init__(max_hp, damage, heal, mana)

        self.text = EntityText()
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

        self._image = Image()
        self._image["alive"] = "bocchi.png"
        self._image["dead"] = "bocchi_dead.png"

    def set_text(self, text: EntityText) -> None:
        self.text = text

    @property
    def image(self):
        return self._image["alive"] if self.current_hp > 0 else self._image["dead"]


class Player(EntityStats):
    pass

class Good_boy(EntityStats):
    def __init__(self, max_hp: int, damage: int, heal: int = 0, mana: int = 0) -> None:
        super().__init__(max_hp, damage, heal, mana)

        self.text = EntityText()
        self.text.set(
            "got_hit",
            Text().add(
                "Tsk..."
            ).add(
                "So annoying"
            ).add(
                "Is that all you got"
            ).add(
                "AH..."
            )
        )

        self.text.set(
            "do_hit",
            Text().add(
                "W E A K"
            ).add(
                "let me show you."
            ).add(
                "I'm not holding back."
            )
        )

        self.text.set(
            "do_heal",
            Text().add(
                "Did you think it will end that easily."
            ).add(
                "Not yet"
            ).add(
                "Come Onnnn"
            )
        )

        self._image = Image()
        self._image["alive"] = "good_boy.png"
        self._image["dead"] = "good_boy_dead.jpg"

    def set_text(self, text: EntityText) -> None:
        self.text = text

    @property
    def image(self):
        return self._image["alive"] if self.current_hp > 0 else self._image["dead"]