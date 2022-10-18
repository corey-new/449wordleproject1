from venv import create
from quart_schema import QuartSchema
from quart import Quart, g, request
from api.game.create import app_create


if __name__ == '__main__':
    app = Quart(__name__)
    QuartSchema(app)


    app.register_blueprint(app_create)

    #config app here
    pass


    app.run(debug=True)