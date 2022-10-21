from quart import g
from quart import current_app
import databases
import sqlite3, sqlalchemy
from api.util.Classes import Game

#just test word bank for now
WORD_BANK = ['hello', 'crane', 'games', 'ghoul']


async def _get_db():
    db = getattr(g, '_wordle_db', None)
    if not db:
        db = g._wordle_db = databases.Database(current_app.config['DATABASE']['URL'])
        await db.connect()
        
    return db


def _check_misplaced(index: int, guess: str, answer: str, correct: list) -> bool:
    '''checks if the letter is misplaced and is not already in a correct spot for duplicate letters.'''
    if index in correct:
        return False
    letter = guess[index]
    for i in range(len(answer)):
        if answer[i] == letter and i not in correct:
            return True
    
    return False

def _process_guess(guess: str, answer: str) -> tuple:
    '''takes in a guess and the correct answer and returns a tuple of correct letters, misplaced letters'''
    correct = []
    misplaced = []
    if len(guess) != len(answer):
        return None, None

    for i in range(len(guess)):
        if guess[i] == answer[i]:
            correct.append(i)
    #done in a separate loop to get all correct letters to make it easier to check for misplaced duplicates
    for i in range(len(guess)):
        if _check_misplaced(i, guess, answer, correct):   #checks if the letter is in wrong place and 
            misplaced.append(i)

    return correct, misplaced


def parse_game(game: Game) -> dict:
    '''takes in game dataclass and processes it to output to end user'''
    #returns if there were no guesses made
    if game.guesses is None:
        return {'guesses_rem': game.guesses_rem, 'guesses': []}

    words = game.guesses.split(',')
    
    #checks if the game is over and returns accordingly.
    if words[-1] == game.word:
        return {'status': 'win', 'num_guesses': 6-game.guesses_rem}
    elif words[-1] != game.word and game.guesses_rem == 0:
        return {'status': 'lost', 'num_guesses': 6}

    result = []
    for w in words:
        correct, misplaced = _process_guess(w, game.word)
        result.append({'guess': w, 'correct': correct, 'misplaced': misplaced})
    
    return {'guesses_rem': game.guesses_rem, 'guesses': result}
    


if __name__ == '__main__':
    game = Game(1, 1234, 4, 'ccane', 'stray,mouse,chace,ccane')   #tests duplicates

    print(parse_game(game))