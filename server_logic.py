from board import Board
from typing import List, Dict


def avoid_my_neck(head: Dict[str, int], body: List[Dict[str, int]], possible_moves: List[str]) -> List[str]:
    """Remove the move that would immediately collide with the snake's neck."""
    if len(body) > 1:
        neck = body[1]
        head_x = head["x"]
        head_y = head["y"]

        if neck["x"] < head_x and "left" in possible_moves:
            possible_moves.remove("left")
        elif neck["x"] > head_x and "right" in possible_moves:
            possible_moves.remove("right")
        elif neck["y"] < head_y and "down" in possible_moves:
            possible_moves.remove("down")
        elif neck["y"] > head_y and "up" in possible_moves:
            possible_moves.remove("up")

    return possible_moves


def choose_move(data: dict) -> str:
    board:Board = Board(data)
    move = board.chose_direction(board.you)
    
    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked")

    return move
