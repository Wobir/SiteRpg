from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Player(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), unique = True,
                         nullable = False)
    password = db.Column(db.String(16), nullable = False)
    hit_points = db.Column(db.Integer, default = 100)
    money = db.Column(db.Integer, default = 500)
    exp = db.Column(db.Integer, default = 0)
    level = db.Column(db.Integer, default = 1)
    weapon_id = db.Column(db.Integer,
                          db.ForeignKey("weapon.id"),
                          nullable = False, default = 1)

class Weapon(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    damage = db.Column(db.Integer, default = 10)
    defense = db.Column(db.Integer, default = 10)

    players = db.relationship('Player',
                              backref = "weapon",
                              lazy = "dynamic")