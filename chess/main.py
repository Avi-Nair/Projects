import board_functions

"""Tasks To do

    Checkmate checking function
    Stalemate checking function
    Check for possible check by exposure after every move
"""
"""Continuous Tasks
    
    Add comments to make the code readable 
"""

""" Tasks Done

    Basic Pawn Moves
    Pawn Captures
    Board Initialisation
    Move choice, which squares, which pieces
    Move & Capture
    Outline of the Program
    Display function
    Turn change mechanism
    Check knight moves
    Check Bishop Moves
    Check Rook Moves
    Check Queen Moves
    Check King Moves
    Pawn Promotion mechanism
    Check for Check mechanism
    En passant mechanism
"""


if __name__ == '__main__':
    board = board_functions.Board()
    board.display()

    while not board.game_over():
        selected_square = input("Choose a cell: ")

        # Error handling for invalid input
        for i in selected_square:
            if not i.isnumeric() and int(i) not in range(8):
                selected_square = input("Choose a valid square: ")

        selected_square = [int(selected_square[0]), int(selected_square[1])]

        board.move(selected_square)

        board.display()
