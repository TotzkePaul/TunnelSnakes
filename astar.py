class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0  # Distance from start node
        self.h = 0  # Estimated distance to end node
        self.f = 0  # Total cost

    def __eq__(self, other):
        return self.position == other.position


def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]


def cost_function(child, end_node, hazard_grid):
    distance = (
        (child.position[0] - end_node.position[0]) ** 2
        + (child.position[1] - end_node.position[1]) ** 2
    )
    penalty = hazard_grid[child.position[0]][child.position[1]]
    return distance + penalty


def astar(maze, start, end, hazard_grid):
    """Return a path from start to end in the given maze using A* search."""
    start_node = Node(None, start)
    end_node = Node(None, end)

    open_list = [start_node]
    closed_list = []

    while open_list:
        current_index = 0
        current_node = open_list[0]
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node == end_node:
            return return_path(current_node)

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_position = (
                current_node.position[0] + new_position[0],
                current_node.position[1] + new_position[1],
            )

            if (
                node_position[0] > len(maze) - 1
                or node_position[0] < 0
                or node_position[1] > len(maze[0]) - 1
                or node_position[1] < 0
            ):
                continue

            if maze[node_position[0]][node_position[1]] != 0:
                continue

            new_node = Node(current_node, node_position)
            children.append(new_node)

        for child in children:
            if child in closed_list:
                continue

            child.g = current_node.g + 1
            child.h = cost_function(child, end_node, hazard_grid)
            child.f = child.g + child.h

            if any(
                open_node for open_node in open_list
                if child.position == open_node.position and child.g > open_node.g
            ):
                continue

            open_list.append(child)

    return None
