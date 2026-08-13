# Room
import random
import time
import copy
rooms = {
    "Homeroom": {
        "description": "You feel the cold slicing through your body\nyou vomit and start to have hallucinations\nwonder what it is",
        "exits": {"straight": "Execution-room", "left": "Mysterious-shop", "right": "Quiet-room"},
        "items": [
            {"name": "rusty-sword", "damage": 15, "type": "sword"},
            {"name": "note", "type": "lore", "damage": 0}
        ],
        "monster": None,
        "npc": None
    },
    "Mysterious-shop": {
        "description": "Shelves overflow with odd potions, dusty relics, and enchanted curiosities from forgotten lands.",
        "exits": {"right": "Homeroom"},
        "items": [
            {"name": "exotic-health-potion", "damage": -50, "type": "potion", "gold": 10},
            {"name": "steel-armor", "defense": 20, "type": "armor","gold": 35},
            {"name": "sword", "damage": 20, "type": "sword", "gold": 30},
            {"name": "apple", "damage": 5, "type": "food", "gold": 3},
            {"name": "poison", "damage": -15, "type": "potion", "gold": 8},
            {"name": "strength-potion", "damage": 10, "type": "potion", "gold": 15}
        ],
        "monster": None,
        "npc": [
            {"name": "shop-dealer", "damage": 20, "type": "npc", "role": "merchant", "hp": 100}
        ]
    },
    "Execution-room": {
        "description": "An abandoned execution room. The old guillotine stands motionless, as if waiting for its next victim.",
        "exits": {"left": "Deadend", "straight": "Deadend", "back": "Homeroom"},
        "items": [
            {"name": "axe", "damage": 30, "type": "sword"},
            {"name": "human-meat", "damage": 10, "type": "food"}
        ],
        "monster": [
            {"name": "executioner", "damage": 30, "type": "monster", "hp": 50},
            {"name": "zombie", "damage": 15, "type": "monster", "hp": 30}
        ],
        "npc": None
    },
    "Quiet-room": {
        "description": "The air is calm, and no monsters are in sight. For a brief moment, you let your guard down.",
        "exits": {"back": "Bersek-room", "straight": "Deadend", "left": "Homeroom"},
        "items": [
            {"name": "magical-book", "type": "sword", "damage": 100},
            {"name": "health-potion", "damage": 30, "type": "potion"}
        ],
        "monster": [
            {"name": "zombie", "damage": 15, "type": "monster", "hp": 70},
            {"name": "orc", "damage": 25, "type": "monster", "hp": 100}
        ],
        "npc": None
    },
    "Bersek-room": {
        "description": "The room is soaked in dried blood. Mangled corpses lie scattered across the floor, their faces frozen in terror. Something is still breathing nearby.",
        "exits": {"right": "Trap-room", "left": "Vault"},
        "monster": [
            {"name": "The fallen knight", "damage": 10, "type": "monster", "hp":200},
            {"name": "Fire of Truth", "damage": 1000, "type": "specialmonster", "hp":1000}
        ],
        "items": [
            {"name": "fire-poison", "damage": -30, "type": "potion"},
            {"name": "fire-sword", "damage": 40, "type": "sword"}
        ],
        "npc": None
    },
    "Vault": {
        "description": "A chamber overflowing with unimaginable wealth. The silence is unsettling, and the treasure seems almost too easy to take.",
        "exits": {"left": "Boss_room", "straight": "Mysterious-shop"},
        "items": [
            {"name": "true-key", "type": "key", "damage": 0},
        ],
        "monster": [
            {"name": "supreme-thief", "damage": 0, "type": "monster","hp":1}
        ],
        "npc": None
    },
    "Trap-room": {
        "description": "The floor is littered with pressure plates and rusty spikes. One wrong step and it's over.",
        "exits": {"back": "Bersek-room", "straight": "Deadend"},
        "items": [
            {"name": "boss-key", "type": "key", "damage": 0},
        ],
        "monster": None,
        "npc": None
    },
    "Boss_room": {
        "description": "A massive chamber cloaked in shadows. At its center stands the final guardian, waiting.",
        "exits": {"back": "Vault"},
        "items": [
            {"name": "boss-loot", "type": "treasure", "damage": 0}
        ],
        "monster": [
            {"name": "the trace of supreme-thief", "damage": 100, "type": "specialmonster", "hp": 500}
        ],
        "npc": None
    },
    "Deadend": {
        "description": "A black face gradually appears out of nowhere. Fortunately, it is just a black wall with meticulous details.",
        "monster": [
            {"name": "Faceless", "damage": 10, "type": "monster", "hp":50 }
        ],
        "npc": None,
        "exits": {"back": "Homeroom"},
        "items": None,
    },
}
character = {
    "hp": 100,
    "items": [],
    "gold": 0,
    "weapon": [],
    "defweapon": [],
    "damage": 10,
    "defense": 10,
    "current_position" : "Homeroom",
    "visited_room": {"Homeroom"}
}
rooms_original = copy.deepcopy(rooms)
character_original = copy.deepcopy(character)

class items:
    def __init__(self, name, damage, type, price=0):
        self.name = name 
        self.damage = damage
        self.type = type
        self.price = price    
class weapon(items):
    def replaceweapon(self, character, slot_weapon):
        old_item = slot_weapon[0]
        character.items.append(old_item)
        slot_weapon.remove(old_item)
        old_item.updatestat(character, add = False)
        slot_weapon.append(self)
        self.updatestat(character, add = True)
        
    def equipweapon(self, character, slot_weapon):
        if len(slot_weapon) == 1:
            self.replaceitem(character, slot_weapon)
        elif self.type == "sword":
            character.weapon.append(self)
            self.updatestat(character, add = True)
        elif self.type == "armor":
            character.defweapon.append(self)
            self.updatestat(character,add = True)
    def updatestat(self, character,add = True):
        if self.type == "sword":
            if add:
                character.damage += self.damage
            else:
                character.damage -= self.damage
        elif self.type == "armor":
            if add:
                character.defense += self.damage
            else:
                character.defense -= self.damage
class potion(items):
    def potioneffect(self, target):
        if self.type == "healing_potion":
            target.hp += self.damage
        elif self.type == "stat_potion":
            target.damage += self.damage
        elif self.type == "damage_potion":
            target.hp -= self.damage        

class key(items):
    def __init__(self, name, unlocks, price=0):
        super().__init__(name = name, damage= 0, type="key",price = price)
        self.unlocks = unlocks
    def unlockroom(self, unlocks):
        return self.unlocks == unlocks
   
#weapon
rustysword = weapon(name="rusty-sword", damage=15, type="sword")
shop_sword = weapon(name="sword", damage=20, type="sword", price=30)
axe = weapon(name="axe", damage=30, type="sword")
magical_book = weapon(name="magical-book", damage=50, type="sword")
fire_sword = weapon(name="fire-sword", damage=40, type="sword")
#potion
exotic_health_potion = potion(name="exotic_potion", damage=70, type="healing_potion", price=80)
strength_potion = potion(name="strength_potion", damage=20, type="stat_potion", price=20)
poison = potion(name="poison", damage=30, type="damage_potion", price=40)
fire_poison = potion(name="fire_poison", damage=40, type="damage_potion", price=0)
health_potion = potion(name="health_potion", damage=25, type="healing_potion", price=0)
#food
apple = potion(name="apple", damage=10, type="healing_potion", price=10)
human_meat = potion(name="human_meat", damage=30, type="healing_potion", price=0)
#key
true_key = key(name= "true_key", unlocks ="Vault", type = "key", price = 0)
boss_key = key(name="boss_key", unlocks ="Boss_room", type="key", price=0)
boss_loot = key(name="boss_loot", unlock ="True_end", type="key", price=0)

    

class rooms:
    def __init__(self, name, information,exits =None, items = None, monsters = None):
        self.name = name
        self.information = information
        self.exits = exits if exits is not None else []
        self.items = items if items is not None else []
        self.monsters = monsters if monsters is not None else []
    def addditem(self, item):
        self.items.append(item)
    def removeitem(self, item):
        self.items.remove(item)
    def addmonster(self, monster):
        self.monsters.append(monster)
    def removemonster(self,monster):
        self.monsters.remove(monster)

        
#rooms self, name, information,exits =None, items = None, monsters = None
Homeroom = rooms(
    name="Homeroom",
    information="You feel the cold slicing through your body, you vomit and start to have hallucinations, wonder what it is",
    exits={"straight": "Execution-room", "left": "Mysterious-shop", "right": "Quiet-room"}
)

Mysterious_shop = rooms(
    name="Mysterious-shop",
    information="Shelves overflow with odd potions, dusty relics, and enchanted curiosities from forgotten lands.",
    exits={"right": "Homeroom"}
)

Execution_room = rooms(
    name="Execution-room",
    information="An abandoned execution room. The old guillotine stands motionless, as if waiting for its next victim.",
    exits={"left": "Deadend", "straight": "Deadend", "back": "Homeroom"}
)

Quiet_room = rooms(
    name="Quiet-room",
    information="The air is calm, and no monsters are in sight. For a brief moment, you let your guard down.",
    exits={"back": "Bersek-room", "straight": "Deadend", "left": "Homeroom"}
)

Bersek_room = rooms(
    name="Bersek-room",
    information="The room is soaked in dried blood. Mangled corpses lie scattered across the floor, their faces frozen in terror. Something is still breathing nearby.",
    exits={"right": "Trap-room", "left": "Vault"}
)

Vault = rooms(
    name="Vault",
    information="A chamber overflowing with unimaginable wealth. The silence is unsettling, and the treasure seems almost too easy to take.",
    exits={"left": "Boss_room", "straight": "Mysterious-shop"}
)

Trap_room = rooms(
    name="Trap-room",
    information="The floor is littered with pressure plates and rusty spikes. One wrong step and it's over.",
    exits={"back": "Bersek-room", "straight": "Deadend"}
)

Boss_room = rooms(
    name="Boss_room",
    information="A massive chamber cloaked in shadows. At its center stands the final guardian, waiting.",
    exits={"back": "Vault"}
)

Deadend = rooms(
    name="Deadend",
    information="A black face gradually appears out of nowhere. Fortunately, it is just a black wall with meticulous details.",
    exits={"back": "Homeroom"}
)

Trueend = rooms(
    name= "Truend",
    information="you win the game",
    exits=None
)
    
class CHARACTER:
    def __init__(self,name, hp, damage, defense =0, gold = 0, 
                 weapon = None,defweapon = None, items = None,
                 current_position = "Homeroom",
                 visited_room = None, type = "character"
                 
                 ):
        self.type = type
        self.name = name
        self.hp = hp
        self.damage = damage 
        self.defense = defense
        self.gold = gold
        self.items = items if items is not None else []
        self.weapon = weapon if weapon is not None else []
        self.defweapon = defweapon if defweapon is not None else []
        self.current_position = current_position
        self.visited_room = visited_room if visited_room is not None else {"Homeroom"}
    @staticmethod
    def spawnmonster(name,hp,damage):
        return CHARACTER(name=name,hp=hp, damage = damage, type = "monster",gold = random.randint(1,10))
    def takedamage(self, damage):
        actual_damage = max(0, damage - self.defense)
        self.hp -= actual_damage
        return actual_damage
    def isdead(self):
        return self.hp <=0
    #item
    def showinventory(target):
        if not target.items:
            print("no item found")
            return
        else:
            for i,item in enumerate(target.items):
                print(f"{i}, {item.name}")
    def chooseitem(target):
        if not target.items:
            return None
        else:
            while True:
                try:
                    target.showinventory()
                    choice = input_int("choose item: ")
                    return target.items[choice]
                except IndexError:
                    print("invalid number")
    def showitemstat(target):
        items = target.chooseitem()
        print((items.name), (items.type), (items.damage))
    def takeitems(target):
        if not rooms[target.current_position].items:
            print("no items found")
            return None
        else: 
            item = target.chooseitem()
            target.items.append(item)
            rooms[target.current_position].items.remove(item)
    def dropitems(target):
        if not target.items:
            print("no items to drop")
            return None
        else: 
            item = target("choose an item to drop: ", character)
            print(f"you have dropped {item}")
            rooms[character.current_position]["items"].append(item)
            character.items.remove(item)

def choosetarget(monster, character):
    print("1.monster\n2.player")
    playerchoice = input_int("please choose a number: ")
    if playerchoice == 1:
        return monster
    elif playerchoice == 2:
        return character           

def equip_item(item, slot_name, stat_name):
    """
    slot_name: "weapon" hoặc "defweapon"
    stat_name: "damage" hoặc "defense"
    """
    if len(character.slot_name) == 1:
        playerchoice = input_int("1.change item\n2.cancel")
        if playerchoice == 1:
            old_item = character[slot_name][0]
            character[slot_name].remove(old_item)
            character.items.append(old_item)
            character[stat_name] -= old_item[stat_name]
            
            character[slot_name].append(item)
            character[stat_name] += item[stat_name]
            character.items.remove(item)
        else:
            return
    else:
        character[slot_name].append(item)
        character[stat_name] += item[stat_name]
        character.items.remove(item)
        
    
    
def useitem(monster):
    item = chooseitem("choose item: ", character)
    if item is None:
        print("no item use")
        return
    if monster is None:
        target = character
    else:
        target = choosetarget(monster, character)
    if item["name"] == "strength-potion":
            character["damage"] += item["damage"]
            character["items"].remove(item)
    elif item["name"] == "magical-book":
            target  ["hp"] -= item["damage"]
            character["items"].remove(item) 
    elif item["type"] == "potion" or item["type"] == "food":
        target["hp"] += item["damage"]
        character["items"].remove(item)
    
    elif item["type"] == "sword":
        equip_item(item, "weapon", "damage")
    
    elif item["type"] == "armor":
        equip_item(item, "defweapon", "defense")
            
    elif item["type"] == "lore":
        print("i am so lazy if you have treasure and defeat\nboss you will win btw there is a key in vault room so good luck")

    
#you
character = CHARACTER(
name = "hero",
hp = character["hp"],
damage = character["damage"],
defense = character["defense"],
items = character["items"],
gold = character["gold"],
weapon = character["weapon"],
defweapon = character["defweapon"],
current_position= character["current_position"],
visited_room = character["visited_room"]
)

# monster thường (name, hp,damage)
executioner = CHARACTER.spawnmonster("executioner", 50, 30)
weak_zombie = CHARACTER.spawnmonster("weak_zombie", 30, 15)
strong_zombie = CHARACTER.spawnmonster("strong_zombie", 70, 15)
orc = CHARACTER.spawnmonster("orc", 100, 25)
fallen_knight = CHARACTER.spawnmonster("The fallen knight", 200, 10)
supreme_thief = CHARACTER.spawnmonster("supreme-thief", 1, 0)
faceless = CHARACTER.spawnmonster("Faceless", 50, 10)

# specialmonster
fire_of_truth = CHARACTER.spawnspecialmonster("Fire of Truth", 1000, 1000)
supreme_thief_trace = CHARACTER.spawnspecialmonster("the trace of supreme-thief", 500, 100)





def reset_game():
    global rooms, character
    rooms = copy.deepcopy(rooms_original)
    character = copy.deepcopy(character_original)
    print("reset the world")

def item_menu():
    while True:
        print("""
                [1] take item
                [2] use item
                [3] drop item
                [4] back to main menu
            """)
        choice = input_int("choose an action: ")
        if choice == 1:
            takeitems()
        elif choice == 2:
            useitem(None)
        elif choice == 3:
            dropitems()
        elif choice == 4:
            return
        else:
            print("invalid choice")
def showmap():
    print("____Map____")
    for names in rooms:
        if names in character.visited_room:
            print(f"[X] {names}")
        else:
            print(f"[?] {names}")
        
def input_int(number):
    while True:
        try:
            return int(input(number))
        except ValueError:
            print("Hey stop fucking my game") 
            
def showroom():
    print(rooms.information)
    print(f"You are in: {rooms.name}")
#The lesson here: enumerate() always hands you (number, item) in that fixed order
def moving_character():
    for i, (direction, rom) in enumerate(rooms.exits.items()):
        if rom in character.visited_room:
                print(f"{i}, {direction} --->{rom}")
        else:
                print(f"{i}, {direction} ---> ???")
    n = input_int("choose where to head to: ")
    for i, (direction,phong)  in enumerate(rooms.exits.items()):
        if n == i:
            character.current_position = phong
            character.visited_room.add(character.current_position)
            return
    else:
        print("path don't exits")
        return

def notenoughgold(character, items):
    if character.gold < items.price:
        print("you don't have enough gold")
        return True
    else:
        return False 

def shop():
    if character.current_position == "Mysterious-shop":
        while True:
            for i,item in enumerate(rooms.Mysterious_shop["items"], start = 1):
                print(f"{i}. {item["name"]}|{item["gold"]}gold")
            print("0.cancel")    
            playerchoice = input_int("press to buy: ")
            if playerchoice == 0:
                return
            if notenoughgold(rooms["Mysterious-shop"]["items"][playerchoice -1]["gold"]):
                continue
            else:   
                    character["gold"] -= rooms["Mysterious-shop"]["items"][playerchoice -1]["gold"]
                    print(f"you buy {rooms["Mysterious-shop"]["items"][playerchoice -1]}")
                    character["items"].append(rooms["Mysterious-shop"]["items"][playerchoice -1])
            
def trap_room():
    if character.current_position == "Trap-room":
        while True:
            print("1.Take the boss-key and exit\n2.Exit")
            n = input_int("press an number: ")
            if n == 1:
                dice = random.randint(0,3)
                time.sleep(0.5)
                if dice == 3:
                    print("you exit with boss key")
                    character.items.append(rooms["Trap-room"]["items"][0])
                    return
                else:
                    character.hp -= 50
                    print("ouch you have stepped on rusty spike (-50hp)")
                    if check_player_die(character):
                        return
                    print("you exit trap-room")
                    return
            elif n == 2:
                dice = random.randint(1,2)
                time.sleep(0.5)
                if dice == 1:
                    character.hp = 1
                    print("you step onto the bomb")
                else:
                    print("you exit")
                    return
                return
def deadend():
    fight("Deadend")
    if check_player_die(character):
        reset_game()
    print("you met final deadend you decide to go thourgh it")
    print("you at homeroom")
    character.current_position = "Homeroom"

def boss_room():
    if character.current_position == "Boss_room":
        for item in character.items:
            if item["name"] == "true-key":
                print("you enter boss-room")
                print("you met supreme-theif")
                showroom("Boss_room")
                fight("Boss_room")
                return
        else:
            print("you don't have the key")
            return

def playerwon():
    for item in character.items:
        if item["name"] == "boss-loot":
            return True
    
def check_monster_die(monster):
    return monster["hp"] <=0

def check_player_die(player):
    return player['hp'] <= 0

#checkdefense <= quai ko
def defensemechanic(character, damage):
    if character["defense"] > damage:
        return 0
    else:
        return damage - character["defense"]
        

def fireoftruth(monster):
    lives = 3
    bossheart = 4
    print("If you must sacrifice one... your life or your name... which survives eternity?")
    print("1. life\n2.name")
    question1 = input_int("choose wisely: ")
    if question1 == 1:
        print("The living fear death. The worthy fear being forgotten")
        lives = lives -1
    else:
        print("A body returns to dust... but a name carved into eternity never dies")
        bossheart = bossheart - 1
    
    print("Next question which exits even if no one believes in it?")
    print("1.Truth\n2.Belief")
    question2 = input_int("choose wisely")
    if question2 == 2:
        print("Falsehood cannot exist without truth.")
        lives = lives -1
    else:
        print ("Belief does not create truth")
        bossheart = bossheart - 1
    print("Next question. Which deserves more protection?")
    print("1. Truth\n2. Your Feelings")
    question3 = input_int("choose wisely: ")
    if question3 == 2:
        print("Feelings change. Truth does not.")
        lives = lives - 1
    else:
        print("Truth survives wounded pride.")
        bossheart = bossheart -1 
    print("Next question. Which creates a king?")
    print("1. Power\n2. Respect")
    question4 = input_int("choose wisely: ")
    if question4 == 1:
        print("Power commands bodies. Respect commands generations.")
        lives = lives - 1
    else:
        print("Power is taken. Respect is earned.")
        bossheart = bossheart - 1
    print("Final Question.")
    print("Choose the lie.")
    print("1. A closed eye cannot see.")
    print("2. An open eye always sees.")
    question5 = input_int("choose wisely: ")

    if question5 == 1:
        print("Sight is not vision. An open eye can still be blind.")
        lives = 0
    else:
        print("Correct.")
        print("Many open their eyes... yet never see.")
        bossheart = bossheart -1
    if bossheart >= lives:
        character["hp"] = 0
        if check_player_die(character):
            print("torturing by numerous question, you quietly fall down to the ground")
            return
    else:
        print("bravo you kill a strong entity")
        for i,n in enumerate(rooms["Bersek-room"]):
            if n["name"] == "Fire of Truth":
                rooms["Bersek-room"].pop(i)
                break
def supthief():
        thief = rooms["Boss_room"]["monster"][0]
        while thief["hp"] > 0 and character["hp"] >0:
            print("the thief stole 10hp from you")
            thief["hp"] += 10
            character["hp"] -= 10
            print("the thief roll a dice")
            time.sleep(1)   # dừng 1 giây trước khi in tiếp
        
            thiefdice = random.randint(1,6)
            playerdice = random.randint(1,6)
            print(f"Thief rolled: {thiefdice}")
            time.sleep(1)
            print(f"You rolled: {playerdice}")
            if thiefdice > playerdice:
                character["hp"] -= (thief["damage"]) / thiefdice
            else:
                thief["hp"] -= character["damage"] * playerdice
        if thief["hp"] <= 0:
            del rooms["Boss_room"]["monster"][0]
        elif check_player_die(character):
            return
            

def check_special_monster(monster):
        return monster["type"] == "specialmonster"

def handle_special_monster(monster):
        if monster["name"] == "Fire of Truth":
            fireoftruth(monster)
        elif monster["name"] == "the trace of supreme-thief":
            supthief()
            
def attack(attacker, target):
        print("let the fate decide your destiny.")
        fate = random.randint(1, 5)
        choose = input_int("press 1 to 5 to attack: ")
        
        if choose == fate:
            target.takedamage(attacker.damage * 2)
        elif choose == fate + 1 or choose == fate - 1:
            target.takedamage(attacker.damage *1.5)
        elif choose == fate + 2 or choose == fate - 2:
            target.takedamage(attacker.damage * 1)
        else:
            print("you missed")
        
        if target.isdead():
            monsterloot(target)
            return
        
        print(f"{target.name} phase")
        if check_player_die(attacker):
            return
        
def monsterloot(monster):
    if check_special_monster(monster):
        return
    else:
        coins = random.randint(1,10)
        print(f"you recieve {coins} coins")
        character.gold +=coins
def monstercounterattack(monster):
    monsterfate = random.randint(1, 5)
    monsterchoose = random.randint(1, 5)
            
    if monsterchoose == monsterfate:
                damage = defensemechanic(character, monster["damage"]*1.5)
    else:
                damage = defensemechanic(character, monster["damage"])
    character["hp"] -= damage
    print(f"{monster['name']} deal {damage}")
            
    if character.isdead():
        return
      
def fight(room_name):
    room = rooms[room_name]
    if room["monster"] is None:
        print("no monster here you are safe now")
        return
    if len(room["monster"]) == 0:
        print("all monster dead")
        return
    n = False
    while n == False: 
        choice = input_int("choose 0 to 3 (if lucky you could flee the attack): ")
        fate = random.randint(0,3)
        if fate == choice and rooms[character.current_position]["monster"][0]["name"] != "the trace of supreme-thief":
            print("It doesn't seem to notice me... I'm safe for now.")
            return
        else:
            n = True   
        print("It noticed me!")
        for i, monster in enumerate(room["monster"]):
            print(f"{i}, {monster['name']}")
        yourchoice = input_int("you decide to encounter: ")
        for i, monster in enumerate(room["monster"]):
            if i == yourchoice:
                print(f"you deal with {rooms[character.current_position]["monster"][i]["name"]}")
                break
        x = False
        target = room["monster"][yourchoice]
        while x == False:
            action = input_int("1. attack\n2. use item\nchoose action: ")   # <- THÊM DÒNG NÀY
            
            if action == 1:
                if check_special_monster(target):
                    handle_special_monster(target)
                else:
                    attack(character, target)
                    if check_monster_die(target):
                        print(f"you slain {target['name']}")
                        monsterloot(target)
                        room["monster"].remove(target)
                        x = True
                        break
                    else:
                        monstercounterattack(target)
                    
            elif action == 2:
                if check_special_monster(target):
                    continue
                else:
                    useitem(target)# truyền quái đang chọn vào, để useitem() biết target là ai
                    if check_monster_die(target):
                        print(f"you slain {target['name']}")
                        monsterloot(target)
                        room["monster"].remove(target)
                        x = True
                        break
                    monstercounterattack(target)
            if character.isdead():
                print("you die")
                return
            
            for m in room["monster"][:]:
                if check_monster_die(m):
                    print(f"you slain {m['name']}")
                    monsterloot(m)
                    room["monster"].remove(m)
                    x = True
                    break
            else:
                continue
           
while True:
    if playerwon():
        print("you won")
        break
    showroom(character.current_position)
    if character.current_position == "Mysterious-shop":
        shop()
    elif character.current_position == "Trap-room":
        trap_room()
    elif character == "Deadend":
        deadend()
    elif character.current_position == "Boss_room":
        boss_room()
    else:
        fight(character.current_position)
    if character.isdead():
        reset_game()
        continue
    while True:
        print("""
                [1] item menu 
                [2] show inventory
                [3] show visited places
                [4] move
                [5] exit
                
            """)
        choice = input_int("choose an action: ")
        if choice == 1:
            item_menu()
        elif choice == 2:
            showinventory()
        elif choice == 3:
            showmap()
        elif choice == 4:
            moving_character(character.current_position)
        elif choice == 5:
            exit()
        else:
            print("invalid choice")
        if character.isdead():
            reset_game
    
        
    


                            
                                
                            
                        
                        
                    
