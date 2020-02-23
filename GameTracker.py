from PieceDetection import PieceDetection
import cv2

class GameTracker:


    def diff(self, li1, li2):

        li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
        return li_dif

    def __define_move(self, green_oc_diff, green_occupied1, green_unoccupied1, red_oc_diff, red_occupied1, red_unoccupied1, player_color='green'):

        move_from = ""
        move_to = ""
        if player_color == 'green':
            for field in green_oc_diff:
                if field in green_occupied1:
                    move_from = field
                if field in green_unoccupied1:
                    move_to = field

        if player_color == 'red':
            for field in red_oc_diff:
                if field in red_occupied1:
                    move_from = field
                if field in red_unoccupied1:
                    move_to = field

        return move_from, move_to

    def __update_board(self, move_from, move_to, move_type, string):

        if move_from != '':
            move_from_index = 90 - 10 * (ord(move_from[1]) - 49) + (ord(move_from[0]) - 97 + 1)
        if move_to != '':
            move_to_index = 90 - 10 * (ord(move_to[1]) - 49) + (ord(move_to[0]) - 97 + 1)

        if move_type == "red_move" or move_type == "green_move" or move_type == "red_capture" or move_type == "green_capture":

            str = list(string)
            print str[move_from_index], str[move_to_index]
            str[move_to_index] = str[move_from_index]
            str[move_from_index] = '.'
            string = ''.join(str)
            print move_from_index, move_to_index

        if move_type == "red_en_passant" or move_type == "green_en_passant":

            str = list(string)
            str[move_to_index] = str[move_from_index]
            str[move_from_index] = '.'
            str[move_to_index + 10] = '.'
            string = ''.join(str)
            print move_from_index, move_to_index

        return  string

    def __move_type(self, diff_green1, diff_green2, red_oc_diff, move_to, diff_red1, diff_red2, green_oc_diff, player_color = 'green'):

        move = None
        print(red_oc_diff)
        if player_color == 'green':
            if len(diff_green1) == 1 and len(diff_green2) == 1 and len(red_oc_diff) != 0 and move_to not in red_oc_diff:
                move = "green_en_passant"
            elif len(diff_green1) == 1 and len(diff_green2) == 1 and move_to in red_oc_diff:
                move = "green_capture"
            elif len(diff_green1) == 1 and len(diff_green2) == 1 and len(diff_red1) == 0 and len(diff_red2) == 0:
                move = "green_move"
            elif len(green_oc_diff) == 4 and all(elem in green_oc_diff for elem in ['e1', 'g1']):
                move = "green_castle_kingside"
            elif len(green_oc_diff) == 4 and all(elem in green_oc_diff for elem in ['e1', 'c1']):
                move = "green_castle_queenside"

        if player_color == 'red':
            if len(diff_red1) == 1 and len(diff_red2) == 1 and len(green_oc_diff) != 0 and move_to not in green_oc_diff:
                move = "red_en_passant"
            elif len(diff_red1) == 1 and len(diff_red2) == 1 and move_to in green_oc_diff:
                move = "red_capture"
            elif len(diff_red1) == 1 and len(diff_red2) == 1 and len(diff_green1) == 0 and len(diff_green2) == 0:
                move = "red_move"
            elif len(red_oc_diff) == 4 and all(elem in red_oc_diff for elem in ['e8', 'g8', 'f8', 'h8']):
                move = "red_castle_kingside"
            elif len(red_oc_diff) == 4 and all(elem in red_oc_diff for elem in ['e8', 'c8', 'd8', 'a8']):
                move = "red_castle_queenside"

        print(move)
        return move

    def track(self, player_color, previous_frame, current_frame, state, chessboard):

        string = state
        change_detected = 0
        piece_detection  = PieceDetection()
        green_occupied1, green_unoccupied1, red_occupied1, red_unoccupied1 = piece_detection.get_chessboard_status(previous_frame,chessboard)
        green_occupied2, green_unoccupied2, red_occupied2, red_unoccupied2 = piece_detection.get_chessboard_status(current_frame,chessboard)

        diff_green2 = list(set(green_unoccupied2) - set(green_unoccupied1))
        diff_green1 = list(set(green_occupied2) - set(green_occupied1))

        diff_red2 = list(set(red_unoccupied2) - set(red_unoccupied1))
        diff_red1 = list(set(red_occupied2) - set(red_occupied1))

        green_oc_diff = self.diff(green_occupied2, green_occupied1)
        red_oc_diff = self.diff(red_occupied2, red_occupied1)

        move_from, move_to = self.__define_move\
            (green_oc_diff, green_occupied1,green_unoccupied1, red_oc_diff, red_occupied1, red_unoccupied1, player_color)

        move_type = self.__move_type\
            (diff_green1, diff_green2, red_oc_diff, move_to, diff_red1, diff_red2, green_oc_diff, player_color)

        string = self.__update_board(move_from, move_to, move_type, string)

        if move_from != '' and move_to != '':
            change_detected = 1

        move = move_from + move_to

        if move_type == "red_castle_queenside":
            move = "e8c8"
        if move_type == "red_castle_kingside":
            move = "e8g8"
        if move_type == "green_castle_queenside":
            move = "e1c1"
        if move_type == "green_castle_kingside":
            move = "e1g1"

        return change_detected, move, string


