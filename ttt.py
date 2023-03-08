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

    def check_for_draw(self, turns, max_turns):
        return True if turns == max_turns else False

    def check_for_win(self):
        rows = self.game_board.split("\n")
        for row in rows:
            if row == "XXX":
                return True
        return False
    
    def is_valid_move(self, cell, token):
        tmp = self.game_board.replace(cell, token)
        if self.game_board == tmp:
            return False
        return True


class GameController():
    brd: Board
    current_player: Player
    
    in_progress: bool
    turns: int
    max_turns: int

    welcome_text: str
    take_turns_text: str

    def __init__(self, 
                 in_progress=True, 
                 turns=1, 
                 max_turns=10, 
                 welcome_text="Welcome to tictactoe", 
                 take_turns_text="Take turn",
                 brd=None,
                 current_player=None):

        self.in_progress = in_progress
        self.turns = turns
        self.max_turns = max_turns

        self.welcome_text = welcome_text
        self.take_turns_text = take_turns_text

        # self.brd = brd if brd else Board()
        if brd:
            self.brd = brd
        else:
            self.brd = Board()

        if current_player:
            self.current_player = current_player
        else:
            self.current_player = Player(token="X")

    def start_game(self):
        _logger.warning(self.turns)
        _logger.warning(self.max_turns)
        self.render_text(self.welcome_text)
        self.game_loop(
            in_progress=self.in_progress)
    
    def game_loop(self, in_progress):
        while in_progress:
            self.brd.render()

            cell = self.get_input(self.take_turns_text)

            if cell == "quit":
                sys.exit()

            if self.brd.is_valid_move(cell, self.current_player.token):
                self.brd.update(cell,self.current_player.token)
                self.current_player = self.current_player.switch_player(self.current_player.token)
            else:
                self.render_text(f"{self.current_player.token} that was an invalid move, please try again.")
            
            if self.max_turns:
                self.turns += 1
                
            #     if self.turns > self.max_turns:
            #         break

            if self.brd.check_for_win():
                self.brd.render()
                self.render_text(f"{self.current_player.token} wins!")
                sys.exit()
            elif self.brd.check_for_draw(self.turns, self.max_turns):
                self.render_text("The game ends in a draw")
                sys.exit()
    
    def render_text(self, text):
        print(text)

    def get_input(self, text):
        return input(text)
            
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