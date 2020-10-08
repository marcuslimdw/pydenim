from pydenim.board import Board
from pydenim.config import Config
from pydenim.renderer.console import ConsoleRenderer

config = Config(n_rows=20, n_cols=15, starting_organism_count=10)
board = Board.initialise(config)
renderer = ConsoleRenderer()

renderer.render_board(board)
