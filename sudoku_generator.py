# Joseph Robinson, 4/9/2024, generator for backend of sudoku game project.

import random
import pygame
import sys
import time


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
BG_COLOR = "black" #global background color (and text on button color)
LINE_COLOR = "white" #global line color (and button color)
BORDER_COLOR = "red" #global highlighted cell color
WIDTH = 800 #global window width (in pixels)
HEIGHT = 600 #global window height (in pixels)
OUTER_BD_THICK = 15 #global sudoku outer-boundary thickness (in pixels). Like, the 3x3 squares.
INNER_BD_THICK = 9 #global sudoku gridline thickness (in pixels)
SIZE = 9 #the size (row length in cells) of the sudoku game
cell_size = (HEIGHT-4*OUTER_BD_THICK-6*INNER_BD_THICK)/9 #the pixel width of the cells


def draw_game_start(screen):
    #This function draws the start screen. Its only parameter is screen, which is the display screen.
    #Title Font init
    startTitleFont = pygame.font.Font(None, 100)#font type and size
    buttonFont = pygame.font.Font(None, 70)
    #Background Color
    screen.fill(BG_COLOR)

    #Title draw and init
    titleSurface = startTitleFont.render("Sudoku", 0, LINE_COLOR) #the title text
    titleRectangle = titleSurface.get_rect(
        center=(WIDTH//2, HEIGHT//2 - 180/600*HEIGHT)) #This is the position of the title text
    screen.blit(titleSurface, titleRectangle) #places it on the screen

    #Buttons init

    easyText = buttonFont.render("Easy", 0, (24, 122, 53))
    mediumText = buttonFont.render("Medium", 0, (184, 171, 32))
    hardText = buttonFont.render("Hard", 0, (143, 22, 22))
    quitText = buttonFont.render("Quit", 0, (0, 0, 0))

    #Sets up each button shape and color based on the text it contains.
    #easy button
    easySurface = pygame.Surface((easyText.get_size()[0]+20, easyText.get_size()[1]+20))
    easySurface.fill(LINE_COLOR)
    easySurface.blit(easyText, (10, 10))
    #medium button
    mediumSurface = pygame.Surface((mediumText.get_size()[0]+20, mediumText.get_size()[1]+20))
    mediumSurface.fill(LINE_COLOR)
    mediumSurface.blit(mediumText, (10, 10))
    #hard button
    hardSurface = pygame.Surface((hardText.get_size()[0]+20, hardText.get_size()[1]+20))
    hardSurface.fill(LINE_COLOR)
    hardSurface.blit(hardText, (10, 10))
    #quit button
    quitSurface = pygame.Surface((quitText.get_size()[0]+20, quitText.get_size()[1]+20))
    quitSurface.fill(LINE_COLOR)
    quitSurface.blit(quitText, (10, 10))
    
    #these are the positions for the buttons.
    #they are written as ratios to the globals for screen height and width.
    easyRectangle = easySurface.get_rect(
        center=(WIDTH//2, HEIGHT//2-50/600*HEIGHT))
    mediumRectangle = easySurface.get_rect(
        center=(WIDTH//2-(mediumText.get_size()[0]-easyText.get_size()[0])/2, HEIGHT//2+45/600*HEIGHT))
    hardRectangle = easySurface.get_rect(
        center=(WIDTH//2-(hardText.get_size()[0]-easyText.get_size()[0])/2, HEIGHT//2+140/600*HEIGHT))
    quitRectangle = quitSurface.get_rect(
        center=(WIDTH//2, HEIGHT//2+235/600*HEIGHT))
    
    #this places the buttons on the screen.
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
    def __init__(self, value, row, col, screen=None, mut=2):
        #Cell class
        #takes a value, row, column, screen, and mutability as parameters
        #most are self explanatory
        #everything except for screen are integers.
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.mut = mut #mutability. Cells with pre-set or non-sketch values are immutable barring reset. Any cell may still be selected.
        #mut = 2 is unsubmitted, mut = 1 is submitted, mut = 0 is preset.
        
        
    def set_cell_value(self, value):
        #When you hit enter after sketching a value to a cell. "locks" that value.
        self.value = value
        self.mut = 1
        
        
    def set_sketched_value(self, value):
        #Sketches a cell value. in main, it can't be done to a cell unless cell.mut == 2
        self.value = value
        
    def draw(self, sel):
        #takes a new attriute, sel, as a parameter
        self.sel = sel #sel is a boolean that refers to whether the cell is selected or not.

        sketchFont = pygame.font.Font(None, 30) #sketched number size
        cellFont = pygame.font.Font(None, 50) #submitted number size
        
        correction = OUTER_BD_THICK - INNER_BD_THICK #This is just a mathematical intermediate. Less clutter.
        leftBound = correction*(self.row//3+1) + INNER_BD_THICK*(self.row+1) + cell_size*self.row #left boundary for a cell
        upBound = correction*(self.col//3+1) + INNER_BD_THICK*(self.col+1) + cell_size*self.col #upper boundary for a cell

        if self.mut < 2: #if the cell is not sketchable.
            if sel == True: #if the cell is selected, it will border it in red. Otherwise, does the same thing as the other option.
                border = pygame.Surface((cell_size, cell_size)) #creates a box
                border.fill(BORDER_COLOR) #colors it red
                surface = pygame.Surface((cell_size-5, cell_size-5)) #Creates a smaller box for the digit to be written on
                surface.fill(BG_COLOR) #colors it black
                border.blit(surface,(cell_size/15, cell_size/15)) #places the black box on the red box, creating a red selection square.
                if self.value != 0:
                    text = cellFont.render(str(self.value), 0, LINE_COLOR) #the value of the cell, as text
                    border.blit(text, (cell_size/3, cell_size/4)) #places the text onto a black square (the cell)
                self.screen.blit(border, (leftBound, upBound)) #places the text, in theory.
            else: #This is if it's not selected
                surface = pygame.Surface((cell_size, cell_size)) #creates a square to cover the old digits
                surface.fill(BG_COLOR) #colors it black
                if self.value != 0:
                    text = cellFont.render(str(self.value), 0, LINE_COLOR) #the value of the cell, as text
                    surface.blit(text, (cell_size/3, cell_size/4)) #places the text onto a black square (the cell)
                self.screen.blit(surface, (leftBound, upBound)) #places the text. 
                
        elif self.mut == 2: #if the cell is sketchable. Same as above, but the number is smaller and in the upper-right corner.
            if sel == True:
                border = pygame.Surface((cell_size, cell_size))
                border.fill(BORDER_COLOR) 
                surface = pygame.Surface((cell_size-5, cell_size-5))
                surface.fill(BG_COLOR)
                border.blit(surface,(cell_size/15, cell_size/15))
                if self.value != 0:
                    text = sketchFont.render(str(self.value), 0, LINE_COLOR) #here, the font for the text is notably smaller.
                    border.blit(text, (cell_size/6, cell_size/8)) #The text is on the upper left now.
                self.screen.blit(border, (leftBound, upBound)) 
            else:
                surface = pygame.Surface((cell_size, cell_size))
                surface.fill(BG_COLOR)
                if self.value != 0:
                    text = sketchFont.render(str(self.value), 0, LINE_COLOR) #the sketched value of the cell, as text. Again, usess the smaller text.
                    surface.blit(text, (cell_size/6, cell_size/8)) #places the text onto a black square (the cell) This is small and on the upper left
                self.screen.blit(surface, (leftBound, upBound)) #places the text 

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
                    self.cells[i][j].mut = 2
                else:
                    self.cells[i][j].mut = 0

    # Draws the Sudoku grid and its cells
    # Draws an outline of the Sudoku grid and each cell on the board
    def draw(self):
        self.screen.fill(BG_COLOR)  # Fill the background
        
        i = 0
        j = OUTER_BD_THICK/2
        
        # Draw horizontal lines for the Sudoku grid
        while j < HEIGHT:
            #Basically, due to the different border sizes, there's a different formula for each section.
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
                self.cells[i][j].draw(False)  # Draw each cell and its value

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
            [Cell(self.board[i][j], i, j, cell_size, cell_size, self.screen) for j in range(self.cols)]
            for i in range(self.rows)
        ]

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
        
        for i in range(SIZE):
            for j in range(SIZE):
                temp = self.board[i][j] #placeholder for the current value due to how is_valid works
                self.board[i][j] = 0 #temporarily sets the val to zero
                if not self.sudoku.is_valid(i, j, temp): #chacks a cell for validity
                    return False #if the solution is not valid
                self.board[i][j] = temp #resets cell value to previous.
        return True #If the board solution is valid

   
    
#main definition
def main():
    restart = False
    win = False
    loss = False
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku")
    
    difficulty = draw_game_start(screen)
    screen.fill(BG_COLOR)
    pygame.display.update()
    
    boardObj = Board(SIZE, SIZE, WIDTH, HEIGHT, screen, difficulty)
    boardObj.draw()

    selRow = 0
    selCol = 0
    oldSel = [int(9),int(9)] #the old selected value. Do not try to parse b4 changing, as it is out of bounds.
    
    #Draws the buttons on the right side: Reset, Restart, Quit. Also puts a game name.
    #It functions almost identically to the 
    #game name on side
    gameTitleFont = pygame.font.Font(None, 70)
    gameButtonFont = pygame.font.Font(None, 65)
    titleSurface = gameTitleFont.render("Sudoku", 0, LINE_COLOR)
    titleRectangle = titleSurface.get_rect(center=((WIDTH-HEIGHT)/2+HEIGHT, HEIGHT*(300-180)/600))            
    screen.blit(titleSurface, titleRectangle)
    
    #Button text
    resetText = gameButtonFont.render("Reset", 0, (0,0,0))
    restartText = gameButtonFont.render("Restart", 0, (0,0,0))
    quitText = gameButtonFont.render("Quit", 0, (0,0,0))
    
    #Button buttons
    #reset button
    resetSurface = pygame.Surface((resetText.get_size()[0]+20, resetText.get_size()[1]+20))
    resetSurface.fill(LINE_COLOR)
    resetSurface.blit(resetText, (10,10))
    #restart button
    restartSurface = pygame.Surface((restartText.get_size()[0]+20, restartText.get_size()[1]+20))
    restartSurface.fill(LINE_COLOR)
    restartSurface.blit(restartText, (10,10))
    #quit button
    quitSurface = pygame.Surface((quitText.get_size()[0]+20, quitText.get_size()[1]+20))
    quitSurface.fill(LINE_COLOR)
    quitSurface.blit(quitText, (10,10))
    
    #button positioning
    resetRectangle = resetSurface.get_rect(center=((WIDTH-HEIGHT)/2+HEIGHT, HEIGHT*(300-50)/600))   
    restartRectangle = restartSurface.get_rect(center=((WIDTH-HEIGHT)/2+HEIGHT, HEIGHT*(300+45)/600))   
    quitRectangle = quitSurface.get_rect(center=((WIDTH-HEIGHT)/2+HEIGHT, HEIGHT*(300+140)/600))   
    
    #place buttons on the screen
    screen.blit(resetSurface, resetRectangle)
    screen.blit(restartSurface, restartRectangle)
    screen.blit(quitSurface, quitRectangle)
     
    pygame.display.update()

    #looped game part of main function
    while True:
        for event in pygame.event.get():
            
            #Manual quit failsafe
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
                
            
            if event.type == pygame.MOUSEBUTTONDOWN: #basically all click actions.
                #This is basically a hard-coded version of the suggested "click" function in Board.
                if int(event.pos[0]) < HEIGHT:
                    selRow = int(int(event.pos[0])//(HEIGHT/SIZE))
                    if int(event.pos[1]) < HEIGHT:
                        selCol = int(int(event.pos[1])//(HEIGHT/SIZE))       
                #selects cell clicked
                if [selRow, selCol] != oldSel:
                    #unborders old cell
                    if oldSel != [9,9]:
                        boardObj.cells[oldSel[0]][oldSel[1]].draw(False)
                    oldSel = [selRow, selCol]
                    #re-borders new cell
                    boardObj.select(selRow, selCol)
                    boardObj.cells[selRow][selCol].draw(True)
                    pygame.display.update()
                #This section is for clicking one of the three side buttons
                
                if resetRectangle.collidepoint(event.pos): #if reset is clicked
                    for i in range(SIZE):
                        for j in range(SIZE):
                            if boardObj.cells[i][j].mut != 0: #checks the mutability values of every cell to see if they are permanent (0) or not.
                                boardObj.cells[i][j].value = 0 #If one cell is mutable, resets the cell.
                                boardObj.cells[i][j].mut = 2 
                                boardObj.cells[i][j].draw(False) #redraws the cell without a selection border
                    #This redraws the board
                    boardObj.update_board()
                    pygame.display.update()
                    
                elif restartRectangle.collidepoint(event.pos): #if restart is clicked
                    restart = True #sets "restart" to true, which will later end the while True loop, causing the main function to reset.
                    
                elif quitRectangle.collidepoint(event.pos): #if quit is clicked
                    pygame.display.quit() #closes the display
                    sys.exit() #closes the application
                    
                time.sleep(0.01) #buffers inputs for stability
             
            #For all key inputs
            if event.type == pygame.KEYDOWN and oldSel == [selRow, selCol]:
                #At some point, I mixed up rows, columns, and logic. It works, so don't mess with it. Consistency > Accuracy. Just be aware when editing.
                keyInput = pygame.key.get_pressed() #records the key that's pressed
                #Movement inputs. Uses either WASD or arrow keys.
                if (keyInput[pygame.K_UP] or keyInput[pygame.K_w]) and selCol != 0: #Upwards Movement
                    selCol += -1 #changes the selected column in the direction of movement.
                    boardObj.cells[oldSel[0]][oldSel[1]].draw(False)
                    oldSel = [selRow, selCol]
                    boardObj.select(selRow, selCol)
                    # boardObj.cells[selRow][selCol].draw(True)
                elif (keyInput[pygame.K_DOWN] or keyInput[pygame.K_s]) and selCol != 8: #Downwards Movement
                    selCol += 1
                    boardObj.cells[oldSel[0]][oldSel[1]].draw(False)
                    oldSel = [selRow, selCol]
                    boardObj.select(selRow, selCol)
                    # boardObj.cells[selRow][selCol].draw(True)
                elif (keyInput[pygame.K_RIGHT] or keyInput[pygame.K_s]) and selRow != 8: #Leftwards Movement
                    selRow += 1
                    boardObj.cells[oldSel[0]][oldSel[1]].draw(False)
                    oldSel = [selRow, selCol]
                    boardObj.select(selRow, selCol)
                    # boardObj.cells[selRow][selCol].draw(True)
                elif (keyInput[pygame.K_LEFT] or keyInput[pygame.K_s]) and selRow != 0: #Rightwards Movement
                    selRow += -1
                    boardObj.cells[oldSel[0]][oldSel[1]].draw(False)
                    oldSel = [selRow, selCol]
                    boardObj.select(selRow, selCol)
                    # boardObj.cells[selRow][selCol].draw(True)
                #Number inputs. At this point, I probably should have used a switch. Oh well.
                elif (keyInput[pygame.K_1] or keyInput[pygame.K_KP1]) and boardObj.cells[selRow][selCol].mut == 2:
                    boardObj.sketch(1) #Input 1 , all others follow same logic. Reads either numpad or normal number key.
                elif (keyInput[pygame.K_2] or keyInput[pygame.K_KP2]) and boardObj.cells[selRow][selCol].mut == 2:
                    boardObj.sketch(2)
                elif (keyInput[pygame.K_3] or keyInput[pygame.K_KP3]) and boardObj.cells[selRow][selCol].mut == 2:
                    boardObj.sketch(3)
                elif (keyInput[pygame.K_4] or keyInput[pygame.K_KP4]) and boardObj.cells[selRow][selCol].mut == 2:
                    boardObj.sketch(4)
                elif (keyInput[pygame.K_5] or keyInput[pygame.K_KP5]) and boardObj.cells[selRow][selCol].mut == 2:
                    boardObj.sketch(5)
                elif (keyInput[pygame.K_6] or keyInput[pygame.K_KP6]) and boardObj.cells[selRow][selCol].mut == 2:
                    boardObj.sketch(6)
                elif (keyInput[pygame.K_7] or keyInput[pygame.K_KP7]) and boardObj.cells[selRow][selCol].mut == 2:
                    boardObj.sketch(7)
                elif (keyInput[pygame.K_8] or keyInput[pygame.K_KP8]) and boardObj.cells[selRow][selCol].mut == 2:
                    boardObj.sketch(8)
                elif (keyInput[pygame.K_9] or keyInput[pygame.K_KP9]) and boardObj.cells[selRow][selCol].mut == 2:
                    boardObj.sketch(9)
                #The Enter button, which writes the values. Reads either numpad or normal enter (return) keys
                elif (keyInput[pygame.K_RETURN] or keyInput[pygame.K_KP_ENTER]) and boardObj.cells[selRow][selCol].mut == 2:
                    boardObj.place_number(boardObj.cells[selRow][selCol].value)
                    boardObj.cells[selRow][selCol].mut = 1
                #The backspace OR delete key, which deletes the values. Reads either backspace or delete keys.
                elif(keyInput[pygame.K_BACKSPACE] or keyInput[pygame.K_DELETE]) and boardObj.cells[selRow][selCol].mut != 0:
                    boardObj.cells[selRow][selCol].value = 0
                    boardObj.cells[selRow][selCol].mut = 2
                #at the end of every loop, the stored array value for the board is updated
                boardObj.update_board()
                #Then, the image to display is updated. Technically, there can be issues with only updating the selected value.
                #To try and mitigate issues, a delay (sleep) is used further below to limit issues.
                boardObj.cells[selRow][selCol].draw(True)
                #Finally, the screen is properly updated.
                pygame.display.update()
                time.sleep(0.01) #stability buffer
        if restart: #If restart is true from the restart button, ends the while loop, effectively resetting main.
            break
        #This section checks to see if the board is fully filled.
        sumMut = 0 #This value is the sum of cells.mut values. If it is equal to the missing cells, where mut = 1 is the minimum non-prefilled cell mut value, then the board is filled.
        for i in range(SIZE):
            for j in range(SIZE):
                sumMut += int(boardObj.cells[i][j].mut) #sums mutability values
        if sumMut == int(difficulty):
            if boardObj.check_board(): #this checks the current board to see if it is valid. If it is, you win. If not, you lose.
                win = True
            else:
                loss = True
            break #ends the loop after setting win or loss to true. Instead of skipping to the beginning of main, it gets stuck in a new loop for the win/loss screen.
            
    if win or loss: #this stays the same, regardless of win or loss (but one must be true). Baseline for the win/loss screen.
        #Background Color
        screen.fill(BG_COLOR)
        #Font
        wlButtonFont = pygame.font.Font(None, 70)
        #button text
        restartText = wlButtonFont.render("Restart", 0, (0,0,0))
        #restart button creation
        restartSurface = pygame.Surface((restartText.get_size()[0]+20, restartText.get_size()[1]+20))
        restartSurface.fill(LINE_COLOR)
        restartSurface.blit(restartText, (10,10))
        #restart button position
        restartRectangle = restartSurface.get_rect(center=(WIDTH/2, (300+235)/600*HEIGHT))
        #place restart button
        screen.blit(restartSurface, restartRectangle)
    if win: #win text
        #Fonts
        winTitleFont = pygame.font.Font(None, 120)

        #Text placement
        titleSurface = winTitleFont.render("YOU WON!!!!!", 0, LINE_COLOR)
        titleRectangle = titleSurface.get_rect(center =(WIDTH/2,HEIGHT*(300-180)/600))
        screen.blit(titleSurface, titleRectangle)
    elif loss: #loss text 
        #Fonts
        lossTitleFont = pygame.font.Font(None, 120)
        #text placement
        titleSurface = lossTitleFont.render("You Lost....", 0, LINE_COLOR)
        titleRectangle = titleSurface.get_rect(center =(WIDTH/2,HEIGHT*(300-180)/600))
        screen.blit(titleSurface, titleRectangle)
    pygame.display.update() #updates the screen.

    while True: #looping for the win/loss screen. Basically, keeps the screen there until restart is hit.
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Manual quit failsafe
                pygame.display.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: #basically all click actions.
                if restartRectangle.collidepoint(event.pos): #if restart is clicked
                    restart = True #sets "restart" to true, which will later end the while True loop, causing the main function to reset.
        if restart: #If restart is true from the restart button, ends the while loop, effectively resetting main.
            break
    
#main here
if __name__ == "__main__":
    while True:
        main()
