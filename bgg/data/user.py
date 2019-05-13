class User:
    def __init__(self, user_id, user_name):
        self.name = user_name
        self.id = user_id

    def __str__(self):
        return "name={}, id={}".format(self.name, self.id)
