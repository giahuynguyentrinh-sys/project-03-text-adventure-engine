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
            {"name": "note", "type": "lore"}
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
        "exits": {"back": "Bersek-room", "straight": "Deadend"},
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
        "exits": {"left": "Boss-room", "straight": "Mysterious-shop"},
        "items": [
            {"name": "true-key", "type": "key"},
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
            {"name": "boss-key", "type": "key"},
        ],
        "monster": None,
        "npc": None
    },
    "Boss_room": {
        "description": "A massive chamber cloaked in shadows. At its center stands the final guardian, waiting.",
        "exits": {"back": "Vault"},
        "items": [
            {"name": "boss-loot", "type": "treasure"}
        ],
        "monster": [
            {"name": "the trace of supreme-thief", "damage": 100, "type": "specialmonster", "hp": 500}
        ],
        "npc": None
    },
    "Deadend": {
        "description": "A black face gradually appears out of nowhere. Fortunately, it is just a black wall with meticulous details.",
        "monster": [
            {"name": "Faceless", "damage": 10, "type": "monster", "hp":10 }
        ],
        "npc": None,
        "exits": {"back": "Homeroom"},
        "items": None
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
    "current_position" : "Homeroom"
}
rooms_original = copy.deepcopy(rooms)
character_original = copy.deepcopy(character)

def reset_game():
    global rooms, character
    rooms = copy.deepcopy(rooms)
    character = copy.deepcopy(character)
    print("reset the world")

def showweapon(weapons):
    for weapon in weapons:
        print(f"you have {weapon["name"],{weapon["damage"]}}")
    


def input_int(number):
    while True:
        try:
            return int(input(number))
        except ValueError:
            print("Hey stop fucking my game")        

def showroom(room_name):
    room = rooms[room_name]
    print(room["description"])
    print(f"You are in: {room_name}")
#The lesson here: enumerate() always hands you (number, item) in that fixed order
def moving_character(room_name):      
    room = rooms[room_name]
    for i, direction in enumerate(room["exits"].keys()):
        print(i, direction)
    n = input_int("choose where to head to: ")
    for i, (direction,phong)  in enumerate((room["exits"]).items()):
        if n == i:
            character["current_position"] = phong
            return
    else:
        print("path don't exits")
        return

def notenoughgold(itemgold):
    if character["gold"] < itemgold:
        print("you don't have enough gold")
        return  
def shop():
    if character["current_position"] == "Mysterious-shop":
        while True:
            for i,item in enumerate(rooms["Mysterious-shop"]["items"], start = 1):
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
    if character["current_position"] == "Trap-room":
        while True:
            print("1.Take the boss-key and exit\n2.Exit")
            n = input_int("press an number: ")
            if n == 1:
                dice = random.randint(0,3)
                time.sleep(0.5)
                if dice == 3:
                    print("you exit with boss key")
                    character["items"].append(rooms["Trap-room"]["items"][0])
                    return
                else:
                    character["hp"] -= 50
                    print("ouch you have stepped on rusty spike (-50hp)")
                    if check_player_die(character):
                        return
                    print("you exit trap-room")
                    return
            elif n == 2:
                dice = random.randint(1,2)
                time.sleep(0.5)
                if dice == 1:
                    character["hp"] = 1
                    print("you step onto the bomb")
                else:
                    print("you exit")
                    return
                return

def boss_room(Boss_room):
    if character["current_position"] == "Boss_room":
        for item in character["items"]:
            if any(item["name"]) == "true-key":
                print("you enter boss-room")
                print("you met supreme-theif")
                showroom(Boss_room)
                fight(Boss_room)
                if check_player_die(character):
                    break
                else:
                    takeitems()
                    break
        else:
            print("you don't have the key")
            return

def playerwon():
    for item in character["items"]:
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
        

def fireoftruth():
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
            fireoftruth()
        elif monster["name"] == "the trace of supreme-thief":
            supthief()
            
def attack(i):
        monster = rooms[character["current_position"]]["monster"][i]
        print("let the fate decide your destiny.")
        fate = random.randint(1, 5)
        choose = input_int("press 1 to 5 to attack: ")
        
        if choose == fate:
            monster["hp"] -= character["damage"] * 2
        elif choose == fate + 1 or choose == fate - 1:
            monster["hp"] -= character["damage"] * 1.5
        elif choose == fate + 2 or choose == fate - 2:
            monster["hp"] -= character["damage"]
        else:
            print("you missed")
        
        if monster["hp"] <= 0:
            return
        
        print(f"{monster['name']} phase")
        
        if monster["damage"] == 0:
            print("supreme-thieft look at you and smirk, slowly vanished through the air")
            del rooms["vault"]["monster"][0]
            return
        
        monsterfate = random.randint(1, 5)
        monsterchoose = random.randint(1, 5)
        
        if monsterchoose == monsterfate:
            dmg = defensemechanic(character, monster["damage"]*1.5)
        else:
            dmg = defensemechanic(character, monster["damage"])
        character["hp"] -= dmg
        print(f"{monster['name']} deal {dmg}")
        
        if check_player_die(character):
            return
        
def monsterloot(monster):
    if check_special_monster(monster):
        return
    else:
        coins = random.randint(1,10)
        print(f"you recieve {coins} coins")
        character["gold"]+=coins
        


def showinventory(target):
    if not target["items"]:
        print("no items")
        return
    else:
        for i,item in enumerate(target["items"]):
            print(f"{i}, {item}")  


def chooseitem(message, target):
    if not target["items"]:
        return None
    else:
        while True:
            try:
                showinventory(target)
                choice = input_int(message)
                return target["items"][choice]
            except IndexError:
                print("invalid number")

def takeitems():
    if not rooms[character["current_position"]]["items"]:
        print("no items found")
        return None
    else: 
        item = chooseitem("choose an item to take: ", rooms[character["current_position"]])
        character["items"].append(item)
        rooms[character["current_position"]]["items"].remove(item) 
    
    
def choosetarget(monster, character):
    print("1.monster\n2.player")
    playerchoice = input_int("please choose a number")
    if playerchoice == 1:
        return monster
    elif playerchoice == 2:
        return character           
    
def equip_item(item, slot_name, stat_name):
    """
    slot_name: "weapon" hoặc "defweapon"
    stat_name: "damage" hoặc "defense"
    """
    if len(character[slot_name]) == 1:
        playerchoice = input_int("1.change item\n2.cancel")
        if playerchoice == 1:
            old_item = character[slot_name][0]
            character[slot_name].remove(old_item)
            character["items"].append(old_item)
            character[stat_name] -= old_item[stat_name]
            
            character[slot_name].append(item)
            character[stat_name] += item[stat_name]
            character["items"].remove(item)
        else:
            return
    else:
        character[slot_name].append(item)
        character[stat_name] += item[stat_name]
        character["items"].remove(item)
        
    
    
def useitem(monster):
    item = chooseitem("choose item", character)
    if monster is None:
        target = character
    else:
        target = choosetarget(monster, character)
    if item["name"] == "strength-potion":
            character["damage"] += item["damage"]
            character["items"].remove(item)
    elif item["name"] == "magical-book":
            monster["hp"] -= item["damage"]
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

def monstercounterattack(monster):
    monsterfate = random.randint(1, 5)
    monsterchoose = random.randint(1, 5)
            
    if monsterchoose == monsterfate:
                dmg = defensemechanic(character, monster["damage"]*1.5)
    else:
                dmg = defensemechanic(character, monster["damage"])
    character["hp"] -= dmg
    print(f"{monster['name']} deal {dmg}")
            
    if check_player_die(character):
        return
      
def fight(room_name):
    room = rooms[room_name]
    if room["monster"] is None:
        print("no monster here you are safe now")
        return
    else:
        print("a figure rising from the dark")
    n = False
    while n == False:
        choice = input_int("choose 0 to 3: ")
        fate = random.randint(0,3)
        if fate == choice and rooms[character["current_position"]]["monster"][0]["name"] != "the trace of supreme-thief":
            print("It doesn't seem to notice me... I'm safe for now.")
            return
        else:
            n = True   
        print("It noticed me!")
        for i, monster in enumerate(room["monster"]):
                        print(f"{i}, {monster['name']}")           
        yourchoice = input_int("you decide to encounter: ")
        print(f"you deal with {monster[yourchoice]["name"]}")
        x = False
        while x == False:
            target = room["monster"][yourchoice]
            action = input_int("1. attack\n2. use item\nchoose action: ")   # <- THÊM DÒNG NÀY
            
            if action == 1:
                if check_special_monster(target):
                    handle_special_monster(target)
                else:
                    attack(yourchoice)
            elif action == 2:
                useitem(target)          # truyền quái đang chọn vào, để useitem() biết target là ai
            
            if check_player_die(character):
                print("you dead")
                return
            
            for m in room["monster"][:]:
                if m["name"] == "Faceless" and m["hp"] <= 0:
                    print("you slain Faceless but something off happen, it not dead")
                    return
                if check_monster_die(m):
                    print(f"you slain {m['name']}")
                    monsterloot(m)
                    room["monster"].remove(m)
                    x = True
                    break
            if len(room["monster"]) > 0 or check_monster_die(target):
                x = True
            else:
                return
        x = True
           
while True:
    if playerwon():
        print("you won")
        break
    showroom(character["current_position"])
    if character["current_position"] == "Mysterious-shop":
        shop()
    elif character["current_position"] == "Trap-room":
        trap_room()
    elif character["current_position"] == "Boss_room":
        boss_room(character["current_position"])
    else:
        fight(character["current_position"])
    if check_player_die(character):
        reset_game()
        continue
    while True:
        print("""
                [1] take item
                [2] use item  
                [3] show inventory
                [4] move
                [5] exit
                
            """)
        choice = input_int("choose an action: ")
        if choice == 1:
            takeitems()
        elif choice == 2:
            useitem(None)
        elif choice == 3:
            showinventory(character)
            showweapon(character["weapon"])
            showweapon(character["defweapon"])
        elif choice == 4:
            moving_character(character["current_position"])
            break
        elif choice == 5:
            exit()
        else:
            print("invalid choice")
        if check_player_die(character):
            reset_game()
    
        
    


                            
                                
                            
                        
                        
                    
