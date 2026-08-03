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
            {"name": "Fire of Truth", "damage": 1000, "type": "monster", "hp":3}
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
            {"name": "the trace of supreme-thief", "damage": 100, "type": "monster", "hp": 500}
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
    }
}
current_room = "Homeroom"
current_health = 100
def input_int(number):
    while True
        

def showroom(room_name):
    room = rooms[room_name]

    print(room["description"])
    print(f"You are in: {room_name}")
#monster for showing
    if room["monster"] is None:
        print("No monsters.")
    else:
        print("You see")
        for monster in room["monster"]:
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
    n = int(input("choose where to head to: "))
    for i, (direction,phong)  in enumerate((room["exits"]).items()):
        if n == i:
            break
    else:
        print("path don't exits")
        return
    return phong
def fight(room_name):
    room = rooms[room_name]
    print("choose 0 or 1")
    flee = False
    while flee == False:
        personchoice = int(input("let the fate decide your destiny!: "))
        if personchoice == random.randint(0,1):
            print("you feel relief as if something has passed you")
            flee = True
        battle = -1
        while battle != 0:
            
        
        
        
    
    
    
    
        