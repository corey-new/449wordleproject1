import dataclasses

@dataclasses.dataclass
class Guess:
    game_id: int
    guess: str

@dataclasses.dataclass
class User:
    user_id: str
    username: str

@dataclasses.dataclass
class Game:
    game_id: int
    user_id: str
    guesses_rem: int
    word: str
    guesses: str

@dataclasses.dataclass
class UserAuth:
    username: str
    password: str