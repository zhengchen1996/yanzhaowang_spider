import tkinter

class Dialog:
    def __init__(self,flag):
        self.win =tkinter.Tk()
        self.win.geometry("200x150+400+200")
        self.win.resizable(0, 0)
        self.win.title("提示")
        self.win.wm_attributes('-topmost', 1)
        self.Button = tkinter.Button(self.win, text="确认", command=self.close, width=15)
        self.Button.place(x=50, y=80)
        if flag == "a":
            label = tkinter.Label(self.win, anchor=tkinter.CENTER,
                                  text="all db data get", width=20,
                                  height=3)
        elif flag == "b":
            label = tkinter.Label(self.win, anchor=tkinter.CENTER,
                                  text="csv out put", width=20,
                                  height=3)

        elif flag == "c":
            label = tkinter.Label(self.win, anchor=tkinter.CENTER,
                                  text="key world data get", width=20,
                                  height=3)

        elif flag == "d":
            label = tkinter.Label(self.win, anchor=tkinter.CENTER,
                                  text="hou rank complete", width=20,
                                  height=3)

        elif flag == "e":
            label = tkinter.Label(self.win, anchor=tkinter.CENTER,
                                  text="spider working complete", width=20,
                                  height=3)

        else:
            pass
        label.pack()
        self.show()

    def show(self):
        self.win.mainloop()

    def close(self):
        self.win.destroy()