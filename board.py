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
        