import unittest
import logging
from unittest.mock import patch, call

from ttt import main, GameController, Board, Player

_logger = logging.getLogger(__package__)

class ttttests(unittest.TestCase):
    @patch("builtins.print")
    @patch("ttt.GameController.get_input")
    def test_main_runs_game_upto_asking_user_for_input(self, mock_input, mock_print):
        mock_input.side_effect = ["quit"]
        
        game = main()

        assert mock_print.mock_calls == [call("Welcome to tictactoe"),  call("123\n456\n789")]
        assert mock_input.mock_calls == [call(game.take_turns_text)]
        
    # @patch("ttt.Player.switch_player")
    @patch("ttt.GameController.get_input")    
    def test_when_user_takes_turn_board_and_user_updates(self, mock_input):
        mock_input.side_effect = ["1", "quit"]
        
        game = main()
        
        assert mock_input.called
        assert game.current_player.token == "O"
        assert game.brd.game_board == "X23\n456\n789"

    @patch("ttt.GameController.render_text")
    @patch("ttt.GameController.get_input")   
    def test_if_user_makes_invalid_move_they_are_asked_to_move_again(self, mock_input, mock_render_text):
        mock_input.side_effect = ["1", "quit"]
        board = Board(game_board="XX3\n456\n789")
        player = Player("O")
        
        game = main(board=board, current_player=player)
        
        assert mock_render_text.is_called_with(f"{game.current_player} that was an invalid move, please try again.")
        assert game.current_player.token == "O"
        

    @patch("builtins.print")
    @patch("ttt.GameController.get_input", return_value="3")    
    def test_when_horizontal_win_occurs_game_shows_win_message_and_quits(self, mock_input, mock_print):
        board = Board(game_board="XX3\n456\n789")
        
        game = main(board=board)

        assert game.game_result == "win"
        assert mock_print.mock_calls == [
        call("Welcome to tictactoe"), 
        call("XX3\n456\n789"), 
        call("XXX\n456\n789"), 
        call(f"{game.current_player.token} wins!"),
        call("Thanks for playing!")]
        assert game.current_player.token == "X"

    @patch("ttt.GameController.render_text")
    @patch("ttt.GameController.get_input", return_value="2")    
    def test_game_states_draw_when_9_moves_are_taken(self, mock_get_input, mock_render_text):
        board = Board(game_board="X2O\nOOX\nXOX")
        game = main(turns=9, board=board)
        mock_render_text.is_called_with("The game ends in a draw")
        
        
    @patch("ttt.GameController.render_text")
    @patch("ttt.GameController.get_input", return_value="quit")   
    def test_if_user_types_exit_the_game_quits(self, mock_get_input, mock_render_text):
            game = main()
            assert game.game_loop() == None

    @patch("ttt.GameController.end_game_message")
    @patch("ttt.GameController.get_input", return_value="3")   
    def test_game_stops_on_win(self, mock_input, mock_end_game_mssg):
        board = Board("XX3\n457\789")
        
        game = main(board=board)
        
        assert game.game_result == "win"
        assert mock_end_game_mssg.is_called()

    @patch("ttt.GameController.get_input")
    def test_draw_match(self, mock_input):
        mock_input.side_effect = ["1","2","3","4","5","6","7","8","9"]

        game = main()
        
        assert game.turns == 10
        assert game.game_result == "draw"

