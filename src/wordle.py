
import dataclasses
import sqlite3
import databases
from quart import Quart, g, request, abort
from quart_schema import QuartSchema, RequestSchemaValidationError, validate_request
from sqlalchemy import true
import toml
import uuid

app = Quart(__name__)
QuartSchema(app)

app.config.from_file(f"./etc/{__name__}.toml", toml.load)

print(app.config["DATABASES"]['URL'])


async def _get_db():
    db = getattr(g, "_sqlite_db", None)
    if db is None:
        db = g._sqlite_db = databases.Database(app.config["DATABASES"]["URL"])
        await db.connect()
    return db


@app.teardown_appcontext
async def close_connection(exception):
    db = getattr(g, "_sqlite_db", None)
    if db is not None:
        await db.disconnect()

@app.route("/") 
def index():
    return "hello world"

@app.route("/register", methods=['POST'])
async def register():
    user = await request.get_json()
    user["id"] = str(uuid.uuid1())
    
    db = await _get_db()
    try:
        res = await db.execute(
            """
            INSERT INTO users(id, username, password)
            VALUES(:id,:username,:password)
            """,user
        )
    except sqlite3.IntegrityError as e:
        abort(409, e)

    return user,201

@app.route("/checkPassword/<username>/<password>", methods=['GET'])
async def check(username, password):

    if request.authorization and request.authorization.username == username and request.authorization.password == password:
        return {"authenticated" : True}
    else:
        return "", 401, {'WWW-Authenticate' : 'Basic Realm = "Fake Realm"'}
    










    # db = await _get_db()
    # data = await request.get_json()
    # email = data['email']
    # password = data['password']
    # user = await db.fetch_one("SELECT * FROM users WHERE email = :email", values={"email": email})
    # value = requests.get(f'http://localhost:5000/login/')
    # print(value)
    #print(dict(user))
    #/ return {"Login":True}