class Game:
    """
    A class used to store the Game progress

    ...
    Attributes
    -----------
    game_id: int
        The Id of the individual game
    players_turn: int
        Keeps track of the id of the current player
    ready : bool
        Indicates if the game has 2 players and is ready to begin
    grid : list
        Keeps track of the tic tac toe grid and moves
    winner : int
        Initially set to None until a winner or tie is reached. Then it's set to an int
    """

    def __init__(self, game_id):
        """
        Constructs all the necessary attributes for a game

        game_id: int
            The Id of the individual game
        players_turn: int
            Keeps track of the id of the current player
        ready : bool
            Indicates if the game has 2 players and is ready to begin
        grid : list
            Keeps track of the tic tac toe grid and moves
        winner : int
            Initially set to None until a winner or tie is reached. Then it's set to an int
        """
        self.id = game_id
        self.players_turn = 0
        self.grid = [[0, 0, 0],
                     [0, 0, 0],
                     [0, 0, 0]]
        self.ready = False
        self.winner = None

    def pos_to_grid_coor(self, pos):
        """
        Returns the grid coordinates based on the click position.
        :param pos: tup: The click position as
        :return: A length 2 list containing the y and x coordinates
        """
        # Dividing by 200 converts the mouse coordinates to grid coordinates
        return [pos[1] // 200, pos[0] // 200]

    def play(self, player, pos):
        """
        Adds the new move to the grid of the game, then checks if the game has ended
        :param player: Id of the player making the move
        :param pos: Mouse click of the making the move
        :return:
        """
        # Converting the mouse coordinates to grid coordinates
        y_pos, x_pos = self.pos_to_grid_coor(pos)

        # Checking if it's the players turn
        if player == 0 and self.players_turn == 0:
            if self.grid[y_pos][x_pos] == 0:
                self.grid[y_pos][x_pos] = 1  # Adding the move to the grid
                self.players_turn = 1  # changing the turn for who is next
        elif player == 1 and self.players_turn == 1:
            if self.grid[y_pos][x_pos] == 0:
                self.grid[y_pos][x_pos] = -1
                self.players_turn = 0

        self.winner = self.get_winner()

    def get_current_turn(self):
        """
        :return: The id of the player whose turn it is
        """
        return self.players_turn

    def connected(self):
        """
        :return: A bool indicating if the game has 2 players
        """
        return self.ready

    def get_winner(self):
        """
        This function checks the different ways a player can win or the game can draw.
        If a player has won, their symbol is returned.
        If it's a tie, 0 is returned
        If there is no winner yet, None is returned
        :return: An int or None indicating the status of the game
        """

        # Checking if there is a horizontal win and if so returning the winning value
        for i in self.grid:
            if i[0] == i[1] and i[0] == i[2] and i[0] != 0:
                return i[0]

        # Checking if there is a vertical win and if so returning the winning value
        if self.grid[0][0] == self.grid[1][0] and self.grid[0][0] == self.grid[2][0]:
            if self.grid[0][0] != 0:
                return self.grid[0][0]
        if self.grid[0][1] == self.grid[1][1] and self.grid[0][1] == self.grid[2][1]:
            if self.grid[0][1] != 0:
                return self.grid[0][1]
        if self.grid[0][2] == self.grid[1][2] and self.grid[0][2] == self.grid[2][2]:
            if self.grid[0][2] != 0:
                return self.grid[0][2]

        # Checking if there is a diagonal win and if so returning the winning value
        if self.grid[0][0] == self.grid[1][1] and self.grid[0][0] == self.grid[2][2]:
            if self.grid[0][0] != 0:
                return self.grid[0][0]
        if self.grid[0][2] == self.grid[1][1] and self.grid[0][2] == self.grid[2][0]:
            if self.grid[0][2] != 0:
                return self.grid[0][2]

        # Checking if the grid is full of moves without a winner
        is_zero_found = False
        for i in self.grid:
            for j in i:
                if j == 0:
                    is_zero_found = True

        # If the grid is full then the game is a tie
        if not is_zero_found:
            return 0  # Tie game

        # The game is not over yet
        return None  # No winner so far

    def reset_game(self):
        """ Resets the games details so the players can play again """
        self.players_turn = 0  # PLayer 0 goes first
        self.grid = [[0, 0, 0],  # Grid becomes empty
                     [0, 0, 0],
                     [0, 0, 0]]
        self.winner = None  # There is no winner
