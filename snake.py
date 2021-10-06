import random
from typing import List, Dict, Tuple
from astar import astar, Node, return_path


class Snake: 
    def __init__(self, snake_data):
        self.id = snake_data['id']
        self.name = snake_data['name']
        self.length = len(snake_data['body'])
        self.body = snake_data['body']
        self.head = snake_data['body'][0]
        self.health = snake_data['health']
        self.color = snake_data['color']
        self.head = snake_data['head']
        self.latency = snake_data['latency']

    def possible_moves(self, board):
        a = self.avoid_walls(board)
        b = self.avoid_my_neck(board)
        c = self.avoid_other_snakes(board)
        possible_moves = list(set(a).intersection(set(b)).intersection(set(c)))
        return possible_moves


    def choose_from_path(choice: Tuple , my_head: Dict[str, int], possible_moves: List[str]):
        if choice[0] == my_head["x"] and  my_head["y"] == choice[1] + 1 and "down" in possible_moves:
            return "down"
        elif choice[0] == my_head["x"] and  my_head["y"] == choice[1] - 1 and "up" in possible_moves:
            return "up"
        elif choice[1] == my_head["y"] and  my_head["x"] == choice[0] + 1 and "left" in possible_moves:
            return "left"
        elif choice[1] == my_head["y"] and  my_head["x"] == choice[0] - 1 and "right" in possible_moves:
            return "right"

    def chose_direction(self, board):
        food : List = board.food
        my_health = self.health
        my_head :Dict = self.head
        my_body: List[dict] = self.body

        possible_moves = self.possible_moves(board)
        maze = board.snake_grid
        free_spots = board.free_spots
        
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
                choice = self.choose_from_path((my_tail["x"], my_tail["y"]), my_head, possible_moves)
                        
                if choice != None:
                    return choice

            tail_adj = [ e for e in tail_adj if e in free_spots ]

            for tail in tail_adj:
                my_path = astar(maze, (my_head["x"], my_head["y"]), tail )
                if my_path != None:
                    choice = self.choose_from_path(my_path[1], my_head, possible_moves)
                
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
                return self.choose_from_path(choice, my_head, possible_moves)

            print("No direction to move in - random")
            return random.choice(possible_moves)


    def avoid_walls(self, board) -> List[str]:
        possible_moves = ['up', 'down', 'left', 'right']
        my_head = self.head
        if "left" in possible_moves and  my_head["x"] == 0:
            possible_moves.remove("left")
        if "right" in possible_moves and  my_head["x"] == board.height - 1:
            possible_moves.remove("right")
        if "down" in possible_moves and my_head["y"] == 0:
            possible_moves.remove("down")
        if "up" in possible_moves and  my_head["y"] == board.width - 1:
            possible_moves.remove("up")
        return possible_moves

    def avoid_my_neck(self, board) -> List[str]:
        possible_moves = ['up', 'down', 'left', 'right']
        my_head = self.head
        my_body = self.body
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

    def avoid_other_snakes(self, board) -> List[str]:
        possible_moves = ['up', 'down', 'left', 'right']
        my_head = self.head
        other_snakes = board.snakes
        for snake in other_snakes:
            if snake.body[0] == my_head:
                continue
            for segment in snake.body[:-1]:
                if "up" in possible_moves and segment["x"] == my_head["x"] and segment["y"] == my_head["y"] + 1:
                    possible_moves.remove("up")
                if "down" in possible_moves and segment["x"] == my_head["x"] and segment["y"] == my_head["y"] - 1:
                    possible_moves.remove("down")
                if "left" in possible_moves and segment["y"] == my_head["y"] and segment["x"] == my_head["x"] - 1:
                    possible_moves.remove("left")
                if "right" in possible_moves and segment["y"] == my_head["y"] and segment["x"] == my_head["x"] + 1:
                    possible_moves.remove("right")

        return possible_moves

    def find_nearest_food(self, board) -> dict:
        my_head = self.head
        food = board.food
        nearest_food = food[0]
        for piece in food:
            if abs(my_head["x"] - piece["x"]) + abs(my_head["y"] - piece["y"]) < abs(my_head["x"] - nearest_food["x"]) + abs(my_head["y"] - nearest_food["y"]):
                nearest_food = piece
        return nearest_food