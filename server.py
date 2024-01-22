# Importing and initializing

# Importing sockets to handle server creation and sending information
import socket
# Importing threads to start a thread to handle either player's data
import _thread
# Importing sprites to handle player position calculations server side
import sprites
# Importing pickle to serialize objects so that entire classes can be sent across the network
import pickle 
# Importing sys to kill the server when too many players join-
import sys 

# Defines the server and port and then globalizes the currentPlayer variable
server = "10.226.50.164"
port = 5555
global currentPlayer

# Configures the socket and assigns it to the variable s
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Try to bind the socket to the server and the port
try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

# Controls how many players can connect to the socket
s.listen(2)
print("Waiting for a connection, Server Started")

# Instantiates the two players in a list
players = [sprites.Player(1640,100,50,50,True), sprites.Player(180,100,50,50,False)]

def quitServer():
    '''Function to close the socket when called'''
    s.close()

def threaded_client(conn, player):
    '''Function which controls sending and recieving of data from the network'''
    # Tries sending data, but excepts if more that 2 players are connected
    try:
        # Pickles player object and send it
        conn.send(pickle.dumps(players[player]))
    except IndexError:
        print("Failed to send data, player limit reached")
    reply = ""

    # Loop that controls sending data from the server and what data to reply with depending on which player's data it recieves
    while True:
        try:
            # Unpickles data and defines it as player data (up to 2048 bytes)
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            # Control what data is sent to who
            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                print("Received: ", data)
                print("Sending : ", reply)
            conn.sendall(pickle.dumps(reply))
        # Kills the server if too many people join and indexing becomes impossible
        except IndexError:
            print("Too many players joined, out of index")
            sys.exit()
    # Closes the connection and prints a message
    print("Lost connection")
    conn.close()

currentPlayer = 0

# Defines the connection ID and Adress as two variables (conn and addr)
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    # Starts a new thread for the new player
    _thread.start_new_thread(threaded_client, (conn, currentPlayer))
    # Increments currentPlayer until it there is 2 players
    currentPlayer += 1
