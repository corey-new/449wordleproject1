from quart import request, Blueprint, abort, g
import random
import dataclasses
from api.util.util import _get_db, VALID_WORD_BANK, CORRECT_WORD_BANK, parse_game, process_guess, validate_guess
from api.util.Classes import Guess, Game
from quart_schema import validate_request, DataSource

app_create = Blueprint('app_create', __name__)


@app_create.route('/game/create', methods=['POST'])
async def create():
    '''creates a new game for a given user.  Returns 401 if they are unauthoized to.'''
    headers = request.headers
    if 'user_id' not in headers:
        abort(401)

    user_id = str(headers['user_id'])

    #gets user and validates userid
    db = await _get_db()
    user = await db.fetch_one(f'SELECT * FROM users WHERE user_id="{user_id}"' )

    if not user:
        return abort(401)
    else:
        #generates a random word and creates a new game entry in the database
        random_word = random.choice(CORRECT_WORD_BANK)
        query = f'INSERT INTO games(user_id, word) VALUES("{user_id}", "{random_word}")'
        id = await db.execute(query)    #id = gameid
    
    if id == -1:
        return abort(500)

    return {'game_id': id}, 201


@app_create.route('/game/<int:id>', methods=['GET'])
async def get_game(id:int):
    '''Gets a single game give the game_id and returns the state of the game.'''
    headers = request.headers
    
    if 'user_id' not in headers:
        return abort(401)

    game_id = int(id)    
    user_id = headers['user_id']

    #gets db and searches for game
    db = await _get_db()
    game = await db.fetch_one(f'SELECT * FROM games WHERE game_id={game_id} AND user_id="{user_id}"')

    if not game:
        return {}
    
    #gets guesses from table
    guesses = await db.fetch_all(f'SELECT guess, guess_num FROM guesses WHERE game_id={game_id} ORDER BY guesses_num ASC')

    if guesses:
        guesses = [g.guess for g in guesses]
    else:
        guesses = []
    
    game = Game(game.game_id, game.user_id, game.guesses_rem, game.word, guesses)
    
    return parse_game(game)
    


@app_create.route('/game/guess', methods=['POST'])
@validate_request(Guess)
async def make_guess(data):
    '''checks and verifies that a user gives a valid guess and if so, returns the results of the guess'''
    headers = request.headers
    
    #gets necessary info from the json body
    data = dataclasses.asdict(data)
    game_id = int(data['game_id'])
    user_id = headers['user_id']

    db = await _get_db()
    
    #gets the status of the game and returns if the game is not found
    game = await db.fetch_one(f'SELECT * FROM games WHERE game_id={game_id} AND user_id="{user_id}"')

    if game is None:
        return abort(401)

    valid, correct = validate_guess(data['guess'], game.word)
    guesses_rem = game.guesses_rem
    #if valid guess was made, decrements guesses_remaining
    if valid:
        guesses_rem -= 1
        r = await db.execute(f'UPDATE games SET guesses_rem={guesses_rem} WHERE game_id={game_id}')
        if r == -1:
            return abort(500)   #error with updating table

    result = {'game_id': game_id, 'valid': valid, 'guesses_remaining': guesses_rem}
    
    #adds optional parameters if a valid guess was made
    c_letters, m_letters = process_guess(data['guess'], game.word)
    if valid and not correct:
        result['correct_guess'] = correct
        result['correct'] = c_letters
        result['misplaced'] = m_letters
    elif valid and correct:
        result['correct_guess'] = correct
    
    return result


    







