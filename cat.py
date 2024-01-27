import bisect



class Cat:
    def __init__(self, position):
        # Initialize the search algorithm with the given maze
        self.neighbours = []
        self.best_move = None
        self.f_score = None
        self.gameover = bool(False)
        self.position = position
        #self.position = self.maze.grid[Constants.GRID_COLS-1] [Constants.GRID_ROWS-1]    #x and y values of the cells in the grid

    # def algorithm(self, maze):
    #     self.maze = maze
    #     self.a_star_search(maze)

    def a_star_search(self, mouse_position):
        self.mouse_position = mouse_position
        # Initialize a priority queue with the cat_position cell
        priority_queue = [self.position]
        visited = []

        while len(priority_queue) > 0:
            # Get the cell with the lowest f_score from the priority queue
            current_cell = priority_queue.pop(0)

            if current_cell != self.mouse_position:
                # If the current cell is not the mouse cell, continue the search

                # Mark the current cell as visited
                visited.append(current_cell)

                for next_cell in current_cell.get_neighbours():
                    # Explore the neighbors of the current cell

                    if next_cell not in visited:
                        # If the neighbor has not been visited

                        # Calculate the f_score (distance + heuristic) for the neighbor
                        self.f_score = current_cell.get_distance()
                        score = next_cell.manhattan_distance(self.mouse_position)

                        # Add the f_score to the heuristic score
                        if self.f_score is not None:
                            score += self.f_score

                        if next_cell not in priority_queue:
                            # If the neighbor is not in the priority queue, add it
                            next_cell.set_parent(current_cell)
                            current_cell.set_score(score)
                            bisect.insort(priority_queue, next_cell)

                        elif self.f_score < next_cell.get_distance():
                            # If the new f_score is smaller than the existing one, update it
                            next_cell.set_parent(current_cell)
                            next_cell.set_score(score)
                            priority_queue.remove(next_cell)
                            bisect.insort(priority_queue, next_cell)

            else:
                # If the current cell is the mouse cell, break out of the loop
                break

        if self.f_score < 2:
            # Check if the cat is besides the mouse, After this, set gameover to True
            print("ja")
            self.gameover = bool(True)

        # Highlight the path from the mouse to the cat_position cell
        self.highlight_path()

    def highlight_path(self):
        # checks the path from the mouse to the cat_position cell
        current_cell = self.mouse_position.parent
        while current_cell is not None and current_cell.parent is not None: #Continue the loop as long as current_cell is not at the cat_position cell(noone) and it has a parent.

            #if current_cell.parent == self.maze.cat_position:
            if current_cell.parent == self.position:
                # If the parent of the current cell is the cat_position cell, set the best_move
                self.best_move = current_cell.get_position()

            current_cell = current_cell.parent
