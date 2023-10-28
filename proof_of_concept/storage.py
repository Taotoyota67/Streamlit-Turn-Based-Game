from typing import Any, TypeVar

T = TypeVar("T")


class PersistanceStorage:
    def __init__(self, st):
        self.st = st
        self.session = st.session_state
    
    def gset(self, key: Any, value: T) -> T:
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