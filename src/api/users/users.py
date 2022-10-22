import dataclasses
import sqlite3
from quart import request, abort, Blueprint
from quart_schema import validate_request
import uuid
from api.util.util import _get_db
from api.util.Classes import UserAuth
import dataclasses


app_users = Blueprint('app_users', __name__)

@app_users.route("/register", methods=['POST'])
@validate_request(UserAuth)
async def register(data:UserAuth):
    form = dataclasses.asdict(data)
    user = {}
    user["user_id"] = str(uuid.uuid1())
    user["password"] = form['password']
    user['username'] = form['username']
    db = await _get_db()
    try:
        res = await db.execute(
            """
            INSERT INTO users(user_id, username, password)
            VALUES(:user_id,:username,:password)
            """,user
        )
    except sqlite3.IntegrityError as e:
        abort(409, "user already exists.")

    return user,201

@app_users.route("/checkPassword", methods=['GET'])
async def check():
    '''Performs simple auth to authenticate a user.'''
    username = ''
    password = ''
    if request.authorization:
        username = request.authorization.username
        password = request.authorization.password
        
    db = await _get_db()
    users = await db.fetch_one(f'SELECT * FROM users WHERE username LIKE "{username}" AND password LIKE "{password}"')
    
    #if user is not None, that means a valid user was found with same credentials
    if users is not None:
        return {"authenticated" : True}
    else:
        return "invalid login", 401, {'WWW-Authenticate' : 'Basic Realm = "Login Required"'}
    

