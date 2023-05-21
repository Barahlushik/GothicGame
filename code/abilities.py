def heal(player, strength, cost):
    if player.heals > 0:
        if player.energy >= cost:
            if player.health + strength >= player.stats['health']:
                player.health = player.stats['health']
            else:
                player.health += strength
            player.heals -= 1
            return True
    else:
        return False


def roll(player, strength, cost):
    if player.energy >= cost:
        player.energy -= cost
        player.speed += strength
        return True
    else:
        return False
