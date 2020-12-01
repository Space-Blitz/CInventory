from flask_jwt_extended import (
    jwt_required, 
    get_jwt_identity,
    create_access_token,
    decode_token
)
from flask import Blueprint, Response, request, jsonify, abort, redirect

import time

from models.fields import LOGIN, REGISTER
from controllers.validator import check_for_required_values
from controllers.connect import db


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
    return jsonify({'message':'Successful registration. Please login'}), 200



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

