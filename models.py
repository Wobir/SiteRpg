from flask_sqlalchemy import SQLAlchemy
import datetime
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
    
    inventory = db.relationship("PlayerItem", backref = "owner", lazy = "dynamic")

class Weapon(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    damage = db.Column(db.Integer, default = 10)
    defense = db.Column(db.Integer, default = 10)

    players = db.relationship('Player',
                              backref = "weapon",
                              lazy = "dynamic")
  
class ShopItem(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    item_type = db.Column(db.String(), nullable = False)
    price = db.Column(db.Integer, nullable = False)
    
    healing_amount = db.Column(db.Integer, default = 0)
    
    weapon_id = db.Column(db.Integer, db.ForeignKey("weapon.id"), nullable = True)
    
    min_level = db.Column(db.Integer, default = 1)
    
class PlayerItem(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    item_id = db.Column(db.Integer, db.ForeignKey("shop_item.id"))
    quantity = db.Column(db.Integer, default = 1)
    
class Monster(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), nullable = False)
    health = db.Column(db.Integer, default = 50)
    damage = db.Column(db.Integer, default = 10)
    defense = db.Column(db.Integer, default = 5)
    exp_reward = db.Column(db.Integer, default = 20)
    gold_reward = db.Column(db.Integer, default = 30)
    min_level = db.Column(db.Integer, default = 1)

class MonsterBattle(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    monster_id = db.Column(db.Integer, db.ForeignKey('monster.id'))
    monster_health_local = db.Column(db.Integer)

class BattleLog(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    monster_id = db.Column(db.Integer, db.ForeignKey('monster.id'))
    result = db.Column(db.String()) # победа, поражение или сбежал
    timestamp = db.Column(db.DateTime, default = datetime.datetime.now(datetime.timezone.utc))
    loot_gold = db.Column(db.Integer)
    loot_exp = db.Column(db.Integer)

