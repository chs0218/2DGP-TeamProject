def check_attack(attack, hit):
    attack_left, attack_bottom, attack_right, attack_top = attack.get_attack_range()
    hit_left, hit_bottom, hit_right, hit_top = hit.get_bb()
    if attack_left > hit_right: return False
    if attack_right < hit_left: return False
    if attack_top < hit_bottom: return False
    if attack_bottom > hit_top: return False
    return True

def check_clear(dungeon, character):
    attack_left, attack_bottom, attack_right, attack_top = dungeon.get_bb()
    hit_left, hit_bottom, hit_right, hit_top = character.get_bb()
    if attack_left > hit_right: return False
    if attack_right < hit_left: return False
    if attack_top < hit_bottom: return False
    if attack_bottom > hit_top: return False
    return True