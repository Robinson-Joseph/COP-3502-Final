# Joseph Robinson, 4/9/2024, generator for backend of sudoku game project.

import random
import pygame
import sys
import numpy as np


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
            #print(f"Removing cell at {rand_row}, {rand_col} value: {self.board[rand_row][rand_col]}")
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


#Visual stuff starts 
#These are globals. Do not modify unless necessary.
BG_COLOR = "black"
LINE_COLOR = "white"
WIDTH = 800
HEIGHT = 600
OUTER_BD_THICK = 15
INNER_BD_THICK = 9
SIZE = 9 #size of the sudoku game
cell_size = (HEIGHT-4*OUTER_BD_THICK-6*INNER_BD_THICK)/9


def draw_game_start(screen):
    #Title Font init
    startTitleFont = pygame.font.Font(None, 100)
    buttonFont = pygame.font.Font(None, 70)
    #Background Color
    screen.fill(BG_COLOR)

    #Title draw and init
    titleSurface = startTitleFont.render("Sudoku", 0, LINE_COLOR)
    titleRectangle = titleSurface.get_rect(
        center=(WIDTH//2, HEIGHT//2 - 180/600*HEIGHT))
    screen.blit(titleSurface, titleRectangle)

    #Buttons init

    easyText = buttonFont.render("Easy", 0, (24, 122, 53))
    mediumText = buttonFont.render("Medium", 0, (184, 171, 32))
    hardText = buttonFont.render("Hard", 0, (143, 22, 22))
    quitText = buttonFont.render("Quit", 0, (0, 0, 0))

    easySurface = pygame.Surface((easyText.get_size()[0]+20, easyText.get_size()[1]+20))
    easySurface.fill(LINE_COLOR)
    easySurface.blit(easyText, (10, 10))
    mediumSurface = pygame.Surface((mediumText.get_size()[0]+20, mediumText.get_size()[1]+20))
    mediumSurface.fill(LINE_COLOR)
    mediumSurface.blit(mediumText, (10, 10))
    hardSurface = pygame.Surface((hardText.get_size()[0]+20, hardText.get_size()[1]+20))
    hardSurface.fill(LINE_COLOR)
    hardSurface.blit(hardText, (10, 10))
    quitSurface = pygame.Surface((quitText.get_size()[0]+20, quitText.get_size()[1]+20))
    quitSurface.fill(LINE_COLOR)
    quitSurface.blit(quitText, (10, 10))

    easyRectangle = easySurface.get_rect(
        center=(WIDTH//2, HEIGHT//2-50/600*HEIGHT))
    mediumRectangle = easySurface.get_rect(
        center=(WIDTH//2-(mediumText.get_size()[0]-easyText.get_size()[0])/2, HEIGHT//2+45/600*HEIGHT))
    hardRectangle = easySurface.get_rect(
        center=(WIDTH//2-(hardText.get_size()[0]-easyText.get_size()[0])/2, HEIGHT//2+140/600*HEIGHT))
    quitRectangle = quitSurface.get_rect(
        center=(WIDTH//2, HEIGHT//2+235/600*HEIGHT))

    screen.blit(easySurface, easyRectangle)
    screen.blit(mediumSurface, mediumRectangle)
    screen.blit(hardSurface, hardRectangle)
    screen.blit(quitSurface, quitRectangle)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit() #for some reason, display.quit is necessary. sys.exit won't close the window, and doing so will crash.
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easyRectangle.collidepoint(event.pos): #if mouse is on easy button and clicking
                    return 30 #goes back to main
                elif mediumRectangle.collidepoint(event.pos): #medium select
                    return 40
                elif hardRectangle.collidepoint(event.pos): #hard select
                    return 50
                elif quitRectangle.collidepoint(event.pos): #if mouse is on quit button and clicking
                    pygame.display.quit()
                    sys.exit() #take a wild guess
        pygame.display.update()

#Cell Class
class Cell:
    def __init__(self, value, row, col, screen=None, mut=True):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.mut = mut #mutability. Cells with pre-set or non-sketch values are immutable barring reset. Any cell may still be selected.
        
        
    def set_cell_value(self, value):
        self.value = value
        self.mut = False
        
        
    def set_sketched_value(self, value):
        self.value = value
        
    def draw(self):
        correction = OUTER_BD_THICK-INNER_BD_THICK #The difference between outer and inner borders. Math reasons.
        leftBound = (self.row%9+1)*INNER_BD_THICK+(self.row%3+1)*correction+(self.row%9)*cell_size+1 #left boundary of a given cell, starting on first white space
        rightBound = leftBound+cell_size-1 #same as above, on the right
        upBound = (self.col%9+1)*INNER_BD_THICK+(self.col%3+1)*correction+(self.col%9)*cell_size+1 #upper bound
        downBound = upBound+cell_size-1 #lower bound
        sketchFont = pygame.font.Font(None, 30) #sketched number size, will be changed
        cellFont = pygame.font.Font(None, 50) #submitted number size, will be changed
        
        correction = OUTER_BD_THICK - INNER_BD_THICK
        leftBound = correction*(self.row//3+1) + INNER_BD_THICK*(self.row+1) + cell_size*self.row
        upBound = correction*(self.col//3+1) + INNER_BD_THICK*(self.col+1) + cell_size*self.col
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     pygame.draw.lines(screen, 'red', True, [(leftBound, upBound), (rightBound, upBound), (rightBound, downBound), (leftBound, downBound)]) #draws a red box on the boundary of the cell
        if self.value != 0:
            if self.mut == False:
                text = cellFont.render(str(self.value), 0, LINE_COLOR) #the value of the cell, as text
                surface = pygame.Surface((cell_size, cell_size)) #creates a square to cover the old digits
                surface.fill(BG_COLOR) #makes it black
                surface.blit(text, (cell_size/3, cell_size/4)) #places the text onto a black square (the cell)
                self.screen.blit(surface, (leftBound, upBound)) #places the text, in theory. Can't verify easily tbh. 
            elif self.mut == True:
                text = sketchFont.render(str(self.value), 0, LINE_COLOR) #the sketched value of the cell, as text
                surface = pygame.Surface((cell_size, cell_size)) #creates a square to cover the old digits
                surface.fill(BG_COLOR) #makes it black
                surface.blit(text, (cell_size/2, cell_size/2)) #places the text onto a black square (the cell) This is small and on the upper left, ideally
                self.screen.blit(text, (leftBound, upBound)) #places the text 

#Board Class
class Board:
    # Constructor for the Board class to initialize the Sudoku board
    def __init__(self, rows, cols, width, height, screen, difficulty):
        self.row = 0
        self.col = 0
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.screen = screen  # The PyGame window to draw on
        self.difficulty = difficulty  # Difficulty level for the Sudoku puzzle

        # Create and set up the Sudoku board
        self.sudoku = SudokuGenerator(SIZE, removed_cells=difficulty)
        self.sudoku.fill_values()  # Fill the Sudoku with complete numbers
        self.sudoku.remove_cells()  # Remove cells to create a puzzle

        # Get the underlying 2D array representation of the board
        self.board = self.sudoku.get_board()

        # Calculate the cell size based on the grid dimensions
        #cell_size = self.width // self.cols

        # Create a 2D array of Cell objects for the board
        self.cells = [
            [Cell(self.board[i][j], i, j, screen) for j in range(cols)]
            for i in range(rows)
        ]
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cells[i][j].value == 0:
                    self.cells[i][j].mut = True
                else:
                    self.cells[i][j].mut = False

    # Draws the Sudoku grid and its cells
    # Draws an outline of the Sudoku grid and each cell on the board
    def draw(self):
        self.screen.fill(BG_COLOR)  # Fill the background
        
        i = 0
        j = OUTER_BD_THICK/2
        
        # Draw horizontal lines for the Sudoku grid
        while j < HEIGHT:
            lineStart = 0, j
            lineEnd = HEIGHT-1, j
            if i%3 == 0:
                pygame.draw.line(self.screen, LINE_COLOR, lineStart, lineEnd, OUTER_BD_THICK)
                j = j + cell_size + (OUTER_BD_THICK+INNER_BD_THICK)/2
            elif i%3 == 1:
                pygame.draw.line(self.screen, LINE_COLOR, lineStart, lineEnd, INNER_BD_THICK)
                j = j + cell_size + INNER_BD_THICK
            else:
                pygame.draw.line(self.screen, LINE_COLOR, lineStart, lineEnd, INNER_BD_THICK)
                j = j + cell_size + (OUTER_BD_THICK+INNER_BD_THICK)/2
            i += 1
            
        i = 0
        j = OUTER_BD_THICK/2
        
        # Draw vertical lines for the Sudoku grid
        while j < HEIGHT:
            lineStart = j, 0
            lineEnd = j, HEIGHT-1
            if i%3 == 0:
                pygame.draw.line(self.screen, LINE_COLOR, lineStart, lineEnd, OUTER_BD_THICK)
                j = j + cell_size + (OUTER_BD_THICK+INNER_BD_THICK)/2
            elif i%3 == 1:
                pygame.draw.line(self.screen, LINE_COLOR, lineStart, lineEnd, INNER_BD_THICK)
                j = j + cell_size + INNER_BD_THICK
            else:
                pygame.draw.line(self.screen, LINE_COLOR, lineStart, lineEnd, INNER_BD_THICK)
                j = j + cell_size + (OUTER_BD_THICK+INNER_BD_THICK)/2
            i += 1

        # Draw the cells on the Sudoku board
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].draw()  # Draw each cell and its value

    # Selects a specific cell on the board
    def select(self, row, col):
        # Update the selected row and column if the cell is empty
        if self.board[row][col] == 0:
            self.row = row
            self.col = col

    # Click detection to convert x, y coordinates to board indices
    def click(self, x, y):
        if y < cell_size * self.cols:
            # Calculate row and column based on x, y
            row = y // cell_size
            col = x // cell_size
            return row, col
        return None

    # Clears the value of the selected cell
    def clear(self):
        # Clear only if the cell isn't predefined
        if self.board[self.row][self.col] == 0:
            self.cells[self.row][self.col].set_cell_value(0)
            self.cells[self.row][self.col].set_sketched_value(0)

    # Sketches a value in the selected cell
    def sketch(self, value):
        self.cells[self.row][self.col].set_sketched_value(value)

    # Sets the value of the selected cell
    def place_number(self, value):
        self.cells[self.row][self.col].set_cell_value(value)

    # Resets the Sudoku board to its original state
    def reset_to_original(self):
        self.cells = [
            [Cell(self.board[i][j], i, j, cell_size, cell_size, screen) for j in range(self.cols)]
            for i in range(self.rows)
        ]
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cells[i][j].value == 0:
                    self.cells[i][j].mut = True
                else:
                    self.cells[i][j].mut = False

    # Checks if the Sudoku board is fully filled
    def is_full(self):
        # Return True if all cells have a non-zero value
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    # Updates the underlying 2D Sudoku board with current cell values
    def update_board(self):
        # Synchronize the board with the cells' current values
        for i in range(self.rows):
            for j in range(self.cols):
                self.board[i][j] = self.cells[i][j].value

    # Finds the first empty cell on the Sudoku board
    def find_empty(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cells[i][j].value == 0:
                    return (i, j)
        return None

    # Checks whether the Sudoku board is solved correctly
    def check_board(self):
        # Create a string representation of the current Sudoku board
        current_board = ''.join(str(self.board[i][j]) for i in range(self.rows) for j in range(self.cols))

        # Compare with the solution from SudokuGenerator
        return self.sudoku.solution == current_board


#main here
if __name__ == "__main__":
    gameOver = False
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku")
    
    difficulty = draw_game_start(screen)
    screen.fill(BG_COLOR)
    pygame.display.update()
    
    boardObj = Board(SIZE, SIZE, WIDTH, HEIGHT, screen, difficulty)
    print(boardObj.board)
    boardObj.draw()
    pygame.display.update()
    #looped game part of main function
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()

