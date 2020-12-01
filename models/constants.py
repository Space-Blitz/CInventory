import os


"""
Database variables
"""
DATABASE_URL=os.getenv('DATABASE_URL')


"""
Development Environment
"""
ENVIRONMENT=os.getenv('ENVIRONMENT')


"""
Secret Key for authentication
"""
JWT_SECRET_KEY=os.getenv('SECRET_KEY')

