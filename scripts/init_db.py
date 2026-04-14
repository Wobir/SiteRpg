import logging
import os
import sys

# Ensure project root is on sys.path so we can import `main` when run as a script
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from main import app
from app.models import db, Player, Weapon, Monster, ShopItem, PlayerItem
from werkzeug.security import generate_password_hash

logger = logging.getLogger(__name__)


def seed_db():
    with app.app_context():
        db.create_all()

        if Weapon.query.count() == 0:
            weapons = [
                Weapon(id = 0,name="Рукопашный бой", damage=10, defense=5),
                Weapon(name="Меч", damage=25, defense=10),
                Weapon(name="Лук", damage=30, defense=5),
                Weapon(name="Топор", damage=15, defense=15),
            ]
            db.session.add_all(weapons)
            db.session.commit()

        if Player.query.count() == 0:
            players = [
                Player(username="Player 1", password=generate_password_hash("password"), weapon_id=2),
                Player(username="Player 2", password=generate_password_hash("password"), weapon_id=3),
            ]
            db.session.add_all(players)
            db.session.commit()

        # Ensure any existing plain-text passwords are replaced with hashed versions
        try:
            all_players = Player.query.all()
            updated = False
            for p in all_players:
                pwd = (p.password or "")
                if not pwd.startswith("pbkdf2:"):
                    p.password = generate_password_hash(pwd)
                    updated = True
            if updated:
                db.session.commit()
                logger.info("Re-hashed existing plain-text player passwords")
        except Exception:
            logger.exception("Failed to re-hash existing passwords")

        if Monster.query.count() == 0:
            monsters = [
                Monster(name="Гоблин", min_level=1),
                Monster(name="Скелет", damage=12, defense=2, gold_reward=50, min_level=1),
            ]
            db.session.add_all(monsters)
            db.session.commit()

        if ShopItem.query.count() == 0:
            items = [
                ShopItem(name="Зелье лечения", item_type="potion", price=50, healing_amount=30),
                ShopItem(name="Большое зелье леченеия", item_type="potion", price=150, healing_amount=70),
                ShopItem(name="Меч", item_type="weapon", price=300, weapon_id=1),
                ShopItem(name="Лук", item_type="weapon", price=300, weapon_id=2),
                ShopItem(name="Топор", item_type="weapon", price=300, weapon_id=3),
            ]
            db.session.add_all(items)
            db.session.commit()

        if PlayerItem.query.count() == 0:
            player_items = [
                PlayerItem(player_id=1, item_id=4),
                PlayerItem(player_id=2, item_id=5),
            ]
            db.session.add_all(player_items)
            db.session.commit()

        logger.info("Database seeded successfully")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    seed_db()
