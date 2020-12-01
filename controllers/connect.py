import requests

import psycopg2
import psycopg2.extras
from flask import jsonify, abort
from flask_jwt_extended import create_access_token, get_jwt_identity



import datetime
import time
from  uuid import uuid4

from models.constants import DATABASE_URL

currency = 'UGX'
class Database():
    """
    Handle database connections
    """

    
    def __init__(self):
        """
        initialise database connection
        """
        connection = psycopg2.connect(DATABASE_URL)
        connection.autocommit = True
        self.cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        self.create_tables()
    
    def __del__(self): 
        """
        Close database connection
        """
        self.cursor.close()


    def create_tables(self):
        """
        Create necessary tables in database
        params:n/a
        returns:n/a
        """
        sql_command = """
            CREATE TABLE IF NOT EXISTS users(
                user_id SERIAL PRIMARY KEY,
                surname VARCHAR (250) NOT NULL,
                othernames VARCHAR (250) NOT NULL,
                email VARCHAR (250) NOT NULL UNIQUE,
                password VARCHAR (250) NOT NULL,
                date_created TIMESTAMP NULL,
                admin BOOLEAN NOT NULL DEFAULT FALSE,
                is_active BOOLEAN NOT NULL DEFAULT TRUE
            );
            CREATE TABLE IF NOT EXISTS items(
                id SERIAL PRIMARY KEY,
                item_name VARCHAR (250) NOT NULL,
                user_id INT NOT NULL,
                price INT NOT NULL,
                number_added INT NOT NULL,
                time TIMESTAMP NOT NULL,
                description VARCHAR (250) NOT NULL
            );
		"""
        self.cursor.execute(sql_command)
        self.insert_admin_user()


    
    def populate_default_data(self,sql_command1,sql_command2):
        """
        Enter Default data to database
        """
        table_empty = self.execute_query(sql_command1)
        if not table_empty[0]['exists']:
            self.cursor.execute(sql_command2)



    def insert_admin_user(self):
        """
        create an admin if non existent
        params:n/a
        returns:n/a
        """
        sql_command = """
        INSERT INTO users (surname,othernames,email,password,date_created,admin) 
        values ('Admin1','Saed','i-sendit@gmail.com','doNot2114',now(),'t');
        INSERT INTO users (surname,othernames,email,password,date_created,admin) 
        values ('Test','User','meKendit@gmail.com','ddwoNot2114',now(),'f');
        """# inserts admin user and  one test user
        
        sql_command1 = """
        SELECT EXISTS(SELECT TRUE FROM users where admin='true');
        """# check if there is any user in the database
        self.populate_default_data(sql_command1,sql_command)

    def execute_query(self, sql_command):
        """
        Execute query
        params: sql query statement
        returns: result
        """
        self.cursor.execute(sql_command)
        rows_returned = self.cursor.fetchall()

        return rows_returned

    def get_from_users(self, column, email, extra_params=''):
        """
        Get column from users table
        params:column name, username
        returns:password
        """
        sql_command="""
        SELECT {column} FROM users where email='{email}' {extra_params};
        """.format(email=email, column=column, extra_params=extra_params)
        db_value = self.execute_query(sql_command)
        if not db_value:
            abort(400, description="Invalid username or password.")
        return db_value[0]
    

    def validate_user_login(self,email,password):
        """
        Check if password password is equal to password in database
        """
        user = self.get_from_users('user_id,password,surname,email,admin',email,"and password = '"+password+"'")

        surname= user.get('surname')
        admin = user.get('admin')
        access_token = create_access_token(
            identity={
            'surname':surname,
            'user_id':user.get('user_id'),
            'admin':admin,
            'email':email,

            },
            expires_delta=datetime.timedelta(days=40)
        )

        return {'token': access_token,'email':email,'username':surname} 


    def signup(self,email,password,surname, othernames):
        """
        Sign up a user
        """
        insert_query="""
        INSERT INTO users (surname,othernames,email,password,date_created,admin) 
        values ('{surname}','{othernames}','{email}','{password}',now(),'f');\
        """.format(
            email=email,
            password=password,
            surname=surname,
            othernames=othernames

        )#sql query for inserting new users
        
        try:
            self.cursor.execute(insert_query)
            token = create_access_token(
            identity={
            'surname':surname,
            'email':email,

            'activation':True
            },
            expires_delta=datetime.timedelta(days=4000)
            )
            return token
        except Exception as identifier:
            print(str(identifier))

            abort(400,description="user already exists")#aborts in case user email already exists

    def update_item(self,data, doc_id):
        """
        Update item in database
        """
        user_info = get_jwt_identity()
        user_id = user_info.get('user_id')
        description = data.get('description')
        rooms = data.get('rooms')
        price= data.get('price')
        number_added = data.get('number_added')
        name = data.get('name')
        
        
        update_query="""
        update items  
        set item_name='{name}',
        description='{description}',
        number_added='{number_added}',
        price='{price}'
        where id = '{id}'
        """.format(
            name=name,
            price=price,
            description=description,
            number_added=number_added,
            user_id=user_id,
            id=doc_id
        )#sql query for inserting new users
        
        try:
            self.cursor.execute(update_query)
            return True
        except Exception as identifier:
            print(str(identifier))
            abort(400,description=str(identifier))#aborts in case user email already exists


    def insert_item_into_inventory(self,data):
        """
        Insert items into inventory
        """



        user_info = get_jwt_identity()
        user_id = user_info.get('user_id')
        description = data.get('description')
        rooms = data.get('rooms')
        price= data.get('price')
        number_added = data.get('number_added')
        name = data.get('name')
        
        
        insert_query="""
        INSERT INTO items (item_name,user_id, price, number_added,time,description) 
        values ('{name}','{user_id}',{price},'{number_added}',now(),'{description}');
        """.format(
            name=name,
            price=price,
            description=description,
            number_added=number_added,
            user_id=user_id
        )#sql query for inserting new users
        
        try:
            self.cursor.execute(insert_query)
            return True
        except Exception as identifier:
            print(str(identifier))

            abort(400,description=str(identifier))#aborts in case user email already exists
        
    def delete_item(self,table_name, doc_id):
        """Deletes item from database
        """
        try:
            delete_query="""
            delete from {table} where id  ='{doc_id}'
            """.format(
            doc_id=doc_id,
            table=table_name
            )
            self.cursor.execute(delete_query)
        except Exception as error:
            print(str(error))
            abort(400, description="Failed to delete.")
        
    
    def get_all_items(self):
        """
        Get all items
        """
        user_info=get_jwt_identity()
        user_id = user_info.get('user_id')
        is_admin = user_info.get('admin')
        transactions_query="""
        select items.*, users.surname from items
        join users on items.user_id=users.user_id
        """
        if not is_admin:
            transactions_query+=" where items.user_id='{user_id}'".format(user_id=user_id)
        return self.execute_query(transactions_query)
    
    def get_item(self, doc_id):
        """
        Get one item
        """
        user_info=get_jwt_identity()
        user_id = user_info.get('user_id')
        is_admin = user_info.get('admin')
        transactions_query="""
        select items.item_name as name,items.*, users.surname from items
        join users on items.user_id=users.user_id
        """
        if not is_admin:
            transactions_query+=" where items.user_id='{user_id}'".format(user_id=user_id)
        transactions_query+=" and items.id='{doc_id}'".format(doc_id=doc_id)
        return self.execute_query(transactions_query)





db = Database()
