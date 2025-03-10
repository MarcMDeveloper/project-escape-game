## agregar grafica al comienzo del juego en ASCII estilo old games de DOS
#######                                       ######
#        ####   ####    ##   #####  ######    #     #  ####   ####  #    #
#       #      #    #  #  #  #    # #         #     # #    # #    # ##  ##
#####    ####  #      #    # #    # #####     ######  #    # #    # # ## #
#            # #      ###### #####  #         #   #   #    # #    # #    #
#       #    # #    # #    # #      #         #    #  #    # #    # #    #
#######  ####   ####  #    # #      ######    #     #  ####   ####  #    #

# Escape Room Game in Python
# This program simulates an escape room game where the player navigates through rooms,
# finds keys, unlocks doors, and eventually escapes the house.

# Define rooms, items, and doors as dictionaries

# Room definitions
game_room = {"name": "game room", "type": "room"}
bedroom_1 = {"name": "bedroom 1", "type": "room"}
bedroom_2 = {"name": "bedroom 2", "type": "room"}
living_room = {"name": "living room", "type": "room"}
outside = {"name": "outside", "type": "room"}

# Door definitions
door_a = {"name": "door a", "type": "door"}
door_b = {"name": "door b", "type": "door"}
door_c = {"name": "door c", "type": "door"}
door_d = {"name": "door d", "type": "door"}

# Key definitions
key_a = {"name": "key for door a", "type": "key", "target": door_a}
key_b = {"name": "key for door b", "type": "key", "target": door_b}
key_c = {"name": "key for door c", "type": "key", "target": door_c}
key_d = {"name": "key for door d", "type": "key", "target": door_d}

# Furniture definitions (objects within rooms)
couch = {"name": "couch", "type": "furniture"}
piano = {"name": "piano", "type": "furniture"}
queen_bed = {"name": "queen bed", "type": "furniture"}
double_bed = {"name": "double bed", "type": "furniture"}
dresser = {"name": "dresser", "type": "furniture"}
dining_table = {"name": "dining table", "type": "furniture"}

# Define relationships between rooms, items, and doors
# This dictionary connects rooms with their respective objects and doors
object_relations = {
    "game room": [couch, piano, door_a],  # Game room contains a couch, a piano, and door A
    "piano": [key_a],  # Piano contains the key for door A
    "bedroom 1": [queen_bed, door_a, door_b, door_c],  # Bedroom 1 has a queen bed and three doors
    "queen bed": [key_b],  # Queen bed contains the key for door B
    "bedroom 2": [double_bed, dresser, door_b],  # Bedroom 2 has a double bed, a dresser, and door B
    "double bed": [key_c],  # Double bed contains the key for door C
    "dresser": [key_d],  # Dresser contains the key for door D
    "living room": [dining_table, door_c, door_d],  # Living room contains a dining table and two doors
    "outside": [door_d],  # Outside can only be accessed through door D
    "door a": [game_room, bedroom_1],  # Door A connects the game room and bedroom 1
    "door b": [bedroom_1, bedroom_2],  # Door B connects bedroom 1 and bedroom 2
    "door c": [bedroom_1, living_room],  # Door C connects bedroom 1 and the living room
    "door d": [living_room, outside]  # Door D connects the living room and outside
}

# Initialize the game state
game_state = {
    "current_room": game_room,  # The player starts in the game room
    "keys_collected": [],  # List to store collected keys
    "target_room": outside  # The goal is to reach outside
}

def checkInventory():
  if len(game_state['keys_collected']) != 0:
    print("You check your pockets. You have the following keys")
    for item in game_state['keys_collected']:
      print(item['name'])
  else:
    print("Nothnig on your pockets")

# Function to print line breaks for better readability
def linebreak():
    print("\n\n")

# Function to start the game
def start_game():
    print("You wake up on a couch in a strange house. You must escape!")
    play_room(game_state["current_room"])

# Function to handle room navigation
def play_room(room):
    game_state["current_room"] = room  # Update current room
    if room == game_state["target_room"]:  # Check if the player has escaped
        print("Congrats! You escaped the house!")
    else:
        print(f"You are now in {room['name']}")
        action = input("What do you want to do? 'explore' or 'examine'? ").strip().lower()
        if action == "explore":
            explore_room(room)
            play_room(room)
        elif action == "examine":
            examine_item(input("What would you like to examine? ").strip().lower())
        else:
            print("Invalid command. Type 'explore' or 'examine'.")
            play_room(room)
        linebreak()

# Function to explore a room and list all items inside
def explore_room(room):
    print(f"You explore {room['name']} and find: ", end="")
    items = [item['name'] for item in object_relations[room['name']]]
    print(", ".join(items) + ".")

# Function to examine an item (doors, furniture, keys)
def examine_item(item_name):
    current_room = game_state["current_room"]
    found = None
    for item in object_relations.get(current_room["name"], []):
        if item["name"] == item_name:
            found = item
            break

    if found is None:
        print("That item is not in this room.")
    else:
        if found["type"] == "door":
            if any(key["target"] == found for key in game_state["keys_collected"]):
                print(f"You unlock {found['name']} and proceed!")
                next_room = object_relations[found["name"]][1]
                if input("Do you want to go to the next room? (yes/no) ").strip().lower() == "yes":
                    play_room(next_room)
            else:
                print(f"{found['name']} is locked. You need a key.")
        elif found["type"] == "key":
            game_state["keys_collected"].append(found)
            print(f"You found {found['name']}!")
        else:
            print(f"There is nothing special about {found['name']}.")

# Start the game
start_game()
