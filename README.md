# project-03-text-adventure-engine
A terminal-based text adventure game engine built in Python, featuring free-text command parsing, inventory management, monsters, locked rooms, exploration, and save/load functionality using .txt files.
# 🗺️ Terminal Adventure Engine — Detailed Mechanics Spec

This document describes **what each function must do** (inputs, outputs, behavior, edge cases) — not how to code it. Use this as your requirements checklist while you build. Check off each item only once you've tested it yourself.

---

## PHASE 1 — Core Loop

### `describe_room(rooms, current_room_name)`
**Purpose:** Show the player what's in their current room.

**Must display:**
- The room's description text
- Any items currently in the room (if none, say so — don't show an empty list)
- Available exits (just the directions, not where they lead — that's part of the mystery)
- Whether a monster is present (if alive) — just a warning, not full combat info

**Edge cases:**
- Room has zero items → show "There is nothing here" or similar, not a blank line
- Room has zero exits (a true dead end) → say so explicitly, don't just show nothing

---

### `parse_command(raw_input)`
**Purpose:** Take whatever the player typed and break it into a usable verb + target.

**Must handle:**
- Splitting the first word (verb) from the rest (target) — e.g. `"take rusty sword"` → verb: `take`, target: `rusty sword`
- Case normalization — `"GO north"`, `"Go North"`, `"go north"` must all behave identically
- Leading/trailing/multiple spaces — `"   go    north  "` must still parse correctly
- Empty input (player just hits Enter) — must not crash, must give a gentle prompt like "Please type a command"
- A single-word command with no target (e.g. `"look"`, `"quit"`) — target should end up empty, not cause an error

**Output:** Should hand back two clean pieces of information — a verb and a target — for the rest of the program to act on.

---

### `move_player(rooms, player, direction)`
**Purpose:** Attempt to move the player from their current room to an adjacent one.

**Must check, in order:**
1. Does this exit exist from the current room at all? If not → clear error message, player stays put.
2. Is the destination room locked? If yes → see `check_locked_room()` below; don't move the player.
3. If valid and unlocked → update `current_room`, mark the new room as visited, increment `moves`.

**Edge cases:**
- Direction typed doesn't match any exit (e.g. player types "up" but no "up" exit exists)
- Direction exists but leads to a locked room without the required key

---

### `take_item(rooms, player, item_name)`
**Purpose:** Move an item from the current room into the player's inventory.

**Must check:**
- Does the item actually exist in the *current room's* item list? (Not the player's inventory, not some other room.)
- Case sensitivity — should "Sword" and "sword" be treated as the same item? **Decide this explicitly and be consistent everywhere.**

**On success:** item is removed from the room's list and added to inventory.
**On failure:** clear message like "There is no [item] here" — never crash.

---

### `drop_item(player, item_name)`
**Purpose:** Move an item from inventory back into the current room.

**Must check:**
- Does the player actually have this item?
**On failure:** "You don't have that" — never crash.

---

### `show_inventory(player)`
**Purpose:** Display everything the player is carrying.

**Edge case:** empty inventory → say so explicitly, don't show a blank list.

---

### `show_help()`
**Purpose:** List every valid command with a one-line description of what it does. Static — doesn't need any inputs.

---

## PHASE 2 — Persistence

### `save_data(rooms, player)`
**Purpose:** Write the current game state to a file so it can be resumed later.

**Must save:**
- The full player state (current room, inventory, health, visited rooms, moves)
- The full world state — **including anything that changed during play** (items taken/dropped from rooms, monsters killed, rooms unlocked). If you only save the *original* room layout and not what changed, the save is broken.

**Design requirement:** You choose your own text format (e.g. one line per data type, fields separated by a delimiter like `|`). Write down your exact format as a comment before coding it — decide field order and delimiter *before* you start, not while debugging.

**Edge case to think about:** What if an item name or room description accidentally contains your delimiter character? Decide how you'll avoid or handle that.

---

### `load_data()`
**Purpose:** On program start, check if a save file exists and restore the game state from it.

**Must handle:**
- **No save file exists** (first-ever run) → start a brand-new game with your default world, don't crash or error
- **Save file exists but is empty or malformed** (e.g. someone manually edited it and broke the format) → detect this gracefully and fall back to a fresh game rather than crashing
- **Save file is valid** → fully reconstruct the `rooms` dict and `player` dict exactly as they were, ready to continue playing

**Output:** Should hand back a working `rooms` dictionary and `player` dictionary, whether freshly created or loaded from file.

---

## PHASE 3 — Combat & Progression

### `attack_monster(rooms, player, current_room_name, monster_name)`
**Purpose:** Player attacks the monster in their current room.

**Must check:**
1. Is there actually a monster with this name in the current room?
2. Is the monster already dead (`alive: False`)? If so, tell the player, don't let them "attack" a corpse repeatedly for no effect.
3. Is this a monster type that **cannot** be attacked directly (like your Ghost design)? If so, explain why the attack does nothing.

**On a valid attack:**
- Deal random damage to the monster using `random.randint(min, max)` — you decide the range per monster
- Deal random damage back to the player (monster's counter-attack) — same mechanic, different range
- If monster's health drops to 0 or below → mark `alive: False`, tell the player they won the fight
- If player's health drops to 0 or below → this is a loss state, decide what happens (game over? respawn? your design choice — just be explicit about it)

**Edge cases:**
- Player has 0 health already when trying to attack — should this even be allowed?
- Monster requires a specific item to damage at all (e.g. Dragon needs magic sword) — attacking without it should explain why nothing happened, not silently fail

---

### `use_item(player, rooms, current_room_name, item_name)`
**Purpose:** Apply an item's special effect — e.g. using a key to unlock a door, using a holy symbol to banish a ghost, using a torch to reveal a hidden path.

**Must check:**
- Does the player actually have this item?
- Does using it here actually do anything? (Using a key in a room with no locked exit nearby should give a sensible "nothing happens" response, not an error.)

**This function's exact behavior depends entirely on your world design** — decide up front which items do what, and write it down before coding.

---

### `check_locked_room(rooms, player, destination_room_name)`
**Purpose:** Determine whether the player is allowed to enter a locked room right now.

**Must check:**
- Is the destination actually locked?
- If locked, does the player's inventory contain the required key/item?

**Output:** A clear yes/no plus an appropriate message either way — "The door is locked" vs. silence when it's not locked at all.

---

### `check_win(player)`
**Purpose:** Determine whether the player has met **all** win conditions (minimum 3, per your design — e.g. owns treasure AND defeated final monster AND reached the exit room).

**Important:** This must check multiple independent conditions together — not just "is current_room == 'Exit'". Write out your exact 3 conditions before coding this function.

---

### `show_map(player)`
**Purpose:** Show the player which rooms they've already visited (from `visited_rooms`), to help them navigate a world they're exploring blind.

**Design decision:** Should this show unvisited rooms too (as "???"), or only what's been explored? Decide and be consistent.

---

## Cross-Cutting Requirements (apply to the whole program)

**The program must never crash**, regardless of input. Every function that takes user input needs to handle:
- Wrong type entirely (letters where a number was expected, if applicable)
- Missing/nonexistent target (item, direction, monster, room)
- Extra whitespace, mixed casing
- Empty input

**No duplicated logic.** If you find yourself writing the same "check if X exists in Y" pattern in three different functions, that's a sign it should be its own small helper function.

**No vague names.** Every variable should say what it *is*, not just what type it is (avoid `x`, `temp`, `data`, `d`).

---

## Your Checklist Before Calling a Phase "Done"

- [ ] Phase 1: I can walk through every room in my map without crashing, using only `go`/`look`/`take`/`drop`/`inventory`/`help`/`quit`
- [ ] Phase 1: Every edge case above has been manually tested (typo direction, take nonexistent item, empty input, etc.)
- [ ] Phase 2: I can quit mid-game, restart the program, and find myself exactly where I left off — items taken, rooms unlocked, everything intact
- [ ] Phase 2: Deleting the save file and running the program still works (fresh game starts cleanly)
- [ ] Phase 3: I can win the game by meeting all 3 conditions, and I can also fail to win if any one condition is missing
- [ ] Phase 3: Every monster type behaves according to its own design (normal, un-attackable, item-gated)
