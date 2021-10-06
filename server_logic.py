from astar import astar
import random
from typing import List, Dict, Tuple

from astar import astar, Node, return_path
from board import Board


def choose_move(data: dict) -> str:
    board = Board(data)
    move = board.you.chose_direction(board)
    
    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move
