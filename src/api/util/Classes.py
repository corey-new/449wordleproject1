import dataclasses

@dataclasses.dataclass
class Users:
    user_id: str
    email: str
    password: str

@dataclasses.dataclass
class Game:
    game_id: int
    user_id: int
    guesses_rem: int
    word: str
    guesses: str