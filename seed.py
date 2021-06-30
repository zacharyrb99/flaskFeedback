from re import U
from models import db, User, Feedback
from app import app

#create tables
db.drop_all()
db.create_all()