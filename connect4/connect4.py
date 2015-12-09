def make_board():
  """
  create a connect4 board. It is represented as a list of lists
  with each inner list containing the elements in a row. The blank spaces
  are represented with *. A connect4 board is 6 X 7
  @returns: a connect4 board.
  """
  board = []
  for row_index in range(6): #for each row in the board
    row = ['*'] * 7 #it should be empty and 7 wide
    board.append(row) #add in the row
  return board

def display_board(board):
  """
  display the given board. 
  @board: a list of lists of characters.
  @returns: None
  """
  for (row_num,row) in enumerate(board): #for each row
    print(5 - row_num, ' '.join(row)) #print it out the row header and each element with | in between
  print(' ', end = '') #display some white space for alignment purposes
  #display the column headers
  for col_num in range(len(board[0])):
    print('', col_num, end = '')
  print()

def is_gameover(board):
  """
  checks if the game is over
  @board: a list of lists of characters.
  @returns: true if the game is over and false otherwise
  """
  return won(board) or tie(board)

def won(board):
  """
  check if someone wone the game
  @board: a list of lists of characters.
  @returns: true if someone won the game and false otherwise
  """
  return (row_win(board) or
          col_win(board) or
          diag_win(board))

def row_win(board):
  """
  check if there is a win in a row
  @board: a list of lists of characters.
  @returns: true if there is a row win and false otherwise
  """
  for row in board: #for each row in the board
      for i in range(len(row)-3):
          if row[i] != "*":
             if (row[i] == row[i+1]) and (row[i] == row[i+2]) and (row[i] == row[i+3]):
                 return True
  else:
      return False

def col_win(board):
  """
  check if there is a win in a column
  @board: a list of lists of characters.
  @returns: true if there is a column win and false otherwise
  """
  for col_index in range(len(board[0])): #for each column
    for i in range(len(board) - 3):
        if board[5-i][col_index] != "*":
            if (board[5-i][col_index] == board[4-i][col_index]) and (board[5-i][col_index] == board[3-i][col_index]) and (board[5-i][col_index] == board[2-i][col_index]):
                return True
  else:
      return False


def diag_win(board):
  """
  check if there is a win in a diagonal
  @board: a list of lists of characters.
  @returns: true if there is a diagnoal win and false otherwise
  """
  return left_diag_win(board) or right_diag_win(board)


def left_diag_win(board):
  """
  check if there is a win in from the bottom left corner to the upper right
  There are several conditions to consider
  @board: a list of lists of characters.
  @returns: true if there is a win in from the bottom left corner to the upper right
  """
  if (board[2][0] != "*")and (board[2][0] == board[3][1]) and (board[2][0] == board[4][2]) and (board[2][0] == board[5][3]):
      return True
  for i in range(2):
      if (board[1+i][i]  != "*")and(board[1+i][i] == board[2+i][1+i]) and (board[1+i][i] == board[3+i][2+i]) and (board[1+i][i] == board[4+i][3+i]):
          return True
  for i in range(3):
      if (board[i][i] != "*")and(board[i][i] == board[i+1][1+i]) and (board[i][i] == board[i+2][2+i]) and (board[i][i] == board[3+i][3+i]):
          return True
  for i in range(3):
      if (board[i][1+i] != "*")and(board[i][1+i] == board[i+1][i+2]) and (board[i][1+i] == board[i+2][i+3]) and (board[i][1+i] == board[i+3][i+4]):
          return True
  for i in range(2):
      if (board[i][2+i] != "*")and(board[i][2+i] == board[i+1][i+3]) and (board[i][2+i] == board[i+2][i+4]) and (board[i][2+i] == board[i+3][i+5]):
          return True
  if (board[0][3] != "*")and(board[0][3] == board[1][4]) and (board[0][3] == board[2][1]) and (board[0][3]== board[3][6]):
      return True
  else:
      return False

def right_diag_win(board):
  """
  check if there is a win in from the bottom right corner to the upper left
  Similar with the left_diag_win
  @board: a list of lists of characters.
  @returns: true if there is a win in from the bottom right corner to the upper left
  """
  if (board[3][0] != "*") and (board[3][0] == board[2][1]) and (board[3][0] == board[1][2]) and (board[3][0] == board[0][3]):
      return True
  for i in range(2):
      if (board[4-i][i] != "*") and(board[4-i][i] == board[3-i][1+i]) and (board[4-i][i] == board[2-i][2+i]) and (board[4-i][i] == board[1-i][3+i]):
          return True
  for i in range(3):
      if (board[5-i][i] != "*") and(board[5-i][i] == board[4-i][1+i]) and (board[5-i][i] == board[3-i][2+i]) and (board[5-i][i] == board[2-i][3+i]):
          return True
  for i in range(3):
      if (board[5-i][i+1] != "*") and(board[5-i][i+1] == board[4-i][i+2]) and (board[5-i][i+1]  == board[3-i][3+i]) and (board[5-i][i+1]  == board[2-i][4+i]):
          return True
  for i in range(2):
      if (board[5-i][i+2] != "*") and(board[5-i][i+2] == board[4-i][i+3]) and (board[5-i][i+2] == board[3-i][4+i]) and (board[5-i][i+2] == board[2-i][5+i]):
          return True
  if (board[5][3] != "*") and(board[5][3] == board[4][4]) and (board[5][3] == board[3][5]) and (board[5][3] == board[2][6]):
      return True
  else:
      return False

def tie(board):
  """
  checks if there is a tie. 
  @returns: True if the game is a tie and False otherwise
  """

  if won(board): #can't tie if you won
    return False

  for row in board: #for every row in the board
    for piece in row: #for every piece in the board
      if piece == '*': #if there is a blank space
        return False #the game isn't tied
  return True


def is_valid_int(integer):
  """
  checks to see if number represents a valid integer
  @number: a string that might represent an integer
  @returns: true if the string represents an integer
  """
  integer = integer.strip()
  if len(integer) == 0:
    return False
  else:
    return (integer.isdigit() or #only digits
            #or a negative sign followed by digits
            (integer.startswith('-') and integer[1:].isdigit()))

def is_valid_move(str_move, board):
  """
  check if the move is valid on the given board
  @str_move: the potential move. should be row column
  @board: a list of lists of characters.
  @returns: True if the move is valid and False otherswise
  """
  if len(str_move) != 1:
    return False
  elif (is_valid_int(str_move) and (int(str_move[0]) in range(7)) and board[0][int(str_move)] == '*'):
    return True
  else:
    return False


def get_move(player, board):
  """
  get a valid move from the player
  @player: a string representing the current player
  @board: the board
  @returns: a valid move, which is a the following tuple (row, col)
  """
  
  move = '' #make the move start as wrong so that we always go into the while loop
  while not is_valid_move(move, board): #while the input is invalid
    move = input('%s please enter a move: ' % player) #keep asking for input

  #turn to integers
  col = int(move)	
  return col

def make_move(piece, move, board):
  for i in range(5,-1,-1):
      if board[i][move] == "*":
         board[i][move] = piece
         break
      else:
          continue

def connect4():
  """
  play a game of connect4
  return None
  """

  board = make_board()
  turn = 0 #if turn is 0 it is X's turn and if it is 1 it is O's turn
  XO = 'XO'

  while not is_gameover(board): #keep playing the game until it is over
    display_board(board)
    move = get_move(XO[turn], board)
    make_move(XO[turn], move, board)
    turn = (turn + 1) % 2 #change the turn

  #game is now over

  #display the board one last time
  display_board(board)
  
  #and declare a winner
  if tie(board):
    print('The game ended in a tie.')
  elif turn == 0:
    print('O won the game.')
  else:
    print('X won the game.')
  
connect4()
