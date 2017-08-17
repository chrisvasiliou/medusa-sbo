from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os, ast, configparser
from flask_mail import Mail

# set up Flask
app = Flask(__name__)

# set config
app.config.from_envvar('MEDUSA_DEVELOPMENT_SETTINGS')
# app.config.from_envvar('MEDUSA_TESTING_SETTINGS')
# app.config.from_envvar('MEDUSA_PRODUCTION_SETTINGS')

# choose which part of the config file to load. default to dev config if the environmental var doesn't exist
# config_file = os.getenv('MEDUSA_CONFIG', '/var/lib/medusa/medusa-development.ini')

# configparser handles everything as strings so some additional conversion work is needed
# config = configparser.ConfigParser()
# prevent configparser from converting to lowercase
# config.optionxform = str
# read in config from ini
# config.read(config_file)

# convert the job list to a python dictionary object and load. this is special because it contains \n characters that need removing
# we do this via literal_eval, i.e. 'True' becomes a python True and '"string"' becomes a python "string"
# app.config['JOBS'] = ast.literal_eval(config['flask']['JOBS'].replace('\n',''))
# config['flask'].pop('JOBS')

# load remaining values
# convert the strings to python objects
# for key in config['flask']:
#    app.config[key] = ast.literal_eval(config['flask'][key])

# initialise database models
db = SQLAlchemy(app)

# initialise Flask-Mail
mail = Mail(app)

from flask_security import Security, SQLAlchemyUserDatastore
from app.models.users import User, Role

#Set up flask_security
# app.config['DEBUG'] = True
# app.config['SECURITY_CONFIRMABLE'] = True
# app.config['SECURITY_REGISTERABLE'] = True
# app.config['SECURITY_RECOVERABLE'] = True
# app.config['SECURITY_TRACKABLE'] = True
# app.config['SECRET_KEY'] = config['security']['key_gen']
# app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
# app.config['SECURITY_PASSWORD_SALT'] = config['security']['salt']
# app.config['SECURITY_EMAIL_SENDER'] = config['configurations']['notify_email']
# app.config['SECURITY_CHANGEABLE'] = True
# app.config['SECURITY_POST_CHANGE_VIEW'] = '/'

app.config['SECURITY_POST_CHANGE_VIEW'] = '/'
app.config['SECURITY_POST_RESET_VIEW'] = '/'
app.config['SECURITY_POST_CONFIRM_VIEW'] = 'security.change_password'

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# set up database connection registry
from app.models import SessionRegistry
registry = SessionRegistry()

# set up event handler
from app.event_handler import EventHandler
event = EventHandler()

# Setup Flask-User to handle user account related forms
from flask_user import UserManager, SQLAlchemyAdapter
from app.models import User
db_adapter = SQLAlchemyAdapter(db, User)  # Setup the SQLAlchemy DB Adapter
user_manager = UserManager(db_adapter, app)  # Init Flask-User and bind to app

# set up bugsnag
import bugsnag
from bugsnag.flask import handle_exceptions
bugsnag.configure(
  api_key = app.config['BUGSNAG_API_KEY'],
  project_root = app.config['PROJECT_ROOT'],
  notify_release_stages = app.config['NOTIFY_RELEASE_STAGES'],
  release_stage = app.config['RELEASE_STAGE']
)
handle_exceptions(app)

# import the remaining. in particular, all views and models must be imported, as well as anything with a decorator
# packages
from app import models, add, admin, cmms, weather, algorithms, reports, scheduling
# modules
from app import controllers

