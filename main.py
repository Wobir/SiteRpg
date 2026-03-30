from flask import Flask, session, request, render_template, redirect, url_for

from models import *
from forms import *
import random
from combat import * 

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] \
    = "sqlite:///game.db"

app.secret_key = "secret"

db.init_app(app)

with app.app_context():
    db.create_all()

    if Weapon.query.count() == 0:
        weapons = [
            Weapon(name = "Меч", damage = 25, defense = 10),
            Weapon(name="Лук", damage=30, defense=5),
            Weapon(name="Топор", damage=15, defense=15),
        ]
        db.session.add_all(weapons)
        db.session.commit()

    if Player.query.count() == 0:
        Players = [
            Player(username = "Player 1",
                   password = "password",
                   weapon_id = 2),
            Player(username = "Player 2",
                   password = "password",
                   weapon_id = 3)
        ]
        db.session.add_all(Players)
        db.session.commit()

    if Monster.query.count() == 0:
        Monsters = [
            Monster(name = "Гоблин",
                    min_level = 1),
            Monster(name = "Скелет",
                    damage = 12,
                    defense = 2,
                    gold_reward = 50,
                    min_level = 1)
        ] 
        db.session.add_all(Monsters)
        db.session.commit()
    print("===========Оружия==========")
    all_weapons = Weapon.query.all()
    for weapon in all_weapons:
        print(f"ID: {weapon.id} | name: {weapon.name }|"+
              f"damage: {weapon.damage}| defense:{weapon.defense}")
    print("===========Игроки==========")
    all_player = Player.query.all()
    for player in all_player:
        player_weapon_name = player.weapon.name
        player_weapon_damage = player.weapon.damage
        player_weapon_defense = player.weapon.defense
        print(f"ID: {player.id} | username {player.username} |"
              f"WeaponName {player_weapon_name} | WeaponDamage {player_weapon_damage}" )
    print("========Монстры========")
    all_monsters = Monster.query.all()
    for monster in all_monsters:
        print(f"ID: {monster.id} | name: {monster.name} | damage: {monster.damage} | min_level : {monster.min_level}")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/reg/", methods=["POST", "GET"])
def reg():
    regForm = RegForm()
    if "player_id" in session:
        return redirect(url_for("inventory"))
    if regForm.validate_on_submit():
        if request.method == "POST":
            username = request.form.get("name")
            password = request.form.get("password")
            if Player.query.filter_by(username = username).count()>0:
                message = "Игрок с таким именем уже существует"
                return render_template("reg.html", form = regForm, message = message)
            new_player = Player(
                username = username,
                password = password,
                )

            db.session.add(new_player)
            db.session.commit()
            session["player_id"] = new_player.id
            session["player_name"] = new_player.username
            print(session["player_id"], session["player_name"])
            return redirect(url_for("inventory"))
    return render_template("reg.html", form = regForm)

@app.route("/auth/", methods=["POST", "GET"])
def auth():
    authForm = AuthForm()
    if "player_id" in session:
        return redirect(url_for("inventory"))
    if authForm.validate_on_submit():
        if request.method == "POST":
            username = request.form.get("name")
            password = request.form.get("password")
            player = Player.query.filter_by(username = username).first()
            if player and player.password == password:
                session["player_id"] = player.id
                session["player_name"] = player.username
                print(session["player_id"], session["player_name"])
                return redirect(url_for("inventory"))
            else:
                message = "Игрок не существует или вы ввели не верный пароль"
                return render_template("auth.html", form=authForm, message=message)
    return render_template("auth.html", form = authForm)

@app.route("/inventory/")
def inventory():
    if not "player_id" in session:
        return redirect(url_for("auth"))
    player = Player.query.filter_by(id = session["player_id"]).first()
    return render_template("inventory.html", player = player)

@app.route("/adventure/", methods =["GET", "POST"])
def adventure():
    if "player_id" in session:
        player_id = session["player_id"]
        player = Player.query.filter_by(id=player_id).first()
    else:
        return redirect(url_for("auth"))
    continue_player = True

    if MonsterBattle.query.filter_by(player_id = player.id).count() == 0 and continue_player :
        available_monsters = Monster.query.filter(Monster.min_level <= player.level).all()
        monster = available_monsters[random.randint(0, len(available_monsters)-1)]
        new_battle = MonsterBattle(player_id = player.id, monster_id = monster.id, monster_health_local = monster.health)
        monster_health = monster.health
        db.session.add(new_battle)
        db.session.commit()
    if continue_player:
        player_battle =  MonsterBattle.query.filter_by(player_id = player.id).first()
        monster_id = player_battle.monster_id
        monster = Monster.query.filter_by(id = monster_id).first()
        monster_health = player_battle.monster_health_local

    if request.method == "GET":
        attack = request.args.get("attack", "")
        defend = request.args.get("defend", "")
        runaway = request.args.get("runaway", "")
        if attack:
            attack_result = player_attack(player, monster, monster_hp=monster_health)
            if attack_result == "Победа":
                player.exp += monster.exp_reward
                player.money += monster.gold_reward
                player_battle = MonsterBattle.query.filter_by(player_id=player_id).first()
                db.session.delete(player_battle)
                continue_player = False
                monster_health = 0
            elif attack_result == "Поражение":
                player_battle = MonsterBattle.query.filter_by(player_id=player_id).first()
                db.session.delete(player_battle)
                continue_player = False
            else:
                player_battle.monster_health_local = attack_result
                monster_health =  player_battle.monster_health_local
            db.session.commit()
        elif defend:
            defend_result = player_defend(player, monster, monster_hp=monster_health)
            if defend_result == "Победа":
                player.exp += monster.exp_reward
                player.money += monster.gold_reward
                player_battle = MonsterBattle.query.filter_by(player_id=player_id).first()
                db.session.delete(player_battle)
                continue_player = False
                monster_health = 0
            elif defend_result == "Поражение":
                player_battle = MonsterBattle.query.filter_by(player_id=player_id).first()
                db.session.delete(player_battle)
                continue_player = False
            else:
                player_battle.monster_health_local= defend_result
                monster_health = player_battle.monster_health_local
            db.session.commit()
        elif runaway:
            player_battle = MonsterBattle.query.filter_by(player_id = player_id).first()
            db.session.delete(player_battle)
            db.session.commit()
            continue_player = False
    return render_template("adventure.html", player = player, monster = monster, monster_health = monster_health, continue_player = continue_player)

@app.route("/shop/", methods= ["POST", "GET"])
def shop():
    if "player_id" in session:
        player = Player.query.filter_by(id = session["player_id"]).first()
    else:
        return redirect(url_for("auth"))
    if request.method == "POST":
        print("получен POST запрос")
        command = request.form.get("command")
        message = "Вам не хватает золота"
        if command == "зелье лечения":
            if player.money >= 50:
                player.hit_points += 20
                if player.hit_points > 100:
                    player.hit_points = 100
                player.money -= 50
                message = "Вы полечились"
        if command == "большое зелье лечения":
            if player.money >= 100:
                player.hit_points += 40
                if player.hit_points > 100:
                    player.hit_points = 100
                player.money -= 100
                message = "Вы полечились"
        db.session.commit()
        return render_template("shop.html", message = message)
    return render_template("shop.html")

@app.route("/logout/")
def logout():
    if "player_id" in session:
        session.pop("player_id")
    return redirect(url_for("auth"))

@app.route("/adminpanel/",methods = ["GET", "POST"])
def adminpanel():
    monsters = Monster.query.all()
    weapons = Weapon.query.all()
    players = Player.query.all()
    return render_template("admin_panel.html", monsters = monsters, weapons = weapons, players = players)

app.run(debug=True)
