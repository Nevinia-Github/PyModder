class Project:
    def __init__(self, name):
        self.name = name

    @classmethod
    def new(cls):
        return Project("Untitled")