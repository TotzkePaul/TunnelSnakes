"""
Starter Unit Tests using the built-in Python unittest library.
See https://docs.python.org/3/library/unittest.html

You can expand these to cover more cases!

To run the unit tests, use the following command in your terminal,
in the folder where this file exists:

    python tests.py -v

"""
import unittest

from board import Board
from snake import Snake


def create_board(head: dict, body: list) -> Board:
    snake_data = {
        "id": "test-snake",
        "name": "snek",
        "head": head,
        "body": body,
        "health": 100,
        "latency": "0",
    }
    data = {
        "game": {"id": "test-game"},
        "turn": 0,
        "board": {
            "height": 11,
            "width": 11,
            "food": [],
            "hazards": [],
            "snakes": [snake_data],
        },
        "you": snake_data,
    }
    return Board(data)


class AvoidNeckTest(unittest.TestCase):
    def test_avoid_neck_all(self):
        """
        The possible move set should be all moves.

        In the starter position, a Battlesnake body is 'stacked' in a
        single place, and thus all directions are valid.
        """
        # Arrange
        test_head = {"x": 5, "y": 5}
        test_body = [{"x": 5, "y": 5}, {"x": 5, "y": 5}, {"x": 5, "y": 5}]
        board = create_board(test_head, test_body)
        # Act
        result_moves = board.avoid_my_neck(board.you)

        # Assert
        self.assertEqual(len(result_moves), 4)
        self.assertEqual(["up", "down", "left", "right"], result_moves)

    def test_avoid_neck_left(self):
        # Arrange
        test_head = {"x": 5, "y": 5}
        test_body = [{"x": 5, "y": 5}, {"x": 4, "y": 5}, {"x": 3, "y": 5}]
        expected = ["up", "down", "right"]

        board = create_board(test_head, test_body)
        # Act
        result_moves = board.avoid_my_neck(board.you)

        # Assert
        self.assertEqual(len(result_moves), 3)
        self.assertEqual(expected, result_moves)

    def test_avoid_neck_right(self):
        # Arrange
        test_head = {"x": 5, "y": 5}
        test_body = [{"x": 5, "y": 5}, {"x": 6, "y": 5}, {"x": 7, "y": 5}]
        expected = ["up", "down", "left"]

        board = create_board(test_head, test_body)
        # Act
        result_moves = board.avoid_my_neck(board.you)

        # Assert
        self.assertEqual(len(result_moves), 3)
        self.assertEqual(expected, result_moves)

    def test_avoid_neck_up(self):
        # Arrange
        test_head = {"x": 5, "y": 5}
        test_body = [{"x": 5, "y": 5}, {"x": 5, "y": 6}, {"x": 5, "y": 7}]
        expected = ["down", "left", "right"]

        board = create_board(test_head, test_body)
        # Act
        result_moves = board.avoid_my_neck(board.you)

        # Assert
        self.assertEqual(len(result_moves), 3)
        self.assertEqual(expected, result_moves)

    def test_avoid_neck_down(self):
        # Arrange
        test_head = {"x": 5, "y": 5}
        test_body = [{"x": 5, "y": 5}, {"x": 5, "y": 4}, {"x": 5, "y": 3}]
        expected = ["up", "left", "right"]

        board = create_board(test_head, test_body)
        # Act
        result_moves = board.avoid_my_neck(board.you)

        # Assert
        self.assertEqual(len(result_moves), 3)
        self.assertEqual(expected, result_moves)

    def test_avoid_neck_diagonal(self):
        """Body diagonally adjacent should not restrict moves."""
        # Arrange
        test_head = {"x": 5, "y": 5}
        test_body = [{"x": 5, "y": 5}, {"x": 6, "y": 6}, {"x": 7, "y": 7}]

        board = create_board(test_head, test_body)
        # Act
        result_moves = board.avoid_my_neck(board.you)

        # Assert
        self.assertEqual(len(result_moves), 4)
        self.assertEqual(["up", "down", "left", "right"], result_moves)


if __name__ == "__main__":
    unittest.main()
