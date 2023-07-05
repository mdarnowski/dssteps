from flask_login import login_user
from models.alchemy import User, db


def login(user_id):
    user = User.query.get(user_id)
    if user is None:
        user = User(id=user_id)
        db.session.add(user)
        db.session.commit()
    login_user(user)
