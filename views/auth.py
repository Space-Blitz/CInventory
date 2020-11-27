from flask_jwt_extended import (
    jwt_required, 
    get_jwt_identity,
    create_access_token,
    decode_token
)
from flask import Blueprint, Response, request, jsonify, abort, redirect

import time

from models.constants import FRONTEND_URL
from models.fields import LOGIN, REGISTER
from controllers.validator import check_for_required_values
from controllers.connect import db
from controllers.emails import Emails
from controllers.extensions import task_after_function


auth = Blueprint('auth', __name__)
blacklist=set()

# doctype_credit = 'credit'

@auth.route('/api/v1/auth/login', methods=['POST'])
def login():
    """
    Login a user
    returns: user data
    """
    data = request.get_json()
    check_for_required_values(data, LOGIN)
    access_token = db.validate_user_login(data.get('email'),data.get('password'))
    return jsonify({'message':'Successful login.','user':access_token}), 200


@auth.route('/api/v1/auth/register', methods=['POST'])
def register():
    """
    Login a user
    returns: user data
    """
    data = request.get_json()
    check_for_required_values(data, REGISTER)
    access_token = db.signup(
        data.get('email'),
        data.get('password'),
        data.get('surname'),
        data.get('othernames'),
        data.get('contact')
    )
    task_after_function(  # Create a daemonic process with heavy function
        target=Emails.send_registration_email,
        args=[data.get('email'),data.get('surname'), data.get('password'), data.get('contact'), data.get('othernames'),access_token,],
        daemon=True
    ).start()
    return jsonify({'message':'Successful registration. Please login'}), 200

@auth.route('/api/v1/auth/register/<token>/activate', methods=['GET'])
def activate_email(token):
    """
    Activate a user after registration
    returns: user data
    """
    try:
        user = decode_token(token).get('identity')
        email = user.get('email')
        surname = user.get('surname')
        if user.get('activation'):
            db.activate_user(email)
            task_after_function(  # Create a daemonic process with heavy function
                target=Emails.send_activation_email,
                args=[email,surname,],
                daemon=True
            ).start()
            print(FRONTEND_URL)
            return redirect(FRONTEND_URL)
        abort(400, description="invalid activation token.")

    except Exception as identifier:
        abort(400, description="invalid activation token.")
    

@auth.route('/api/v1/auth/request-password-reset', methods=['POST'])
def request_to_reset_password():
    """
    Login a user
    returns: user data
    """
    return jsonify({'message':'Lift off'}), 200

@auth.route('/api/v1/auth/reset-password', methods=['PATCH'])
def reset_password():
    """
    Login a user
    returns: user data
    """
    return jsonify({'message':'Lift off'}), 200


@auth.route("/api/v2/logout", methods=['POST'])
@jwt_required
def logout():
    """
    logout user and dismiss refresh token
    """
    response = jsonify({'logged out':True})
    unique_identifier = get_raw_jwt()['jti']
    blacklist.add(unique_identifier)
    return response, 200

