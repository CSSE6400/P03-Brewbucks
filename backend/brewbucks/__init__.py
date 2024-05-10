from os import environ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
 
def create_app(config_overrides=None): 
   app = Flask(__name__) 
 
   app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///db.sqlite")
   if config_overrides: 
       app.config.update(config_overrides)
 
   # Load the models 
   from brewbucks.models import db 
   db.init_app(app) 
 
   # Create the database tables 
   with app.app_context(): 
      db.create_all() 
      db.session.commit() 
 
   # Register the blueprints 
   from brewbucks.views.routes import api 
   app.register_blueprint(api) 
 
   return app