"""Server

This script is responsible for setting up the server on the given address and port

This script requires pickle and socket to be installed.

When this function is imported as a module a server is started.

"""


import socket
from _thread import *
import pickle
from game import Game

server = socket.gethostbyname(socket.gethostname())  # Getting local IPv4
port = 6000  # Port number for the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen(2)  # Only allowing 2 clients
print("Waiting for connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(connection, player, game_id):
    """
    This function reads in the data sent by the clients and performs
    the necessary subsequent tasks

    The function is threaded so that multiple clients can receive have feedback simultaneously

    :param connection: socket object: Information given from accepting the data
    :param player: int: Player id
    :param game_id: int: id of the current game
    """
    global idCount
    connection.send(str.encode(str(player)))

    while True:
        try:
            data = pickle.loads(connection.recv(4096))  # Receives the data
            if game_id in games:
                game = games[game_id]
                if not data:  # Ensuring the data exists
                    break
                else:
                    # If reset requested the game is restarted
                    if data == 'reset':
                        game.reset_game()
                    # If data != "get" then a move has been passed
                    elif data != 'get':
                        game.play(player, data)
                    # Send back the changes
                    connection.sendall(pickle.dumps(game))
            else:
                break
        except Exception as ex:
            print(ex)
            break
    print("Lost connection")
    # If this point is reached, the game has been terminated so it's
    # getting removed from the server
    try:
        # Trying because both clients will result in trying to delete,
        # but only one can
        del games[game_id]
        print("Closing game:", game_id)
    except Exception as exc:
        pass
    idCount -= 1
    connection.close()


while True:
    conn, address = s.accept()  # accepts incoming connections
    print("Connected to: ", address)

    idCount += 1  # number of clients getting incremented
    p = 0  # First player has an id of 0
    gameId = (idCount - 1) // 2

    # If there is a new pair of clients a new game needs to be created
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        # Game is ready to begin
        games[gameId].ready = True
        p = 1

    # Starting a thread for each player
    start_new_thread(threaded_client, (conn, p, gameId))
