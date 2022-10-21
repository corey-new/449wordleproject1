from quart import request, Blueprint, abort, g
import random
from api.util.util import _get_db, WORD_BANK, parse_game
from api.util.Classes import Users, Game


app_create = Blueprint('app_create', __name__)

@app_create.route('/game/create', methods=['POST'])
async def create():
    '''creates a new game for a given user.  Returns 401 if they are unauthoized to.'''
    headers = request.headers
    if 'user_id' not in headers:
        abort(401)

    user_id = int(headers['user_id'])

    #gets user and validates userid
    db = await _get_db()
    user = await db.fetch_one(f'SELECT * FROM users WHERE user_id={user_id}' )

    if not user:
        return abort(401)
    else:
        #generates a random word and creates a new game entry in the database
        random_word = random.choice(WORD_BANK)
        query = f'INSERT INTO games(user_id, word) VALUES("{user_id}", "{random_word}")'
        id = await db.execute(query)    #id = gameid
    
    if id == -1:
        return abort(500)

    return {'game_id': id}



@app_create.route('/game/<int:id>', methods=['GET'])
async def get_game(id):
    '''Gets a single game give the game_id and returns the state of the game.'''
    headers = request.headers
    
    if 'user_id' not in headers:
        return abort(401)

    game_id = int(id)    
    user_id = int(headers['user_id'])

    #gets db and searches for game
    db = await _get_db()
    game = await db.fetch_one(f'SELECT * FROM games WHERE game_id={game_id} AND user_id={user_id}')

    if not game:
        return {}
    
    game = Game(game.game_id, game.user_id, game.guesses_rem, game.word, game.guesses)
    
    return parse_game(game)
    



