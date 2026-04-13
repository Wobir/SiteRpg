from models import Player, db
def level_up(player: Player):
    if player.exp >= 100 + 10 * player.level:
        player.exp = 0
        player.level += 1
        player.max_hit_points += 10
        player.hit_points += 10
    db.session.commit()    