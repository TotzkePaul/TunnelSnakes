
class Snake: 
    def __init__(self, snake_data):
        self.id = snake_data['id']
        self.name = snake_data['name']        
        self.head = snake_data['head']
        self.body = snake_data['body']
        self.length = len(snake_data['body'])
        self.health :int = snake_data['health']        
        self.latency:int = snake_data['latency']


