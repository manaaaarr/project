# GUI for othello boards
from tkinter import *  # <-- Use Tkinter

# Constants for colors
BLACK = 1
WHITE = 2

is_listening = False
valid_moves = []
cur_color = None
board_size = 8
canvas = None
root = Tk()
valid_move = None
waitVar = IntVar()


def init(board):
    global board_size, canvas
    board_size = len(board)

    # Start canvas initialization
    root.title("Othello")  # Your screen size may be different from 1270 x 780.
    frame = Frame(root, width=200, height=200)
    frame.pack(expand=True, fill=BOTH)  # .grid(row=0,column=0)
    canvas = Canvas(frame, bg='#FFFFFF', width=200, height=200)
    hbar = Scrollbar(frame, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=canvas.xview)
    vbar = Scrollbar(frame, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=canvas.yview)
    canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    canvas.pack(side=LEFT, expand=True, fill=BOTH)

    # Create board in canvas
    canvas.create_rectangle(0, 0, 75 * board_size, 75 * board_size,
                              width=1, fill='DARKGREEN')
    for i in range(1, board_size):  # draw vertical lines
        canvas.create_line(75 * i, 0, 75 * i, 75 * board_size, width=2, fill='BLACK')
    for i in range(1, board_size):  # draw horizontal lines
        canvas.create_line(0, 75 * i, 75 * board_size, 75 * i, width=2, fill='BLACK')

    points = canvas.bbox("all")
    canvas.config(width=points[2]-points[0], height=points[3]-points[1])
    canvas.config(scrollregion=canvas.bbox("all"))
    root.bind('<Button-1>', click)  # 1 = LEFT  mouse button.
    root.bind('<Button-3>', click)  # 3 = RIGHT mouse button.
    root.call('wm', 'attributes', '.', '-topmost', True)



def refresh_board(board, valid_moves, color):
    global cur_color
    cur_color = color  #current color

    move_coords = [valid_move["coordinate"] for valid_move in valid_moves]
    for i in range(board_size):
        for j in range(board_size):
            sx = j * 75 + 37.5
            sy = i * 75 + 37.5
            if board[i][j] == BLACK:
                canvas.create_oval(sx - 25, sy - 25, sx + 25, sy + 25, fill='BLACK')
            elif board[i][j] == WHITE:
                canvas.create_oval(sx - 25, sy - 25, sx + 25, sy + 25, fill='WHITE')
            elif (i, j) in move_coords:
                if cur_color == BLACK:
                    color = "#151"
                else:
                    color = "#4b4"
                canvas.create_oval(sx - 25, sy - 25, sx + 25, sy + 25, fill=color)
            else:
                canvas.create_rectangle(sx - 30, sy - 30, sx + 30, sy + 30, width=0, fill='DARKGREEN')

    canvas.update()


def click(evt):
    global is_listening, valid_move
    if not is_listening:
        return

    move_coords = [move["coordinate"] for move in valid_moves]
    i = evt.y // 75
    j = evt.x // 75
    if (i, j) in move_coords:
        valid_move = valid_moves[move_coords.index((i, j))]
    else:
        return

    # Done listening
    is_listening = False #no action
    waitVar.set(1) #first action waiting
    return


def start_listening(moves, color):
    global is_listening, valid_moves, cur_color
    is_listening = True
    valid_moves = moves
    cur_color = color


def get_choice():
    canvas.wait_variable(waitVar)
    return valid_move
