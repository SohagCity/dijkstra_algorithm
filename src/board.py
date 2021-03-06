import random
from typing import List



class Board:
    height: int
    width: int
    board: List[List[int]]
    moves: list
    game_mode: int = 0

    GREEN = '\033[92m'
    ENDC  = '\033[0m'

    def __init__(
        self,
        height: int,
        width: int,
        game_mode: int = 1,
        distribution = random.randint,
        **kwargs
    ) -> None:
        self.height = height
        self.width = width
        self.game_mode = game_mode
        self.moves = [
            self.move_up, 
            self.move_down, 
            self.move_left, 
            self.move_right
        ]
        self.board = []
        for _ in range(height):
            self.board.append(
                [distribution(**kwargs) for _ in range(width)]
            )

    def print_board(self, path: List[tuple] = []):
        """
        Print the board highlighting the path given.
        """
        for x, row in enumerate(self.board):
            for y, value in enumerate(row):
                if (x, y) in path:
                    color = self.GREEN
                
                else:
                    color = ''

                print("{}%{}f".format(color, 2) % value + self.ENDC, end=" ")

            print()

    def get_weight(self, starting_x, starting_y, x, y):
        """
        Get the weight of a node based on the selected game mode.
        """
        if self.game_mode == 0:
            return self.board[x][y]
        
        else:
            return abs(self.board[x][y] - self.board[starting_x][starting_y])

    def is_within_limits(self, x, y):
        """
        Check if the given coordinates are within the board's size.
        """
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
    
    def possible_moves(self, x, y) -> List[tuple]:
        return [move(x, y) for move in self.moves if move(x, y) != None]
