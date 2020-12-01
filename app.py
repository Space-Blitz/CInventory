import flask
from flask import jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from models.constants import ENVIRONMENT
from config import app_config
from views.auth import auth
from views.inventory import inventory



app = flask.Flask(__name__)
CORS(app)

app.config.from_object(app_config[ENVIRONMENT])

#jwt configurations
jwt = JWTManager(app)
blacklist = set()

app.register_blueprint(auth)
app.register_blueprint(inventory)

@app.route('/', methods=['GET'])
def home():
    """
    Called every time there is a bad request
    """
    return '''<h1>Inventory | v2</h1>
            <p>Accomodation at ts best.</p>'''


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(400)
def bad_request(e):
    """
    Called every time there is a bad request
    """
    return jsonify(error=str(e.description)), 400


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    """
    Check if a user is logged out
    """
    unique_identifier = decrypted_token['jti']
    return unique_identifier in blacklist



if __name__ == "__main__":
    app.run()
