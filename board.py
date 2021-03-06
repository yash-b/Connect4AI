"""
FALL 2019 CPSC 481 Artificial Intelligence Project
File Description: board.py
    Class representing the gamme board

Authors:
    Nathaniel Richards
    Yash Bhambani
    Matthew Camarena
    Dustin Vuong

"""

import pygame
import slot as sl
'''
board contains 6 rows and 7 columns 
(5,0) (5,1) .. .. (5,6)
..                 ..
..                 ..
(1,0)
(0,0) (0,1) .. .. (0,6)

'''
class Board:
    
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        # Board images (background, buttons)
        self.background = pygame.image.load("outline.png")    # might be used for the background?
        self.rect = self.background.get_rect() 
        self.select_button = pygame.image.load("button.png")
        self.select_button = pygame.transform.scale(self.select_button, (96, 92))
        self.red_select_button = pygame.image.load("button-red.png")
        self.red_select_button = pygame.transform.scale(self.red_select_button, (96, 92))
        self.clear_select_button = pygame.image.load("clear_select_button.png")
        self.clear_select_button= pygame.transform.scale(self.clear_select_button, (96, 92))
        self.winhigh = pygame.image.load("win-star.png")
        self.winhigh= pygame.transform.scale(self.winhigh, (96, 92))
        #dimensions and grid                       
        rows = 6
        columns = 7
        pygame.mixer.init()
        pygame.mixer.music.load("images/background-music.wav")
        self.grid = [ [sl.Slot(self.screen) for c in range(columns)] for r in range(rows)] 

        self.button_position = 0 # 0-6 column of where button is
        self.rows_position = [0, 0, 0, 0, 0, 0, 0] # 0-5 row of where coin on 7 columns
        self.debug_mode = 0
        self.define_slot_positions()
        self.turn = "red"
        self.move_count = 0
        self.oppGrid = [0,0,0,0,0,0,0]
        self.optMoveRow = 0
        self.optMoveCol = 0

    def define_slot_positions(self):
        for i in range(6):
            for j in range(7):
                self.grid[i][j].set_slot_position((100*j)+6,(500-100*i+50)+6)
    
    def reset_game(self):
        #print("reset game")
        self.reset_slots()
        self.rows_position = [0, 0, 0, 0, 0, 0, 0]
        self.button_position = 0
        self.move_count = 0
        self.turn="red"

    def change_selector_color(self, color):
        if color is "yellow":
            self.screen.blit(self.select_button,(self.button_position*100,-25))
        else:
            self.screen.blit(self.red_select_button,(self.button_position*100,-25))
        pygame.display.update()

    def reset_slots(self):
        #print("reset slots")
        for i in range(6):
            for j in range(7):
                self.grid[i][j].reset()

    def change_turn(self):
        if self.turn is "red":
            self.turn = "yellow"
        else:
            self.turn = "red"

        self.change_selector_color(self.turn)

    # loads board slots, defines slots, and places select button
    def load_board(self):
        if self.debug_mode:
            print("Loading board.")
        for i in range(7):
            for j in range(6):
                self.screen.blit(self.background,(100*i,100*j+50))
        #loading selector Button 
        self.screen.blit(self.red_select_button,(self.button_position,-25))
        pygame.mixer.music.play(-1)

    # Checks if there is an available space on the column
    def check_valid_move(self):
        if self.debug_mode:
            print("Checking valid move")
        if self.rows_position[self.button_position] < 6:
            if self.debug_mode:                    
                print("Space to place!")
            return True
        else:
            if self.debug_mode:
                print("This column is full.")
            return False

    # places a chip in the column then updates the rows position
    def move(self):
        #print("in move: " + str(self.button_position))
        # need to check valid move before moving
        self.move_count = self.move_count + 1
        #print("trying to move: " + str(self.button_position) + str(self.rows_position[self.button_position]))
        slot = self.grid[self.rows_position[self.button_position]][self.button_position]
        slot.change_state(self.turn)
        slot.blit()
        self.rows_position[self.button_position] += 1
        #print(str(self.move_count))

    # select button with checks on bounds
    def move_select_button(self,direction):
        # Valid move Clear last button --> update position --> place new button
        
        self.screen.blit(self.clear_select_button,(self.button_position*100,-25))
        if direction is "right":
            if self.button_position < 6:    self.button_position += 1      
            else:
                if(self.debug_mode):    print("You've hit the right wall! Try moving left! button_position: " + str(self.button_position))
        elif direction is "left":
            if self.button_position > 0:    self.button_position -= 1
            else:
                if(self.debug_mode):    print("You've hit the left wall! Try moving right! button_position: " + str(self.button_position))
        if self.turn is "red":
            self.screen.blit(self.red_select_button,(self.button_position*100,-25)) 
        else:
            self.screen.blit(self.select_button,(self.button_position*100,-25))

    def reset_select_button(self):
        for i in range(7):
            self.screen.blit(self.clear_select_button,(i*100,-25))
    # check the board to win (theres an easier way to do this) from last move?
    def check_win(self): # fix the turn = self.turn later
        # check for 4 UP 
        turn = self.turn
        for i in range(3):
            for j in range(7):
                if self.grid[i][j].state is not "black":
                    if self.grid[i][j].state is turn:
                        if self.grid[i+1][j].state is turn and self.grid[i+2][j].state is turn and  self.grid[i+3][j].state is turn:
                            print(str(turn) + " wins up")
                            # highlight win spaces
                            self.screen.blit(self.winhigh,self.grid[i][j].rect)
                            self.screen.blit(self.winhigh,self.grid[i+1][j].rect)
                            self.screen.blit(self.winhigh,self.grid[i+2][j].rect)
                            self.screen.blit(self.winhigh,self.grid[i+3][j].rect)
                            pygame.display.update()
                            return True
        #check 4 across 
        for i in range(6):
            for j in range(4):
                if self.grid[i][j].state is not "black":
                    if self.grid[i][j].state is turn:
                        if self.grid[i][j+1].state is turn and self.grid[i][j+2].state is turn and  self.grid[i][j+3].state is turn:
                            print(str(turn) + " wins across")
                            # highlight win spaces
                            self.screen.blit(self.winhigh,self.grid[i][j].rect)
                            self.screen.blit(self.winhigh,self.grid[i][j+1].rect)
                            self.screen.blit(self.winhigh,self.grid[i][j+2].rect)
                            self.screen.blit(self.winhigh,self.grid[i][j+3].rect)
                            pygame.display.update()
                            return True
                            
       # check diagnoal to the right
        for i in range(3):
            for j in range(4):
                if self.grid[i][j].state is not "black":
                    if self.grid[i][j].state is turn:
                        if self.grid[i+1][j+1].state is turn and self.grid[i+2][j+2].state is turn and  self.grid[i+3][j+3].state is turn:
                            print(str(turn) + " wins diag right")
                            # highlight win spaces
                            self.screen.blit(self.winhigh,self.grid[i][j].rect)
                            self.screen.blit(self.winhigh,self.grid[i+1][j+1].rect)
                            self.screen.blit(self.winhigh,self.grid[i+2][j+2].rect)
                            self.screen.blit(self.winhigh,self.grid[i+3][j+3].rect)  
                            pygame.display.update()
                            return True                   
        
        # check diagnol to the left
        for i in range(3):
            for j in range(4):
                if self.grid[5-i][j].state is not "black":
                    if self.grid[5-i][j].state is turn:
                        if self.grid[5-i-1][j+1].state is turn and self.grid[5-i-2][j+2].state is turn and  self.grid[5-i-3][j+3].state is turn:
                            print(str(turn) + " wins diag left")
                            # highlight win spaces
                            self.screen.blit(self.winhigh,self.grid[5-i][j].rect)
                            self.screen.blit(self.winhigh,self.grid[5-i-1][j+1].rect)
                            self.screen.blit(self.winhigh,self.grid[5-i-2][j+2].rect)
                            self.screen.blit(self.winhigh,self.grid[5-i-3][j+3].rect)
                            pygame.display.update()
                            return True
        return False

    def ifValidCol(self, col):
        return self.grid[6 - 1][col].state == "black"

    def gameFinished(self):
        if (self.move_count == 42 or len(self.getValidLocations()) == 0) :
            return True
        return False
    def getValidLocations(self):
        validCol = []
        for i in range(7):
            if self.ifValidCol(i):
                validCol.append(i)
        return validCol

    def obtainNextAvailRow(self, col):
        for i in range(6):
            if self.grid[i][col].state == "black":
                # print("i: " + str(i))
                return i

    def score_position(self, board):
        score = 0

        # score center column
        centerCount = 0
        # print("Current Turn: " + str(self.turn))
        centerAr = []
        for i in range(6):
            centerAr.append(self.grid[i][3].state)
            if (self.grid[i][3].state == self.turn):
                centerCount += 1
            else:
                pass
        score += centerCount * 3

        # print(centerAr)
        # print("Amount of pieces in Central Column: " + str(centerCount) + ": Score: " + str(score))

        for r in range(6):
            row_array = []
            for c in range(7):
                row_array.append(board.grid[r][c].state)
            for c in range(4):  #
                window = row_array[c:c + 4]
                score += self.evaluate_window(window, board.turn)
        # print("Score of Horizontal " + self.turn + ":" + str(score))

        # score vertical
        for c in range(7):  # Row_count - 3
            col_array = []
            for r in range(6):
                col_array.append(board.grid[r][c].state)
            # print(col_array)
            # print("Column: " + str(c))
            for r in range(3):  # Column count  - 3
                window = col_array[r:r + 4]
                # print("Turn:" + str(board.turn))
                # print("Added Score: " + str(self.evaluate_window(window, board.turn)))
                score += self.evaluate_window(window, board.turn)
        # print("Score:" + str(score))
        # print("Score of Vertical " + self.turn + ":" + str(score))

        for r in range(3):  # Rowcount - 3
            for c in range(4):
                window = [board.grid[r + i][c + i].state for i in range(4)]
                score += self.evaluate_window(window, board.turn)
        # print("Score of Positive Diagonals " + self.turn + ":" + str(score))
        #
        for r in range(3):
            for c in range(4):
                window = [board.grid[r + 3 - i][c + i].state for i in range(4)]
                score += self.evaluate_window(window, board.turn)
        # print("Score of Negative Diagonals " + self.turn + ":" + str(score))
        # print("Score in Score_Position: " + str(score))
        return score

    def evaluate_window(self, window, piece):
        score = 0
        piece = self.turn
        self.change_turn()
        opp_piece = self.turn
        self.change_turn()
        accum = 0
        selfPiece = 0
        oppPiece = 0

        for i in range(len(window)):
            if (window[i] == 'black'):
                accum += 1
            if (window[i] == piece):
                selfPiece += 1
            if(window[i] == opp_piece):
                oppPiece += 1
        # print("AI: " + str(selfPiece))
        # print("Player: " + str(oppPiece))

        if selfPiece == 4:
            score += 1000
        elif selfPiece == 3 and accum == 1:
            score += 5
        elif selfPiece == 2 and accum == 2:
            score += 2
        if oppPiece == 3 and accum == 1:
            score -= 1000
        # print("Score of " + self.turn + ":" + str(score))
        # print("Score: " + str(score))
        # print("Score at Evaluate Window: " + str(score))
        return score


    def optimalMove(self, turn):
        availableLocations = self.getValidLocations()
        bestVal = -1000000
        bestCol = 0
        for i in range(availableLocations):
            r = self.obtainNextAvailRow(i)
            selfCopy = self.copy()
            selfCopy.grid[r][i].state = self.turn
            val = self.score_position(selfCopy, self.turn)
            if val > bestVal:
                val = bestVal
                bestCol = i
        return bestCol

    def ai_check_win(self): # fix the turn = self.turn later
        # check for 4 UP
        turn = self.turn
        for i in range(3):
            for j in range(7):
                if self.grid[i][j].state is not "black":
                    if self.grid[i][j].state is turn:
                        if self.grid[i+1][j].state is turn and self.grid[i+2][j].state is turn and  self.grid[i+3][j].state is turn:
                            print(str(turn) + " wins up")

                            return True
            # check 4 across
        for i in range(6):
            for j in range(4):
                if self.grid[i][j].state is not "black":
                    if self.grid[i][j].state is turn:
                        if self.grid[i][j + 1].state is turn and self.grid[i][j + 2].state is turn and self.grid[i][
                            j + 3].state is turn:
                            print(str(turn) + " wins across")
                            # highlight win spaces

                            return True

                # check diagnoal to the right
        for i in range(3):
            for j in range(4):
                if self.grid[i][j].state is not "black":
                    if self.grid[i][j].state is turn:
                        if self.grid[i + 1][j + 1].state is turn and self.grid[i + 2][j + 2].state is turn and \
                                self.grid[i + 3][j + 3].state is turn:
                            print(str(turn) + " wins diag right")
                            # highlight win spaces

                            return True

                            # check diagnol to the left
        for i in range(3):
            for j in range(4):
                if self.grid[5 - i][j].state is not "black":
                    if self.grid[5 - i][j].state is turn:
                        if self.grid[5 - i - 1][j + 1].state is turn and self.grid[5 - i - 2][
                            j + 2].state is turn and self.grid[5 - i - 3][j + 3].state is turn:
                            print(str(turn) + " wins diag left")
                            # highlight win spaces

                            return True
        return False


