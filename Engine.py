import re, sys, time
from EstimateChessboard import EstimateChessboard
from CoordinatesTransform import CoordinatesTransform
import cv2
import socket
from RobotScript import RobotScript
from GameDisplay import GameDisplay
from Searcher import Searcher
from Functions import *


def main():

    graveyard_red = (-500, -500)
    graveyard_green = (400, -600)

    game_params = get_gui_setup()

    mode = str(game_params["game_mode"])
    online_game = game_params["online_game"]
    player_side = game_params["player_side"]
    initial = game_params["initial_setup"]
    load_game = game_params["load_new"]
    if load_game == "Load Previous Game":
        initial = load_previous_game()

    HOST_UR1, PORT_UR1 = game_params["ur1_ip"], game_params["ur1_port"]
    HOST_UR2, PORT_UR2 = game_params["ur2_ip"], game_params["ur2_port"]

    manipulator = game_params["manipulator"]

    hist = [Position(initial, 0, (True, True), (True, True), 0, 0)]
    searcher = Searcher()
    visualization = GameDisplay()
    est_chessboard = EstimateChessboard()

    if mode == '3':
        transform_UR1 = CoordinatesTransform(manipulator)
        transform_UR2 = CoordinatesTransform(manipulator)

        if manipulator == "UR1":
            HOST_UR2, PORT_UR2 = HOST_UR1, PORT_UR1
        if manipulator == "UR2":
            HOST_UR1, PORT_UR1 = HOST_UR2, PORT_UR2

    else:
        transform_UR1 = CoordinatesTransform("UR1")
        transform_UR2 = CoordinatesTransform("UR2")

    if mode == '2':
        opening_moves = get_opening()

    img = cv2.imread("basic_frame.png")

    if online_game == 'Online':
        img = warm_up_camera()

    chessboard = est_chessboard.estimate_chessboard_postion(img)

    visualization.display(initial, 'green')

    while True:

################## Green's Move ###########################

        print_pos(hist[-1])
        move = None
        board = hist[-1].get_board()

        execute_flag = None

        if mode == '0' or (mode == '1' and player_side == 'green'):
            move = input_move(hist, "green")
            execute_flag = True
        if (mode == '1' and player_side == "red"):
            move = calculate_move(searcher, hist)
            execute_flag = True
        if mode == '2':
            if opening_moves and load_game == "Play New Game":
                move = opening_moves.pop(0)
                move = parse(move[0:2]), parse(move[2:4])
            else:
                move = calculate_move(searcher, hist)
        if mode == '3' and player_side == "green":
            move = vision_move(hist, player_side, chessboard)
            execute_flag = False
        if mode == "3" and player_side == "red":
            move = calculate_move(searcher, hist)
            execute_flag = True


        move1s = render(move[0])
        move2s = render(move[1])

        move1 = chessboard[move1s]
        move2 = chessboard[move2s]

        move_1 = transform_UR1.coords_conversion((move1[0], move1[1]))
        move_2 = transform_UR1.coords_conversion((move2[0], move2[1]))



        if execute_flag and online_game == 'Offline':
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #s.connect((HOST_UR1, PORT_UR1))
            script = RobotScript('prog', s)
            execute_move(move1s, move2s, chessboard, transform_UR1, script, board, graveyard_red, move_1, move_2, None, None)
            s.close()

        hist.append(hist[-1].move(move))
        print_pos(hist[-1].rotate())

        time.sleep(1)

        mate_flag = check_mate(hist, searcher)
        if mate_flag:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST_UR1, PORT_UR1))
            script = RobotScript('prog', s)
            visualization.display(hist[-1][0], "Green Won!")
            execute_mate_move(hist, chessboard, s, script, transform_UR1, "green")
            s.close()

        visualization.display(hist[-1].rotate()[0], 'Red')

        save_game(hist)

######################### Red's Move ########################################

        if mode == "0" or (mode == "1" and player_side == "red"):
            move = input_move(hist, "red")
            execute_flag = True
        if (mode == "1" and player_side == "green"):
            move = calculate_move(searcher, hist)
            execute_flag = True
        if mode == '2' and load_game == "Play New Game":
            if opening_moves:
                move = opening_moves.pop(0)
                move = 119 - parse(move[0:2]), 119 - parse(move[2:4])
            else:
                move = calculate_move(searcher, hist)
        if mode == "3" and player_side == "green":
            move = calculate_move(searcher, hist)
            execute_flag = True
        if mode == "3" and player_side == "red":
            move = vision_move(hist, player_side, chessboard)
            execute_flag = False

        board = hist[-1].get_board()

        hist.append(hist[-1].move(move))

        move2_s = render(move[1])
        move1_s = render(move[0])

        move1s = render(119 - move[0])
        move2s = render(119 - move[1])

        move1 = chessboard[move1s]
        move2 = chessboard[move2s]

        move_1 = transform_UR2.coords_conversion((move1[0], move1[1]))
        move_2 = transform_UR2.coords_conversion((move2[0], move2[1]))

        time.sleep(1)
        visualization.display(hist[-1][0], 'Green')

        if execute_flag and online_game == 'Offline':
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #s.connect((HOST_UR2, PORT_UR2))
            script = RobotScript('prog', s)
            execute_move(move1_s, move2_s, chessboard, transform_UR2, script, board, graveyard_green, move_1, move_2, move1s, move2s)
            s.close()

        save_game(hist)

        mate_flag = check_mate(hist, searcher)
        if mate_flag:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST_UR2, PORT_UR2))
            script = RobotScript('prog', s)
            visualization.display(hist[-1][0], "Red Won!")
            execute_mate_move(hist, chessboard, s, script, transform_UR1, "red")
            s.close()

if __name__ == '__main__':
    main()

