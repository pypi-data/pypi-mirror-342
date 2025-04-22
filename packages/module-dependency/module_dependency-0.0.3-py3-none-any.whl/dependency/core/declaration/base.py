from abc import ABC

class ABCComponent(ABC):
    def __init__(self, base_cls: type) -> None:
        self.base_cls: type = base_cls
    
    def __repr__(self) -> str:
        return self.base_cls.__name__

class ABCProvider(ABC):
    def __init__(self, provided_cls: type) -> None:
        self.provided_cls: type = provided_cls

    def __repr__(self) -> str:
        return self.provided_cls.__name__

class ABCDependent(ABC):
    def __repr__(self) -> str:
        return self.__class__.__name__