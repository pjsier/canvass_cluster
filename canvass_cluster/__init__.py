from flask import Flask
from canvass_cluster.views import views
import os

MAPZEN_KEY = os.getenv('MAPZEN_KEY', None)

def create_app():
    app = Flask(__name__)
    app.config['MAPZEN_KEY'] = MAPZEN_KEY
    app.register_blueprint(views)

    return app

# Exposing so can be picked up by Zappa
app = create_app()

if __name__ == "__main__":
    import sys
    app = create_app()
    try:
        port = int(sys.argv[1])
    except (IndexError, ValueError):
        port = 5000
    app.run(debug=True, port=port)
