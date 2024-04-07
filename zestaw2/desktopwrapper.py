import tkinter as tk
from tkinter import ttk
import task1and2
import task3
import task4
import re
import networkx as nx
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

LARGE_FONT= ("Verdana", 28)

def validate_sequence(value):
    pattern = r'[0-9 ]+'
    if re.fullmatch(pattern, value) is None:
        return False
    return True
def validate_number(value):
    value = value.replace(" ", "")
    if str.isdigit(value):
        return True
    return False

def string_to_list(value):
    return [int(element) for element in value.split()]

class GraphsSet2(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Zestaw 2")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour): 

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        label1 = tk.Label(self, text="Wybierz co chcesz zrobić:")
        label1.pack()
        button = ttk.Button(self, text="Stwórz graf z ciągu graficznego",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = ttk.Button(self, text="Randomizuj krawędzie",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = ttk.Button(self, text="Znajdź największą spójną składową",
                            command=lambda: controller.show_frame(PageThree))
        button3.pack()

        button4 = ttk.Button(self, text="Wygeneruj graf eulerowski i znajdź cykl Eulera",
                            command=lambda: controller.show_frame(PageFour))
        button4.pack()
    
class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        self.sequence = tk.StringVar()
        self.returned = tk.StringVar()
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Stwórz graf z ciągu graficznego", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        label1 = tk.Label(self, text="Wpisz ciąg graficzny liczb całkowitych oddzielonych spacją")
        label1.pack()
        entry = ttk.Entry(self, textvariable=self.sequence)
        entry.pack()

        button = ttk.Button(self, text="Enter",
                            command=self.enter_clicked)
        button.pack()

        button1 = ttk.Button(self, text="Wróć do strony głównej",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        self.fig = Figure(figsize = (5, 5), dpi = 100) 
        self.plot1 = self.fig.add_subplot(111) 
        self.plot1.plot()
        
        self.canvas = FigureCanvasTkAgg(self.fig, 
                        master = self)   
        self.canvas.draw() 
    
        self.canvas.get_tk_widget().pack() 
    
        self.toolbar = NavigationToolbar2Tk(self.canvas, 
                                    self) 
        self.toolbar.update() 
    
        self.canvas.get_tk_widget().pack()

        self.label_with_component = tk.Label(self, textvariable=self.returned)
        self.label_with_component.pack()

    def enter_clicked(self):
        seq = self.sequence.get()
        if validate_sequence(seq):
            sequence_list = string_to_list(seq)
            if task1and2.check_if_degree_sequence(sequence_list):
                self.plot1.clear()
                graph = task1and2.create_graph_from_sequence(sequence_list)
                nx.draw_circular(graph, ax=self.plot1, with_labels=True)
                self.canvas.draw()
                self.returned.set("Podany ciąg jest graficzny.")
            else:
                self.returned.set("Podany ciąg nie jest graficzny.")
        else:
            self.returned.set("Wpisz tylko liczby i spacje.")
    
class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.sequence = tk.StringVar()
        self.number = tk.StringVar()
        self.returned = tk.StringVar()
        label = tk.Label(self, text="Randomizuj krawędzie", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        label1 = tk.Label(self, text="Wpisz ciąg graficzny liczb całkowitych oddzielonych spacją")
        label1.pack()
        
        entry = ttk.Entry(self, textvariable=self.sequence)
        entry.pack()

        label2 = tk.Label(self, text="Wpisz ilość randomizacji")
        label2.pack()
        
        entry1 = ttk.Entry(self, textvariable=self.number)
        entry1.pack()

        button = ttk.Button(self, text="Enter",
                            command=self.enter_clicked)
        button.pack()

        button1 = ttk.Button(self, text="Wróć do strony głównej",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        self.fig = Figure(figsize = (5, 5), dpi = 100) 
        self.plot1 = self.fig.add_subplot(111) 
        self.plot1.plot()
        
        self.canvas = FigureCanvasTkAgg(self.fig, 
                        master = self)   
        self.canvas.draw() 
    
        self.canvas.get_tk_widget().pack() 
    
        self.toolbar = NavigationToolbar2Tk(self.canvas, 
                                    self) 
        self.toolbar.update() 
    
        self.canvas.get_tk_widget().pack()

        self.label_with_component = tk.Label(self, textvariable=self.returned)
        self.label_with_component.pack()

    def enter_clicked(self):
        seq = self.sequence.get()
        num = self.number.get()
        if validate_sequence(seq) and validate_number(num):
            sequence_list = string_to_list(seq)
            random_num = int(num)
            if task1and2.check_if_degree_sequence(sequence_list):
                self.plot1.clear()
                random_graph = task1and2.randomize_edges(random_num, sequence_list)
                nx.draw_circular(random_graph, ax=self.plot1, with_labels=True)
                self.canvas.draw()
                self.returned.set("Podany ciąg jest graficzny.")
            else:
                self.returned.set("Podany ciąg nie jest graficzny.")
        else:
            self.returned.set("Wpisz tylko liczby i spacje.")

class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        super(PageThree, self).__init__()
        self.sequence = tk.StringVar()
        self.returned = tk.StringVar()

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Znajdź największą spójną składową", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        label1 = tk.Label(self, text="Wpisz ciąg graficzny liczb całkowitych oddzielonych spacją")
        label1.pack()
        
        entry = ttk.Entry(self, textvariable=self.sequence)
        entry.pack()

        button = ttk.Button(self, text="Enter",
                            command=self.enter_clicked)
        button.pack()

        button1 = ttk.Button(self, text="Wróć do strony głównej",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        self.label_with_component = tk.Label(self, textvariable=self.returned)
        self.label_with_component.pack()

    def enter_clicked(self):
        seq = self.sequence.get()
        if validate_sequence(seq):
            sequence_list = string_to_list(seq)
            if task1and2.check_if_degree_sequence(sequence_list):
                components = task3.find_largest_component(task1and2.create_graph_from_sequence(sequence_list))
                self.returned.set(components)
            else:
                self.returned.set("Podany ciąg nie jest graficzny.")
        else:
            self.returned.set("Wpisz tylko liczby i spacje.")


class PageFour(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.number = tk.StringVar()
        self.returned = tk.StringVar()
        label = tk.Label(self, text="Wygeneruj graf eulerowski i znajdź cykl Eulera", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        label1 = tk.Label(self, text="Wpisz ilość wierzchołków grafu")
        label1.pack()
        
        entry = ttk.Entry(self, textvariable=self.number)
        entry.pack()

        button = ttk.Button(self, text="Enter",
                            command=self.enter_clicked)
        button.pack()

        button1 = ttk.Button(self, text="Wróć do strony głównej",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        self.fig = Figure(figsize = (5, 5), dpi = 100) 
        self.plot1 = self.fig.add_subplot(111) 
        self.plot1.plot()
        
        self.canvas = FigureCanvasTkAgg(self.fig, 
                        master = self)   
        self.canvas.draw() 
    
        self.canvas.get_tk_widget().pack() 
    
        self.toolbar = NavigationToolbar2Tk(self.canvas, 
                                    self) 
        self.toolbar.update() 
    
        self.canvas.get_tk_widget().pack()

        self.label_with_component = tk.Label(self, textvariable=self.returned)
        self.label_with_component.pack()
    def enter_clicked(self):
        num = self.number.get()
        if validate_number(num):
            random_num = int(num)
            self.plot1.clear()
            graph = task4.generate_euler_graph(random_num)
            nx.draw_circular(graph, ax=self.plot1, with_labels=True)
            self.canvas.draw()
            cycle = task4.find_euler_cycle(graph, [])
            self.returned.set(self.cycle_to_string(cycle))
        else:
            self.returned.set("Wpisz tylko liczby i spacje.")
    def cycle_to_string(self, cycle: list) -> str:
        string = ""
        for i in range(len(cycle)):
            string = string + ", " + str(cycle[i])
            if not (i+1) % 10:
                string += "\n"
        return string
    
app = GraphsSet2()
app.mainloop()

    