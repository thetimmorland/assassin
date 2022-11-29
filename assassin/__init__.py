import os

from dotenv import load_dotenv
from flask import Flask, render_template
from werkzeug.exceptions import InternalServerError
from werkzeug.middleware.proxy_fix import ProxyFix

import assassin.auth
import assassin.cli
import assassin.db
import assassin.game


def create_app(test_config=None):
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, "assassin.sqlite"),
    )

    load_dotenv()
    app.config.from_prefixed_env()

    if test_config is not None:
        app.config.update(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.errorhandler(InternalServerError)
    def handle_exception(e):
        response = e.get_response()
        return render_template("error.html")

    assassin.db.init_app(app)
    assassin.cli.init_app(app)

    app.register_blueprint(assassin.auth.bp)
    app.register_blueprint(assassin.game.bp)

    return app
