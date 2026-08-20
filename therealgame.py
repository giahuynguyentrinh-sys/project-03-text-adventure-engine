# Room
import random
import time
import copy
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


class items:
    def __init__(self, name, damage, type, category, price=0):
        self.name = name
        self.damage = damage
        self.type = type
        self.category = category
        self.price = price

    def usingitem(self, character, monster=None):
        if self.category == "weapon":
            weapon.equipweapon(self, character, character.defweapon, character.weapon)
        elif self.category == "potion":
            target = character.choosetarget(monster)
            if target is None:
                print("invalid target, item not used")
                return
            potion.potioneffect(self, target)
        elif self.category == "key":
            print("required exact room")

        
class weapon(items):
    def replaceweapon(self, character, slot_weapon):
        old_item = slot_weapon[0]
        character.items.append(old_item)
        slot_weapon.remove(old_item)
        old_item.updatestat(character, add = False)
        slot_weapon.append(self)
        character.items.remove(self)
        self.updatestat(character, add = True)
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
    def equipweapon(self, character, defweapon, weapon):
        if len(character.weapon) == 1 and self.type == "sword":
            self.replaceweapon(character, weapon)
        elif len(character.defweapon) == 1 and self.type == "armor":
            self.replaceweapon(character, defweapon)
        elif self.type == "sword":
            character.weapon.append(self)
            character.items.remove(self)
            self.updatestat(character, add = True)
        elif self.type == "armor":
            character.defweapon.append(self)
            character.items.remove(self)
            self.updatestat(character,add = True)

class potion(items):
    def potioneffect(self, target):
        if self.type == "healing_potion":
            target.hp += self.damage
        elif self.type == "stat_potion":
            target.damage += self.damage
        elif self.type == "damage_potion":
            target.hp -= self.damage        
        else:
            return
class key(items):
    def __init__(self, name, unlocks,category, type,price=0):
        super().__init__(name = name, damage= 0,category =category, type = type, price = price)
        self.unlocks = unlocks
    def unlockroom(self, unlocks):
        return self.unlocks == unlocks
   
#weapon
rustysword = weapon(name="rusty-sword", damage=15, category="weapon", type="sword")
shop_sword = weapon(name="sword", damage=20, category="weapon", type="sword", price=30)
axe = weapon(name="axe", damage=30, category="weapon", type="sword")
magical_book = weapon(name="magical-book", damage=50, category="weapon", type="sword")
fire_sword = weapon(name="fire-sword", damage=40, category="weapon", type="sword")
#defweapon
shield = weapon(name="shield", damage=30, category="weapon", type="armor")
supershield = weapon(name="shield", damage="50", category ="weapon", type="armor" )
#potion
exotic_health_potion = potion(name="exotic_potion", damage=70, category="potion", type="healing_potion", price=80)
strength_potion = potion(name="strength_potion", damage=20, category="potion", type="stat_potion", price=20)
poison = potion(name="poison", damage=30, category="potion", type="damage_potion", price=40)
fire_poison = potion(name="fire_poison", damage=40, category="potion", type="damage_potion", price=0)
health_potion = potion(name="health_potion", damage=25, category="potion", type="healing_potion", price=0)
#food
apple = potion(name="apple", damage=10, category="potion", type="healing_potion", price=10)
human_meat = potion(name="human_meat", damage=30, category="potion", type="healing_potion", price=0)
#key
true_key = key(name="true_key", category = "key", type = "key",unlocks="Vault", price=0)
boss_key = key(name="boss_key", category = "key", type = "key",unlocks="Boss_room", price=0)
boss_loot = key(name="boss_loot", category = "key", type = "key",unlocks="True_end", price=0)
   

class rooms:
    def __init__(self, name, information,exits =None, items = None, monsters = None):
        self.name = name
        self.information = information
        self.exits = exits if exits is not None else []
        self.items = items if items is not None else []
        self.monsters = monsters if monsters is not None else []
    def additem(self, item):
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
    exits={"back": "Bersek-room", "straight": "Deadend", "left": "Homeroom"},
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
roomlist = {
    "Homeroom": Homeroom,
    "Mysterious-shop": Mysterious_shop,
    "Execution-room": Execution_room,
    "Quiet-room": Quiet_room,
    "Bersek-room": Bersek_room,
    "Vault": Vault,
    "Trap-room": Trap_room,
    "Boss_room": Boss_room,
    "Deadend": Deadend,
    "Trueend": Trueend
}
Quiet_room.items.extend([true_key])
Homeroom.items.extend([rustysword])
Mysterious_shop.items.extend([exotic_health_potion, shop_sword, strength_potion, poison,apple])
Execution_room.items.extend([axe, human_meat])
Bersek_room.items.extend([fire_poison, fire_sword])
Vault.items.extend([supershield])
Trap_room.items.extend([boss_key])
Boss_room.items.extend([boss_loot])
Deadend.items.extend([]) 
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
    def spawnmonster(name,hp,damage,type ="monster"):
        return CHARACTER(name=name,hp=hp, damage = damage, type = type,gold = random.randint(1,10))
    
    def dealdamage(self, damage, attacker):
        actual_damage = max(0, damage - self.defense)
        self.hp -= actual_damage
        print(f"{attacker.name} deal {actual_damage}")
        return actual_damage
    def statincombat(self, monster):
        print("╔══════════════════════════════════════╗")
        print("║              COMBAT STATUS           ║")
        print("╠════════════════════╦═════════════════╣")
        print("║      CHARACTER     ║     MONSTER     ║")
        print("╠════════════════════╬═════════════════╣")
        print(f"║ HP: {self.hp:<14} ║ HP: {monster.hp:<12} ║")
        print(f"║ DMG: {self.damage:<13} ║ DMG: {monster.damage:<11} ║")
        print("╚════════════════════╩═════════════════╝")
    def isdead(self):
        return self.hp <=0
    #item
    def choosetarget(self, monster):
        if monster is None:
            print("no monster here, using on yourself")
            return self
        print("1.yourself\n2.monster")
        playerchoice = input_int("please choose a number: ")
        if playerchoice == 1:
            return self
        elif playerchoice == 2:
            return monster
        else:
            print("invalid choice")
            return None

 
#you
character = CHARACTER(
name = "hero",
hp = 10000000,
damage = 1000000,
defense = character["defense"],
items = character["items"],
gold = character["gold"],
weapon = character["weapon"],
defweapon = character["defweapon"],
current_position= "Homeroom",
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
fire_of_truth = CHARACTER.spawnmonster("Fire of Truth", 1000, 1000,type ="specialmonster")
supreme_thief_trace = CHARACTER.spawnmonster("the trace of supreme-thief", 500, 100, type= "specialmonster")

Execution_room.monsters.extend([executioner, weak_zombie])
Quiet_room.monsters.extend([strong_zombie, orc])
Bersek_room.monsters.extend([fallen_knight, fire_of_truth])
Vault.monsters.extend([supreme_thief])
Boss_room.monsters.extend([supreme_thief_trace])
Deadend.monsters.extend([faceless])
#gia tri goc cua game
rooms_original = copy.deepcopy(roomlist)
character_original = copy.deepcopy(character)

def reset_game():
    global roomlist, character 
    roomlist = copy.deepcopy(rooms_original)
    character = copy.deepcopy(character_original)
    print("reset the world")
    
#item
#show inventory cho người chơi.
def showinventory(target):
    if not target.items:
        print("no item")
        return
    for i, item in enumerate(target.items):
        print(f"{i}, {item.name}")

def chooseitem(target):
    if not target.items:
        return None
    while True:
        try:
            choice = input_int("choose item: ")
            return target.items[choice]
        except IndexError:
            print("invalid number")

def showitemstat():
    item = chooseitem(character)
    if item is None:
        print("no item found")
        return
    print(f"{item.name}, {item.damage}")

def takeitems():
    current_room = roomlist[character.current_position]
    if not current_room.items:
        print("no items found")
        return
    showinventory(current_room)
    item = chooseitem(current_room)
    character.items.append(item)
    current_room.items.remove(item)

def dropitems():
    current_room = roomlist[character.current_position]
    if not character.items:
        print("no item to drop")
        return
    showinventory(character)
    item = chooseitem(character)
    print(f"you dropped {item.name}")
    current_room.items.append(item)
    character.items.remove(item)

def item_menu():
    while True:
        current_monsters = roomlist[character.current_position].monsters
        print(f"hp: {character.hp}")
        print(f"damage: {character.damage}")
        print("inventory:")
        showinventory(character)
        print("""
                [1] take item
                [2] use item
                [3] drop item
                [4] show item stat
                [5] back to main menu
            """)
        choice = input_int("choose an action: ")
        if choice == 1:
            takeitems()
        elif choice == 2:
            if not character.items:
                print("no item to use")
                continue
            showinventory(character)
            chosen_item = chooseitem(character)
            if chosen_item is None:
                continue
            if chosen_item.category == "potion" and current_monsters:
                idx = choosemonster()
                chosen_item.usingitem(character, current_monsters[idx])
            else:
                chosen_item.usingitem(character, None)
        elif choice == 3:
            dropitems()
        elif choice == 4:
            showitemstat()
        elif choice == 5:
            return
        else:
            print("invalid choice")


def showmap():
    print("____Map____")
    for names in roomlist:
        if names in character.visited_room:
            print(f"[X] {names}")
        else:
            print(f"[?] {names}")
        
def input_int(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Hey stop fucking my game") 
            
def showroom():
    current_room = roomlist[character.current_position]
    print(current_room.information)
    print(f"You are in: {current_room.name}")
    
#The lesson here: enumerate() always hands you (number, item) in that fixed order
def moving_character():
    current_room = roomlist[character.current_position]
    for i, (direction, rom) in enumerate(current_room.exits.items()):
        if rom in character.visited_room:
                print(f"{i}, {direction} --->{rom}")
        else:
                print(f"{i}, {direction} ---> ???")
    n = input_int("choose where to head to: ")
    for i, (direction,phong)  in enumerate(current_room.exits.items()):
        if n == i:
            character.current_position = phong
            character.visited_room.add(character.current_position)
            return
    else:
        print("path don't exits")
        return

def enoughgold(character, items):
    if character.gold > items.price:
        return True
    else:
        return False

def shop():
        current_room = roomlist[character.current_position]
        while True:
            for i,item in enumerate(current_room.items, start = 1):
                print(f"{i}. {item.name}|{item.price}gold")
            print("0.cancel")    
            playerchoice = input_int("press to buy: ") 
            if playerchoice == 0:
                return
            if enoughgold(character, current_room.items[playerchoice -1]):   
                character.gold -= current_room.items[playerchoice -1].price
                print(f"you buy {current_room.items[playerchoice -1]}")
                character.items.append(current_room.items[playerchoice -1])
                   
            
def trap_room():
        while True:
            print("1.Take the boss-key and exit\n2.Exit")
            n = input_int("press an number: ")
            if n == 1:
                dice = random.randint(0,3)
                time.sleep(0.5)
                if dice == 3:
                    print("you exit with boss key")
                    character.items.append(roomlist[character.current_position].items[0])
                    return
                else:
                    character.hp -= 50
                    print("ouch you have stepped on rusty spike (-50hp)")
                    if character.isdead():
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
    fight()
    if character.isdead():
        reset_game()
    print("you met final deadend you decide to go thourgh it")
    print("you at homeroom")
    character.current_position = "Homeroom"

def boss_room():
    for item in character.items:
            if item.name == "true_key":
                print("you enter boss-room")
                print("you met supreme-theif")
                showroom()
                fight()
                return
    else:
        print("you don't have the key")
        return

def playerwon():
    for item in character.items:
        if item.name == "boss_loot":
            return True


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
        character.hp = 0
        if character.isdead():
            print("torturing by numerous question, you quietly fall down to the ground")
            return
    else:
        print("bravo you kill a strong entity")
        for i,n in enumerate(roomlist["Bersek-room"].monsters):
            if n.name == "Fire of Truth":
                roomlist["Bersek-room"].pop(i)
                break
def supthief():
        thief = roomlist.Boss_room.monsters[0]
        while thief.hp > 0 and character.hp >0:
            print("the thief stole 10hp from you")
            thief.hp += 10
            character.hp -= 10
            character.statincombat(thief)
            print("the thief roll a dice")
            time.sleep(1)   # dừng 1 giây trước khi in tiếp
            thiefdice = random.randint(1,6)
            playerdice = random.randint(1,6)
            print(f"Thief rolled: {thiefdice}")
            time.sleep(1)
            print(f"You rolled: {playerdice}")
            if thiefdice > playerdice:
                character.hp -= thief.damage / thiefdice
            else:
                thief.hp -= character.damage * playerdice
            character.statincombat(thief)
        if thief.hp <= 0:
            del roomlist["Boss_room"].monsters[0]
        elif character.isdead():
            return



def check_special_monster(monster):
        return monster.type == "specialmonster"

def handle_special_monster(monster):
        if monster.name == "Fire of Truth":
            fireoftruth()
        elif monster.name == "the trace of supreme-thief":
            supthief()
            
def attack(character, monster):
        fate = random.randint(1, 5)
        choose = input_int("press 1 to 5 to attack: ")
        
        if choose == fate:
            monster.dealdamage(character.damage * 2, character)
        elif choose == fate + 1 or choose == fate - 1:
            monster.dealdamage(character.damage *1.5, character)
        elif choose == fate + 2 or choose == fate - 2:
            monster.dealdamage(character.damage * 1, character)
        else:
            print("you missed")
        character.statincombat(monster)
        if monster.isdead():
            monsterloot(monster)
            return
        print(f"{monster.name} phase")
        if character.isdead():
            return

def choosemonster():
    current_room = roomlist[character.current_position]
    for i, monster in enumerate(current_room.monsters):
        print(f"{i}, {monster.name}")
    yourchoice = input_int("you decide to encounter: ")
    return yourchoice
        
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
                damage = character.dealdamage(monster.damage*1.5, monster)
    else:
                damage = character.dealdamage(monster.damage, monster)
    character.hp -= damage       
    if character.isdead():
        return
      
def fight():
    room = roomlist[character.current_position]
    if room.monsters is None:
        print("no monster here you are safe now")
        return
    if len(room.monsters) == 0:
        return
    n = False
    while n == False:
        if len(room.monsters) == 0:
            return
        if room.monsters is None:
            return  
        choice = input_int("choose 0 to 3 (if lucky you could flee the attack): ")
        fate = random.randint(0,3)
        if fate == choice:
            print("It doesn't seem to notice me... I'm safe for now.")
            return  
        print("It noticed me!")
        yourchoice = choosemonster()
        for i, monster in enumerate(room.monsters):
            if i == yourchoice:
                print(f"you deal with {monster.name}")
                break
        x = False
        target = room.monsters[yourchoice]
        if check_special_monster(target):
            handle_special_monster(target)
            continue
        while x == False:
            action = input_int("1. attack\n2. use item\nchoose action: ") 
            if action == 1:
                attack(character, target)
                if target.isdead():
                    print(f"you slain {target.name}")
                    monsterloot(target)
                    room.monsters.remove(target)
                    x = True
                    break
                else:
                    monstercounterattack(target)
                    
            elif action == 2:
                if check_special_monster(target):
                    handle_special_monster(target)
                else:
                    if not character.items:
                        print("no item to use")
                        continue
                    showinventory(character)
                    chosen_item = chooseitem(character)
                    chosen_item.usingitem(character, target)
                    if  target.isdead():
                        print(f"you slain {target.name}")
                        monsterloot(target)
                        room.monsters.remove(target)
                        x = True
                        break
                    monstercounterattack(target)
            if character.isdead():
                print("you die")
                return
            
            for m in room.monsters[:]:
                if m.isdead():
                    print(f"you slain {m.name}")
                    monsterloot(m)
                    room.monsters.remove(m)
                    x = True
                    break
            else:
                continue
           
while True:
    if playerwon():
        print("you won")
        break
    showroom()
    if character.current_position == "Mysterious-shop":
        shop()
    elif character.current_position == "Trap-room":
        trap_room()
    elif character.current_position == "Deadend":
        deadend()
    elif character.current_position == "Boss_room":
        boss_room()
    else:
        fight()
    if character.isdead():
        reset_game()
        continue
    while True:
        print("╔══════════════════════════════════════╗")
        print("║              CHARACTER               ║")
        print("╠══════════════════════════════════════╣")
        print(f"║ HP        : {character.hp:<25}║")
        print(f"║ DAMAGE    : {character.damage:<22}║")
        print(f"║ INVENTORY : {', '.join(item.name for item in character.items):<22}║")
        print(f"║ ROOM      : {character.current_position:<22}║")
        print("╚══════════════════════════════════════╝")
        print("""
                [1] item menu 
                [2] show visited places
                [3] move
                [4] exit
            """)
        choice = input_int("choose an action: ")
        if choice == 1:
            item_menu()
        elif choice == 2:
            showmap()
        elif choice == 3:
            moving_character()
            break
        elif choice == 4:
            exit()
        else:
            print("invalid choice")
        if character.isdead():
            reset_game()

        
    


                            
                                
                            
                        
                        
                    
