import socket
import threading
import sqlite3
import rsa
import os

DB_PATH = "db/ac.db"
SERVER = "10.10.1.81"
PORT = 1337

#Summary: Clear the console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

#Summary: Input with user prefix
def inputu(ip):
    return input(f"{name}>{ip}")

#Summary: Print with user prefix
def printu(op):
    print(f"{name}: op")

#Summary: Print with SYSTEM prefix
def printc(op):
    print(f"SYSTEM: {op}\n")

#Summary: Initial startup screen
def startup():
    print(
    """
     _______  _        _______  _       _________ _______  _______           _______ _________  
    (  ___  )( (    /|(  ___  )( (    /|\__   __/(       )(  ____ \|\     /|(  ___  )\__   __/ 
    | (   ) ||  \  ( || (   ) ||  \  ( |   ) (   | () () || (    \/| )   ( || (   ) |   ) (   
    | (___) ||   \ | || |   | ||   \ | |   | |   | || || || |      | (___) || (___) |   | |    
    |  ___  || (\ \) || |   | || (\ \) |   | |   | |(_)| || |      |  ___  ||  ___  |   | |     
    | (   ) || | \   || |   | || | \   |   | |   | |   | || |      | (   ) || (   ) |   | |    
    | )   ( || )  \  || (___) || )  \  |___) (___| )   ( || (____/\| )   ( || )   ( |   | |
    |/     \||/    )_)(_______)|/    )_)\_______/|/     \|(_______/|/     \||/     \|   )_(
    """)

#Summary: Login to a user
def login():
    try:
        creds = input("login (user:pass): ")
        user = creds.split(":")[0].replace("'", "").replace('"', "")
        pwd = creds.split(":")[1].replace("'", "").replace('"', "")
        c.execute("""
        SELECT uid, name, pwd FROM users WHERE
        name=? AND pwd=?
        """, (user, pwd))
        ret = c.fetchone()
        if ret:
            name = str(ret[0]) + user
            printc(f"LOGGED IN AS {name}!")
            return name
        else:
            return ""
    except Exception as e:
        print(e)

#Summary: Join a room
def join_room():
    try:
        creds = inputu("connect(name:pass): ")
        room_name = creds.split(":")[0]
        pwd = creds.split(":")[1]
        c.execute("""
        SELECT name FROM rooms WHERE
        name=? AND pwd=?
        """, (room_name, pwd))
        ret = c.fetchone()
        if ret:
            printc(f"CONNECTED TO {ret[0]}!")
            return room_name
        else:
            return ""
    except Exception as e:
        print(e)

#Summary: Sending messages loop that runs continously on a thread
def sending_messages(c):
    while True:
        msg = input("> ")
        c.send(f"{room_name}:{name}:{msg}".encode())

#Summary: Receiving messages loop that runs continously on a thread
def receiving_messages(c):
    while True:
        _msg = c.recv(1024).decode()
        if (_msg == "__room__"):
            c.send(room_name.encode())
            continue
        user = _msg.split(":")[0]
        msg = _msg.split(":")[1]
        print(f"{user}: {msg}")
        print("> ", end="", flush=True)

#Summary: Connect to a server
def connect_to_room(room_name):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    threading.Thread(target=sending_messages, args=(client,)).start()
    threading.Thread(target=receiving_messages, args=(client,)).start()

#Summary: Main function which will run during the process
def main():
    clear_console()
    startup()
    global conn
    global c
    global name
    global room_name
    name = ""
    room_name = ""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    while not name:
        name = login()
    while not room_name:
        room_name = join_room()
    connect_to_room(room_name)

if __name__ == "__main__":
    main()