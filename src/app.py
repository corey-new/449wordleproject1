from venv import create
from quart_schema import QuartSchema
from quart import Quart, g, request
from api.game.create import app_create
import toml


if __name__ == '__main__':
    app = Quart(__name__)
    QuartSchema(app)


    app.register_blueprint(app_create)

    #config app here
    app.config.from_file(f'./config/config.toml', toml.load)

    app.run(debug=True)