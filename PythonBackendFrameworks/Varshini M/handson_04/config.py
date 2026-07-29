class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///courses.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'flask-coursemanager-secret'
    DEBUG = True
