from typing import List

from board import Board
from priority_queue import PriorityQueue


class PathFinder:

    board: Board
    path: List[tuple] = [(0, 0)]

    def __init__(self, height: int, width: int, game_mode: int = 1) -> None:
        self.board = Board(height, width, game_mode)

    def print_board(self):
        self.board.print_board(self.path)

    def heuristic_path(self):
        """
        This is my approach to finding the shortest path.
        The logic can be summed up as follows:
        Check the neighbour nodes and compare their weight.
        Take the node with the smallest weight.
        If there aren't any possible moves we go back one and try again.
        Whilist doing this we keep a list of traversed nodes and the path we have taken so far.
        The process is repeated until we get to the final Node.
        """
        start_position = (0, 0)
        current_position = start_position
        final_node = (self.board.width - 1, self.board.height - 1)
        traversed_nodes = [current_position]
        path_weight = 0

        # Repeat this process until we get to the final node
        while current_position != final_node:
            smallest_weigth = None
            move = start_position
            possible_moves = self.board.possible_moves(
                current_position[0], current_position[1]
            )

            # Go through all the possible moves from the current position.
            for x, y in possible_moves:
                weight = self.board.get_weigth(*current_position, x, y)
                # If this is the final node always take it
                if (x, y) == final_node:
                    smallest_weigth = weight
                    move = (x, y)
                    break

                # If the node has been traversed already ignore it
                if (x, y) in traversed_nodes:
                    continue

                # If this is the first node being traversed then, it is the best possible node for the moment
                # Compare the result of the remaining nodes with this result and get save the one with less weight.
                if smallest_weigth == None:
                    smallest_weigth = weight
                    move = (x, y)

                elif smallest_weigth > weight:
                    smallest_weigth = weight
                    move = (x, y)

            # If there were no possible moves (i.e. weigth hasn't been touched)
            # Go back to the previous node resetting all the necessary variables to the previous state
            if smallest_weigth == None:
                poped_node = self.path[-1]
                traversed_nodes.append(poped_node)
                path_weight -= self.board.get_weigth(*poped_node, *current_position)
                current_position = poped_node
                continue

            traversed_nodes.append(move)
            current_position = move
            path_weight += smallest_weigth
        
        self.path = [start_position]
        self.path = traversed_nodes
        return path_weight

    def dijkstra_path(self):
        """
        Dijkstra's path implementation using a priority queue.
        """
        # For each node we will keep track of the previous node
        # This will allow us to rebuild the selected path.
        previous = {}
        start_position = (0, 0)
        # Create a dictionary with all the positions as key and distances as value
        # Set all the distances to infinity
        distances = {
            (x, y): float('inf')
            for x, row in enumerate(self.board.board)
            for y, value in enumerate(row)
        }
        # Set starting point's distance to 0
        distances[start_position] = 0

        priority_queue = PriorityQueue()
        priority_queue.put((0, start_position))

        while not priority_queue.empty():
            current_distance, current_position = priority_queue.get()

            # Compare neighbors (i.e. the possible moves from the current node)
            for neighbor in self.board.possible_moves(current_position[0], current_position[1]):
                distance = self.board.get_weigth(*current_position, *neighbor) + current_distance

                # If we already have a better path to this node, then ignore current path
                if current_distance > distances[current_position]:
                    continue

                # If this is a better path, update the distances and the priority queue.                        
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    priority_queue.put((distance, neighbor))
                    previous[neighbor] = current_position

        final_node = (self.board.width - 1, self.board.height - 1)
        self.path = [start_position]
        self.shortest(final_node, previous)
        return distances[final_node]

    def shortest(self, node, previous):
        """
        Rebuild the path using the dictionary created in self.dijkstra_path
        """
        if previous.get(node):
            self.path.append(node)
            self.shortest(previous[node], previous)
