"""
Short Exercises #4
"""
SIZE = 3

"""
Add your Board class here
""" 

"""
DO NOT MODIFY THE CODE BELOW
"""

"""
The Player class
""" 

class Player:

    def __init__(self, name, symbol):
        """
        Constructor for the Player class

        Player attributes:
          name (string): player's name
          symbol (string): player's symbol (one character)
        """
        self.name = name
        self.symbol = symbol

"""
The Game class
"""
class Game:

    def __init__(self):
        """
        Constructor for the Game class

        Game attributes:
          board (Board): the game board
          player1 (Player): player
          player2 (Player): player
          won (Boolean): True if game has a winner,
            False otherwise 
        """
        self.board = Board()
        self.player1 = None
        self.player2 = None
        self.winner = False

    def valid_input(self, keyboard):
        """
        Validate name and symbol:
          name is one string
          symbol is one character

        Input:
          keyboard (string): keyboard input

        Returns: True if valid, False otherwise
        """
        split = keyboard.split()
        return len(split) == 2 and len(split[1]) == 1

    def get_intput(self, player_num):
        """
        Get name and symbol from player

        Input:
          player_num (string): player 

        Returns:
          name (string): name of player
          symbol (string): player's symbol
        """
        s = "Player " + player_num + ": Enter you name and pick your symbol: "

        valid = False
        while not valid:
            keyboard = input(s)
            valid = self.valid_input(keyboard)
            if not valid:
                print("Player", player_num, "enter valid input this time...")
        name, symbol = keyboard.split()
        return name, symbol

    def start(self):
        """
        Method to start game 
          Collect keyboard input
          Initialize player1 and player2
        """
        print("\nReady to play tic-tac-toe?\n")

        name, symbol = self.get_intput("1")
        self.player1 = Player(name, symbol)
        name, symbol = self.get_intput("2")
        self.player2 = Player(name, symbol)

        print()

    def next_up(self, player):
        """
        Method to switch players

        Input:
          player (Player): current player

        Returns: next player
        """
        if player is self.player1:
            return self.player2
        else: 
            return self.player1

    def turn(self, player):
        """
        Method to play one turn of game
          Collect keyboard input
          Play move

        Input:
          player (Player): current player
        """
        valid = False
        while not valid:
            keyboard = input("Enter your move {}: ".format(player.name))
            row, col = keyboard.split()
            valid = self.board.valid_move(int(row), int(col))
            if not valid:
                print("Please play a valid move this time...")
        self.board.move(int(row), int(col), player)

    def play(self):
        """
        Method to run the game
          Start game
          Play turns 
          Check for winner
          Display result
        """
        self.start()
        player = self.player1

        for play in range(SIZE*SIZE):
            self.turn(player)
            print(self.board)
            if self.board.winner(player):
                print(player.name, "wins!")
                self.winner = True
                break
            player = self.next_up(player)

        if not self.winner:
            print("Tie game!")
        print("Nice game {} and {}!".format(self.player1.name, self.player2.name))

"""
Run game from the command line
"""
if __name__ == "__main__":
    g = Game()
    g.play()

