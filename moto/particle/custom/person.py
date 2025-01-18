class person:
    def __init__(
        self,
        name=None,
        age=None,
        gender=None,
        photo=None,
    ):
        self.name = name
        self.age = age
        self.gender = gender
        self.photo = photo

    def __str__(self):
        return self.name
