from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy as sa


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


users_in_community = db.Table('users_in_community',
                              db.Column('community_id', db.Integer,
                                        db.ForeignKey('communities.id')),
                              db.Column('user_id', db.Integer,
                                        db.ForeignKey('user.id'))
                              )

# TODO: Move all class files into this file and setup models to initialize DB tables etc.
#   Currently having issues with import loop ie importing db from index and then importing User from models
#   Restructuring should resolve this issue
#   Need help from Dr. Layman regarding the best way to go about this (?)


class User(db.Model, UserMixin):
    # id = db.Column(db.Integer, unique=True, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    #communities = db.Column(db.BLOB)
    #collections = db.Column(db.BLOB)
    admin = db.Column(db.Boolean)
    profile_picture = db.Column(db.BLOB)
    bio = db.Column(db.VARCHAR)
    posts = db.relationship('Posts', backref='author', lazy=True)
    collections = db.relationship(
        'Collections', backref='collectionAuthor', lazy=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

    def getUserInfo(self):
        user = db.get_or_404(User, self.id)
        return user

    def __repr__(self):
        return f'<User {self.username}, {self.email}, {self.password}>'


class CollectionItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    desc = db.Column(db.String)
    collection_id = db.Column(db.Integer, db.ForeignKey(
        'collections.id'), nullable=False)

    def __init__(self, user, community, photo, text, collection, likes, dislikes, likers, dislikers):
        self.collection = collection
        self.user = user
        self.community = community
        self.photo = photo
        self.text = text
        self.likes = 0
        self.dislikes = 0
        self.likers = []
        self.dislikers = []

    def add_like(self):
        self.likes += 1
        return(self.likes)
    def add_dislike(self):
        self.disliskes += 1
        return (self.disliskes)
    def add_like(self,user_who_liked):
        if user_who_liked not in self.likers():
            self.likers.append(user_who_liked)
            self.likes += 1
            return self.likes
        else:
            self.likers.remove(user_who_liked)
            self.likes -= 1
            return self.likes
    def add_dislike(self,user_who_disliked):
        if user_who_disliked not in self.dislikers():
            self.dislikers.append(user_who_disliked)
            self.dislikes += 1
            return self.dislikes
        else:
            self.dislikers.remove(user_who_disliked)
            self.dislikes -= 1
            return self.dislikes




class Collections(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    desc = db.Column(db.String)
    owner = db.Column(db.Integer)
    items = db.relationship('Items', backref='collections', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    community_id = db.Column(
        db.Integer, db.ForeignKey('communities.id'), nullable=False)
    def __init__(self, community, user):
        self.user = user
        self.community = community
        self.items = []



class Communities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    desc = db.Column(db.String)
    collections = db.relationship(
        'Collections', backref='communities', lazy=True)

    users_in_communities = db.relationship(
        'User', secondary=users_in_community, backref='users')



class Photos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_blob = db.Column(db.BLOB)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    body = db.Column(db.String)
    meta = db.Column(db.String)
    responses = db.Column(db.BLOB)
    item = db.Column(db.String)
