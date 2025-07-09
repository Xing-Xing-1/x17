from typing import Any, Dict

class Attributes:
    """
    Base class representing runtime attributes of Docker resources.
    
    """
    
    @classmethod
    def from_dict(
        cls, 
        data: Dict[str, Any]
    ) -> "Attributes":
        return cls(**data)
    
    def __init__(
        self, 
        **kwargs: Any,
    ):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self) -> Dict[str, Any]:
        return dict(self.__dict__)
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, dict):
            return self.to_dict() == other
        if isinstance(other, Attributes):
            return self.to_dict() == other.to_dict()
        return False

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)
    


    
