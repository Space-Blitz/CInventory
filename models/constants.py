import os


"""
Database variables
"""
DATABASE_URL=os.getenv('DATABASE_URL')

"""
Email variables
"""
MAIL_SERVER=os.getenv('MAIL_SERVER')
MAIL_PORT=os.getenv('MAIL_PORT')
MAIL_USE_TLS=os.getenv('MAIL_USE_TLS')
MAIL_USE_SSL=os.getenv('MAIL_USE_SSL')
MAIL_USERNAME=os.getenv('MAIL_USERNAME')
MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')

"""
Redirect urls
"""
REDIRECT_URL=os.getenv('REDIRECT_URL')

"""
JWT variables
"""
JWT_SECRET_KEY=os.getenv('SECRET_KEY')


"""
Environment variables
"""
ENVIRONMENT=os.getenv('ENVIRONMENT')

"""
Frontend url
"""
FRONTEND_URL=os.getenv('FRONTEND_URL')

"""
FLUTTERWAVE KEYS
"""
MM_URL=os.getenv('MM_URL')
FL_KEY=os.getenv('FL_KEY')
SECRET_HASH=os.getenv('SECRET_HASH')

