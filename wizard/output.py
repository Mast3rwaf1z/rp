import tkinter as tk
import tkinter.ttk as ttk

class table(tk.Frame):
    rows:list[tk.Frame]
    labels:list[list[tk.Label]]
    master:tk.Toplevel

    def __init__(self, content:list[list], width=2, height=2, title="", icon="", master=tk.Toplevel, scrollable = "None"):
        self.master = master
        tk.Frame.__init__(self, self.master)
        if type(self.master) is tk.Toplevel:
            self.master.resizable(False,False)
            self.master.title(title)
            if not icon == "":
                try:
                    self.master.iconbitmap(icon)
                except:
                    print("failed to set window icon")
        if not len(content) > 0 or not len(content[0]) > 0:
            print("failed to make table: bad list")
            return
        rows = len(content)
        cols = len(content[0])
        if scrollable == "None":
            container = self
        elif scrollable == "x":
            if len(content) > 10:
                mod = 10
            else:
                mod = len(content)
            __container = ScrollableFrame_X(self, width=width*7.5*len(content[0]), height=height*mod*20)
            container = __container.scrollable_frame
            __container.pack(side=tk.LEFT)
        elif scrollable == "y":
            if len(content) > 10:
                mod = 10
            else:
                mod = len(content)
            __container = ScrollableFrame_Y(self, width=width*7.5*len(content[0]), height=height*mod*20)
            container = __container.scrollable_frame
            __container.pack(side=tk.LEFT)
        self.rows = [tk.LabelFrame(container) for i in range(rows)]
        [self.rows[i].pack(side=tk.TOP) for i in range(len(self.rows))]
        self.labels = [[tk.Label(self.rows[i], text=content[i][j], width=width, height=height).pack(side=tk.LEFT) for i in range(rows)] for j in range(cols)]

class ScrollableFrame_Y(tk.Frame):
    ###source: https://blog.teclado.com/tkinter-scrollable-frames/
    def __init__(self, container, width=300, height=300, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set, width=width, height=height)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

class ScrollableFrame_X(tk.Frame):
    ###source: https://blog.teclado.com/tkinter-scrollable-frames/
    def __init__(self, container, width=300, height=300, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="horizontal", command=canvas.xview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(xscrollcommand=scrollbar.set, width=width, height=height)

        canvas.pack(side="top", fill="both", expand=True)
        scrollbar.pack(side="bottom", fill="x")


if __name__ == "__main__":
    window = tk.Tk()
    tab= table([[i*j for i in range(10)] for j in range(10)],master=window, scrollable="y")
    tab.pack(side=tk.TOP)
    window.mainloop()