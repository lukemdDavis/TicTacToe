import pygame
from network import Network

"""Client

This script is responsible for handling the client logic and displaying the game window

This script requires pygame to be installed
"""

pygame.font.init()
width = 800
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

board = pygame.image.load('images/board.jpg')
x_img = pygame.image.load('images/x.png')
o_img = pygame.image.load('images/o.png')


def redraw_window(window, game, p):
    """
    This displays the game assets on the window depending on if the game has started or client is waiting

    :param window: Pygame Window for the client to see the game
    :param game: The game object the client is apart of
    :param p: The id of the player
    """

    # Covering the previous frame
    window.fill((0, 0, 0))
    font = pygame.font.SysFont("comicsans", 90)

    # Loading screen if the player does not have an opponent
    if not game.connected():
        text = font.render("Waiting for Player...", True, (255, 255, 255), True)
        # Displaying the text
        window.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:
        # Displaying the board
        window.blit(board, (0, 0))
        # Text displayed when the game is in progress
        result_text = font.render("", True, (255, 255, 255))
        if game.winner is None:
            if game.get_current_turn() == p:
                turn_text = font.render("Your Turn", True, (255, 255, 255))
            else:
                turn_text = font.render("Opponents Turn", True, (255, 255, 255))
            window.blit(turn_text, (width / 2 - turn_text.get_width() / 2, 610))

        # Displaying  that the game is a tie
        elif game.winner == 0:
            result_text = font.render("Tie", True, (255, 255, 255))

        # Displaying that the player won
        elif (game.winner == 1 and p == 0) or (game.winner == -1 and p == 1):
            result_text = font.render("Won", True, (255, 255, 255))

        # Displaying that the player lost
        elif (game.winner == 1 and p == 1) or (game.winner == -1 and p == 0):
            result_text = font.render("Lost", True, (255, 255, 255))

        # Prompting the player to play again
        if game.winner is not None:
            play_again_text = font.render("Space to Play Again", True, (255, 255, 255))
            window.blit(play_again_text, (width / 2 - play_again_text.get_width() / 2, 610))
        window.blit(result_text, (610, 50))

        # Loops through the grid and displays x for 1's and o for -1's
        for i in range(len(game.grid)):
            for j in range(3):
                if game.grid[i][j] == 1:
                    window.blit(x_img, (j * 200, i * 200))
                elif game.grid[i][j] == -1:
                    window.blit(o_img, (j * 200, i * 200))

    # updates the window display
    pygame.display.update()


def main():
    """
    Executes the main loop for the client's game

    This function has a while loop that repeats until the client or opponent disconnects
    """
    run = True
    n = Network()  # Initializing a network object
    player = int(n.get_player())
    clock = pygame.time.Clock()
    print("You are player", player)
    while run:
        clock.tick(60)
        try:
            game = n.send("get")  # Gets the game object from network
        except Exception as e:
            print(e)
            break

        # Gets a list of keys the client has pressed
        keys = pygame.key.get_pressed()

        # If the client presses space and the game is over then the game resets
        if keys[pygame.K_SPACE] and isinstance(game.winner, int):
            try:
                game = n.send("reset")
            except Exception as e:
                print(e)

        for event in pygame.event.get():
            # Checks if the user has closed the game window
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            # Checking is the player hsa clicked on the board
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                pygame.time.delay(1000)
                print(f"comparing: player: {player} to current_turn{game.get_current_turn()}")
                # If the game is in progress, it's this clients turn and the client clicked an empty square
                # Then send the move to game class and update the grid
                if game.winner is None:
                    if game.get_current_turn() == player:
                        if pos[0] < 600 and pos[1] < 600:
                            n.send(pos)

        # Updates the window view after each iteration
        redraw_window(win, game, player)


# Executing the main loop
main()
