from __future__ import annotations
from layer_store import *
from data_structures.referential_array import ArrayR

class Grid:
    DRAW_STYLE_SET = "SET"
    DRAW_STYLE_ADD = "ADD"
    DRAW_STYLE_SEQUENCE = "SEQUENCE"
    DRAW_STYLE_OPTIONS = (
        DRAW_STYLE_SET,
        DRAW_STYLE_ADD,
        DRAW_STYLE_SEQUENCE
    )

    DEFAULT_BRUSH_SIZE = 2
    MAX_BRUSH = 5
    MIN_BRUSH = 0

    def __init__(self, draw_style, x, y) -> None:
        """
        Initialise the grid object.
        - draw_style:
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.
        - x, y: The dimensions of the grid.

        Should also intialise the brush size to the DEFAULT provided as a class variable.

        Time complexity: 
            Best case: O(x * y), as we need to initialize a LayerStore for each grid cell.
            Worse case: O(x * y), as we need to initialize a LayerStore for each grid cell.
        """

        #initialising dimension of the grid
        self.x = x 
        self.y = y

        self.grid = [ArrayR(y) for _ in range(x)]

        self.draw_style = draw_style 

        #initialising draw style
        if draw_style not in self.DRAW_STYLE_OPTIONS:
            raise ValueError 
        else:
            for row in range(self.x):
                for column in range(self.y):
                    if self.draw_style == self.DRAW_STYLE_SET:
                        self.grid[row][column] = SetLayerStore()
                    elif self.draw_style == self.DRAW_STYLE_ADD:
                        self.grid[row][column] = AdditiveLayerStore()
                    elif self.draw_style == self.DRAW_STYLE_SEQUENCE:
                        self.grid[row][column] = SequenceLayerStore()

        #initialising brush size
        self.brush_size = self.DEFAULT_BRUSH_SIZE

        

    def __getitem__(self, index):
        """
        Get the LayerStore at the specified index.

         Args:
            index (int): The index of the LayerStore to retrieve.

        Returns:
            LayerStore: The LayerStore at the given index.

        Time complexity: 
            Best case: O(1)
            Worse case: O(1)
        """
        return self.grid[index]

        
    def __setitem__(self, index: tuple[int, int], value: LayerStore) -> None:
        """ Sets the LayerStore at the given (x, y) index to the provided value.

        Args:
            index (tuple[int, int]): The (x, y) index at which to set the LayerStore.
            value (LayerStore): The LayerStore value to set at the index.
 
        :pre: 0 <= x < self.x and 0 <= y < self.y

        Time complexity: 
            Best case: O(1)
            Worse case: O(1)
        """
        self.grid[index] = value
        

    def increase_brush_size(self):
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.

        Time complexity: 
            Best case: O(1)
            Worse case: O(1)
        """

        if self.brush_size != self.MAX_BRUSH:
            self.brush_size += 1

    def decrease_brush_size(self):
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.
        
        Time complexity: 
            Best case: O(1)
            Worse case: O(1)
        """
        if self.brush_size != self.MIN_BRUSH:
            self.brush_size -= 1

    def special(self):
        """
        Activate the special affect on all grid squares.

        Time complexity: 
            Best case: O(x * y), as the special effect is applied to each grid cell
            Worse case: O(x * y), as the special effect is applied to each grid cell
        """
        for row in range(self.x):
            for column in range(self.y):
                self.grid[row][column].special()
              

    