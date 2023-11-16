from typing import Any, TypeVar

T = TypeVar("T")


class PersistanceStorage:
    def __init__(self, st):
        self.st = st
        self.session = st.session_state

    def nset(self, key: Any, value: Any) -> None:
        """Set if not exists.

        Args:
            key (Any): The key.
            value (Any): Value.
        """
        if key not in self.session:
            self.session[key] = value

    def gset(self, key: str, value: T) -> T:
        """Get if exists and set if not exists.

        Args:
            key (Any): The key.
            value (T): The value.

        Returns:
            T: The value.
        """
        if key in self.session:
            return self.session[key]

        self.session[key] = value
        return value

    def __getitem__(self, __name: str) -> Any:
        return self.session[__name]

    def __setitem__(self, __name: str, __value: Any) -> None:
        self.session[__name] = __value

    def __contain__(self, item: str) -> bool:
        return item in self.session
