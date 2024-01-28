import bisect
import pygame


class Cat:
    def __init__(self, cell, name):
        self.name = name
        self.neighbours = []
        self.best_move = None
        self.f_score = None
        self.game_over = bool(False)
        self.cell = cell
        self.image = pygame.image.load("cat4.png")
        self.image = pygame.transform.scale(self.image, (20, 20))

    def set_position(self, cell):
        if cell != self.cell:
            self.cell = cell

    def a_star_search(self, mouse_cell):
        """performs the A* search algorithm for every cat"""
        # Initialize a priority queue with the cat_position cell
        priority_queue = [self.cell]
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
                break
        self.best_move_finder(mouse_cell)

    def best_move_finder(self, mouse_cell):
        """This method makes the best move for the cat by creating a list
        of the shortest path and taking the second last move
        from the list, which is the best next possible move for the cat."""
        current_cell = mouse_cell.parent
        shortest_path = []
        while current_cell is not None and current_cell != self.cell:

            current_cell = current_cell.parent
            shortest_path.append(current_cell)

        if len(shortest_path) > 2:              #only give the best move if there are more than 2 moves left, because otherwise gameover
                                                #With >1 there will often be 1 square between mouse and cat which can lead to almost infinte fleeing,
                                                # therefore 2 is chosen
            self.best_move = shortest_path[-2]
        else:
            self.game_over = self.game_over = bool(True)
