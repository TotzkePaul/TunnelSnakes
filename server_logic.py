import random
from typing import List, Dict

"""
This file can be a nice home for your move logic, and to write helper functions.

We have started this for you, with a function to help remove the 'neck' direction
from the list of possible moves!
"""


def avoid_my_neck(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str]) -> List[str]:
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with the 'neck' direction removed
    """
    for segment in my_body[:-1]:
            if "up" in possible_moves and segment["x"] == my_head["x"] and my_head["y"] + 1 == segment["y"] :
                possible_moves.remove("up")
            if "down" in possible_moves and segment["x"] == my_head["x"] and my_head["y"]  - 1 == segment["y"]:
                possible_moves.remove("down")
            if "left" in possible_moves and segment["y"] == my_head["y"] and my_head["x"] == segment["x"] + 1:
                possible_moves.remove("left")
            if "right" in possible_moves and segment["y"] == my_head["y"] and my_head["x"] == segment["x"] - 1:
                possible_moves.remove("right")

    return possible_moves


def avoid_other_snakes(my_head: Dict[str, int], other_snakes: List[dict], possible_moves: List[str]) -> str:
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    other_snakes: List of dictionaries of x/y coordinates for each snake on the board.
            e.g. [ {"id": "abc123", "name": "Bob", "health": 100, "body": [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ] },
                   {"id": "def456", "name": "Alice", "health": 100, "body": [ {"x": 3, "y": 0}, {"x": 4, "y": 0}, {"x": 5, "y": 0} ] } ]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with the 'neck' direction removed
    """
    for snake in other_snakes:
        if snake["body"][0] == my_head:
            continue
        for segment in snake["body"][:-1]:
            if "up" in possible_moves and segment["x"] == my_head["x"] and segment["y"] == my_head["y"] + 1:
                possible_moves.remove("up")
            if "down" in possible_moves and segment["x"] == my_head["x"] and segment["y"] == my_head["y"] - 1:
                possible_moves.remove("down")
            if "left" in possible_moves and segment["y"] == my_head["y"] and segment["x"] == my_head["x"] + 1:
                possible_moves.remove("left")
            if "right" in possible_moves and segment["y"] == my_head["y"] and segment["x"] == my_head["x"] - 1:
                possible_moves.remove("right")

    return possible_moves

def avoid_walls( my_head: Dict[str, int], height :int, width :int, possible_moves: List[str]) -> List[str]:
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with the 'neck' direction removed
    """
    print(my_head)
    if "left" in possible_moves and  my_head["x"] == 0:
        possible_moves.remove("left")
    if "right" in possible_moves and  my_head["x"] == height - 1:
        possible_moves.remove("right")
    if "down" in possible_moves and my_head["y"] == 0:
        possible_moves.remove("down")
    if "up" in possible_moves and  my_head["y"] == width - 1:
        possible_moves.remove("up")

    return possible_moves

def find_nearest_food(my_head: Dict[str, int], food: List[dict]) -> dict:
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    food: List of dictionaries of x/y coordinates for each piece of food on the board.
            e.g. [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]

    return: The dictionary of the nearest piece of food.
    """
    nearest_food = food[0]
    for piece in food:
        if abs(my_head["x"] - piece["x"]) + abs(my_head["y"] - piece["y"]) < abs(my_head["x"] - nearest_food["x"]) + abs(my_head["y"] - nearest_food["y"]):
            nearest_food = piece
    return nearest_food

def choose_direction(my_head: Dict[str, int], food: List[dict], possible_moves: List[str]) -> str:
    """
    Pick a direction to move in towards the nearest piece of food by manhatten distance.

    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    food: List of dictionaries of x/y coordinates for each piece of food.
            e.g. [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    possible_moves: List of strings. Moves to pick from.

    return: A string of the direction to move in.
            e.g. "up"
    """
    if(len(possible_moves) == 1):
        print("Only one move possible")
        return possible_moves[0]

    if len(food) == 0:
        print("No food - random")
        return random.choice(possible_moves)
    else:
        nearest_food = find_nearest_food(my_head, food)
        print("Nearest food: " + str(nearest_food))
        if nearest_food["x"] > my_head["x"] and "right" in possible_moves:
            return "right"
        elif nearest_food["x"] < my_head["x"] and "left" in possible_moves:
            return "left"
        elif nearest_food["y"] < my_head["y"] and "down" in possible_moves:
            return "down"
        elif nearest_food["y"] > my_head["y"] and "up" in possible_moves:
            return "up"

        print("No direction to move in - random")
        return random.choice(possible_moves)
        
    

def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    my_head = data["you"]["head"]  # A dictionary of x/y coordinates like {"x": 0, "y": 0}
    my_body = data["you"]["body"]  # A list of x/y coordinate dictionaries like [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    other_snakes = data["board"]["snakes"]  # A list of dictionaries of x/y coordinates for each snake on the board.
    food = data["board"]["food"]  # A list of dictionaries of x/y coordinates for each piece of food on the board.
    width = data["board"]["width"]  # How wide the board is
    height = data["board"]["height"]  # How high the board is

    # TODO: uncomment the lines below so you can see what this data looks like in your output!
    print(f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~")
    print(f"All board data this turn: {data}")
    print(f"My Battlesnakes head this turn is: {my_head}")
    print(f"My Battlesnakes body this turn is: {my_body}")

    possible_moves = ["up", "down", "left", "right"]

    # Don't allow your Battlesnake to move back in on it's own neck
    possible_moves = avoid_walls(my_head, height, width, possible_moves)
    print(f"Possible moves after avoiding walls: {possible_moves}")
    possible_moves = avoid_my_neck(my_head, my_body, possible_moves)
    print(f"Possible moves after avoiding my neck: {possible_moves}")
    possible_moves = avoid_other_snakes(my_head, other_snakes, possible_moves)
    print(f"Possible moves after avoiding other snakes: {possible_moves}")
    

    # TODO: Using information from 'data', find the edges of the board and don't let your Battlesnake move beyond them
    # board_height = ?
    # board_width = ?

    

    # TODO Using information from 'data', don't let your Battlesnake pick a move that would hit its own body

    # TODO: Using information from 'data', don't let your Battlesnake pick a move that would collide with another Battlesnake

    # TODO: Using information from 'data', make your Battlesnake move towards a piece of food on the board

    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    move = choose_direction(my_head, food, possible_moves)
    # TODO: Explore new strategies for picking a move that are better than random

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move
