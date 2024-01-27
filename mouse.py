
class Mouse:
    def __init__(self, position):
        self.position = position
        #self.position = self.maze.grid[Constants.GRID_COLS-1] [Constants.GRID_ROWS-1]    #x and y values of the cells in the grid

    def set_position(self, cell):
            self.position = cell


