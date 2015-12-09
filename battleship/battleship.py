#implementing a one player version of battleship that allows the user to play against an AI.

#import the sys and random modules
import sys
import random

def make_board(row, col):
  """
  create a battleship board. It is represented as a list of lists
  with each inner list containing the elements in a row. The blank spaces
  are represented with *. A tic tac toe board is row * col
  @returns: a battleship board.
  """
  board = []
  for row_index in range(row): #for each row in the board
    row = ['*'] * col #it should be empty and col wide
    board.append(row) #add in the row
  return board

def display_board(board):
  """
  display the given board. 
  @board: a list of lists of characters.
  @returns: None
  """
  print(' '*2, end = '')
  for i in range(len(board[0])):
        print(i, end = ' ') #print the number of col
  print()#for an another line
  for i, row in enumerate(board):
      print(i, end = ' ') #print the number of the row
      for j in row:
          print(j, end = ' ') #print the board
      print()

def get_input():
    """
    It is the step of set up, get the input that we needed in the program
    there are five variables that we get: seed, the width of the board, the height of the board
    the content in the file and hte number of AI that we choose to dispaly
    :return:a list of the five input
    """
    seed = ""
    #Seed needs to be an integer
    while not (seed.isdigit() or (seed.startswith('-') and seed[1:].isdigit())):
        seed = input("Enter the seed: ") #get the seed
        seed = seed.strip()
    seed = int(seed) #turn the seed to be int

    width = ""
    #The width of the board: An integer greater than 0
    while not (width.isdigit() and int(width) > 0):
        width = input("Enter the width of the board: ") #get the width
        width = width.strip()
    width = int(width)#turn the width to be int

    height = ""
    #The height of the board: An integer greater than 0
    while not (height.isdigit() and int(height) > 0):
        height = input("Enter the height of the board: ")
        height = height.strip()
    height = int(height)

    file = input("Enter the name of the file containing your ship placements: ")
    file = file.strip()
    #The name of the file containing the user's ship placements
    with open(file, "r") as fl: #open the file
        content = fl.readlines()
        
    AI = ""   
    while not (AI.isdigit() and 0 < int(AI) < 4):
        print("Choose your AI.\n1. Random\n2. Smart\n3. Cheater")
        AI = input(" Your choice: ").strip()
    AI = int(AI)

    return [seed, width, height, content, AI]

def find_ship(content):
    """
    get the information in the file
    :param content: the content in the file
    :return: a list which contents five list: symbol, row1, col1, row2, col2
    """
    symbol = []; row1 = []; col1 =[]; row2 = []; col2 = [] #initializa the five paramether
    for i in range(len(content)):
        contentlist = content[i].split() #split the content with space to be a list
        symbol.append(contentlist[0]) #the fist one is the symbol
        row1.append(int(contentlist[1])) #add row1_index
        col1.append(int(contentlist[2])) #add column1_index
        row2.append(int(contentlist[3])) #add row2_index
        col2.append(int(contentlist[4])) #add column2_index
    return [symbol, row1, col1, row2, col2]


def check_ship_construct(symbol, row1, col1, row2, col2, width, height):
    """
    check all ship palcement files whether it is be structured correctly
    :param symbol:Symbol_for_ship
    :param row1:row1_index
    :param col1:column1_index
    :param row2:row2_index
    :param col2:column2_index
    :param width: the width of the board
    :param height: the height of the board
    :return: if the ship placement files all correctly constructed, it will return the board: otherwise it will exit
    """
    for sy in symbol:
        if sy in ["x", "X", "o", "O", "*"]:#user choose either x,X, o, O, or * as those are symbols
            print("Symbol of ship cannot be %s. Terminating game."%sy)
            #If the user violated any of the above constraints, an appropriate message should be displayed to the screen and the program should terminate
            sys.exit(0)
        if symbol.count(sy) > 1:
            print("Error symbol %s is already in use. Terminating game"%sy)
            sys.exit(0)

    #user placed all of their ships on the board
    for i in range(len(row1)):
        if max(row1[i], row2[i]) > height or max(col1[i], col2[i]) > width or min(row1[i], row2[i]) < 0 or min(col1[i], col2[i]) < 0:
            print("Error %s is placed outside of the board. Terminating game." %symbol[i])
            sys.exit(0)

    #user did not try to place their ships diagonally
    for i in range(len(row1)):
        if (row1[i] != row2[i] and col1[i] != col2[i]):
            print('Ships cannot be placed diagonally. Terminating game.')
            sys.exit(0)


    #user did not place their ships on top of each other
    board = [['*' for i in range(width)] for i in range(height)]
    for i in range(len(symbol)):
        if(row1[i] == row2[i]):#if the ship displays horizontal
            for j in range(abs(col1[i]-col2[i]) + 1):#get the size of the ship
                if board[row1[i]][j + min(col1[i], col2[i])] != '*': #means there is already a ship
                    print('There is already a ship at location %d, %d. Terminating game.' %(row1[i], j + min(col1[i], col2[i])))
                    sys.exit(0)
                else: #there is not a ship that at the top of the other, so the board can have that display that ship
                    board[row1[i]][j + min(col1[i], col2[i])] = symbol[i]
        else:#if the ship displays not horizontal
            for j in range(abs(row1[i]-row2[i]) + 1):
                if board[j + min(row1[i], row2[i])][col1[i]] != '*':
                    print('There is already a ship at location %d, %d. Terminating game.' %(row1[i], j + min(col1[i], col2[i])))
                    sys.exit(0)
                else:#else place the symbol in the board
                    board[j + min(row1[i], row2[i])][col1[i]] = symbol[i]

    return board        
            

def check_AI_construct(symbol, row1, col1, row2, col2, width, height):
    """
    check the AI play and construct the AI board
    The AI will have the same ships that the user has but will position its ships randomly throughout the board
    :param symbol: the symbol of the ship that in the content
    :param row1, col1, row2, col2: the position of the ship
    :param width: the input width of the board
    :param height: the input height of the board
    :return:the AI board
    """
    board = [['*' for i in range(width)] for i in range(height)] #initailized the board
    for i in range(len(symbol)):
        while True:
            direct = random.choice(["vert","horz"]) #The AI should first select a direction for the ship they wish to place, either vertical or horizontal
            #get the size of the ship
            if(row1[i] == row2[i]): #if the number of row is the same then calculate the col number which is the size of the ship
                size = abs(col1[i]-col2[i]) + 1
            else: #if they have the same col number, calculate the row
                size = abs(row1[i]-row2[i]) + 1
                
            if direct == "vert":
                #select a valid starting point based on the direction vertical
                start_row = random.randint(0, height - size)
                start_col = random.randint(0, width - 1)
               
                for j in range(size):
                    #check whether it is overlap
                    if board[start_row + j][start_col] != "*": #means the position is not valid to place the ship. so get out of the while loop
                        break
                else: #means all the positions are valid to place a ship
                    for k in range(start_row, start_row + size):
                        board[k][start_col] = symbol[i]               
                    print('Placing ship from %d,%d to %d,%d.' %(start_row, start_col, start_row + size - 1, start_col))
                    break
            if direct == "horz":#means if the direction is horizontal
                start_row = random.randint(0, height - 1) #get the start points
                start_col = random.randint(0, width - size)
                #check whether it is overlap
                for j in range(size):
                    if board[start_row][start_col + j] != "*":
                        break 
                else:#means all the positions are valid to place a ship
                    for k in range(start_col, start_col + size):
                        board[start_row][k] = symbol[i]#put the symbol to the corresponding position
                    print('Placing ship from %d,%d to %d,%d.' %(start_row, start_col, start_row, start_col + size - 1))
                    break
    return board

#fire
def check_firelocation(inputfire, width, height, board):
    """
    check the fire place whether it is valid
    :param inputfire: the position to input the fire
    :param width: the input width of the board
    :param height: the input height of the board
    :param board: board to check the corresponding place whether it is valid
    :return: True or False; if the place is valid, return True, otherwise, return False
    """
    inputfire = inputfire.strip().split() #get rid of the spaces in front and last, then split by the sapce
    if (len(inputfire) != 2): #if there are
        return False
    if (inputfire[0].isdigit() and inputfire[1].isdigit()): #if the input are not all be to the number
        inputrow = int(inputfire[0])
        inputcol = int(inputfire[1])
    else:
        return False
    if (inputrow >= height or inputcol >= width): #input out of the board
        return False
    if (board[inputrow][inputcol]) in ["x", "X", "o", "O"]:#overlap
        return False

    return True


def fire(inputfire, width, height, board):
    """
    get the file place
    :param inputfire: the position to input the fire
    :param width: the input width of the board
    :param height: the input height of the board
    :param board: board to check the corresponding place whether it is valid
    :return: the valid fire place
    """
    while not check_firelocation(inputfire, width, height, board):
        #if the file location is not valid
        inputfire = input("Enter row and column to fire on separated by a space: ") #input again
    inputfire = inputfire.strip().split() #make the valid input to be an list, the list element is the row, the second element is the col
    return(int(inputfire[0]), int(inputfire[1]))
  
#AI play
def RandomAI(board):
    """
    This AI randomly chooses a location to fire upon that it hasn't fired upon before
    :param board: the board that the random AI plays
    :return:a list, the first is the fire place, the second is the location that no fire
    """
    width = len(board[0]) #get the width of the board
    height = len(board) #get the height of the board
    locUnfire = [] #initialized the unfire place
    for i in range(height):
        for j in range(width):
            if board[i][j] not in ["x", "X", "o", "O"]: #get the unfire places
                locUnfire.append([i, j])
    fire_place = random.choice(locUnfire) #random choose an unfire place
    locUnfire.remove(fire_place)
    return [fire_place, locUnfire]

def SmarterAI(board, checklist, firelist):
    """
    Display the smart AI. The Smarter AI has 2 modes: Hunt and Destroy
    In Hunt mode the AI behaves like the Random AI
    In Destroy mode the AI fires above, below, to the left of, then to the
    right of the location it hit, excluding spaces it has already checked.
    :param board: the board to display the samrt AI
    :param checklist: in the Destroy mode, the positions can be choose to fire
    :param firelist: the list of the positions that are fired before
    :return:a list. The first element is the checklist, the second element is the fire place
    """
    #In Hunt mode the AI behaves like the Random AI in that it randomly chooses a location to fire upon that it hasn't fired upon before
    if checklist == []:
        fire_place = RandomAI(board)[0]
    else: #in the Destroy mode
        fire_place = checklist.pop(0)

    #get the fire place
    firerow = fire_place[0]
    firecol = fire_place[1]
    firelist.append(fire_place) #add the fire place in the firelist
    newlist = firelist + checklist #after the fire, the new list to be check whether the position has been fired before
    if board[firerow][firecol] not in ["x", "X", "o", "O","*"]:#means hit
        #in the conditions below, I check whether the left and to the right of the hit and the top to below of the hit can be added to the checklist
        #check the left postion
        if ((firerow-1 >= 0) and ([firerow - 1, firecol] not in newlist)):
            checklist.append([firerow - 1, firecol])
        #check the right position
        if ((firerow+1 < len(board)) and ([firerow + 1, firecol] not in newlist)):
            checklist.append([firerow + 1, firecol])
        #check the position below the hit position
        if ((firecol - 1 >=0) and ([firerow, firecol - 1] not in newlist)):
            checklist.append([firerow , firecol - 1])
        #check the position above the hit position
        if ((firecol+ 1 < len(board[0])) and ([firerow, firecol+1] not in newlist)):
            checklist.append([firerow, firecol+1])
    return [checklist, fire_place]
    
    
def CheatAI(user_board):
    """
    This AI cheats and uses the location of the player ships to play a perfect game.
    :param user_board: the user board used to cheat
    :return: the position to fire
    """
    width = len(user_board[0])#get the width of the board
    height = len(user_board)#get the height of the board
    #for all elements in the board
    for i in range(height):
        for j in range(width):
            if user_board[i][j] not in ["*", "x", "X"]: #there is a ship in the position user_board[i][j]
                return[i,j]

def Dboard(board):
    """
    check whether the board is destroyed
    :param board: the board to be check whether it is destroyed
    :return: True if the board is destroyed, otherwise return False
    """
    #for all the element in the board
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] not in ["x", "X", "o", "O", "*"]:#means there are still positions that not be hit
                return True #the board is not destroyed
    return False

def notdestroy(uboard, AIboard):
  """
  check if someone win the game: either the user board or the AI board are been destroyed.
  @board: a list of lists of characters.
  @returns: true if someone won the game and false otherwise
  """
  return (Dboard(uboard) and
          Dboard(AIboard))


def check_hit(board, row, col):
    """
    check whether the position is hit or missed
    :param board: the board to be check
    :param row: the row number of the position
    :param col: the column number of the position
    :return: a list, the first element is whether the position is hit, the second one the the board after hit
    """
    #If the location does contain an opposing ship a hit is announced unless that is the last hit on the ship
    # then it is announced that you destroyed that ship
    if board[row][col] != "*":
        symbol = board[row][col]
        board[row][col] = 'X'#Hits are marked with X
        sink = "False" #check whether the ship sinks
        hit = "True" #check whether get the hit or miss
        for i in range(len(board)):
            for j in range(len(board[0])):
                if (board[i][j] == symbol and sink == "False"):
                    print("Hit!") #means you get the hit position
                    sink = "True" #the ship did not get sinks 
        if sink == "False":#the ship sinks
            print("You sunk my %s"%symbol)
    else:
        hit = "False" #If the location does not contain an opposing ship a miss is announced
        board[row][col] = "O" #Misses are marked with O
        print("Miss!")
    return[hit, board]
                


   
def main():
    """
    the main function to implemente a one player version of battleship game
    :return:None
    """
    #Setup
    #get the seed, width, height, content, AInum
    seed, width, height, content, AInum = get_input()
    initialboard = make_board(height, width) #get the initial board
    #initialize the other element that we need to paly the game
    checklist = [] #the list of positions for ship to choose
    firedlist = [] #the list of fired position
    #the unfired position
    locUnfire = []
    for i in range(height):
        for j in range(width):
            locUnfire.append([i,j])
    random.seed(seed)#Seed the random number generator with the provided seed

    #according to the content in the input, get the user board information
    usymbol, urow1, ucol1, urow2, ucol2 = find_ship(content)
    uboard = check_ship_construct(usymbol, urow1, ucol1, urow2, ucol2, width, height)
    #The AI should place ships in sorted order based on the symbol used for each ship
    content.sort()
    #construct the AI board
    AIsymbol, AIrow1, AIcol1, AIrow2, AIcol2 = find_ship(content)
    # the ship does not overlap with any other ships it should be placed at the chosen
    #location and the location should be printed out
    AIboard = check_AI_construct(AIsymbol, AIrow1, AIcol1, AIrow2, AIcol2, width, height)

    #The player and the AI alternate taking turns until one of them has destroyed all of their opponents ships
    turn  = random.randint(0,1)
    #if either of the two ship are distroyed
    while (notdestroy(uboard, AIboard)):
        if turn == 0: #If 0 is selected the player goes first.
            #Displaying the state of the game
            print("Scanning Board")
            display_board(initialboard)
            print()
            print("My Board")
            display_board(uboard)
            inputfire = input('Enter row and column to fire on separated by a space: ').strip() #get the move postion
            fireplace = fire(inputfire, width, height, AIboard) #check whether the position can be fired and return the valid fired postion
            #get the row and column of the fired place
            row = fireplace[0]
            col = fireplace[1]

            checkresult = check_hit(AIboard, row, col)#check whether the fired position is hit or miss
            if checkresult[0] == "True": #means get hit
                initialboard[row][col] = "X" #if get hit the initialboard should be palced "X"
            else:
                initialboard[row][col] = "O" #not get hit, so placed "O"
        else:#AI plays
            #the AInum is the result of input in the get_input() function
            if AInum == 1:
                AIfire = RandomAI(uboard)[0]
            if AInum == 2:
                AIfire = SmarterAI(uboard, checklist, firedlist)[1]
            if AInum == 3:
                AIfire = CheatAI(uboard)
            print('The AI fires at location (%d, %d)' %(AIfire[0],AIfire[1]))
            uboard = check_hit(uboard, AIfire[0], AIfire[1])[1] #use the useboard to check whether it is hit

        turn = (turn + 1)%2 #turn the other one to play

    #after one board is destoryed, show the two board
    print("Scanning Board")
    display_board(initialboard)
    print()
    print("My Board")
    display_board(uboard)

    #Declaring a winner after the game is over
    if turn == 0:
        print("The AI wins.")
    if turn == 1:
        print("You win!")


#paly the battleship game
if __name__ == '__main__':
  main()
















    
