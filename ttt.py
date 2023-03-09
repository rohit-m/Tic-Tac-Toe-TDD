import sys
import logging
from typing import Optional

_logger = logging.getLogger(__package__)


class Player():
    token: str

    def __init__(self, token):
        self.token = token

    def set_player(self, token):
        self.token = token

    def switch_player(self, token):
        if token == "X":
            return Player("O")
        return Player("X")


class Board():
    game_board: str

    def __init__(self, game_board="123\n456\n789"):
        self.game_board = game_board
    
    def update(self, cell, token):
        self.game_board = self.game_board.replace(cell, token)

    def render(self):
        print(self.game_board)
    
    def is_valid_move(self, cell, token):
        tmp = self.game_board.replace(cell, token)
        if self.game_board == tmp:
            return False
        return True

class GameResult():
    board: Board

    def __init__(self, board):
        self.board = board
        self.result = ""
        self.check_results()

    def check_for_draw(self):
        if any(char.isdigit() for char in self.board.game_board):
            return False
        return True

    def check_for_win(self):
        rows = self.board.game_board.split("\n")
        for row in rows:
            if row == "XXX" or row == "OOO":
                return True
        return False

    def check_results(self):
        if self.check_for_win():
            self.result = "win"
            return self.result
        elif self.check_for_draw():
            self.result = "draw"
            return self.result
        else:
            self.result = "continue"
            return self.result


class GameController():
    brd: Board
    current_player: Player
    
    turns: int
    max_turns: int

    welcome_text: str
    take_turns_text: str
    game_draw_text: str
    game_end_text: str

    def __init__(self, 
                 brd=None,
                 current_player=None,
                 turns=1, 
                 max_turns=10, 
                 welcome_text="Welcome to tictactoe", 
                 take_turns_text="Take turn",
                 game_draw_text="The game ends in a draw",
                 game_end_text="Thanks for playing!",
                 ):

        
        self.turns = turns
        self.max_turns = max_turns

        self.welcome_text = welcome_text
        self.take_turns_text = take_turns_text
        self.game_draw_text = game_draw_text
        self.game_end_text = game_end_text

        self.game_result = None

        self.brd = brd if brd else Board()

        self.current_player = current_player if current_player else Player(token="X")

    def start_game(self):
        self.render_text(self.welcome_text)
        self.game_result = self.game_loop()

        if self.game_result == "draw":
            self.render_text(f"{self.game_draw_text}")
            self.end_game_message()
        elif self.game_result == "win":
            self.render_text(f"{self.current_player.token} wins!")
            self.end_game_message()
    
    def game_loop(self):
        self.brd.render()

        cell = self.get_input(self.take_turns_text)

        if cell == "quit":
            return None

        valid_move = self.brd.is_valid_move(cell, self.current_player.token)

        if valid_move:
            self.brd.update(cell,self.current_player.token)
        else:
            self.render_text(f"{self.current_player.token} that was an invalid move, please try again.")
        
        if self.max_turns:
            self.turns += 1

        if GameResult(board=self.brd).result == "continue":
            if valid_move:
                self.current_player = self.current_player.switch_player(self.current_player.token)
            self.game_loop()
        else:
            self.brd.render()

        return GameResult(board=self.brd).result
    
    def render_text(self, text):
        print(text)

    def get_input(self, text):
        return input(text)
    
    def end_game_message(self):
        self.render_text(f"{self.game_end_text}")
            
def main(max_turns=10, board=None, current_player=None, turns=1):
    x = GameController(
        max_turns=max_turns, 
        brd=board, 
        current_player=current_player,
        turns=turns)
    x.start_game()
    return x

if __name__ == "__main__":
    main()