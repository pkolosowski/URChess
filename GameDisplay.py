import itertools
import pygame as pg
import time

class GameDisplay:

    def __init__(self):

        pg.init()
        pg.display.set_caption('Chess')
        self.screen = pg.display.set_mode((800, 900))
        self.tile_size = 100
        #load pieces icons
        self.red_knight = pg.image.load("Icons/Knight_Red.png")
        self.red_king = pg.image.load("Icons/King_Red.png")
        self.red_rook = pg.image.load("Icons/Rook_Red.png")
        self.red_pawn = pg.image.load("Icons/Pawn_Red.png")
        self.red_bishop = pg.image.load("Icons/Bishop_Red.png")
        self.red_queen = pg.image.load("Icons/Queen_Red.png")

        self.green_knight = pg.image.load("Icons/Knight_Green.png")
        self.green_king = pg.image.load("Icons/King_Green.png")
        self.green_rook = pg.image.load("Icons/Rook_Green.png")
        self.green_pawn = pg.image.load("Icons/Pawn_Green.png")
        self.green_bishop = pg.image.load("Icons/Bishop_Green.png")
        self.green_queen = pg.image.load("Icons/Queen_Green.png")

        self.icons = {"r": self.red_rook,
                      "R": self.green_rook,
                      "n": self.red_knight,
                      "N": self.green_knight,
                      "p": self.red_pawn,
                      "P": self.green_pawn,
                      "q": self.red_queen,
                      "Q": self.green_queen,
                      "k": self.red_king,
                      "K": self.green_king,
                      "b": self.red_bishop,
                      "B": self.green_bishop }

    def __display_turn(self, turn="green"):

        text_color = (0,0,0)
        info = ""
        if turn == "red":
            info = "Red's Turn"
            text_color = (235, 52, 52)
        elif turn == "green":
            info = "Green's Turn"
            text_color = (0, 128, 0)
        elif turn == "red won!":
            info = "Checkmate! Red Won!"
            text_color = (0, 0, 0)
        elif turn == "green won!":
            info = "Checkmate! Green Won!"
        font = pg.font.SysFont("TNR", 60)
        text = font.render(info, True, text_color)
        self.screen.blit(text, (400 - text.get_width() // 2, 850 - text.get_height() // 2))


    def __display_pieces(self, background, board):


        pieces = ['R', 'r', 'N', 'n', 'B', 'b', 'Q', 'q', 'K', 'k', 'P', 'p']
        self.screen.blit(background, (0, 0))

        for i in range(0, 120):
            if board[i] in pieces:
                icon = pg.transform.scale(self.icons[board[i]], (80, 80))
                x = 10 + (i % 10 - 1) * self.tile_size
                y = 10 + (i / 10 - 2) * self.tile_size
                self.screen.blit(icon, (x, y))

            pg.display.flip()

    def display(self, board, color):

        color = color.lower()
        self.screen.fill((130, 210, 245))
        self.__display_turn(color)

        BLACK = pg.Color('white')
        WHITE = pg.Color('gray')
        colors = itertools.cycle((BLACK, WHITE))


        width, height = 8*self.tile_size, 8*self.tile_size
        background = pg.Surface((width, height))

        for y in range(0, height, self.tile_size):
            for x in range(0, width, self.tile_size):
                rect = (x, y, self.tile_size, self.tile_size)
                pg.draw.rect(background, next(colors), rect)
            next(colors)

        self.__display_pieces(background, board)
