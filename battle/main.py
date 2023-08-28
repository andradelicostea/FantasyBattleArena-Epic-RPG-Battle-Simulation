from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random


# Create black magic spells
flame_bomb = Spell("Flame Bomb", 20, 100, "black")
bolt_of_burning_souls = Spell("Bolt of Burning Souls", 20, 100, "black")
frost = Spell("Frost", 20, 100, "black")
soulsteal = Spell("Soulsteal", 40, 2000, "black")
wave_of_redemption = Spell("Wave of Redemption", 10, 150, "black")

# Create white magic spells
cure = Spell("Cure", 25, 600, "white")
life_bolt = Spell("Life Bolt", 30, 1500, "white")
spell_of_health = Spell("Spell of Health", 50, 5000, "white")

# Create some items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
potion_of_luck = Item("Potion of Luck", "potion", "Heals 100 HP", 100)
brew_of_the_undead = Item("Brew of the Undead", "potion", "Heals 1000 HP", 1000)
elixer = Item("Elixer", "elixer", "Completely restores HP/MP of one party member.", 9999)
elixir_of_redemption = Item("Elixir of Redemption", "elixer", "Completely replenishes the entire party's HP and MP.", 9999)

poison_strike = Item("Poison Strike", "attack", "Inflicts 500 points of damage.", 500)

# Create lists of spells and items
player_spells = [flame_bomb, bolt_of_burning_souls, frost, soulsteal, wave_of_redemption, cure, life_bolt]
enemy_spells = [flame_bomb, soulsteal, spell_of_health]
player_items = [{"item": potion, "quantity": 15}, {"item": potion_of_luck, "quantity": 5},
                {"item": brew_of_the_undead, "quantity": 5}, {"item": elixer, "quantity": 5}, 
                {"item": elixir_of_redemption, "quantity": 2}, {"item": poison_strike, "quantity": 5}]

# Instantiate player characters
player1 = Person("Nera  ", 3500, 150, 300, 35, player_spells, player_items)
player2 = Person("Oma   ", 4100, 200, 325, 35, player_spells, player_items)
player3 = Person("Dalvir", 3200, 180, 280, 35, player_spells, player_items)

# Instantiate enemy characters
enemy1 = Person("Nyx   ", 1250, 130, 500, 300, enemy_spells, [])
enemy2 = Person("Zilla ", 12000, 700, 600, 50, enemy_spells, [])
enemy3 = Person("Delano", 1250, 130, 500, 300, enemy_spells, [])

# Create lists of players and enemies
players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

# Print battle start message
print(bcolors.FAIL + bcolors.BOLD + "THE ENEMIES ARE ATTACKING!" + bcolors.ENDC)

# Main battle loop
while running:
    # Print players' and enemies' stats
    print("If the last enemy has died and one more player has to attack, choose '0' to win the game!")
    print("If you want to come back to the list of options, choose '0'")
    print("▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀")

    print("\n\n")
    # Print players' stats
    print("NAME                    HP                                     MP")
    for player in players:
        player.get_stats()
    print("\n") 

    # Print enemies' stats
    for enemy in enemies:
        enemy.get_enemy_stats()

    # Players' turn
    for player in players:
        player.choose_action()
        choice = input("    Choose action:")
        index = int(choice) - 1

        if index == 0:
            # Physical attack
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print("You attacked " + enemies[enemy].name.replace(" ", "") + " for", dmg, "points of damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died.")
                del enemies[enemy]

        elif index == 1:
            # Choose magic spell
            player.choose_magic()
            magic_choice = int(input("    Choose magic:")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_damage = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print (bcolors.FAIL + "\nNot enough mp.\n" + bcolors.ENDC)
                continue
            
            player.reduce_mp(spell.cost)

            if spell.type == "white":
                    player.heal(magic_damage)
                    print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_damage), "HP." + bcolors.ENDC)
            elif spell.type =="black":
                # Choose target and deal damage
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_damage)

                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_damage), "points of damage to " + enemies[enemy].name.replace(" ", "") + "." + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]

        elif index == 2:
            # Choose item
            player.choose_item()
            item_choice = int(input("    Choose item: " )) - 1

            if item_choice == -1:
                continue
            
            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for " + str(item.prop), "HP." + bcolors.ENDC)
            elif item.type == "elixer":
                # Use elixir item
                if item.name == "Elixir of Redemption":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP. " + bcolors.ENDC)
            elif item.type == "attack":
                # Choose target and deal damage
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals ", str(item.prop), "points of damage to" + enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]

    # Check if battle is over
    defeated_enemies = sum(1 for enemy in enemies if enemy.get_hp() <= 0)
    defeated_players = sum(1 for player in players if player.get_hp() <= 0)

    # Check if player won
    if defeated_enemies == len(enemies):
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False

    # Check if enemy won
    elif defeated_players == len(players):
        print(bcolors.FAIL + "Your enemies have defeated you!" + bcolors.ENDC)
        running = False

    print("\n")
    
    # Print the number of defeated enemies and remaining players
    print("Target:", defeated_enemies)
    print("Number of players:", len(players))

    # Enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            # Choose attack
            target = random.randrange(0, len(players))
            enemy_damage = enemy.generate_damage()
            players[target].take_damage(enemy_damage)  

            print(enemy.name.replace(" ", "") + " attacks " + players[target].name.replace(" ", "") + " for", enemy_damage, ".")
        elif enemy_choice == 1:
            # Choose spell and deal damage
            if len(players) != 0:
                (spell, magic_damage) = enemy.choose_enemy_spell() 
                enemy.reduce_mp(spell.cost)
            else: 
                running = False
            

            if spell.type == "white":
                    enemy.heal(magic_damage)
                    print(bcolors.OKBLUE + spell.name + " heals " + enemy.name + " for", str(magic_damage), "HP." + bcolors.ENDC)
            elif spell.type =="black":
                # Choose target and deal damage
                target = random.randrange(0, len(players))
                players[target].take_damage(magic_damage)

                enemy.take_damage(magic_damage)
                print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ", "") + "'s " + spell.name + " deals", str(magic_damage), "points of damage to " + players[target].name.replace(" ", "") + "." + bcolors.ENDC)

                if players[target].get_hp() <= 0:
                    print(players[target].name.replace(" ", "") + " has died.")
                    players.remove(player)
