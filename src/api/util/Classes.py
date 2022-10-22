import dataclasses

@dataclasses.dataclass
class Guess:
    game_id: int
    guess: str


@dataclasses.dataclass
class Game:
    game_id: int
    user_id: str
    guesses_rem: int
    word: str
    guesses: str