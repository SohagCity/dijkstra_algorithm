import abc
import random
from typing import List

random.seed(2)


class Board:
    height: int
    width: int
    board: List[List[int]] = []
    moves: list
    path: List[tuple] = [(0, 0)]

    GREEN = '\033[92m'
    ENDC  = '\033[0m'

    def __init__(self, height: int, width: int) -> None:
        self.height = height
        self.width  = width
        self.moves = [
            #self.move_up, 
            self.move_down, 
            #self.move_left, 
            self.move_right
        ]
        for _ in range(height):
            self.board.append(
                [random.randint(0, 9) for _ in range(width)]
            )

    def print_board(self):
        # TODO: make space depend on the number of digits
        for x, row in enumerate(self.board):
            for y, value in enumerate(row):
                if (x, y) in self.path:
                    color = self.GREEN
                
                else:
                    color = ''

                print("{}%{}d".format(color, 2) % value + self.ENDC, end=" ")

            print()


    def get_weigth(self, starting_x, starting_y, x, y):
        return self.board[x][y]

    def is_within_limits(self, x, y):
        if x < self.width and x >= 0 and y < self.height and y >= 0 :
            return x, y
        
        else:
            return None

    def move_up(self, x: int, y: int):
        return self.is_within_limits(x - 1, y)

    def move_down(self, x: int, y: int):
        return self.is_within_limits(x + 1, y)
    
    def move_right(self, x: int, y: int):
        return self.is_within_limits(x, y + 1)
    
    def move_left(self, x: int, y: int):
        return self.is_within_limits(x, y - 1)
    
    def possible_moves(self, x, y):
        return [move(x, y) for move in self.moves if move(x, y) != None]
    
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
        current_position = (0, 0)
        final_node = (self.width - 1, self.height - 1)
        traversed_nodes = [current_position]
        path_weight = 0

        # Repeat this process until we get to the final node
        while current_position != final_node:
            smallest_weigth = None
            move = (0, 0)
            possible_moves = self.possible_moves(current_position[0], current_position[1])

            # Go through all the possible moves from the current position.
            for x, y in possible_moves:
                weight = self.get_weigth(*current_position, x, y)
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
                path_weight -= self.get_weigth(*poped_node, *current_position)
                current_position = poped_node
                continue

            traversed_nodes.append(move)
            current_position = move
            path_weight += weight
        
        self.path = traversed_nodes
        return path_weight
    
    def dijkstra_path(self):
        pass


board = Board(4, 4)
board.print_board()
board.heuristic_path()
board.print_board()


