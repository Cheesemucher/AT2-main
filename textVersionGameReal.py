from mage import Mage
from goblin import Goblin

#combat between a mage and a goblin

player = Mage("mageman", 90, 80, 100)
goblin = Goblin("position", "window", 80, 95) 
#image to load:
#'pygame.image.load("assets/goblin.png").convert_alpha()'

print(player.getCurrentMana, player.getMagicPower)
print(goblin.getCurrentHP, goblin.getMagicResistanceMultiplier)

player.chooseAttack(goblin)

print(goblin.getCurrentHP)
