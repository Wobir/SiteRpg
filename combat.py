import random
from models import db
def calculate_damage(attacker_damage, defender_defense):
    base = max(1, attacker_damage - defender_defense * 0.5)
    variance = random.randint(8,12) * 0.1
    return int(base * variance)

def battle( player, monster):
    log = []
    p_hp, m_hp = player.hit_points, monster.health
    
    while p_hp > 0 or m_hp > 0:
        
        dmg = calculate_damage(player.weapon.damage, monster.defense)
        m_hp -= dmg
        log.append(f"{player.username} нанёс {dmg} урона")   

        if m_hp <= 0:
            log.append("Победа")
            player.exp += monster.exp_reward
            player.money += monster.gold_reward
            # TODO: добавить прокачку уровня при повышении опыта
            return {"result":"win", "log":log, "rewards":{"loot_gold":monster.gold_reward, "loot_exp":monster.exp_reward}}
        
        dmg = calculate_damage(monster.damage, player.weapon.defense )
        p_hp -= dmg
        player.hit_points -= dmg
        log.append(f"{monster.name} нанёс {dmg} урона игроку {player.username}")
        
        if p_hp <= 0:
            log.append("Поражение")
            player.hit_points = 0

            return {"result":"lose", "log":log, "rewards":{"loot_gold":0, "loot_exp":0} }
    
    """player.hit_points = max(0, p_hp)
    db.session.commit()  """