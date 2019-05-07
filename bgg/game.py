class Game:
    def __init__(self):
        self.name = None
        self.id = None

    def __str__(self):
        return "(Game)id={} - name={}".format(self.id, self.name)