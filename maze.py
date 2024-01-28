import random
from grid_element import GridElement
from helpers.constants import Constants
from cat import Cat
from mouse import Mouse



class Maze:
    """
        Generates a grid based maze based on GridElements
        This class also contains search algorithms for
        depth first, breath first, greedy and A* star search to
        solve the generated mazes
        """

    def __init__(self, grid_size_x, grid_size_y, screen_size):
        self.active = True
        self.cat_image = None
        self.grid_size = (grid_size_x, grid_size_y)
        self.cell_width = screen_size[0] / grid_size_x
        self.cell_height = screen_size[1] / grid_size_y
        self.grid = []
        for x in range(grid_size_x):
            self.grid.append([])
            for y in range(grid_size_y):
                self.grid[x].append(GridElement(x, y, (self.cell_width, self.cell_height)))
        self.mouse = Mouse(self.grid[random.randint(0,Constants.GRID_COLS-1)][random.randint(0,Constants.GRID_ROWS-1)])
        """make cats"""
        #self.cat = Cat(self.grid[random.randint(0,Constants.GRID_COLS-1)][random.randint(0,Constants.GRID_ROWS-1)])  # Create a new cat
        self.cats = []  # List to store cats
        self.num_cats = 2  # Number of cats
        # Create and initialize cats
        for number in range(self.num_cats):
            cat = Cat(self.grid[random.randint(0,Constants.GRID_COLS-1)][random.randint(0,Constants.GRID_ROWS-1)], number)  # Create a new cat
            #cat = Cat(self.grid[0][0],number)  # Create a new cat
            self.cats.append(cat)  # Add the cat to the list
        self.reset_all()



    def update(self):
        for cat in self.cats:
            """doe de best move , uiteindelijk doet de kat de beste move dus elke kat heeft dan een nieuwe positie"""
            if cat.best_move is not None:
                #print(cat," best move = ",cat.best_move)
                cat.set_position((self.grid[cat.best_move.position[0]][cat.best_move.position[1]]))
        self.reset_state()
        # if self.cat.best_move is not None:
        #     self.set_cat((self.grid[self.cat.best_move[0]][self.cat.best_move[1]]))
    """
    Resets the GridElements of the maze
    """

    def reset_all(self):
        for row in self.grid:
            for cell in row:
                cell.reset_neighbours()
        self.reset_state()
        return None

    def reset_state(self):
        for row in self.grid:
            for cell in row:
                cell.reset_state()
        for cat in self.cats:
            cat.cell.set_distance(0)
            cat.cell.set_score(0)
        return None




    def set_mouse(self, cell):
        self.cell = cell
        for cat in self.cats:
            if cell != cat.cell:
                self.mouse.set_position(self.cell)
                self.reset_state()

    def move_mouse(self, dx, dy):

        #print("--++ move muis: x=" + str(dx) + " y=" + str(dy))
        self.current_mouse = self.mouse.cell

        #print("--++ self.mouse.cell=" + str(self.mouse.cell))

        if self.current_mouse:
            new_mouse_x = max(0, min(self.current_mouse.position[0] + dx, self.grid_size[0] - 1))
            new_mouse_y = max(0, min(self.current_mouse.position[1] + dy, self.grid_size[1] - 1))

            # Check if there is a link between the current position and the new position
            if self.grid[new_mouse_x][new_mouse_y] in self.current_mouse.get_neighbours():
                self.set_mouse(self.grid[new_mouse_x][new_mouse_y])
                for cat in self.cats:
                    print(self.mouse.cell)
                    cat.a_star_search(self.mouse.cell)


    def print_maze(self):
        transposed = list(zip(*self.grid))
        for row in transposed:
            print(row)
        return None

    def draw_maze(self, surface):
        for row in self.grid:
            for element in row:
                #element.draw_grid_element(surface, self.cats, self.cat_image, self.mouse, self.mouse_image)
                element.draw_grid_element(surface, self.cats, self.mouse)
        return None




    def possible_neighbours(self, cell):
        neighbours = []
        if cell.position[0] > 0:  # North
            neighbours.append(self.grid[cell.position[0] - 1][cell.position[1]])
        if cell.position[0] < self.grid_size[0] - 1:  # East
            neighbours.append(self.grid[cell.position[0] + 1][cell.position[1]])
        if cell.position[1] < self.grid_size[1] - 1:  # South
            neighbours.append(self.grid[cell.position[0]][cell.position[1] + 1])
        if cell.position[1] > 0:  # West
            neighbours.append(self.grid[cell.position[0]][cell.position[1] - 1])
        return neighbours

    def del_link(self, cell1, cell2):
        if cell2 in cell1.neighbours:
            cell1.neighbours.remove(cell2)
        if cell1 in cell2.neighbours:
            cell2.neighbours.remove(cell1)
        return None

    def add_link(self, cell1, cell2):
        if cell1.manhattan_distance(cell2) == 1:
            cell1.neighbours.append(cell2)
            cell2.neighbours.append(cell1)
        return None

    """
     Generate the maze based on depth first search 
     """

    def generate_maze(self):
        self.reset_all()
        for cat in self.cats:
            wait = [cat.cell]
            passed = set()
            while len(wait) > 0:
                current_element = wait.pop(-1)
                if current_element not in passed:
                    passed.add(current_element)

                    neighbours = self.possible_neighbours(current_element)  # Here we want to us all possible neighbours
                    for cell in neighbours[:]:
                        if cell in passed:
                            neighbours.remove(cell)
                    random.shuffle(neighbours)
                    wait.extend(neighbours)
                    for next_element in neighbours:
                        next_element.parent = current_element

                    if current_element.parent is not None:  # The cat has no parent
                        self.add_link(current_element.parent, current_element)

            # add a few random links
            for i in range(max(self.grid_size)):
                random_row = random.choice(self.grid)
                random_element = random.choice(random_row)
                possible = self.possible_neighbours(random_element)
                for cell in possible[:]:
                    if cell in random_element.get_neighbours():
                        possible.remove(cell)
                if len(possible) > 0:
                    random_neighbor = random.choice(possible)
                    self.add_link(random_element, random_neighbor)

            self.reset_state()
            return None


    def generate_open_maze(self):
        self.reset_all()
        for col in self.grid:
            for cell in col:
                cell.neighbours = self.possible_neighbours(cell)



    def generate_room(self):
        """Generates rooms, with specific positions."""
        self.reset_all()
        self.generate_open_maze()

        for x in range(self.grid_size[0] // 4 + 2, self.grid_size[0] // 2 + 1):
            self.del_link(self.grid[x][self.grid_size[1] // 4], self.grid[x][(self.grid_size[1] // 4) - 1])

        for y in range(self.grid_size[1] // 4 + 2, self.grid_size[1] // 2 + 1):
            self.del_link(self.grid[self.grid_size[0] // 4][y], self.grid[(self.grid_size[0] // 4) - 1][y])

        for x in range(0, self.grid_size[0] // 2 - 1):
            self.del_link(self.grid[x][self.grid_size[1] // 2], self.grid[x][(self.grid_size[1] // 2) + 1])

        for x in range(self.grid_size[0] // 2 + 1, self.grid_size[0]):
            self.del_link(self.grid[x][self.grid_size[1] // 2], self.grid[x][(self.grid_size[1] // 2) + 1])

        for y in range(0, self.grid_size[1] // 2 - 2):
            self.del_link(self.grid[self.grid_size[0] // 2][y], self.grid[(self.grid_size[0] // 2) + 1][y])

        for y in range(self.grid_size[1] // 2 + 3, self.grid_size[1]):
            self.del_link(self.grid[self.grid_size[0] // 2][y], self.grid[(self.grid_size[0] // 2) + 1][y])

        for x in range(3 * self.grid_size[0] // 4, self.grid_size[0]):
            self.del_link(self.grid[x][self.grid_size[1] // 2], self.grid[x][(self.grid_size[1] // 2) + 1])

        for y in range(0, self.grid_size[1] // 4):
            self.del_link(self.grid[3 * self.grid_size[0] // 4][y], self.grid[(3 * self.grid_size[0] // 4) + 1][y])

        for x in range(self.grid_size[0] // 8, 3 * self.grid_size[0] // 4 + 1):
            self.del_link(self.grid[x][3 * self.grid_size[1] // 4], self.grid[x][(3 * self.grid_size[1] // 4) - 1])

        for y in range(3 * self.grid_size[1] // 4, self.grid_size[1] - 1):
            self.del_link(self.grid[3 * self.grid_size[0] // 4][y], self.grid[(3 * self.grid_size[0] // 4) + 1][y])

        for y in range(3 * self.grid_size[1] // 4, self.grid_size[1] - 5):
            self.del_link(self.grid[self.grid_size[0] // 8][y], self.grid[(self.grid_size[0] // 8) - 1][y])

        for y in range(self.grid_size[1] - 3, self.grid_size[1]):
            self.del_link(self.grid[self.grid_size[0] // 8][y], self.grid[(self.grid_size[0] // 8) - 1][y])

    def generate_obstacles(self):
        """Generate a Manhattan like grid, with a few road blocks"""

        self.reset_all()
        self.generate_open_maze()

        # The basic boxes
        for n in range(1, self.grid_size[1], 5):
            for m in range(1, self.grid_size[0], 5):
                max_x = min(3, self.grid_size[0] - m - 1)
                max_y = min(3, self.grid_size[1] - n - 1)
                for x in range(0, max_x):
                    self.del_link(self.grid[m + x][n], self.grid[m + x][n - 1])
                    self.del_link(self.grid[m + x][n + max_y], self.grid[m + x][n + max_y - 1])
                for y in range(0, max_y):
                    self.del_link(self.grid[m][n + y], self.grid[m - 1][n + y])
                    self.del_link(self.grid[m + max_x][n + y], self.grid[m + +max_x - 1][n + y])

        # add a few random links
        for i in range(max(self.grid_size)):
            random_row = random.choice(self.grid)
            random_element = random.choice(random_row)
            possible = self.possible_neighbours(random_element)
            for cell in possible[:]:
                if cell in random_element.get_neighbours():
                    possible.remove(cell)
            if len(possible) > 0:
                random_neighbor = random.choice(possible)
                self.add_link(random_element, random_neighbor)

        # vertical blocks
        block_x = random.choice(range(3, self.grid_size[0], 5))
        self.del_link(self.grid[block_x][0], self.grid[block_x - 1][0])
        for m in range(4, self.grid_size[1] - 2, 5):
            block_x = random.choice(range(3, self.grid_size[0], 5))
            self.del_link(self.grid[block_x][m], self.grid[block_x - 1][m])
            self.del_link(self.grid[block_x][m + 1], self.grid[block_x - 1][m + 1])
        block_x = random.choice(range(3, self.grid_size[0], 5))
        self.del_link(self.grid[block_x][self.grid_size[1] - 1], self.grid[block_x - 1][self.grid_size[1] - 1])

        # horizontal blocks
        block_y = random.choice(range(3, self.grid_size[1], 5))
        self.del_link(self.grid[0][block_y], self.grid[0][block_y - 1])
        for n in range(4, self.grid_size[0] - 2, 5):
            block_y = random.choice(range(3, self.grid_size[1], 5))
            self.del_link(self.grid[n][block_y], self.grid[n][block_y - 1])
            self.del_link(self.grid[n + 1][block_y], self.grid[n + 1][block_y - 1])
        block_y = random.choice(range(3, self.grid_size[1], 5))
        self.del_link(self.grid[self.grid_size[0] - 1][block_y], self.grid[self.grid_size[0] - 1][block_y - 1])

    def is_game_over(self):
        stop_game = False
        for cat in self.cats:
            if cat.gameover is True:
                print("One Cat is Game Over")
                stop_game = True
        return stop_game
