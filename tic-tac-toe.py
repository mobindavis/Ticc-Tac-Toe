# All module content combined into one file to avoid ModuleNotFoundError

from abc import ABC, abstractmethod
import random
import os
import unittest

# --------------------- game_engine.py ---------------------
class Board:
    def __init__(self):
        self.cells = [" " for _ in range(9)]

    def display(self):
        for i in range(0, 9, 3):
            print(" | ".join(self.cells[i:i+3]))
            if i < 6:
                print("-" * 5)

    def update_cell(self, index, symbol):
        if self.cells[index] == " ":
            self.cells[index] = symbol
            return True
        return False

    def check_winner(self, symbol):
        wins = [(0,1,2),(3,4,5),(6,7,8), (0,3,6),(1,4,7),(2,5,8), (0,4,8),(2,4,6)]
        return any(self.cells[a] == self.cells[b] == self.cells[c] == symbol for a, b, c in wins)

    def is_full(self):
        return " " not in self.cells

class GameEngine:
    def __init__(self, player1, player2, file_handler):
        self.board = Board()
        self.player1 = player1
        self.player2 = player2
        self.file_handler = file_handler

    def play(self):
        current_player = self.player1
        while True:
            self.board.display()
            move = current_player.get_move(self.board)
            if self.board.update_cell(move, current_player.symbol):
                if self.board.check_winner(current_player.symbol):
                    self.board.display()
                    print(f"{current_player.symbol} wins!")
                    self.file_handler.log(f"Winner: {current_player.symbol}\n")
                    break
                if self.board.is_full():
                    self.board.display()
                    print("It's a draw!")
                    self.file_handler.log("Result: Draw\n")
                    break
                current_player = self.player1 if current_player == self.player2 else self.player2
            else:
                print("Invalid move. Try again.")

# --------------------- players.py ---------------------
class Player(ABC):
    def __init__(self, symbol):
        self.symbol = symbol

    @abstractmethod
    def get_move(self, board):
        pass

class HumanPlayer(Player):
    def __init__(self, symbol, predefined_moves):
        super().__init__(symbol)
        self.moves = predefined_moves
        self.index = 0

    def get_move(self, board):
        if self.index < len(self.moves):
            move = self.moves[self.index]
            self.index += 1
            return move
        else:
            return random.choice([i for i in range(9) if board.cells[i] == " "])

class ComputerPlayer(Player):
    def get_move(self, board):
        print(f"Computer ({self.symbol}) is making a move...")
        return random.choice([i for i in range(9) if board.cells[i] == " "])

# --------------------- file_handler.py ---------------------
class FileHandler:
    def __init__(self, filename):
        self.filename = filename
        self.logs = []

    def log(self, text):
        self.logs.append(text)

    def save_game_log(self):
        with open(self.filename, "a") as f:
            for line in self.logs:
                f.write(line)

    def load_game_log(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                print("Previous Game Logs:")
                print(f.read())
        else:
            print("No previous game log found.")

# --------------------- main.py ---------------------
def main():
    print("Welcome to Tic-Tac-Toe!")
    file_handler = FileHandler("game_log.txt")
    file_handler.load_game_log()

    # Replace input with pre-defined moves to avoid input error in sandboxed environments
    simulated_moves = [0, 4, 1, 3, 2]  # Sample moves for human player

    player1 = HumanPlayer("X", simulated_moves)
    player2 = ComputerPlayer("O")

    game = GameEngine(player1, player2, file_handler)
    game.play()

    file_handler.save_game_log()

if __name__ == "__main__":
    main()

# --------------------- test_game.py ---------------------
class TestBoard(unittest.TestCase):
    def test_initial_board_empty(self):
        board = Board()
        self.assertEqual(board.cells.count(" "), 9)

    def test_update_cell(self):
        board = Board()
        self.assertTrue(board.update_cell(0, "X"))
        self.assertEqual(board.cells[0], "X")
        self.assertFalse(board.update_cell(0, "O"))

    def test_check_winner(self):
        board = Board()
        board.cells = ["X", "X", "X", " ", " ", " ", " ", " ", " "]
        self.assertTrue(board.check_winner("X"))

    def test_board_full(self):
        board = Board()
        board.cells = ["X" if i % 2 == 0 else "O" for i in range(9)]
        self.assertTrue(board.is_full())

# Uncomment below line to run tests manually
# unittest.main()
