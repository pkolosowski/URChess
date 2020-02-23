#!/usr/bin/python

import sys
import socket
import numpy as np


class RobotScript:

    def __init__(self, name, socket):

        self.s = socket
        self.name = name
        self.pre = "def {}():\n".format(self.name)
        self.script = ""
        self.post = "end\n"
        self.loaded = False

    def load_script(self, filename):

        with open(filename) as f:
            for line in f:
                self.script += line + '\n'

        self.loaded = True

    def get_script(self):

        if self.loaded:
            return self.script
        else:
            return self.pre + self.script + self.post

    def add_message(self, message):

        self.script += '  textmsg("{}")\n'.format(message)

    def add_movep(self, p, v, a, b):

        cmd = "  movep(p{p}, {a}, {v}, {b})\n".format(p=p, v=v, a=a, b=b)
        self.script += cmd

    def add_movel(self, p, v, a, t, b):

        cmd = "  movel(p{p}, {a}, {v}, {t}, {b})\n".format(p=p, v=v, a=a, t=t, b=b)
        self.script += cmd

    def add_digital_out(self, x):

        cmd = "  set_digital_out(7,{x})\n".format(x=x)
        self.script += cmd

    def send_script(self, socket, script):

        socket.send(script)

    def save(self, filename, contents):

        fh = open(filename, 'w')
        fh.write(contents)
        fh.close()

    def add_sleep(self, s):

        cmd = "  sleep({s})\n".format(s=s)
        self.script += cmd

    def pick(self, coords, height1, height2, program): #height1 - safety level; height2 - desired level

        program.add_movel([coords[0] / 1000.00, coords[1] / 1000.00, height1/1000.00, 0, -3.14, 0], 2, 2, 3, 0.0)
        program.add_sleep(1)
        program.add_movel([coords[0] / 1000.00, coords[1] / 1000.00, height2/1000.00, 0, -3.14, 0], 0.5, 0.5, 1, 0.0)
        program.add_sleep(1)
        program.add_digital_out(False)
        program.add_sleep(1)
        program.add_movel([coords[0] / 1000.00, coords[1] / 1000.00, height1/1000.00, 0, -3.14, 0], 2, 2, 1, 0.0)
        program.add_sleep(1)

    def place(self, coords, height1, height2, program):

        program.add_movel([coords[0] / 1000.00, coords[1] / 1000.00, height1/1000.00, 0, -3.14, 0], 2, 2, 2, 0.0)
        program.add_sleep(1)
        program.add_movel([coords[0] / 1000.00, coords[1] / 1000.00, height2/1000.00, 0, -3.14, 0], 0.5, 0.5, 1, 0.0)
        program.add_sleep(1)
        program.add_digital_out(True)
        program.add_sleep(1)
        program.add_movel([coords[0] / 1000.00, coords[1] / 1000.00, height1/1000.00, 0, -3.14, 0], 2, 2, 1, 0.0)
        program.add_sleep(1)

    def go_home_position(self, program):

        program.add_movel([0.0, -0.160, 0.450, -1, -3.00, 0], 2, 2, 2, 0.0)
        program.add_sleep(1)

    def execute(self, program, coords, move_type):

        coords = coords
        program = program

        if move_type == "normal":

            program.pick(coords[0], 400, 230, program)
            program.place(coords[1], 400, 230, program)
            program.go_home_position(program)

        if move_type == "castle":

            program.pick(coords[0], 400, 230, program)
            program.place(coords[1], 400, 230, program)
            program.pick(coords[2], 400, 230, program)
            program.place(coords[3], 400, 230, program)
            program.go_home_position(program)

        if move_type == "capture" or move_type == "en_passant":

            program.pick(coords[0], 400, 230, program)
            program.place(coords[1], 400, 380, program)
            program.pick(coords[2], 400, 230, program)
            program.place(coords[3], 400, 230, program)
            program.go_home_position(program)

        if move_type == 'checkmate':

            height1 = 280
            program.add_digital_out(False)
            program.add_movel([coords[0] / 1000.00, (coords[1]+50) / 1000.00, 450 / 1000.00, 0, -3.14, 0], 2, 2, 2, 0.0)
            program.add_sleep(2)
            program.add_movel([coords[0] / 1000.00, (coords[1]+50) / 1000.00, height1 / 1000.00, 0, -3.14, 0], 2, 2, 2, 0.0)
            program.add_sleep(2)
            program.add_movel([coords[0] / 1000.00, (coords[1]-50) / 1000.00, height1 / 1000.00, 0, -3.14, 0], 0.5, 0.5, 1, 0.0)
            program.add_sleep(5)
            program.go_home_position(program)
            program.add_digital_out(True)

        self.script = self.get_script()
      #  print self.script
        #self.save('script.txt', self.script)
        #self.send_script(self.s, self.script)
        self.script = ""