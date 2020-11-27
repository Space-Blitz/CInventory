"""
handles all money related transactions
"""
from controllers.connect import db


class Transactions():
    @staticmethod
    def initialize_mobile_money(data):
        """
        Initializes mobile money payments and stores object in db
        """
         