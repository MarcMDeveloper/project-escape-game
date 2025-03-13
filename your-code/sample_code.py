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

# Import required modules
import time
import threading
import os
import tkinter as tk
from tkinter import font as tkfont 
import pygame


# Game duration in seconds (3 minutes)
GAME_DURATION = 180

# Timer variables
start_time = None
game_over_flag = False
timer_window = None

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

def playMusic():
    pygame.init()
    pygame.mixer.music.load("sci-fi-background-258999.mp3")
    pygame.mixer.music.play()

# Function to print line breaks for better readability
def linebreak():
    print("\n\n")

# Create and update timer window in a separate thread
def create_timer_window():
    global timer_window

    # Create a new window
    timer_window = tk.Tk()
    timer_window.title("Escape Room Timer")
    timer_window.geometry("500x450")  # Width x Height
    timer_window.attributes("-topmost", True)  # Keep window on top

    # Configure window appearance
    timer_window.configure(bg="black")
    timer_window.resizable(False, False)  # Fixed size window

    # Create a large font for the timer
    timer_font = tkfont.Font(family="Courier", size=24, weight="bold")
    warning_font = tkfont.Font(family="Courier", size=12)
    inventory_font = tkfont.Font(family="Courier", size=12)

    # Create timer label
    time_display = tk.Label(timer_window, 
                         text="03:00", 
                         fg="lime green",
                         bg="black", 
                         font=timer_font)

    time_display.pack(pady=20)


    # Create warning label (hidden initially)
    warning_label = tk.Label(timer_window, 
                          text="TIME IS RUNNING OUT!", 
                          fg="red",
                          bg="black", 
                          font=warning_font)
    warning_label.pack(pady=10)
    warning_label.pack_forget()  # Hide initially

    inventory_label = tk.Label(timer_window, 
                         text="INVENTORY", 
                         fg="lime green",
                         bg="black", 
                         font=inventory_font)

    inventory_label.pack(pady=20)
    # Update timer function
    def update_timer():
        global game_over_flag
        
        if timer_window is None:
            return

        # Put here the counter of the keys, should not be here but it works
        Fact = "INVENTORY" + "\n"
        if len(game_state["keys_collected"]) > 0:
            for key in game_state["keys_collected"]:
                Fact += key["name"] + " \n"

        inventory_label.config(text = Fact)
        
        # Calculate remaining time
        elapsed = time.time() - start_time
        remaining = max(0, GAME_DURATION - elapsed)


        # Convert to minutes:seconds format
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)

        # Update timer text
        time_display.config(text=f"{minutes:02d}:{seconds:02d}")
        
        # Change color based on remaining time
        if remaining <= 60:  # Last minute
            time_display.config(fg="red")
            warning_label.pack()  # Show warning
        elif remaining <= 120:  # Last 2 minutes
            time_display.config(fg="yellow")

        # Check if game is over due to time
        if remaining <= 0:
            game_over_flag = True
            time_display.config(text="00:00")
            warning_label.config(text="GAME OVER - YOU ARE TRAPPED FOREVER!", font=("Courier", 10, "bold"))
            print("\n*** TIME'S UP! YOU ARE TRAPPED FOREVER! ***\n")
            timer_window.after(3000, lambda: os._exit(0))  # Exit after 3 seconds
            return

        # Schedule next update
        timer_window.after(500, update_timer)
        
    # Start the timer update
    update_timer()
    
    # Handle window close event
    timer_window.protocol("WM_DELETE_WINDOW", lambda: None)  # Prevent window from closing
    
    # Start the Tkinter event loop in the current thread
    timer_window.mainloop()

# Timer display function that runs in a separate thread
def timer_display():
    create_timer_window()

def get_next_room_of_door(door, current_room):
    """
    From object_relations, find the two rooms connected to the given door.
    Return the second room.
    """
    connected_rooms = object_relations[door["name"]]
    object_relations[door["name"]] = list(reversed(object_relations[door["name"]]))
    return connected_rooms[1]

# Function to explore a room and list all items inside
def explore_room(room):
    if room["name"] in object_relations:
        items = [item['name'] for item in object_relations[room["name"]]]
        print(f"You explore {room['name']} and find: {', '.join(items)}.")
    else:
        print(f"There is nothing in {room['name']}.")

# Function to examine an item (doors, furniture, keys)
def examine_item(item_name):
    """
    Examine an item which can be a door or furniture.
    First make sure the intended item belongs to the current room.
    Then check if the item is a door. Tell player if key hasn't been 
    collected yet. Otherwise ask player if they want to go to the next
    room. If the item is not a door, then check if it contains keys.
    Collect the key if found and update the game state. At the end,
    play either the current or the next room depending on the game state
    to keep playing.
    """
    current_room = game_state["current_room"]
    next_room = ""
    output = None
    
    for item in object_relations[current_room["name"]]:
        if(item["name"] == item_name):
            output = "You examine " + item_name + ". "
            if(item["type"] == "door"):
                have_key = False
                for key in game_state["keys_collected"]:
                    if(key["target"] == item):
                        have_key = True
                if(have_key):
                    output += "You unlock it with a key you have."
                    next_room = get_next_room_of_door(item, current_room)
                else:
                    output += "It is locked but you don't have the key."
            else:
                if(item["name"] in object_relations and len(object_relations[item["name"]])>0):
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    output += "You find " + item_found["name"] + "."
                else:
                    output += "There isn't anything interesting about it."
            print(output)
            break

    if(output is None):
        print("The item you requested is not found in the current room.")
    
    if(next_room and input("Do you want to go to the next room? Enter 'yes' or 'no': ").strip().lower() == 'yes'):
        play_room(next_room)
    else:
        play_room(current_room)

# Function to handle room navigation
def play_room(room):
    global game_over_flag
    # Check if game is over due to time
    if game_over_flag:
        return

    game_state["current_room"] = room  # Update current room
    if room == game_state["target_room"]:  # Check if the player has escaped
        print("Congrats! You escaped the house!")
        os._exit(0)  # Exit the program
    else:
        print(f"You are now in {room['name']}")
        action = input("What do you want to do? 'explore', 'examine'? ").strip().lower()
        if action == "explore":
            explore_room(room)
            play_room(room)
        elif action == "examine":
            examine_item(input("What would you like to examine? ").strip().lower())
        else:
            print("Invalid command. Type 'explore', 'examine', or 'inventory'.")
            play_room(room)
        linebreak()

# Function to start the game
def start_game():
    global start_time
    
    # Initialize timer
    start_time = time.time()
    playMusic()

    # Start timer thread
    timer_thread = threading.Thread(target=timer_display, daemon=True)
    timer_thread.start()    

    # Display ASCII art and intro text
    os.system('cls' if os.name == 'nt' else 'clear')
    print("""
#######                                       ######
#        ####   ####    ##   #####  ######    #     #  ####   ####  #    #
#       #      #    #  #  #  #    # #         #     # #    # #    # ##  ##
#####    ####  #      #    # #    # #####     ######  #    # #    # # ## #
#            # #      ###### #####  #         #   #   #    # #    # #    #
#       #    # #    # #    # #      #         #    #  #    # #    # #    #
#######  ####   ####  #    # #      ######    #     #  ####   ####  #    #
    """)

    print("You wake up on a couch in a strange house. You must escape!")
    print("You have 3 minutes before the doors lock forever!")
    time.sleep(2)  # Give player time to read instructions
    
    play_room(game_state["current_room"])

# Start the game
if __name__ == "__main__":
    start_game()