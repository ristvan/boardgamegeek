class Player:
    def __init__(self):
        self.user_id = None
        self.play_id = None
        self.score = None
        self.name = None
        self.starting_position = None
        self.color = None
        self.rating = None
        self.is_new = False
        self.is_win = False

    def __str__(self):
        return "uid={}/player={}/name={}/score={}/position={}/color={}/rate={}/new={}/win={}".format(
            self.user_id,
            self.play_id,
            self.name,
            self.score,
            self.starting_position,
            self.color,
            self.rating,
            self.is_new,
            self.is_win
        )
