class Board:

# initialise the board and the turn variable
    def __init__(self):
        # board
        # for letter represents the color of the piece
        # second letter represents the type of piece
        # "XX" represents empty squares
        self.board = [["BR", "BN", "BB", "BQ", "BK", "BB", "BN", "BR"],
                      ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
                      ["XX", "XX", "XX", "XX", "XX", "XX", "XX", "XX"],
                      ["XX", "XX", "XX", "XX", "XX", "XX", "XX", "XX"],
                      ["XX", "XX", "XX", "XX", "XX", "XX", "XX", "XX"],
                      ["XX", "XX", "XX", "XX", "XX", "XX", "XX", "XX"],
                      ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"],
                      ["WR", "WN", "WB", "WQ", "WK", "WB", "WN", "WR"]]

        # current player: -1 for white, 1 for black
        # -1 for white because the white pawn moves upward, (i.e) array index reduces.
        # 1 for black because the black pawn moves downward (i.e) array index increases.

        self.currPlayer = -1
        self.blackOrWhite = {-1: "W", 1: "B"}

        self.last_move_double = False
        self.last_double = []
        self.en_passant = False

# Function to display the Board
    def display(self):
        print("-" * 41)

        # display the board
        for i in self.board:
            for j in i:
                print("|", j, end=" ")
            print("|")

        print("-" * 41)
        return

# Function to find the location of the king
    def find_king_position(self, color):
        print(color)
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == color + "K":
                    return [i, j]

# Function to make a move and check if it results in a check
    def make_and_check(self, cell, move):
        temp = [] + self.board
        print(self.board[cell[0]][cell[1]])
        color = self.board[cell[0]][cell[1]][0]

        self.board[move[0]][move[1]] = self.board[cell[0]][cell[1]]
        self.board[cell[0]][cell[1]] = "XX"

        king_position = self.find_king_position(color)
        if color != "X":
            if self.check_check(king_position):
                self.board = [] + temp
                return False
            else:
                self.board = [] + temp
                return True
        return True


# Function to find all possible pawn moves (except en passant)
    def check_pawn_moves(self, moveset, cell):

        # Check which way the pawn moves, determined by whether its black or white
        inc = -1
        if self.board[cell[0]][cell[1]][0] == "B":
            inc *= -1

        color = self.blackOrWhite[inc]

        # check if the pawn is free to move one step forward
        if cell[0] + inc < 8 and self.board[cell[0] + inc][cell[1]] == "XX":
            moveset.append([cell[0] + inc, cell[1]])

        # check if the pawn can capture left of the board
        if cell[1] > 0 and self.board[cell[0] + inc][cell[1] - 1][0] == self.blackOrWhite[-inc]:
            moveset.append([cell[0] + inc, cell[1] - 1])

        # check if the pawn can capture right of the board
        if cell[1] < 7 and self.board[cell[0] + inc][cell[1] + 1][0] == self.blackOrWhite[-inc]:
            moveset.append([cell[0] + inc, cell[1] + 1])

        # check for possibility of moving two steps
        if cell[0] == (7 + inc) % 7 and self.board[cell[0] + inc + inc][cell[1]] == "XX":
            moveset.append([cell[0] + inc + inc, cell[1]])

        return

# Function to check for possible en passant
    def check_en_passant(self, moveset, cell):

        # Check which way the pawn moves, determined by whether its black or white
        inc = -1
        if self.board[cell[0]][cell[1]][0] == "B":
            inc *= -1

        if self.last_move_double:
            if (cell[1] - self.last_double[1]) ** 2 == 1:
                if cell[0] == self.last_double[0]:
                    moveset.append(cell[0] + inc)
                    moveset.append(self.last_double[1])

        return

# Function to find all possible knight moves
    def check_knight_moves(self, moveset, cell):

        # color of knight does not affect possible moves, only position does
        # However, we still need to color to know which piece it can capture and where it cant go
        vals = {0, 1, 2, 3, 4, 5, 6, 7}
        piece_color = self.board[cell[0]][cell[1]][0]
        for x, y in [[1, 2], [2, 1]]:
            if cell[0] - x in vals and cell[1] - y in vals and self.board[cell[0] - x][cell[1] - y][0] != piece_color:
                moveset.append([cell[0] - x, cell[1] - y])
            if cell[0] - x in vals and cell[1] + y in vals and self.board[cell[0] - x][cell[1] + y][0] != piece_color:
                moveset.append([cell[0] - x, cell[1] + y])
            if cell[0] + x in vals and cell[1] - y in vals and self.board[cell[0] + x][cell[1] - y][0] != piece_color:
                moveset.append([cell[0] + x, cell[1] - y])
            if cell[0] + x in vals and cell[1] + y in vals and self.board[cell[0] + x][cell[1] + y][0] != piece_color:
                moveset.append([cell[0] + x, cell[1] + y])

        return

# Function to find all possible Bishop moves
    def check_bishop_moves(self, moveset, cell):

        curr_piece = self.board[cell[0]][cell[1]]
        available_range = range(8)

        for i, j in [[1, 1], [1, -1], [-1, 1], [-1, -1]]:
            for x in range(1, 8):
                cx, cy = cell[0] + (x * i), cell[1] + (x * j)
                if cx not in available_range or cy not in available_range:
                    break
                possible_move = self.board[cx][cy]
                if possible_move[0] != curr_piece[0]:
                    moveset.append([cx, cy])
                else:
                    break

        return

# Function to find all possible Rook moves
    def check_rook_moves(self, moveset, cell):

        for x, y in [cell]:

            curr_piece = self.board[x][y]

            for i in range(x + 1, 8):
                if self.board[i][y][0] != curr_piece[0]:
                    moveset.append([i, y])
                else:
                    break

            for i in range(x - 1, -1, -1):
                if self.board[i][y][0] != curr_piece[0]:
                    moveset.append([i, y])
                else:
                    break

            for j in range(y + 1, 8):
                if self.board[x][j][0] != curr_piece[0]:
                    moveset.append([x, j])
                else:
                    break

            for j in range(y-1, -1, -1):
                if self.board[x][j][0] != curr_piece[0]:
                    moveset.append([x, j])
                else:
                    break

            return

# Function to find all possible Queen moves
    def check_queen_moves(self, moveset, cell):

        self.check_rook_moves(moveset, cell)
        self.check_bishop_moves(moveset, cell)

        return

# Function to find all possible King moves
    def check_king_moves(self, moveset, cell):

        set_2 = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
        for i in [1, -1]:
            set_2.append([0, i])
            set_2.append([i, 0])

        for x, y in [cell]:

            curr_piece = self.board[x][y]
            vals = {0, 1, 2, 3, 4, 5, 6, 7}

            for i, j in set_2:
                if ((x + i) in vals) and ((y + j) in vals) and self.board[x + i][y + j][0] != curr_piece[0]:
                    temp = [] + self.board

                    self.board[x + i][y + j] = curr_piece
                    self.board[x][y] = "XX"

                    if not self.check_check([x + i, y + j]):
                        moveset.append([x + i, y + j])
                    self.board[x + i][y + j] = "XX"
                    self.board[x][y] = curr_piece

        return

# Function to check  if said king is under check
    def check_check(self, cell):
        print(cell)
        color = self.board[cell[0]][cell[1]][0]
        invalid = color + "X"
        for i in range(8):
            for j in range(8):
                if self.board[i][j][0] not in invalid:
                    moveset = []
                    match self.board[i][j][1]:
                        case "P":
                            self.check_pawn_moves(moveset, [i, j])
                        case "N":
                            self.check_knight_moves(moveset, [i, j])
                        case "B":
                            self.check_bishop_moves(moveset, [i, j])
                        case "R":
                            self.check_rook_moves(moveset, [i, j])
                        case "Q":
                            self.check_queen_moves(moveset, [i, j])

                    if self.board[i][j][1] != "P":
                        if cell in moveset:
                            return True
                    else:
                        new_moveset = [i for i in moveset if i[1] != cell[1]]
                        if cell in new_moveset:
                            return True

        set_2 = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
        for i in [1, -1]:
            set_2.append([0, i])
            set_2.append([i, 0])

        enemy_king = "K"
        if color == "B":
            enemy_king = "W" + enemy_king
        else:
            enemy_king = "B" + enemy_king

        vals = {1, 2, 3, 4, 5, 6, 7, 0}

        for x, y in [cell]:
            for i, j in set_2:
                if x + i in vals and y + j in vals and self.board[x + i][y + j] == enemy_king:
                    return True

        return False

    def checkmate(self):
        return False

    def stalemate(self):
        return False

    def game_over(self):
        if self.checkmate() or self.stalemate():
            return True
        return False

# Function to make a move
    def move(self, cell):

        # check if selected square has a piece that can be moved

        curr_piece = self.board[cell[0]][cell[1]]
        if curr_piece == "XX":
            print("Invalid Cell")
            return
        if curr_piece[0] != self.blackOrWhite[self.currPlayer]:
            print("Invalid Color")
            return

        # check all valid squares the piece can be moved
        valid_moves = []

        if curr_piece[1] == "P":
            self.check_pawn_moves(valid_moves, cell)

            en_passant = []
            if self.last_move_double:
                self.check_en_passant(en_passant, cell)

            # to check for check by exposure for every possible move
            final_moves = []
            for i in valid_moves:
                if self.make_and_check(cell, i):
                    final_moves.append(i)

            valid_moves = [] + final_moves

            print("Possible Moves: ", end="")

            if en_passant != []:
                print(valid_moves + [en_passant])
            else:
                print(valid_moves)

            intended_move = input("Enter square to move to: ")

            intended_move = [int(intended_move[0]), int(intended_move[1])]

            if intended_move not in valid_moves:
                if intended_move == en_passant:
                    self.board[intended_move[0]][intended_move[1]] = self.board[cell[0]][cell[1]]
                    self.board[cell[0]][cell[1]] = "XX"
                    self.board[self.last_double[0]][self.last_double[1]] = "XX"

                    self.last_move_double = False
                    self.currPlayer *= -1
                else:
                    print("Invalid Move")
                return

            self.board[intended_move[0]][intended_move[1]] = curr_piece
            self.board[cell[0]][cell[1]] = "XX"

            if intended_move[0] in {0, 7}:
                promotion_to = input("Choose what to promote the piece to: \n1. Knight\n2. Bishop\n3. Rook\n4. Queen")
                match promotion_to:
                    case "1":
                        self.board[intended_move[0]][intended_move[1]] = self.board[intended_move[0]][intended_move[1]][0] + "K"
                    case "2":
                        self.board[intended_move[0]][intended_move[1]] = self.board[intended_move[0]][intended_move[1]][0] + "B"
                    case "3":
                        self.board[intended_move[0]][intended_move[1]] = self.board[intended_move[0]][intended_move[1]][0] + "R"
                    case _:
                        self.board[intended_move[0]][intended_move[1]] = self.board[intended_move[0]][intended_move[1]][0] + "Q"

            self.last_move_double = False

            if (intended_move[0] - cell[0]) ** 2 == 4:
                self.last_move_double = True
                self.last_double = [] + intended_move

            self.currPlayer *= -1

            return

        match curr_piece[1]:
            case "N":
                self.check_knight_moves(valid_moves, cell)
            case "B":
                self.check_bishop_moves(valid_moves, cell)
            case "R":
                self.check_rook_moves(valid_moves, cell)
            case "Q":
                self.check_queen_moves(valid_moves, cell)
            case "K":
                self.check_king_moves(valid_moves, cell)

        # to check for check by exposure for every possible move
        final_moves = []
        for i in valid_moves:
            if self.make_and_check(cell, i):
                final_moves.append(i)

        valid_moves = [] + final_moves

        print("Possible Moves: ", end="")
        print(valid_moves)

        intended_move = input("Enter square to move to: ")

        intended_move = [int(intended_move[0]), int(intended_move[1])]

        if intended_move not in valid_moves:
            print("Invalid move")
            return

        self.board[intended_move[0]][intended_move[1]] = curr_piece
        self.board[cell[0]][cell[1]] = "XX"

        self.last_move_double = False

        self.currPlayer *= -1

        return
