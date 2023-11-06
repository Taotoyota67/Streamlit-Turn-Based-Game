

class Entity:
    def __init__(self, **kwargs) -> None:
        """Initialize when enter a combat.

        Kwargs:
            damage (float): entity damage.
            defense (float): entity defense.
            hp (float): entity health.
            mana (float): entity mana.
        """
        self.damage = kwargs.get("damage", 0)

        hp = kwargs.get("hp", 0)
        self.health = hp
        self.max_health = hp

        self.defense = kwargs.get("defense", 0)

        mana = kwargs.get("mana", 0)
        self.mana = mana
        self.max_mana = mana

        # [[duration (turns), value], ...]
        # value > 0; heal
        # value < 0; damage
        self._effects = []

    @property
    def is_alive(self) -> bool:
        """Is entity alive?

        Returns:
            bool: alive.
        """
        return self.health > 0

    def tick(self) -> None:
        """Applied one tick of combat state. (Poison, Mana regen, etc.)
        """
        # Increase mana by 5% of max mana every turns.
        self.increase_mana(self.max_mana * 0.05)

        for index, value in enumerate(self._effects):
            # Take effect
            if value[1] > 0:
                self.increase_health(value[1])
            else:
                self.reduce_health(value[1])

            # Reduce poison turns
            self._effects[index][0] -= 1

        # Clear out poison if duration ran out
        self._clear_ran_out_effects()

    def add_effect(self, duration: int, value: float) -> None:
        """_summary_
        """

    def clear_effects(self) -> None:
        """Clear all effects.
        """
        self._effects = []

    def _clear_ran_out_effects(self) -> None:
        """Clear ran out effects.
        """
        self._effects = [
            i for i in self._effects if i[0] > 0]

    def set_health(self, health: float) -> None:
        """Set entity current health. (Cannot exceed max health)

        Args:
            health (float): amount of health.
        """
        self.health = min(health, self.max_health)

    def set_max_health(self, health: float) -> None:
        """Set entity max health (will NOT change current health)

        Args:
            health (float): amount of health.
        """
        self.max_health = health

    def increase_health(self, amount: float) -> None:
        """Increase entity current health. (Cannot exceed max health)

        Args:
            amount (float): amount of health to increase.
        """
        self.health = min(self.health + amount, self.max_health)

    def increase_max_health(self, amount: float) -> None:
        """Increase entity max health (Will also increase current health)

        Args:
            amount (float): amount of health to increase.
        """
        self.max_health += amount
        self.health += amount

    def reduce_health(self, amount: float) -> None:
        """Reduce entity current health (Will not goes below 0)

        Args:
            amount (float): amount of health to reduce.
        """
        self.health = max(self.health - amount, 0)

    def reduce_max_health(self, amount: float) -> None:
        """Reduce entity max health.
        Max health will not go below 1.
        (Will also reduce current health, entity will not die from this)

        Args:
            amount (float): amount of max health to reduce.
        """
        self.max_health = max(self.max_health - amount, 1)
        self.health = max(self.health - amount, self.max_health)

    def set_mana(self, mana: float) -> None:
        """Set entity current mana. (Will not exceed max mana)

        Args:
            mana (float): amount of mana.
        """
        self.mana = min(mana, self.max_mana)

    def set_max_mana(self, mana: float) -> None:
        """Set entity max mana (Will NOT change current mana)

        Args:
            mana (float): amount of mana.
        """
        self.max_mana = mana

    def increase_mana(self, amount: float) -> None:
        """Increase entity current mana (Will not exceed max_mana)

        Args:
            amount (float): amount of mana.
        """
        self.mana = min(self.mana + amount, self.max_mana)

    def increase_max_mana(self, amount: float) -> None:
        """Increase entity max mana (Will also increase current mana)

        Args:
            amount (float): amount of mana.
        """
        self.max_mana += amount
        self.mana += amount

    def reduce_mana(self, amount: float) -> None:
        """Reduce entity current mana (Will not goes below 0)

        Args:
            amount (float): _description_
        """
        self.mana = max(self.mana - amount, 0)

    def reduce_max_mana(self, amount: float) -> None:
        """Reduce entity max mana.
        Max mana will not goes below 0
        (Will also reduce current mana, will not goes below max mana.)

        Args:
            amount (float): _description_
        """
        self.max_mana = max(self.max_mana - amount, 0)
        self.mana = max(self.mana - amount, self.max_mana)

    def got_hit(self, damage: float) -> None:
        """Deal damage to this entity, Will calculate defense inside this function.

        Args:
            damage (float): amount of damage.
        """
        damage *= 1 - (self.defense / (self.defense + 9))
        self.reduce_health(damage)
