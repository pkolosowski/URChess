#!/usr/bin/env pypy
# -*- coding: utf-8 -*-

from __future__ import print_function
from Utils import *
from Position import Position
import time, re, sys
from Motion_Detection import MotionDetection
import random
from GUI import GUI
import Camera

if sys.version_info[0] == 2:
    input = raw_input

def parse(c):

    fil, rank = ord(c[0]) - ord('a'), int(c[1]) - 1
    return A1 + fil - 10*rank


def render(i):

    rank, fil = divmod(i - A1, 10)
    return chr(fil + ord('a')) + str(-rank + 1)


def print_pos(pos):

    print()
    uni_pieces = {'R':'♜', 'N':'♞', 'B':'♝', 'Q':'♛', 'K':'♚', 'P':'♟',
                  'r':'♖', 'n':'♘', 'b':'♗', 'q':'♕', 'k':'♔', 'p':'♙', '.':'·'}
    for i, row in enumerate(pos.board.split()):
        print(' ', 8-i, ' '.join(uni_pieces.get(p, p) for p in row))
    print('    a b c d e f g h \n\n')


def check_capture(board, position):


    row = ord(position[1]) - 48
    column = ord(position[0]) - 97 + 1
    row = 110 - 20 - 10*(row-1)

    if board[row+column] != '.':
        return True
    else:
        return False


def check_enpassant(board, move1s, move2s):

    pos1 = parse(move1s)
    pos2 = parse(move2s)

    print(pos1, pos2)
    if board[pos2] == '.' and move1s[0] != move2s[0] and (board[pos1] == 'p' or board[pos1] == 'P'):
        return True
    else:
        return False

def check_mate(hist, searcher):

    result = True
    hist_fake = [Position(hist[-1][0], 0, (True, True), (True, True), 0, 0)]
    legal_moves = sorted(hist_fake[-1].gen_moves())
    start = time.time()
    for mov in legal_moves:
        hist_fake = [Position(hist[-1][0], 0, (True, True), (True, True), 0, 0)]
        hist_fake.append(hist_fake[-1].move(mov))
        for _depth, move, score in searcher.search(hist_fake[-1], hist_fake):
            if time.time() - start > 1:
                break
        if move != None:
            if hist_fake[-1][0][move[1]] != 'k':
                result = False

    return result


def execute_mate_move(hist, chessboard, s, script, transform, turn):

    mate_move = hist[-1][0].find('K')
    if turn == "green":
        mate_move = render(mate_move)
    if turn == "red":
        mate_move = render(119-mate_move)

    time.sleep(10)
    exit()
    coords = chessboard[mate_move]
    move = transform.coords_conversion((coords[0], coords[1]))
    script.execute(script, move, "checkmate")
    s.close()

def calculate_move(searcher, hist):

    move = None
    start = time.time()
    for _depth, move, score in searcher.search(hist[-1], hist):
        if time.time() - start > 1:
            break

    return move

def input_move(hist, turn):

    move = None

    while move not in hist[-1].gen_moves():
        match = re.match('([a-h][1-8])' * 2, input('Your move: '))
        if match:
            if turn == "green":
                move = parse(match.group(1)), parse(match.group(2))
            if turn == "red":
                move = 119 - parse(match.group(1)), 119 - parse(match.group(2))
            print(move)
            time.sleep(1)
        else:
            print("Please enter a move like g8f6")

    return move

def vision_move(hist, player_color,chessboard):

    motion_detection = MotionDetection()
    move = motion_detection.motion_detection(hist[-1][0], player_color,chessboard)
    if player_color == 'green':
        move = parse(move[0:2]), parse(move[2:4])
    if player_color == 'red':
        move = 119 - parse(move[0:2]), 119 - parse(move[2:4])
    if move not in hist[-1].gen_moves():
        print("You made an illegal move!")

    return move


def execute_move(move1s, move2s, chessboard, transform_UR, script, board, graveyard, move_1, move_2, move1rot='', move2rot=''):

    delay = 1

    if move1rot == "e8" and (move2rot == "g8" or move2rot == "c8"): #castle moves

        print("castle")
        if move2rot == "g8":
            move3 = chessboard["h8"]
            move4 = chessboard["f8"]
        if move2rot == "c8":
            move3 = chessboard["a8"]
            move4 = chessboard["d8"]

        move_3 = transform_UR.coords_conversion((move3[0], move3[1]))
        move_4 = transform_UR.coords_conversion((move4[0], move4[1]))
        script.execute(script, [move_1, move_2, move_3, move_4], "castle")
        time.sleep(1)

    elif move1s == "e1" and (move2s == "g1" or move2s == "c1"):

        print("castle")
        if move2s == "g1":
            move3 = chessboard["h1"]
            move4 = chessboard["f1"]
        if move2s == "c1":
            move3 = chessboard["a1"]
            move4 = chessboard["d1"]

        move_3 = transform_UR.coords_conversion((move3[0], move3[1]))
        move_4 = transform_UR.coords_conversion((move4[0], move4[1]))
        script.execute(script, [move_1, move_2, move_3, move_4], "castle")
        time.sleep(1)

    elif move2s != '' and check_capture(board, move2s):

        print("CAPTURE")
        script.execute(script, [move_2, graveyard, move_1, move_2], "capture")
        time.sleep(1)

    elif check_enpassant(board, move1s, move2s):

        print("EN PASSANT")
        move_0 = move2s[0] + move1s[1]
        move_0 = chessboard[move_0]
        move_0 = transform_UR.coords_conversion((move_0[0], move_0[1]))
        script.execute(script, [move_0, graveyard, move_1, move_2], "en_passant")
        time.sleep(1)

    else:

        print("NORMAL")
        script.execute(script, [move_1, move_2], "normal")
        time.sleep(1)


def save_game(hist): #save state of the game to the text file

    with open("Chessboard_State.txt", "w") as text_file:
        text_file.write(hist[-1][0])

def get_opening():


    openings = ["Grunfeld_Defence.txt",
                "Italian_Game.txt",
                "Queens_Indian_Defence.txt",
                "Scotch_Game.txt",
                "London_System.txt"]

    opening = openings[random.randint(0, 4)]
    opening_moves = []

    with open("Openings/" + opening, 'r') as myfile:
        for line in myfile:
            opening_moves.append(line.rstrip())

    print("Opening: " + opening[0:len(opening) - 4])

    return opening_moves

def get_gui_setup():

    gui = GUI()
    gui.draw()

    game_mode = gui.game_modes[gui.var2.get()][1]
    online_game = gui.online_offline[gui.var1.get()][0]
    load_new = gui.load_new[gui.var3.get()][0]
    player_side = gui.color[gui.var4.get()][0]
    manipulator = gui.robots[gui.var5.get()][0]

    ur1_ip = gui.content.get()
    ur2_ip = gui.content2.get()
    ur1_port = gui.content3.get()
    ur2_port = gui.content4.get()
    initial = gui.chessboard

    game_params = {"game_mode": game_mode,
                   "online_game": online_game,
                   "player_side": player_side,
                   "load_new": load_new,
                   "manipulator": manipulator,
                   "ur1_ip": ur1_ip,
                   "ur2_ip": ur2_ip,
                   "ur1_port": int(ur1_port),
                   "ur2_port": int(ur2_port),
                   "initial_setup": initial,
                   }
    return game_params

def load_previous_game():

    with open('Chessboard_State.txt', 'r') as myfile:
        initial = myfile.read()

    return initial

def warm_up_camera():

    camera = Camera()
    i = 0
    while i != 50:
        img = camera.get_frame()
        i += 1
    del camera

    return img