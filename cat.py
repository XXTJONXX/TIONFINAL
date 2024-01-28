import bisect
import pygame


class Cat:
    def __init__(self, cell, name):
        # Initialize the search algorithm with the given maze
        self.name = name
        self.neighbours = []
        self.best_move = None
        self.f_score = None
        self.gameover = bool(False)
        self.cell = cell
        self.image = pygame.image.load("cat4.png")
        self.image = pygame.transform.scale(self.image, (20, 20))
        print(self," - ",self.cell)

    def set_position(self, cell):
        if cell != self.cell:
            self.cell = cell

    def a_star_search(self, mouse_cell):
        #print(self," location = ",self.cell)
        #self.mouse_cell = mouse_cell
        # Initialize a priority queue with the cat_position cell
        priority_queue = [self.cell]
        #print(self, " priority queue", priority_queue)
        visited = []

        while len(priority_queue) > 0:
            # Get the cell with the lowest f_score from the priority queue
            current_cell = priority_queue.pop(0)

            if current_cell != mouse_cell:
                # If the current cell is not the mouse cell, continue the search

                # Mark the current cell as visited
                visited.append(current_cell)

                for next_cell in current_cell.get_neighbours():
                    # Explore the neighbors of the current cell

                    if next_cell not in visited:
                        # If the neighbor has not been visited

                        # Calculate the f_score (distance + heuristic) for the neighbor
                        self.f_score = current_cell.get_distance()
                        score = next_cell.manhattan_distance(mouse_cell)

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

        #print(self,"-------F-SCORE = ",self.f_score)
        if self.f_score <= 2:
            # Check if the cat is besides the mouse, After this, set gameover to True
            self.gameover = bool(True)
        else:
            # Highlight the path from the mouse to the cat_position cell
            self.best_move_finder(mouse_cell)

    # def highlight_path(self, mouse_cell):
    #     # checks the path from the mouse to the cat_position cell
    #     print(self," mouseposition ",mouse_cell)
    #     print(self," mouse Parent ",mouse_cell.parent)
    #     current_cell = mouse_cell.parent
    #
    #     # Continue the loop as long as current_cell is not at the cat_position cell(none) and it has a parent.
    #     count = 0
    #     while current_cell is not None and current_cell.parent is not None:
    #         count = count + 1
    #         if count < 100:
    #             print(self," current_cell = ",current_cell,", current_cell.parent = ", current_cell.parent)
    #         # if current_cell.parent == self.maze.cat_position:
    #
    #         if current_cell.parent == self.cell:
    #             # If the parent of the current cell is the cat_position cell, set the best_move
    #             self.best_move = current_cell.get_position()
    #
    #         current_cell = current_cell.parent
    #     print("BEST MOVE...", self, " current_cell = ", current_cell, ", current_cell.parent = ", current_cell.parent)

    def best_move_finder(self, mouse_cell):
        current_cell = mouse_cell.parent        #current cell is in de fastest path de cel VOORDAT hij dezelfde locatie heeft als de muis
        print("current_cell", current_cell)
        shortest_path = []
        while current_cell is not None and current_cell != self.cell:

            current_cell = current_cell.parent      #hier is de current cell de beste move, gerekend tov de current cell hierboven
            shortest_path.append(current_cell)
            #print("current_cell na while loop:", current_cell)

        self.best_move = shortest_path[-2]

        # print("shortest pat", shortest_path)
        # print("beste move (want een na laatste move voordat je op target zit)", shortest_path[-2])

        # print("best_move?  = ", best_move.position)
        # print("best_move?  = ", best_move.position[0])
        # print("best_move?  = ", best_move.position[1])


    def __str__(self):
        return "CAT " + str(self.name)