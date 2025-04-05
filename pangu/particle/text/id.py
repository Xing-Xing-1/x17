import re
import uuid
import random 
import string

class Id:
    """
    Id class to represent a unique identifier for a particle.
    
    """
    @staticmethod
    def uuid(length: int = 8) -> str:
        """
        Generate a UUID string of the specified length.
        
        """
        return str(uuid.uuid4())[:length]
    

    def __init__(self, id: str = ''):
        self.id = id or self.uuid()


    