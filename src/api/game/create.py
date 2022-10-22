from email import header
from quart import request, Blueprint, abort, g
import random
import dataclasses
from api.util.util import _get_db, CORRECT_WORD_BANK, parse_game, process_guess, validate_guess
from api.util.Classes import Guess, Game, User
from quart_schema import validate_request, validate_headers

app_create = Blueprint('app_create', __name__)


@app_create.route('/game/create', methods=['POST'])
@validate_headers(User)
async def create(headers:User):
    '''creates a new game for a given user.  Returns 401 if they are unauthoized to.'''
    headers = dataclasses.asdict(headers)

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

    return {'game_id': id}


@app_create.route('/game/list', methods=['GET'])
@validate_headers(User)
async def get_all_games(headers: User):
    '''gets a list of all the active games for a given user.'''
    headers = dataclasses.asdict(headers)
    user_id = headers['user_id']

    db = await _get_db()
    games = await db.fetch_all(f'SELECT game_id FROM games WHERE user_id LIKE "{user_id}" AND finished=0')

    #converts the games found into a list of ints for the game_id
    games = [int(g.game_id) for g in games]

    return {'game_ids': games}



@app_create.route('/game/<int:id>', methods=['GET'])
@validate_headers(User)
async def get_game(id:int, headers:User):
    '''Gets a single game give the game_id and returns the state of the game.'''
    headers = dataclasses.asdict(headers)
    
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
    guesses = await db.fetch_all(f'SELECT guess, guess_num FROM guesses WHERE game_id={game_id} ORDER BY guess_num ASC')
    if guesses:
        guesses = [g.guess for g in guesses]
    else:
        guesses = []
    
    game = Game(game.game_id, game.user_id, game.guesses_rem, game.word, guesses)
    return parse_game(game)
    


@app_create.route('/game/guess', methods=['POST'])
@validate_request(Guess)
@validate_headers(User)
async def make_guess(data:Guess, headers:User):
    '''checks and verifies that a user gives a valid guess and if so, returns the results of the guess'''
    
    #gets necessary info from the json body and headers
    headers = dataclasses.asdict(headers)
    data = dataclasses.asdict(data)
    guess = data['guess']
    game_id = int(data['game_id'])
    user_id = headers['user_id']

    db = await _get_db()
    
    #gets the status of the game and returns if the game is not found
    game = await db.fetch_one(f'SELECT * FROM games WHERE game_id={game_id} AND user_id="{user_id}" AND finished=0')

    if game is None:
        return abort(401)

    valid, correct = validate_guess(guess, game.word)
    guesses_rem = game.guesses_rem
    #if valid guess was made, decrements guesses_remaining and adds to guesses database
    if valid:
        guesses_rem -= 1
        guess_num = 6 - guesses_rem
        finished = (guesses_rem == 0 or correct)
        #updates the number of guesses remaining
        r = await db.execute(f'UPDATE games SET guesses_rem={guesses_rem}, finished={finished} WHERE game_id={game_id}')
        #adds the guess to the guesses database.
        g_id = await db.execute(f'INSERT INTO guesses(game_id, guess, guess_num) VALUES({game_id}, "{guess}", {guess_num})')
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


    







