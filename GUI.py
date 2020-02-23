from Tkinter import *
from ttk import *

class GUI:

    def __init__(self):


        self.window = Tk()
        self.window.title("Game settings")
        self.window.geometry('600x520')
        self.online_offline = [
            ("Online", 0),
            ("Offline", 1),
        ]

        self.color = [
            ("green", 0),
            ("red", 1),
        ]

        self.game_modes = [
            ("Human vs Human (terminal)", 0),
            ("Human vs Robot (terminal)", 1),
            ("Robot vs Robot", 2),
            ("Human vs Robot (vision tracking)", 3)
        ]

        self.robots = [
            ("UR1", 0),
            ("UR2", 1)
        ]

        self.load_new = [
            ("Play New Game", 0),
            ("Load Previous Game", 1),
        ]
        self.initial = (
            '         \n'  # 0 -  9
            '         \n'  # 10 - 19
            ' rnbqkbnr\n'  # 20 - 29
            ' pppppppp\n'  # 30 - 39
            ' ........\n'  # 40 - 49
            ' ........\n'  # 50 - 59
            ' ........\n'  # 60 - 69
            ' ........\n'  # 70 - 79
            ' PPPPPPPP\n'  # 80 - 89
            ' RNBQKBNR\n'  # 90 - 99
            '         \n'  # 100 -109
            '         \n'  # 110 -119
        )



    def disable_widgets(self,game_mode_btns,manipulators,var2,game_modes):

        game_mode_btns[3].configure(state="disabled")
        manipulators[0].configure(state="disabled")
        manipulators[1].configure(state="disabled")
        var2.set(game_modes[0][1])

    def enable_widgets(self,game_mode_btns,manipulators):

        game_mode_btns[3].configure(state="normal")
        manipulators[0].configure(state="normal")
        manipulators[1].configure(state="normal")


    def quit(self,):

        self.chessboard = self.initial_setup.get('1.0','end-1c')
        self.window.destroy()

    def draw(self,):


        self.var1 = IntVar()
        self.var1.set(self.online_offline[0][1])

        frame = Frame(self.window, border=5)
        frame.grid(column=0,row=0,sticky='nw')
        lbl = Label(frame, text='Play online or offline:')
        lbl.grid(row=0,column=0,sticky='w')

        if self.var1.get() == 1:
            status="disabled"
        if self.var1.get() == 0:
            status="normal"

        self.var2 = IntVar()
        self.var2.set(self.game_modes[0][1])

        frame2 = Frame(self.window, border=5)
        frame2.grid(column=1,row=0,sticky='nw')
        lbl2 = Label(frame2, text='Select game mode:')
        lbl2.grid(row=0,column=0,sticky='w')
        i=0
        game_mode_btns = []

        for txt, val in self.game_modes:
            button = Radiobutton(frame2, text=txt,state=status,variable=self.var2, value=val,)
            button.grid(row=1+i,column=0, sticky='w')
            game_mode_btns.append(button)
            i+=1

        self.var3 = IntVar()
        self.var3.set(self.load_new[0][1])

        frame3 = Frame(self.window, border=5)
        frame3.grid(column=0,row=4,sticky='nw')
        lbl3 = Label(frame3, text='Load previous/ play new game:')
        lbl3.grid(row=0,column=0)
        i=0

        for txt, val in self.load_new:
            Radiobutton(frame3, text=txt, variable=self.var3, value=val,
             ).grid(row=1+i,column=0, sticky='w')
            i+=1

        self.var4 = IntVar()
        self.var4.set(self.color[0][1])

        frame4 = Frame(self.window, border=5)
        frame4.grid(column=1,row=4,sticky='nw')
        lbl4 = Label(frame4, text='Select color:')
        lbl4.grid(row=0,column=0)
        i=0

        for txt, val in self.color:
            button = Radiobutton(frame4, text=txt, variable=self.var4, value=val,)
            button.grid(row=1 + i, column=0, sticky='w')
            i+=1


        self.var5 = IntVar()
        self.var5.set(self.robots[0][1])

        frame5 = Frame(self.window, border=5)
        frame5.grid(column=0,row=5,sticky='nw')
        lbl5 = Label(frame5, text='Select robot:')
        lbl5.grid(row=0,column=0,sticky='w')
        i=0

        manipulators = []
        for txt, val in self.robots:
            button = Radiobutton(frame5, text=txt, variable=self.var5, value=val,)
            button.grid(row=1+i,column=0, sticky='w')
            i+=1
            manipulators.append(button)


        frame6 = Frame(self.window, border=0)
        frame6.grid(column=1,row=5,sticky='nw')

        self.content = StringVar()

        self.ur1_ip = Entry(frame6,textvariable=self.content)
        lbl = Label(frame6, text='UR1 IP:', )
        lbl.grid(column=0,row=0,pady=10)
        self.ur1_ip.grid(column=0, row=1,padx=10,)
        self.ur1_ip.insert(END, "192.168.0.110")

        self.content2 = StringVar()
        lbl = Label(frame6, text='UR2 IP:')
        lbl.grid(column=0,row=2,pady=10)
        self.ur2_ip = Entry(frame6, textvariable=self.content2)
        self.ur2_ip.grid(column=0, row=3,padx=10)
        self.ur2_ip.insert(END, "192.168.0.113")

        self.content3 = StringVar()
        self.ur1_host = Entry(frame6,width=10, textvariable=self.content3)
        lbl = Label(frame6, text='UR1 PORT:')
        lbl.grid(column=1,row=0)
        self.ur1_host.grid(column=1, row=1)
        self.ur1_host.insert(END, "30001")

        self.content4 = StringVar()
        self.ur2_host = Entry(frame6,width=10, textvariable=self.content4)
        lbl = Label(frame6, text='UR2 PORT:')
        lbl.grid(column=1,row=2)
        self.ur2_host.grid(column=1, row=3)
        self.ur2_host.insert(END, "30001")

        frame7 = Frame(self.window, border=0)
        frame7.grid(row=7,column=0)

        self.initial_setup = Text(frame7, width=10,height=12,)
        lbl = Label(frame7, text='Initial chessboard setup:')
        lbl.grid(column=0,row=0)
        self.initial_setup.grid(column=0,row=1)
        self.initial_setup.insert(END,self.initial)


        Button1 = Button(frame5, text ="Start", width=15, command= lambda: self.quit())
        Button1.grid(row=4,pady=30,padx=40)

        Radiobutton(frame, text=self.online_offline[0][0], variable=self.var1, command= lambda:
        self.enable_widgets(game_mode_btns,manipulators), value=self.online_offline[0][1],).grid(row=1,column=0,sticky='w')
        Radiobutton(frame, text=self.online_offline[1][0], variable=self.var1, command=lambda:
        self.disable_widgets(game_mode_btns,manipulators,self.var2,self.game_modes),value=self.online_offline[1][1],).grid(row=2,column=0,sticky='w')

        self.window.mainloop()






