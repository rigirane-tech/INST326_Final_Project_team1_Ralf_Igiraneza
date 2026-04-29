"""
game.py
 
Manages the overall flow of the Battleship game, including turn alternation,
win condition checking, and coordinating interactions between the player and
the computer opponent.
"""
 
# These imports assume teammates have built their respective modules.
# Replace with actual module/file names once the group finalizes naming.
from board import Board
from player import Player
from computer_player import ComputerPlayer
 
 
class Game:
    """
    Controls the overall flow of a Battleship game between a human player
    and a computer opponent.
 
    Attributes:
        player (Player): The human player.
        computer (ComputerPlayer): The AI opponent.
        current_turn (str): Tracks whose turn it is ('player' or 'computer').
        game_over (bool): Flag indicating whether the game has ended.
    """
 
    def __init__(self):
        """
        Initializes the Game by creating the player, computer opponent,
        and setting up the starting turn and game state.
 
        Arguments:
            None
 
        Returns:
            None
        """
        self.player = Player()
        self.computer = ComputerPlayer()
        self.current_turn = "player"
        self.game_over = False
 
    def setup_game(self):
        """
        Sets up the game by placing ships on both the player's and
        computer's boards before the main game loop begins.
 
        Arguments:
            None
 
        Returns:
            None
        """
        print("Setting up the game...\n")
 
        # Player places their ships on their board
        self.player.place_ships()
 
        # Computer places ships automatically on its board
        self.computer.place_ships()
 
        print("All ships have been placed. Let the battle begin!\n")
 
    def play_turn(self):
        """
        Executes a single turn for whichever player's turn it currently is.
        Gets an attack coordinate, applies it to the correct board, and
        prints the result. Then switches the active turn.
 
        Arguments:
            None
 
        Returns:
            None
        """
        if self.current_turn == "player":
            print("Your turn!")
 
            # Show the computer's board (with hits/misses only, ships hidden)
            self.computer.board.display(hide_ships=True)
 
            # Get attack coordinates from the player
            row, col = self.player.get_attack()
 
            # Apply attack to the computer's board and capture the result
            result = self.computer.board.receive_attack(row, col)
 
            print(f"Result: {result}\n")
 
            # Switch turn to computer
            self.current_turn = "computer"
 
        else:
            print("Computer's turn...")
 
            # Computer decides where to attack using its AI logic
            row, col = self.computer.generate_move()
 
            # Apply attack to the player's board and capture the result
            result = self.player.board.receive_attack(row, col)
 
            print(f"Computer attacked ({row}, {col}): {result}\n")
 
            # Switch turn back to player
            self.current_turn = "player"
 
    def check_win_condition(self):
        """
        Checks whether either the player or the computer has won the game
        by verifying if all of one side's ships have been sunk.
 
        This method implements an original algorithm that iterates over each
        side's ship list and evaluates the sunk status of every ship.
 
        Arguments:
            None
 
        Returns:
            str or None: Returns 'player' if the player has won, 'computer'
            if the computer has won, or None if the game should continue.
        """
        # Step 1: Retrieve the full list of ships for both the player and computer
        player_ships = self.player.board.ships
        computer_ships = self.computer.board.ships
 
        # Step 2: Iterate over all computer ships and check if every one is sunk
        all_computer_ships_sunk = True
        for ship in computer_ships:
            if not ship.is_sunk():
                # At least one computer ship is still afloat; player has not won yet
                all_computer_ships_sunk = False
                break
 
        # Step 3: If all computer ships are sunk, return 'player' as the winner
        if all_computer_ships_sunk:
            return "player"
 
        # Step 4: Iterate over all player ships and check if every one is sunk
        all_player_ships_sunk = True
        for ship in player_ships:
            if not ship.is_sunk():
                # At least one player ship is still afloat; computer has not won yet
                all_player_ships_sunk = False
                break
 
        # Step 5: If all player ships are sunk, return 'computer' as the winner
        if all_player_ships_sunk:
            return "computer"
 
        # Step 6: Neither side has won yet; return None to continue the game
        return None
 
    def run(self):
        """
        Runs the full game loop from setup through completion. Calls setup,
        then repeatedly plays turns and checks win conditions until one side
        has won. Displays the final result.
 
        Arguments:
            None
 
        Returns:
            None
        """
        print("Welcome to Battleship!\n")
 
        # Set up both boards and place all ships
        self.setup_game()
 
        # Main game loop: continue until someone wins
        while not self.game_over:
 
            # Execute the current player's turn
            self.play_turn()
 
            # Check if the last attack ended the game
            winner = self.check_win_condition()
 
            if winner == "player":
                print("Congratulations! You sank all of the computer's ships. You win!")
                self.game_over = True
 
            elif winner == "computer":
                print("The computer sank all of your ships. You lose. Better luck next time!")
                self.game_over = True
 
        print("\nGame over. Thanks for playing!")
if __name__ == "__main__":
    game = Game()
    game.run()