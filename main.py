from flask import Flask, session, request, render_template, redirect, url_for

from models import *
from forms import *

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
                password = password
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

app.run(debug=True)
