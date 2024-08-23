from random import randint


class Enemy:
    def __init__(self, rank, level):
        self.rank = rank
        self.level = level
        self.is_dead = False
        self.health = self.rank * self.level * 10
        self.max_health = self.rank * self.level * 10
        self.min_dmg = int(self.rank * self.level)
        self.max_dmg = int(self.rank * self.level * 1.5)
        self.xp = self.rank * self.level * 2

    def __repr__(self):
        return "\n***Information about the enemy***\n" \
               "Rank: {rank} - Level: {level}\n" \
               "Max health: {max_health}\n" \
               "Min damage: {min_dmg}\n"\
               "Max damage: {max_dmg}".format(
                rank=self.rank,
                level=self.level,
                max_health=self.max_health,
                min_dmg=self.min_dmg,
                max_dmg=self.max_dmg)

    def killed(self):
        self.is_dead = True
        print("The enemy is killed.")

    def lose_health(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.killed()
            player.gain_xp()
        else:
            return None

    def attack(self):
        amount = randint(self.min_dmg, self.max_dmg)
        print(f"The enemy hit you, and you suffered {amount} damage.")
        player.lose_health(amount)
        if player.health > 0:
            print(f"Your remaining health: {player.health}")
        return amount


class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.xp = 0
        self.health = self.level * 50
        self.max_health = self.level * 50
        self.damage_potions = 0
        self.health_potions = 0
        self.min_dmg = int(self.level * 15)
        self.max_dmg = int(self.level * 25)
        self.kill_count = 0
        self.is_dead = False

    def __repr__(self):
        return "\n***Information about your character***\n" \
               "Level: {level}\n" \
               "Max health: {max_health}\n" \
               "Remaining damage potions: {dmg_ptn}\n" \
               "Remaining health potions: {hlt_ptn}\n" \
               "Min damage: {min_dmg}\n" \
               "Max damage: {max_dmg}\n" \
               "Killed enemies: {kill_count}\n"\
               "Exp points: {xp}".format(
                level=self.level,
                max_health=self.max_health,
                dmg_ptn=self.damage_potions,
                hlt_ptn=self.health_potions,
                min_dmg=self.min_dmg,
                max_dmg=self.max_dmg,
                kill_count=self.kill_count,
                xp=self.xp)

    def death_event(self):
        self.is_dead = True
        print("Your health reached 0.\n   ***GAME OVER***")

    def lose_health(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.death_event()
        else:
            return None

    def attack(self):
        amount = randint(self.min_dmg, self.max_dmg)
        print(f"You hit the enemy, who suffered {amount} damage.")
        enemy.lose_health(amount)
        if enemy.health > 0:
            print(f"Enemy's remaining health: {enemy.health}")
        return amount

    def gain_xp(self):
        if enemy.is_dead or enemy.health == 0:
            self.xp += enemy.xp
            self.damage_potions += 1
            self.health_potions += 1
            self.kill_count += 1
            self.health = self.max_health
        print("You gained {xp} xp.".format(xp=enemy.xp))
        self.set_level()

    def set_level(self):
        levels = {
            1: (0, 100),
            2: (101, 250),
            3: (251, 500),
            4: (501, 800),
            5: (801, 1150),
            6: (1151, 1350),
            7: (1351, 1750),
            8: (1751, 2200),
            9: (2201, 2600),
            10: (2601, 999_999_999)}
        new_level = 0
        for level, xp_range in levels.items():
            if xp_range[0] <= self.xp <= xp_range[1]:
                new_level = int(level)
                self.health = new_level * 50
                self.max_health = new_level * 50
                self.min_dmg = int(new_level * 15)
                self.max_dmg = int(new_level * 25)
            else:
                continue

        if new_level > self.level:
            self.level = new_level
            print("LEVEL UP! You reached level {level}!".format(level=self.level))

    def use_health_potion(self):
        if self.health_potions == 0:
            print("You don't have a health potion.")
        else:
            self.health_potions -= 1
            gained_health = self.max_health * 0.25
            if gained_health > (self.max_health - self.health):
                gained_health = self.max_health - self.health
                self.health = self.max_health
            else:
                self.health += gained_health
            print("1 health potion used.\nGained {health} health points.\nYour health: {actual_health}".format(
                health=gained_health, actual_health=self.health))

    def use_damage_potion(self):
        if self.damage_potions == 0:
            print("You don't have a damage potion.")
        else:
            self.damage_potions -= 1
            gained_damage = int(self.max_dmg * 0.25)
            self.min_dmg += gained_damage
            self.max_dmg += gained_damage
            print("1 damage potion used (+{damage} damage)".format(damage=gained_damage))


def create_enemy_instance():
    while True:
        try:
            rank_input = input("Select your enemy's rank (1-5): ")
            rank = int(rank_input)
            if rank in range(1, 6):
                break
            else:
                print("Error: The number must be between 1 and 5. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    while True:
        try:
            level_input = input("Select your enemy's level (1-10): ")
            level = int(level_input)
            if level in range(1, 11):
                break
            else:
                print("Error: The number must be between 1 and 10. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    return Enemy(rank, level)


# Starting the game
print("Welcome to Monstrous Rampage!")
# Creating a player character object
player = Player(input("Add your character name: "))
# Creating the game loop
while player.health > 0:

    if player.health == 0:
        player.death_event()
        break

    to_continue = input("\nWould you like to fight an enemy? "
                        "Type \"Yes\" or hit Enter to exit the game.\n"
                        "Your answer: ")
    if not to_continue:
        print("Thank you for playing, {name}!".format(name=player.name))
        print("You reached level {level} and killed {kill_count} monsters.".
              format(level=player.level, kill_count=player.kill_count))
        break

    # Creating an enemy object
    enemy = create_enemy_instance()

    print(player)
    print(enemy)

    print("\n***FIGHT***")

    while enemy.health > 0:
        str_input = input("\nYour turn!\n"
                          "What would you like to do?\n"
                          "A) Attack\n"
                          "B) Use a health potion ({hlt_ptn} remaining)\n"
                          "C) Use a damage potion ({dmg_ptn} remaining)\n"
                          "Your answer: ".format(
                            hlt_ptn=player.health_potions,
                            dmg_ptn=player.damage_potions))
        if str_input == "A":
            player.attack()
            if enemy.health == 0:
                break
            enemy.attack()
            if player.health == 0:
                break
        elif str_input == "B":
            player.use_health_potion()
            player.attack()
            if enemy.health == 0:
                break
            enemy.attack()
            if player.health == 0:
                break
        else:
            player.use_damage_potion()
            player.attack()
            if enemy.health == 0:
                break
            enemy.attack()
            if player.health == 0:
                break

        player.set_level()
