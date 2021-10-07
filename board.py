import random
from typing import List, Dict, Tuple
from astar import astar, Node, return_path

from snake import Snake

class Board: 
    def __init__(self, data: dict):
        self.data = data
        self.height = data["board"]["height"]
        self.width = data["board"]["width"]
        self.food = data["board"]["food"] 
        self.hazards = data["board"]["hazards"] 
        self.you = Snake(data["you"])
        self.set_snakes(data["board"]["snakes"])
        self.set_grids()

    def set_snakes(self, snakes: list):
        self.snakes = []
        for snake in snakes:
            self.snakes.append(Snake(snake))

    def set_grids(self):      
        self.set_food_grid()
        self.set_hazard_grid()
        self.set_snake_grid()
        self.set_free_spots()

    def set_free_spots(self):
        self.free_spots =  []
        self.free_spots_grid = [[0 for x in range(self.width)] for y in range(self.height)]
        for x in range(self.width):
            for y in range(self.height):
                if self.snake_grid[x][y] > 0:
                    self.free_spots.append({'x': x, 'y': y})
                else:
                    self.free_spots_grid[x][y] = 1

    def set_snake_grid(self):
        self.snake_grid = [[0 for x in range(self.width)] for y in range(self.height)]
        for snake in self.snakes:
            for index, segment in enumerate(snake.body):
                self.snake_grid[segment['x']][segment['y']] = len(snake.body) - index
    
    def set_food_grid(self):
        self.food_grid = [[0 for x in range(self.width)] for y in range(self.height)]
        for food in self.food:
            self.food_grid[food['x']][food['y']] = 1

    def set_hazard_grid(self):
        self.hazard_grid = [[0 for x in range(self.width)] for y in range(self.height)]
        for hazard in self.hazards:
            self.hazard_grid[hazard['x']][hazard['y']] = -16
        
    def possible_moves(self, my_snake:Snake):
        board = self
        a = board.avoid_walls(my_snake)
        b = board.avoid_my_neck(my_snake)
        c = board.avoid_other_snakes(my_snake)
        possible_moves = list(set(a).intersection(set(b)).intersection(set(c)))

        if len(possible_moves) > 1:
            d = board.avoid_longer_snakes_next_move(my_snake)
            possible_moves = list(set(possible_moves).intersection(set(d)))

        return possible_moves


    def choose_from_path(self, choice: Tuple , my_head: Dict[str, int], possible_moves: List[str]):
        if choice[0] == my_head["x"] and  my_head["y"] == choice[1] + 1 and "down" in possible_moves:
            return "down"
        elif choice[0] == my_head["x"] and  my_head["y"] == choice[1] - 1 and "up" in possible_moves:
            return "up"
        elif choice[1] == my_head["y"] and  my_head["x"] == choice[0] + 1 and "left" in possible_moves:
            return "left"
        elif choice[1] == my_head["y"] and  my_head["x"] == choice[0] - 1 and "right" in possible_moves:
            return "right"

    def chose_direction(self, my_snake:Snake):
        board = self
        food : List = board.food
        my_health = my_snake.health
        my_head :Dict = my_snake.head
        my_body: List[dict] = my_snake.body

        possible_moves = board.possible_moves(my_snake)
        maze = board.snake_grid
        free_spots = board.free_spots
        
        if(len(possible_moves) == 1):
            print("Only one move possible")
            return possible_moves[0]

        food_length = len(food)
        free_spots_length = len(free_spots) - food_length

        print(f"len(food): {food_length} vs free{free_spots_length}")
        print(f"my_health: {my_health}")

        if len(food) == 0 or (food_length < free_spots_length and my_health > 33 and len(my_body) > 8):
            print("Chase Tail!")

            
            my_tail = my_body[-1]

            tail_adj = [(my_tail["x"] + x[0], my_tail["y"]+x[1] ) for x in [(0, -1), (0, 1), (-1, 0), (1, 0)]]

            if((my_head["x"], my_head["y"]) in tail_adj) and board.hazard_grid[my_head["x"]][my_head["y"]] == 0:
                choice = board.choose_from_path((my_tail["x"], my_tail["y"]), my_head, possible_moves)
                        
                if choice != None:
                    return choice

            tail_adj = [ e for e in tail_adj if e in free_spots ]

            for tail in tail_adj:
                my_path = astar(maze, (my_head["x"], my_head["y"]), tail, board.hazard_grid)
                if my_path != None:
                    choice = board.choose_from_path(my_path[1], my_head, possible_moves)
                
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
                food_path = astar(maze, (my_head["x"], my_head["y"]), (food_piece["x"], food_piece["y"]), board.hazard_grid)
                if food_path != None:
                    if nearest_food_path is None or len(food_path) < len(nearest_food_path):
                        nearest_food_path = food_path


            if nearest_food_path is not None and (len(nearest_food_path) > 1):
                choice = food_path[1]        
                return board.choose_from_path(choice, my_head, possible_moves)

            print("No direction to move in - random")
            return random.choice(possible_moves)


    def avoid_walls(self, my_snake:Snake) -> List[str]:
        board = self
        possible_moves = ['up', 'down', 'left', 'right']
        my_head = my_snake.head
        if "left" in possible_moves and  my_head["x"] == 0:
            possible_moves.remove("left")
        if "right" in possible_moves and  my_head["x"] == board.height - 1:
            possible_moves.remove("right")
        if "down" in possible_moves and my_head["y"] == 0:
            possible_moves.remove("down")
        if "up" in possible_moves and  my_head["y"] == board.width - 1:
            possible_moves.remove("up")
        return possible_moves

    def avoid_my_neck(self, my_snake:Snake) -> List[str]:
        board = self
        possible_moves = ['up', 'down', 'left', 'right']
        my_head = my_snake.head
        my_body = my_snake.body
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

    def avoid_other_snakes(self, my_snake:Snake) -> List[str]:
        board = self
        possible_moves = ['up', 'down', 'left', 'right']
        my_head = my_snake.head
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

    def avoid_longer_snakes_next_move(self, my_snake:Snake) -> List[str]:
        board = self
        possible_moves = ['up', 'down', 'left', 'right']
        my_head = my_snake.head
        other_snakes = board.snakes
        for snake in other_snakes:
            if snake.body[0] == my_head or len(snake.body) < len(my_snake.body):
                continue
            for segment in snake.body[:-1]:
                if segment["x"] == my_head["x"] -1 and segment["y"] == my_head["y"] + 1:
                    if "up" in possible_moves:
                        possible_moves.remove("up")
                    if "left" in possible_moves:
                        possible_moves.remove("left")
                if segment["x"] == my_head["x"] + 1 and segment["y"] == my_head["y"] + 1:
                    if "up" in possible_moves:
                        possible_moves.remove("up")
                    if "right" in possible_moves:
                        possible_moves.remove("right")
                if segment["x"] == my_head["x"] - 1 and segment["y"] == my_head["y"] - 1:
                    if "down" in possible_moves:
                        possible_moves.remove("down")
                    if "left" in possible_moves:
                        possible_moves.remove("left")
                if segment["x"] == my_head["x"] + 1 and segment["y"] == my_head["y"] - 1:
                    if "down" in possible_moves:
                        possible_moves.remove("down")
                    if "right" in possible_moves:
                        possible_moves.remove("right")

        return possible_moves

    def find_nearest_food(self, my_snake:Snake) -> dict:
        board = self
        my_head = my_snake.head
        food = board.food
        nearest_food = food[0]
        for piece in food:
            if abs(my_head["x"] - piece["x"]) + abs(my_head["y"] - piece["y"]) < abs(my_head["x"] - nearest_food["x"]) + abs(my_head["y"] - nearest_food["y"]):
                nearest_food = piece
        return nearest_food
 