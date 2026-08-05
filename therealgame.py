# Room
import random
rooms = {
    "Homeroom": {
        "description": "You feel the cold slicing through your body\nyou vomit and start to have hallucinations\nwonder what it is",
        "exits": {"straight": "Execution-room", "left": "Mysterious-shop", "right": "Quiet-room"},
        "items": [
            {"name": "rusty-sword", "damage": 15, "type": "weapon"},
            {"name": "note", "type": "lore"}
        ],
        "monster": None,
        "npc": None
    },
    "Mysterious-shop": {
        "description": "Shelves overflow with odd potions, dusty relics, and enchanted curiosities from forgotten lands.",
        "exits": {"right": "Homeroom"},
        "items": [
            {"name": "exotic-health-potion", "damage": 50, "type": "healing-items"},
            {"name": "steel-armor", "defense": 20, "type": "armor"},
            {"name": "sword", "damage": 20, "type": "weapon"},
            {"name": "apple", "damage": 5, "type": "healing-items"},
            {"name": "poison", "damage": 15, "type": "weapon"}
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
            {"name": "axe", "damage": 30, "type": "weapon"},
            {"name": "human-meat", "damage": 10, "type": "healing-items"}
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
            {"name": "magical-book", "type": "opitem"},
            {"name": "health-potion", "damage": 30, "type": "healing-items"}
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
            {"name": "fire-poison", "damage": 10, "type": "weapon"},
            {"name": "fire-sword", "damage": 30, "type": "weapon"}
        ],
        "npc": None
    },
    "Vault": {
        "description": "A chamber overflowing with unimaginable wealth. The silence is unsettling, and the treasure seems almost too easy to take.",
        "exits": {"left": "Boss-room", "straight": "Mysterious-shop"},
        "items": [
            {"name": "True key", "type": "key"},
            {"name": "Gold", "type": "money"}
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
            {"name": "rusty-spike", "damage": 15, "type": "weapon"},
            {"name": "bomb", "damage": 100, "type": "weapon"}
        ],
        "monster": None,
        "npc": None
    },
    "Boss-room": {
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
    "damage": 10,
    "defense": 10,
    "current_position" : "Homeroom"
}

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
#monster for showing
    if room["monster"] is None:
        print("", end="")
    else:
        print("You see")
        for monster in room:
            print(f"-{monster["name"]}")
#npc for showing
    if room["npc"] is None:
        print("No NPCs.")
    else:
        print("You meet")
        for npc in room["npc"]:
            print(f"-{npc["name"]}")
#items for showing
    if room["items"] is None:
        print("No items here in this room")
    else:
        print("you found")
        for items in room["items"]:
            print(f"-{items["name"]}")
#exit for showing
    if room["exits"] is None:
        print("The biggest wall i have ever seen in my life and you still think that i can't pass this, screw you")
    else:
        print("you can go")
        for exit, name in room["exits"].items():
            print (f"-{exit}")
#The lesson here: enumerate() always hands you (number, item) in that fixed order
def moving_character(room_name):
    room = rooms[room_name]
    for i, direction in enumerate(room["exits"].keys()):
        print(i, direction)
    n = input_int("choose where to head to: ")
    for i, (direction,phong)  in enumerate((room["exits"]).items()):
        if n == i:
            break
    else:
        print("path don't exits")
        return
    return phong

def fireoftruth():
    lives = 3
    print("If you must sacrifice one... your life or your name... which survives eternity?")
    print("1. life\n2.name")
    question1 = input_int("choose wisely: ")
    if question1 == 1:
        print("The living fear death. The worthy fear being forgotten")
        lives = lives -1
    else:
        print("A body returns to dust... but a name carved into eternity never dies")
    
    print("Next question which exits even if no one believes in it?")
    print("1.Truth\n2.Belief")
    question2 = input_int("choose wisely")
    if question2 == 2:
        print("Falsehood cannot exist without truth.")
        lives = lives -1
    else:
        print ("Belief does not create truth")
        
    print("Next question. Which deserves more protection?")
    print("1. Truth\n2. Your Feelings")
    question3 = input_int("choose wisely: ")
    if question3 == 2:
        print("Feelings change. Truth does not.")
        lives = lives - 1
    else:
        print("Truth survives wounded pride.")
        
    print("Next question. Which creates a king?")
    print("1. Power\n2. Respect")
    question4 = input_int("choose wisely: ")
    if question4 == 1:
        print("Power commands bodies. Respect commands generations.")
        lives = lives - 1
    else:
        print("Power is taken. Respect is earned.")
        
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

    

def check_special_monster(i):
    room = rooms[character["current_position"]]
    for monster in room["monster"]:
        if monster["name"] == "Fire of Truth":
            
        
def attack(i):
    hp_character = character["hp"]
    hp_monster = rooms[character["current_position"]]["monster"][i]["hp"]
    list_monster = rooms[character["current_position"]]["monster"][i]
    print("let the fate decide your destiny.")
    fate = random.randint(1,5)
    choose = input_int("press 1 to 5 to attack: ")
    if choose == fate:
        hp_monster = hp_monster - (character["damage"] *2)
    elif choose == fate +1 or choose == fate -1:
        hp_monster = hp_monster - (character["damage"] *1.5)
    elif choose == fate +2 or choose == fate -2:
        hp_monster = hp_monster - (character["damage"])
    else:
        print("you missed")
    if hp_monster <= 0:
        return
    print(f"{list_monster["name"]} phase")
    if list_monster["damage"] == 0:
        print("supreme-thieft look at you and smirk, slowly vanished through the air")
    else:
        monsterfate = random.randint(1,5)
        monsterchoose = random.randint(1,5)
        if monsterchoose == monsterfate:
            hp_character = hp_character - (list_monster["damage"]*1.5)
            print(f"{list_monster["name"]} deal {list_monster["damage"]*1.5} ")
        else:
            hp_character = hp_character - (list_monster["damage"])
            print(f"{list_monster["name"]} deal {list_monster["damage"]} ")
        if hp_character <= 0:
                return
    character["hp"] = hp_character
    rooms[character["current_position"]]["monster"][i]["hp"] = hp_monster     
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
        if fate == choice:
            print("It doesn't seem to notice me... I'm safe for now.")
            return
        else:
            n = True   
    print("It noticed me!")
    while character["hp"] >0 and len(room["monster"]) > 0:
            for i,monster in enumerate(room["monster"]):
                print(f"{i}, {monster["name"]}")
                yourchoice = input_int("you decide to encounter: ")
                if i == yourchoice:
                    attack(i)
                if character["hp"] <= 0:
                    print("you die")
                    return
            for i,monster in enumerate(room["monster"][:]):
                if monster["name"] == "Faceless" and monster["hp"] <=0:
                    print(f"you slain Faceless but something off happen, it not dead")
                    monster["hp"] = 10
                    continue
                else:   
                    if monster["hp"] <= 0:
                        print(f"you slain {monster["name"]}")
                        room["monster"].remove(monster)


                
                
            
        
        
    
