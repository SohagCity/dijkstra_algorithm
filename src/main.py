from path_finder import PathFinder


path_finder = PathFinder(4, 4, 0, a = 0, b = 10)
path_finder.print_board()

print(path_finder.dijkstra_path())
path_finder.print_board()

print(path_finder.heuristic_path())
path_finder.print_board()
