from astar import astar
import random
from typing import List, Dict, Tuple

from astar import astar, Node, return_path

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
            if "left" in possible_moves and segment["y"] == my_head["y"] and segment["x"] == my_head["x"] - 1:
                possible_moves.remove("left")
            if "right" in possible_moves and segment["y"] == my_head["y"] and segment["x"] == my_head["x"] + 1:
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

def choose_from_path(choice: Tuple , my_head: Dict[str, int], possible_moves: List[str]):
    if choice[0] == my_head["x"] and  my_head["y"] == choice[1] + 1 and "down" in possible_moves:
        return "down"
    elif choice[0] == my_head["x"] and  my_head["y"] == choice[1] - 1 and "up" in possible_moves:
        return "up"
    elif choice[1] == my_head["y"] and  my_head["x"] == choice[0] + 1 and "left" in possible_moves:
        return "left"
    elif choice[1] == my_head["y"] and  my_head["x"] == choice[0] - 1 and "right" in possible_moves:
        return "right"


def choose_direction(my_head: Dict[str, int],  my_body: List[dict], my_health:int, food: List[dict], other_snakes: List[dict], height :int, width :int, possible_moves: List[str]) -> str:
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
    maze = make_maze(my_head, other_snakes, height, width)
    free_spots = [(row_index,col_index) for row_index, row in enumerate(maze) for col_index, col in enumerate(row) if col==0]
    if(len(possible_moves) == 1):
        print("Only one move possible")
        return possible_moves[0]

    food_length = len(food)
    free_spots_length = len(free_spots) - food_length
    print(f"len(food): {food_length} vs free{free_spots_length}")
    print(f"my_health: {my_health}")
    if len(food) == 0 or (food_length < free_spots_length and my_health > 33 and len(my_body) > 5):
        print("Chase Tail!")

        
        my_tail = my_body[-1]

        tail_adj = [(my_tail["x"] + x[0], my_tail["y"]+x[1] ) for x in [(0, -1), (0, 1), (-1, 0), (1, 0)]]

        if((my_head["x"], my_head["y"]) in tail_adj):
            choice = choose_from_path((my_tail["x"], my_tail["y"]), my_head, possible_moves)
                   
            if choice != None:
                return choice

        tail_adj = [ e for e in tail_adj if e in free_spots ]

        for tail in tail_adj:
            my_path = astar(maze, (my_head["x"], my_head["y"]), tail )
            if my_path != None:
                choice = choose_from_path(my_path[1], my_head, possible_moves)
            
                if choice != None:
                    return choice
        
        return random.choice(possible_moves)
    else:
        print("Eat food!")
        # print 2d array
        print("MAZE")
        for row in maze:
            print(row)
        
        nearest_food_path = None

        for food_piece in food:
            food_path = astar(maze, (my_head["x"], my_head["y"]), (food_piece["x"], food_piece["y"]))
            if food_path != None:
                if nearest_food_path is None or len(food_path) < len(nearest_food_path):
                    nearest_food_path = food_path


        if nearest_food_path is not None and (len(nearest_food_path) > 1):
            choice = food_path[1]        
            return choose_from_path(choice, my_head, possible_moves)

        print("No direction to move in - random")
        return random.choice(possible_moves)
        
def make_maze(my_head: Dict[str, int], other_snakes: List[dict], height :int, width :int):
    #make a maze that is height by width
    maze = [[0 for x in range(width)] for y in range(height)]
    # fill 1s where there are snakes
    for snake in other_snakes:
        for segment in snake["body"]:
            maze[segment["x"]][segment["y"]] = 1

    return maze




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
    my_health = data["you"]["health"]  # A number between 0 and 100
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
    
    


    move = choose_direction(my_head, my_body, my_health, food, other_snakes, height, width, possible_moves)

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move
