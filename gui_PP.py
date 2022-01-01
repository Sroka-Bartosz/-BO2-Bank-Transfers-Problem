#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *

import evolutionaryAlgorithm
import time
import specimen
import numpy as np

# global variables
matrix_ = None
selection_ = 'roulette'

max_size_of_spec = 30
min_size_of_spec = 3
max_value_of_spec = 500
min_value_of_spec = 1

# create a window
window = tk.Tk()
window.title('Problem przelewowy')
window.geometry('1000x600')
window.resizable(False, False)
window.iconbitmap('./cash_icon.ico')

# create a notebook
notebook = ttk.Notebook(window, width=690, height=530)
notebook.pack(pady=5, side='left', expand=True)

container1 = ttk.Frame(notebook, width=690, height=530)
container2 = ttk.Frame(notebook, width=690, height=530)

# create frames
frame3 = ttk.Frame(notebook, width=690, height=530)
frame3.pack(fill='x', expand=True)

# add frames to notebook
notebook.add(container1, text='Macierz początkowa')
notebook.add(container2, text='Wynik')
notebook.add(frame3, text='Przebieg algorytmu')

# Create label frame
lf = ttk.LabelFrame(window, text='Właściwości')
lf.pack(padx=10, pady=20)

# Create a class to print matrix
class Table:
    def __init__(self, root, matrix, cols, rows, total_rows, total_columns):

        canvas = tk.Canvas(root)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):
                self.e = tk.Label(scrollable_frame, width=4, text=str(matrix[i][j]))
                self.e.grid(row=i, column=j, sticky='ns')

            la = tk.Label(scrollable_frame, width=4, bg="gray51", text=str(rows[i]))
            la.grid(row=i, column=total_columns+1, sticky='ns')

        for x in range(total_columns):
            la1 = tk.Label(scrollable_frame, width=4, bg="gray51", text=str(cols[x]))
            la1.config(bg="gray")
            la1.grid(row=total_rows+1, column=x, sticky='ns')

        scroll = Scrollbar(root, orient="vertical", command=canvas.yview)
        scroll2 = Scrollbar(root, orient="horizontal", command=canvas.xview)
        canvas.configure(yscrollcommand=scroll.set, xscrollcommand=scroll2.set)

        scroll.pack(fill='y', side=RIGHT)
        scroll2.pack(fill='x', side=BOTTOM)
        canvas.pack(side=LEFT, expand=True, fill='both')

# function to create new window
def openNewWindow():
    newWindow = Toplevel(window)
    newWindow.title("Inicjalizacja macierzy")
    newWindow.geometry("500x500")
    newWindow.iconbitmap('./cash_icon.ico')
    Label(newWindow, text="Tworzenie macierzy").pack(padx=10, pady=20, expand=True)

    # First button to create matrix
    def NewWindowButton1():
        global matrix_
        first_button = Toplevel(window)
        first_button.title("Własna macierz")
        first_button.geometry("300x300")
        first_button.iconbitmap('./cash_icon.ico')
        Label(first_button, text="Podaj rozmiar macierzy").pack(padx=10, pady=5)
        size_x = Label(first_button, text="Liczba wierszy: ")
        size_x.pack(padx=10, pady=5, fill='x')
        size_1 = Entry(first_button)
        size_1.pack(padx=10, pady=5, fill='x')

        size_y = Label(first_button, text="Liczba kolumn: ")
        size_y.pack(padx=10, pady=5, fill='x')
        size_2 = Entry(first_button)
        size_2.pack(padx=10, pady=5, fill='x')

        def create_matrix():
            cre_matrix = Toplevel(window)
            cre_matrix.iconbitmap('./cash_icon.ico')
            cre_matrix.title("Tworzenie własnej macierzy")
            matrix_size_x = int(size_1.get())
            matrix_size_y = int(size_2.get())

            if matrix_size_x > 500 or matrix_size_x < 3:
                messagebox.showwarning("Warning", "Zła wartość")
                cre_matrix.destroy()
                return

            if matrix_size_y > 500 or matrix_size_y < 3:
                messagebox.showwarning("Warning", 'Zła wartość')
                cre_matrix.destroy()
                return

            def process():
                global matrix_
                matrix_ = np.zeros((matrix_size_x, matrix_size_y), dtype=np.int64)
                values = []
                for e_next in entry:
                    if type(e_next) is not str:
                        values.append(e_next.get())
                    else:
                        values.append(e_next)
                for i_x in range(matrix_size_x):
                    for j_x in range(matrix_size_y):
                        if i_x == j_x:
                            matrix_[i_x][j_x] = 0
                        else:
                            x = int(values[i_x*matrix_size_x + j_x])
                            matrix_[i_x][j_x] = x
                print(matrix_)
                cols_m = np.sum(matrix_, axis=0)
                rows_m = np.sum(matrix_, axis=1)
                Table(container1, matrix_, cols_m, rows_m, len(matrix_), len(matrix_[0]))

                first_button.destroy()
                cre_matrix.destroy()
                newWindow.destroy()

            entry = []
            for i in range(matrix_size_x):
                for j in range(matrix_size_y):
                    if i == j:
                        entry.append("0")
                        Label(cre_matrix, text="0").grid(row=i, column=j, padx=2, pady=2)
                    else:
                        e = Entry(cre_matrix, width="10")
                        e.grid(row=i, column=j, padx=2, pady=2)
                        entry.append(e)

            b = Button(cre_matrix, text='Process', command=process)
            b.grid(row=(matrix_size_x + 1), column=(matrix_size_y-1) // 2 - 1, columnspan=3, sticky=E + W)


        start_button_1 = Button(first_button, text="Start", command=create_matrix)
        exit_button_1 = Button(first_button, text="Exit", command=lambda: first_button.destroy())
        start_button_1.pack(padx=40, side=LEFT)
        exit_button_1.pack(padx=40, side=RIGHT)


    # second button to enter matrix from file
    def NewWindowButton2():
        second_button = Toplevel(window)
        second_button.title("Gotowa macierz")
        second_button.geometry("300x200")
        second_button.iconbitmap('./cash_icon.ico')

        # open file from the computer
        def openFile():
            global matrix_
            tf = tk.filedialog.askopenfilename(
                initialdir="C:/Users/MainFrame/Desktop/",
                title="Open Text file",
                filetypes=(("Text Files", "*.txt"),)
            )

            with open(tf, 'r') as f:
                matrix_ = [[int(num) for num in line.split(',')] for line in f]

            matrix_ = np.array(matrix_)
            cols_m = np.sum(matrix_, axis=0)
            rows_m = np.sum(matrix_, axis=1)
            print(matrix_)
            Table(container1, matrix_, cols_m, rows_m, len(matrix_), len(matrix_[0]))

            second_button.destroy()
            newWindow.destroy()

        lab_2 = Label(second_button, text="Wybierz plik z komputera")
        lab_2.pack(padx=10, pady=5)
        Button(second_button, text="Open File", command=openFile).pack(fill='x', padx=20, pady=10)
        Button(second_button, text="Exit", command=lambda: second_button.destroy()).pack(fill='x', padx=20, pady=20)

    # third button to generate random matrix
    def NewWindowButton3():
        global matrix_
        third_button = Toplevel(window)
        third_button.title("Losowa macierz")
        third_button.geometry("300x300")
        third_button.iconbitmap('./cash_icon.ico')

        lab_3 = Label(third_button, text="Podaj właściowości macierzy")
        lab_3.pack(padx=10, pady=5)
        L1_m = Label(third_button, text="Maksymalna wartość: ")
        L1_m.pack(padx=5, pady=5, fill='x')
        E1_m = Entry(third_button)
        E1_m.pack(padx=5, pady=5, fill='x')
        L2_m = Label(third_button, text="Rozmiar osobnika")
        L2_m.pack(padx=5, pady=5, fill='x')
        E2_m = Entry(third_button)
        E2_m.pack(padx=5, pady=5, fill='x')

        def generate_matrix():
            global matrix_
            max_generated_value = int(E1_m.get())
            size_of_specimen = int(E2_m.get())

            if max_generated_value > max_value_of_spec or max_generated_value < min_value_of_spec:
                messagebox.showinfo("Warning", "Zła wartość")
                return
            if size_of_specimen > max_size_of_spec or size_of_specimen < min_size_of_spec:
                messagebox.showwarning("Warning", 'Zła wartość')
                return

            matrix_ = np.random.randint(low=0, high=max_generated_value, size=(size_of_specimen, size_of_specimen))
            np.fill_diagonal(matrix_, 0)

            S = specimen.Specimen(matrix_)
            print(matrix_)
            cols_m = np.sum(matrix_, axis=0)
            rows_m = np.sum(matrix_, axis=1)
            Table(container1, matrix_, cols_m, rows_m, len(matrix_), len(matrix_[0]))
            print("quality: ", S.quality(), "\n")
            third_button.destroy()
            newWindow.destroy()

        start_button_3 = tk.Button(third_button, text="Generuj macierz", command=generate_matrix)
        exit_button_3 = Button(third_button, text="Exit", command=lambda: third_button.destroy())
        start_button_3.pack(padx=40, side=LEFT)
        exit_button_3.pack(padx=40, side=RIGHT)

    btn1 = tk.Button(newWindow, text="Własna macierz", command=NewWindowButton1)
    btn1.config(height=5, width=40)
    btn1.pack(padx=5, pady=5, expand=True)
    btn2 = tk.Button(newWindow, text="Gotowa macierz", command=NewWindowButton2)
    btn2.config(padx=5, pady=5, height=5, width=40)
    btn2.pack(expand=True)
    btn3 = tk.Button(newWindow, text="Losowa macierz", command=NewWindowButton3)
    btn3.config(padx=5, pady=5, height=5, width=40)
    btn3.pack(expand=True)


# property setting
btn = Button(lf, text="Inicjalizacja macierzy", command=openNewWindow)
btn.pack(pady=10)

itera = Label(lf, text="Liczba iteracji: ")
itera.pack(fill='x', padx=10, expand=True)
itera_entry = Entry(lf)
itera_entry.pack(fill='x', padx=10, expand=True)

lf2 = ttk.LabelFrame(lf, text='Populacja')
lf2.pack(fill='x', padx=10, pady=20)

value_frame = ttk.Frame(lf2)
value_frame.pack(padx=10, pady=10, fill='x', expand=True)

L1 = Label(value_frame, text="Rozmiar populacji: ")
L1.pack(fill='x', expand=True)
E1 = Entry(value_frame)
E1.pack(fill='x', expand=True)
L2 = Label(value_frame, text="Liczba krzyżowań")
L2.pack(fill='x', expand=True)
E2 = Entry(value_frame)
E2.pack(fill='x', expand=True)
L3 = Label(value_frame, text="Rozmiar mutacji")
L3.pack(fill='x', expand=True)

size_x = Label(value_frame, text="Liczba wierszy: ")
size_x.pack(fill='x', expand=True)
E3_1 = Entry(value_frame)
E3_1.pack(fill='x', expand=True)

size_y = Label(value_frame, text="Liczba kolumn: ")
size_y.pack(fill='x', expand=True)
E3 = Entry(value_frame)
E3.pack(fill='x', expand=True)

L4 = Label(value_frame, text="Liczba mutacji")
L4.pack(fill='x', expand=True)
E4 = Entry(value_frame)
E4.pack(fill='x', expand=True)

CheckVar1 = IntVar()
C1 = Checkbutton(lf2, text="Elita", variable=CheckVar1, onvalue=1, offvalue=0)
C1.pack(padx=10, pady=5, fill='x', expand=True)

lf1 = ttk.LabelFrame(lf, text='Metoda selekcji')
lf1.pack(padx=10)

selected_method = tk.IntVar()
selections = ('roulette', 'ranking', 'tournament')

def sel():
    global selection_
    chose_value = selected_method.get()
    if chose_value == 1:
        selection_ = 'roulette'
    elif chose_value == 2:
        selection_ = 'ranking'
    elif chose_value == 3:
        selection_ = 'tournament'
    else:
        selection_ = 'roulette'

grid_column = 0
for method in selections:
    # create a radio button
    radio = ttk.Radiobutton(lf1, text=method, value=grid_column+1, variable=selected_method, command=sel)
    radio.grid(column=grid_column, row=0, ipadx=10, ipady=10)
    # grid column
    grid_column += 1

def start_algorithm():
    global matrix_
    elite_ = None

    size_population_ = int(E1.get())
    if size_population_ > 50 or size_population_ < 1:
        messagebox.showinfo("Warning", "Zły rozmiar populacji. Max:50, Min:1")
        return

    number_mutation_ = int(E4.get())
    if number_mutation_ > 50 or number_mutation_ < 1:
        messagebox.showinfo("Warning", "Zła liczba mutacji. Max: 50, Min:1")
        return

    number_crossover_ = int(E2.get())
    if number_crossover_ > 50 or number_crossover_ < 1:
        messagebox.showinfo("Warning", "Zła liczba krzyżowania. Max: 50, Min:1")
        return

    if C1 == 1:
        elite_ = True
    else:
        elite_ = False

    iteration_ = int(itera_entry.get())
    if iteration_ > 10000 or iteration_ < 1:
        messagebox.showinfo("Warning", "Zła liczba iteracji. Max: 10000, Min:1")
        return

    mut_size_x = int(E3.get())
    mut_size_y = int(E3_1.get())

    if mut_size_y > len(matrix_[0])//2 or mut_size_y < 1:
        messagebox.showinfo("Warning", "Zły rozmiar mutacji. Max: liczba wierszy/2, Min:1")
        return

    if mut_size_x > len(matrix_[0])//2 or mut_size_x < 1:
        messagebox.showinfo("Warning", "Zły rozmiar mutacji. Max: liczba kolumn/2, Min:1")
        return

    size_of_mutation_ = [mut_size_x, mut_size_y]

    start = time.time()
    best_Specimen = evolutionaryAlgorithm.EvolutionaryAlgorithm(primitive_specimen=matrix_,
                                                                size_of_population=size_population_,
                                                                iterations=iteration_,
                                                                # time=,
                                                                # size_of_elite=,
                                                                number_of_mutations=number_mutation_,
                                                                size_of_mutation=size_of_mutation_,
                                                                number_of_crossover=number_crossover_,
                                                                selection_type=selection_)

    print("\nTime:    ", time.time() - start)

    best_Specimen_cols = np.sum(best_Specimen.matrix, axis=0)
    best_Specimen_rows = np.sum(best_Specimen.matrix, axis=1)

    Table(container2, best_Specimen.matrix, best_Specimen_cols, best_Specimen_rows, len(best_Specimen.matrix), len(best_Specimen.matrix[0]))

    # best_Specimen_cols = np.sum(best_Specimen.matrix, axis=0)
    # best_Specimen_rows = np.sum(best_Specimen.matrix, axis=1)

    # print("Valid:   ", (best_Specimen_cols == cols_).all() and (best_Specimen_rows == rows_).all())
    print("The best Specimen:")
    best_Specimen.display()


start_button = Button(lf, text="Start", command=start_algorithm)
start_button.pack(padx=10, pady=10, expand=True)


window.mainloop()
