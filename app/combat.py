import random
import logging

logger = logging.getLogger(__name__)


def calculate_damage(attacker_damage, defender_defense):
    base = max(1, attacker_damage - defender_defense * 0.5)
    variance = random.randint(8, 12) * 0.1
    return int(base * variance)


def player_attack(player, monster, monster_hp):
    logger.debug("player_attack called for %s vs %s", getattr(player, 'username', None), getattr(monster, 'name', None))
    dmg = calculate_damage(player.weapon.damage, monster.defense)
    monster_hp -= dmg
    if monster_hp <= 0:
        return "Победа"
    dmg = calculate_damage(monster.damage, player.weapon.defense)
    player.hit_points -= dmg
    if player.hit_points <= 0:
        return "Поражение"
    return monster_hp


def player_defend(player, monster, monster_hp):
    logger.debug("player_defend called for %s vs %s", getattr(player, 'username', None), getattr(monster, 'name', None))
    dmg = calculate_damage(monster.damage, player.weapon.defense)
    player.hit_points -= dmg
    if player.hit_points <= 0:
        return "Поражение"
    dmg = calculate_damage(player.weapon.damage, monster.defense)
    monster_hp -= dmg
    if monster_hp <= 0:
        return "Победа"
    return 0
