from pygame import draw
class GridElement:
    """
    GridElement used as a tile in the exercise
    """

    """
    Initialise the GridElement and assign the starting values
    """

    def __init__(self, x, y, size):
        self.position = (x, y)
        self.neighbours = []
        self.size = (size[0], size[1])
        self.parent = None
        self.distance = None
        self.score = None
        self.color = (64, 64, 64)

    """
    Overload the equals operator
    """

    def __eq__(self, other):
        return self.position == other.position
    """
    Overload the less than operator
    """

    def __lt__(self, other):
        return (self.score is not None) and (other.score is None or self.score < other.score)

    """
       Overload the hash operator
    """
    def __hash__(self):
        return hash(self.position)
    """
    Overload the string representation of the object
    """

    def __repr__(self):
        return "[%s, %s]" % (self.position, self.score)

    """
    Remove all neighbours
    """

    def reset_neighbours(self):
        self.neighbours = []

    """
    Sets the state of the GridElement 
    """

    def reset_state(self):
        self.parent = None
        self.score = None
        self.distance = None
        self.color = (64, 64, 64)

    def get_neighbours(self):
        return self.neighbours[:]

    """
     Method to calculate the Manhattan distance from a certain 
     GridElement to another GridElement of the exercise
     """

    def manhattan_distance(self, other):
        x_distance = abs(self.position[0] - other.position[0])
        y_distance = abs(self.position[1] - other.position[1])
        return x_distance + y_distance

    def null_distance(self, other):
        x_distance = abs(self.position[0] - other.position[0])
        y_distance = abs(self.position[1] - other.position[1])
        return max(x_distance ,y_distance)

    def direction(self, other):
        return other.position[0] - self.position[0], other.position[1] - self.position[1]

    def set_score(self, score):
        self.score = score

    def set_distance(self, distance):
        self.distance = distance

    def get_distance(self):
        return self.distance

    def get_score(self):
        return self.score

    def get_position(self):
        return self.position

    """
    Assign the GridElement used to reach this GridElement
    """

    def set_parent(self, parent):
        self.parent = parent
        if parent.distance is not None:
            self.distance = parent.distance+1

    def set_color(self, color):
        self.color = color

    """
    Draw the GridElement
    """

    def draw_grid_element(self, surface, cats, mouse):
        """Draws a mouse image"""
        mouse_image_rect = mouse.image.get_rect(topleft=(mouse.cell.position[0] * self.size[0], mouse.cell.position[1] * self.size[1]))
        surface.blit(mouse.image, mouse_image_rect)

        """Draws all the cats"""
        for cat in cats:
            cat_image_rect = cat.image.get_rect(
                topleft=(cat.cell.position[0] * self.size[0], cat.cell.position[1] * self.size[1]))
            surface.blit(cat.image, cat_image_rect)

        # discard the directions where neighbours are
        compass = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # The four directions
        for neighbour in self.neighbours:
            if self.direction(neighbour) in compass:
                compass.remove(self.direction(neighbour))

        for direction in compass:
            if direction == (0, -1):  # North
                draw.line(surface, (173, 216, 230), (self.position[0] * self.size[0], self.position[1] * self.size[1]),
                          ((self.position[0] + 1) * self.size[0], self.position[1] * self.size[1]), 2)
            if direction == (1, 0):  # East
                draw.line(surface, (173, 216, 230), ((self.position[0] + 1) * self.size[0], self.position[1] * self.size[1]),
                          ((self.position[0] + 1) * self.size[0], (self.position[1] + 1) * self.size[1]), 2)
            if direction == (0, 1):  # South
                draw.line(surface, (173, 216, 230), (self.position[0] * self.size[0], (self.position[1] + 1) * self.size[1]),
                          ((self.position[0] + 1) * self.size[0], (self.position[1] + 1) * self.size[1]), 2)
            if direction == (-1, 0):  # West
                draw.line(surface, (173, 216, 230), (self.position[0] * self.size[0], self.position[1] * self.size[1]),
                          (self.position[0] * self.size[0], (self.position[1] + 1) * self.size[1]), 2)


    def print_neighbours(self):

        directions = []
        for neighbor in self.neighbours:
            if self.direction(neighbor) == (0, -1):  # North
                directions.append("North")
            elif self.direction(neighbor) == (1, 0):  # East
                directions.append("East")
            elif self.direction(neighbor) == (0, 1):  # South
                directions.append("South")
            elif self.direction(neighbor) == (-1, 0):  # West
                directions.append("West")
            else:
                directions.append(self.direction(neighbor))

        print(directions)
        return None

    def print_walls(self):
        # discard the directions where neighbours are
        compass = {(0, -1): "North",
                   (1, 0): "East",
                   (0, 1): "South",
                   (-1, 0): "West"}  # The four directions
        for neighbor in self.neighbours:
            compass.pop(self.direction(neighbor))

        print(list(compass.values()))
        return None
