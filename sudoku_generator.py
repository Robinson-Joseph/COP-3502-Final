# Joseph Robinson, 4/9/2024, generator for backend of sudoku game project.

import random


class SudokuGenerator:
    """A class with methods related to sudoku Generation

    Attributes:
        row_length (int): the length and width of the board.

        removed_cells (int): How many cells have been removed from the board for the user to fill back in.

        board (list[list[int]]): A 2d matrix containing the values representing the board.

        box_length (int): An integer representing the length of each box. This is always the square root of row_length.
    """    

    def __init__(self, row_length: int, removed_cells: int) -> None:
        """Creates a sudoku board. Initializes the variables and sets up the 2D matrix representation.

        Args:
            row_length (int): how many rows and columns will the board have
            removed_cells (int): how many cells will be removed from the board (20,30,50 for easy,medium, and hard)
        
        
        """        
        
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = []
        self.box_length = int(row_length**0.5)
        for i in range(0, row_length):
            self.board.append([0 for i in range(0, row_length)])


    def get_board(self) -> list[list[int]]:
        """Returns a 2D python list of numbers which represents the board
        
        Returns: 
            list[list[int]]: The matrix containing the board state.
        """
        return self.board


    def print_board(self) -> None:
        """Displays the board to the console.
        This is not strictly required, but it may be useful for debugging purposes
        """
        for i in self.board:
            for j in i:
                print(j, end=" ")
            print()

    def valid_in_row(self, row:int, num:int) -> bool:
        """Determines if `num` is contained in the specified row of the board.

        Args:
            row (int): row to check on the board.
            num (int): num to check for.

        Returns:
            bool: `True` if in the board, otherwise `False`
        """        
        for i in range(0, self.row_length):
            if self.board[row][i] == num:
                return False
        return True


    def valid_in_col(self, col:int, num:int) -> bool:
        """Determines if `num` is contained in the column specified.

        Args:
            col (int): the index of the column to check.
            num (int): the number to check for.

        Returns:
            bool: `False` if num is in the column, `True` if it is a valid number in the column.
        """        
        for i in range(0, self.row_length):
            if self.board[i][col] == num:
                return False
        return True

    

    def valid_in_box(self, row_start:int, col_start:int, num:int) -> bool:
        """Determines if `num` is valid in the 3x3 box starting at [`row_start`,`col_start`]

        Args:
            row_start (int): row index of the upper left position of the box to check.
            col_start (int): column index of the upper left position of the box to check.
            num (int): number to check the validity of.

        Returns:
            bool: True if valid, false if not valid.
        """        
        for row in range(row_start, row_start+self.box_length):
            for col in range(col_start, col_start+self.box_length):
                if self.board[row][col] == num:
                    return False
            print()
        return True



    

    def is_valid(self, row:int, col:int, num:int) -> bool:
        """Checks if `num` is valid at a specific position on the board.

        Args:
            row (int): row of the position to check.
            col (int): column of the position to chekc
            num (int): number to check for validity

        Returns:
            bool: `True` if the value is valid, `False` if it is not valid.
        """        
        row_start = (row//self.box_length)*self.box_length
        col_start = (col//self.box_length)*self.box_length
        if not self.valid_in_box(row_start, col_start, num):
            return False
        if not self.valid_in_col(col, num):
            return False
        if not self.valid_in_row(row, num):
            return False
        return True

    
    def fill_box(self, row_start: int, col_start: int) -> None:
        """Fills the box of size `box_length` x `box_length` (3x3 for this project) at the starting indice [`row_start`,`col_start`]

        Args:
            row_start (int): The row of the spot that is the upper left of the box
            col_start (int): The column of the spot that is the upper left of the box
        """        
        unused_in_box = [i for i in range(1, self.row_length+1)]
        for row in range(row_start, row_start+self.box_length):
            for col in range(col_start, col_start+self.box_length):
                unused_value = unused_in_box[random.randint(0, len(unused_in_box)-1)]
                self.board[row][col] = unused_value
                unused_in_box.remove(unused_value)
        return



    def fill_diagonal(self):
        """Fills the three boxes along the main diagonal of the board
        These are the boxes which start at (0,0), (3,3), and (6,6)
        """
        for i in range(0, self.row_length//self.box_length):
            self.fill_box(i*self.box_length, i*self.box_length)
        self.print_board()
        return


    def fill_remaining(self, row: int, col: int) -> bool:
        """
        DO NOT CHANGE
        Provided for students
        Fills the remaining cells of the board
        Should be called after the diagonal boxes have been filled
        
        Parameters:
        row, col specify the coordinates of the first empty (0) cell

        Return:
        boolean (whether or not we could solve the board)
        """
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False


    def fill_values(self) -> None:
        """
        DO NOT CHANGE
        Provided for students
        Constructs a solution by calling fill_diagonal and fill_remaining
        """
        
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)
        


    def remove_cells(self) -> None:
        """Removes the appropriate amount of cells (self.removed_cells) from the board by setting their value to `0`. Called after board is filled.
        """
        count = 0
        while count < self.removed_cells:
            rand_row = random.randint(1,self.row_length-1)
            rand_col = random.randint(1, self.row_length-1)
            print(f"Removing cell at {rand_row}, {rand_col} value: {self.board[rand_row][rand_col]}")
            if self.board[rand_row][rand_col] != 0:
                self.board[rand_row][rand_col] = 0
                count += 1
        return







def generate_sudoku(size:int, removed:int) -> list[list[int]]:
    """
    DO NOT CHANGE
    Provided for students
    Given a number of rows and number of cells to remove, this function:
    1. creates a SudokuGenerator
    2. fills its values and saves this as the solved state
    3. removes the appropriate number of cells
    4. returns the representative 2D Python Lists of the board and solution

    Parameters:
    size is the number of rows/columns of the board (9 for this project)
    removed is the number of cells to clear (set to 0)

    Return: list[list] (a 2D Python list to represent the board)
    """
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board() # literally overwritten 2 lines later. - Joseph
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board # function description incorrect, this only returns the unsolved board. - Joseph
