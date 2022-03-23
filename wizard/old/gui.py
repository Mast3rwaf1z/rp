import tkinter as tk
import json
import threading
def main():
    text = tk.Label(text="Test Window")
    text2 = tk.Label(text="Hello World")
    text.pack()
    text2.pack()
    tk.mainloop()

class table(threading.Thread):
    def __init__(self, content:dict):
        threading.Thread.__init__(self)
        self.content = content
        self.entrylist = []
        self.running=False

    def display(self):
        self.running = True
        self.update()
        self.window.after(10000,self.update)
        self.window.mainloop()

    def run(self):
        self.window = tk.Tk()
        self.display()

    def update(self):
        i=0
        for E1 in self.content:
            e = tk.Entry(self.window,width=10, font=("Arial",16,"bold"))
            e.grid(row=0, column=i)
            e.insert(tk.END,E1)
            j=1
            for E2 in self.content[E1]:
                e = tk.Entry(self.window,width=10,font=("Arial",16,"bold"))
                e.grid(row=j,column=i)
                e.insert(tk.END, self.content[E1][E2])
                j=j+1
            i+=1
        self.window.after(10000, self.update)
    
    def setContent(self, content:dict):
        self.content = content

if __name__ == "__main__":
    o = table({
        "test":{
            "test":1,
            "test2":2
        },
        "test2":{
            "test":1,
            "test2":2
            }
        }
    )
    o.start()
    o.close()
    #main()
