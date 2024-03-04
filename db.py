import sqlite3
import re
import os
import keyboard
import sys
import pygetwindow as gw

DB_PATH = "db/ac.db"
commands = ["quit", "clear", "restart", "setup", "reformat", "create_room", "delete_room", "delete_all_rooms", "rooms", "create_user", "delete_user", "delete_all_users", "users"]

#Summary: Print with a database prefix
def printc(op):
    print(f"SYSTEM: {op}")

#Summary: Create the users table in the database
def create_users():
    try:
        c.execute(
        """
        CREATE TABLE users(
        uid INTEGER PRIMARY KEY AUTOINCREMENT,
        name text,
        pwd text
        )
        """)
        con.commit()
        printc("users table created!")
    except Exception as e:
        printc(e)

#Summary: Create the users table in the database
def create_rooms():
    try:
        c.execute(
        """
        CREATE TABLE rooms(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name text,
        pwd text
        )
        """)
        con.commit()
        printc("rooms table created!")
    except Exception as e:
        printc(e)

#Summary: Create the tables in the database which will be used
def create_tables():
    create_rooms()
    create_users()

#Summary: Create a room in the rooms table with the name and password valuse provided
def create_room(name, pwd):
    try:
        c.execute(f"""
        INSERT INTO rooms
        VALUES
        (NULL, ?, ?)
        """, (name, pwd))
        con.commit()
        printc(f'"{name}" room has been created with "{pwd}" password!')
    except Exception as e:
        printc(e)

#Summary: Delete a room from the rooms table that matches the name and the password provided
def delete_room(name, pwd):
    try:
        c.execute(f"""
        SELECT * FROM rooms WHERE
        name=? AND pwd=?
        """, (name, pwd))
        if len(c.fetchall()) > 0:
            c.execute(f"""
            DELETE FROM rooms WHERE
            name=? AND pwd=?
            """, (name, pwd))
            con.commit()
            printc(f'"{name}" room has been deleted!')
        else:
            printc("Incorrect room name or password!")
    except Exception as e:
        printc(e)

#Summary: List all the rooms
def list_rooms():
    try:
        c.execute("""
        SELECT * FROM rooms
        """)
        rooms = c.fetchall()
        for room in rooms:
            printc(f"Room ID: {room[0]}, Room name: '{room[1]}', Password: '{room[2]}'")
        printc(f"Currently there are {len(rooms)} rooms!")
    except Exception as e:
        printc(e)

#Summary: Delete all the currently created rooms
def delete_all_rooms():
    try:
        c.execute(f"""
        DELETE FROM rooms
        """)
        con.commit()
        printc(f'All rooms has been deleted!')
    except Exception as e:
        printc(e)

#Summary: Create a user in the users table with the name and password valuse provided
def create_user(name, pwd):
    try:
        c.execute(f"""
        INSERT INTO users
        VALUES
        (NULL, ?, ?)
        """, (name, pwd))
        con.commit()
        printc(f'"{name}" user has been created with "{pwd}" password!')
    except Exception as e:
        printc(e)

#Summary: Delete a user from the users table that matches the name and the password provided
def delete_user(name, pwd):
    try:
        c.execute(f"""
        SELECT * FROM users WHERE
        name=? AND pwd=?
        """, (name, pwd))
        if len(c.fetchall()) > 0:
            c.execute(f"""
            DELETE FROM users WHERE
            name=? AND pwd=?
            """, (name, pwd))
            con.commit()
            printc(f'"{name}" room has been deleted!')
        else:
            printc("Incorrect room name or password!")
    except Exception as e:
        printc(e)

#Summary: List all the users
def list_users():
    try:
        c.execute("""
        SELECT * FROM users
        """)
        rooms = c.fetchall()
        for room in rooms:
            printc(f"UID: {room[0]}, Username: '{room[1]}', Password: '{room[2]}'")
        printc(f"Currently there are {len(rooms)} users!")
    except Exception as e:
        printc(e)

#Summary: Delete all the currently created users
def delete_all_users():
    try:
        c.execute(f"""
        DELETE FROM users
        """)
        con.commit()
        printc(f'All users has been deleted!')
    except Exception as e:
        printc(e)

#Summary: Clear the console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

#Summary: Restart the script
def restart():
    printc("Restarting the script...")
    os.system(os.path.basename(__file__))
    clear_console()
    startup()

#Summary: Initial startup screen
def startup():
    print(
    """
     _______  _        _______  _       _________ _______  _______           _______ _________ ______   ______  
    (  ___  )( (    /|(  ___  )( (    /|\__   __/(       )(  ____ \|\     /|(  ___  )\__   __/(  __  \ (  ___ \ 
    | (   ) ||  \  ( || (   ) ||  \  ( |   ) (   | () () || (    \/| )   ( || (   ) |   ) (   | (  \  )| (   ) )
    | (___) ||   \ | || |   | ||   \ | |   | |   | || || || |      | (___) || (___) |   | |   | |   ) || (__/ / 
    |  ___  || (\ \) || |   | || (\ \) |   | |   | |(_)| || |      |  ___  ||  ___  |   | |   | |   | ||  __ (  
    | (   ) || | \   || |   | || | \   |   | |   | |   | || |      | (   ) || (   ) |   | |   | |   ) || (  \ \ 
    | )   ( || )  \  || (___) || )  \  |___) (___| )   ( || (____/\| )   ( || )   ( |   | | _ | (__/  )| )___) )
    |/     \||/    )_)(_______)|/    )_)\_______/|/     \|(_______/|/     \||/     \|   )_((_)(______/ |/ \___/ 
    """)

#Summary: Shut down the process
def shutdown():
    con.close()
    printc("Connection closed, process will terminate...")
    exit(0)

#Summary: Reformats the database
def reformat():
    global con
    if (os.path.exists(DB_PATH)):
        con.close()
        os.remove(DB_PATH)
        con = sqlite3.connect(DB_PATH)
        c = con.cursor()
        printc("Database reformatted!")
    else:
        con.close()
        con = sqlite3.connect(DB_PATH)
        c = con.cursor()
        printc("Database has not been found, but has been created!")

#Summary: Run a command
def run(cmd):
    if cmd == "quit":
        shutdown()
    elif cmd == "clear":
        clear_console()
    elif cmd == "restart":
        restart()
    elif cmd == "setup":
        create_tables()
    elif cmd == "reformat":
        reformat()
    elif re.match(r"create_room [a-zA-Z0-9]* [a-zA-Z0-9]*$", cmd):
        words = cmd.split()
        create_room(words[1], words[2])
    elif re.match(r"delete_room [a-zA-Z0-9]* [a-zA-Z0-9]*$", cmd):
        words = cmd.split()
        delete_room(words[1], words[2])
    elif cmd == "delete_all_rooms":
        delete_all_rooms()
    elif cmd == "rooms":
        list_rooms()
    elif re.match(r"create_user [a-zA-Z0-9]* [a-zA-Z0-9]*$", cmd):
        words = cmd.split()
        create_user(words[1], words[2])
    elif re.match(r"delete_user [a-zA-Z0-9]* [a-zA-Z0-9]*$", cmd):
        words = cmd.split()
        delete_user(words[1], words[2])
    elif cmd == "delete_all_users":
        delete_all_users()
    elif cmd == "users":
        list_users()
    else:
        printc(f"{cmd} is an unknown command...")

#Summary: Tab completion for commands
def tab_completion(cmd):
    list = []
    for prompt in commands:
        if (prompt.startswith(cmd)):
            list.append(prompt)
    return list

#Summary: Helper function for clamping a number
def clamp(n, min, max):
    if n <= max and n >= min:
        return n
    elif n > max:
        return min + n - max - 1
    else:
        return min - n + max + 1

#Summary: Main function which will run during the process
def main():
    clear_console()
    startup()
    global con
    global c
    con = sqlite3.connect(DB_PATH)
    c = con.cursor()
    cmd = ""
    temp = []
    tempIdx = 0
    write = sys.stdout.write
    print("> ", end="", flush=True)
    while True:
        key_event = keyboard.read_event(suppress=True)
        if key_event.event_type == "up":
            continue
        elif keyboard.is_modifier(key_event.name):
            continue
        elif key_event.name == "tab":
            _temp = cmd
            if len(temp) == 0:
                temp = tab_completion(_temp)
                if len(temp) > 0:
                    while len(cmd) > 0:
                        cmd = cmd[:-1]
                        write('\b \b')
                        sys.stdout.flush()
                    cmd = temp[tempIdx]
                    print(cmd, end="", flush=True)
            else:                
                while len(cmd) > 0:
                    cmd = cmd[:-1]
                    write('\b \b')
                    sys.stdout.flush()
                tempIdx = clamp(tempIdx + 1, 0, len(temp) - 1)
                cmd = temp[tempIdx] 
                print(cmd, end="", flush=True)
            continue
        temp = []
        tempIdx = 0
        if key_event.name == "enter":
            print()
            run(cmd)
            print("> ", end="", flush=True)
            cmd = ""
            continue
        elif key_event.name == "space":
            cmd += " "
            print(" ", end="", flush=True)
            continue
        elif key_event.name == "backspace":
            if len(cmd) > 0:
                cmd = cmd[:-1]
                write('\b \b')
                sys.stdout.flush()
            continue
        if key_event.name == "up" or key_event.name == "down" or key_event.name == "left" or key_event.name == "right":
            continue
        else:
            cmd += key_event.name
        print(key_event.name, end="", flush=True)

if __name__ == "__main__":
    main()