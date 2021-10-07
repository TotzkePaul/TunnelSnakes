from board import Board


def choose_move(data: dict) -> str:
    board:Board = Board(data)
    move = board.chose_direction(board.you)
    
    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked")

    return move
