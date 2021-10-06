
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


