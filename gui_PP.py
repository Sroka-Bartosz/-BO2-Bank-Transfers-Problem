#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading

import functions
import population
import time
import timeit
from typing import List
import numpy as np

# global variables
matrix_ = None
selection_ = 'roulette'

max_size_of_spec = 30
min_size_of_spec = 4
max_value_of_spec = 500
min_value_of_spec = 1

# create a window
window = tk.Tk()
window.title('Problem przelewowy')
window.geometry('1000x600')
# window.resizable(False, False)
window.iconbitmap('./cash_icon.ico')

# create a notebook
notebook = ttk.Notebook(window, width=690, height=530)
notebook.pack(fill='x', pady=5, side='left', expand=True)

container1 = ttk.Frame(notebook, width=690, height=530)
container2 = ttk.Frame(notebook, width=690, height=530)

# create frames
frame3 = ttk.Frame(notebook, width=690, height=530)
frame3.pack(fill='x', expand=True)
frame4 = ttk.Frame(notebook, width=690, height=530)
frame4.pack(fill='x', expand=True)

# add frames to notebook
notebook.add(container1, text='Macierz początkowa')
notebook.add(container2, text='Wynik')
notebook.add(frame4, text='Wynik 2')
notebook.add(frame3, text='Przebieg algorytmu')

# Create label frame
lf = ttk.LabelFrame(window, text='Właściwości')
lf.pack(padx=10, pady=20)


def EvolutionaryAlgorithm(
        primitive_specimen,
        size_of_population: int = 20,
        iterations: int = 50,
        time_: int = 1000,
        size_of_elite: int = 1,
        number_of_mutations: int = 0,
        size_of_mutation: List = [2, 2],
        number_of_crossover: int = 0,
        selection_type: str = "roulette"):
    time_ea, i = 0, 1
    pb1['value'] = 0
    # initialize of population
    population_ = population.Population(size=size_of_population)
    population_.make_population(primitive_specimen)

    # choose first best specimen from initial population
    best_specimen_ = population_.specimens[0]

    # create elite
    population_.create_elite(size_of_elite=size_of_elite)

    # run i iterations of algorithm
    while i <= iterations:
        pb1['value'] += 100 / iterations
        window.update_idletasks()
        # mutation
        [population_.mutation(size_of_mutation[0], size_of_mutation[1]) for i in range(number_of_mutations)]

        # crossover
        [population_.crossover() for i in range(number_of_crossover)]

        # selection
        population_.selection(selection_type=selection_type)

        # update elite if better specimen in population
        population_.update_elite()

        # print quality changes
        # population_.display_elite_quality()
        # population_.display_population_quality()
        population_.display_quality_changes(i)

        # get new best specimen
        if population_.best_specimen().quality() > population_.best_quality:
            best_specimen_ = population_.best_specimen()
            population_.best_quality = best_specimen_.quality()

        # time stop condition
        time_ea += timeit.timeit()
        if time_ea >= time_:
            break
        i += 1

    return best_specimen_, population_.global_quality


# Create a class to print matrix
class Table:
    def __init__(self, root, matrix, cols, rows, total_rows, total_columns, program_time=None):

        canvas = tk.Canvas(root)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        for i in range(total_rows):
            for j in range(total_columns):
                self.e = tk.Label(scrollable_frame, width=5, text=str(matrix[i][j]))
                self.e.grid(row=i, column=j, sticky='ns')

            la = tk.Label(scrollable_frame, width=5, bg="gray51", text=str(rows[i]))
            la.grid(row=i, column=total_columns + 1, sticky='ns')

        for x in range(total_columns):
            la1 = tk.Label(scrollable_frame, width=5, bg="gray51", text=str(cols[x]))
            la1.config(bg="gray")
            la1.grid(row=total_rows + 1, column=x, sticky='ns')

        if program_time:
            dis_time = tk.Label(root, text="Czas wykonania programu: " + str(program_time))
            dis_time.config(font=("Courier", 10))
            dis_time.pack(padx=10, pady=10, side=BOTTOM)

        quality_temp = total_rows * total_columns - np.count_nonzero(matrix == 0)
        dis_quality = tk.Label(root, text="Wartość funkcji celu: " + str(quality_temp))
        dis_quality.config(font=("Courier", 10))
        dis_quality.pack(padx=10, pady=10, side=BOTTOM)

        scroll = Scrollbar(root, orient="vertical", command=canvas.yview)
        scroll2 = Scrollbar(root, orient="horizontal", command=canvas.xview)
        canvas.configure(yscrollcommand=scroll.set, xscrollcommand=scroll2.set)

        scroll.pack(fill='y', side=RIGHT)
        scroll2.pack(fill='x', side=BOTTOM)
        canvas.pack(side=LEFT, expand=True, fill='both')


def display_score(matrix):
    canvas = tk.Canvas(frame4)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    row_to = 0
    for i in range(len(matrix)):
        person = tk.Label(scrollable_frame, text=f"Osoba {i + 1}", font=("Helvetica", 12))
        person.grid(row=row_to, column=0)
        for j in range(len(matrix[0])):
            if matrix[i][j] != 0:
                to_person = tk.Label(scrollable_frame, text=f" -> Osoba {j + 1} : {matrix[i][j]} zł",
                                     font=("Helvetica", 12))
                to_person.grid(row=row_to, column=1)
                row_to += 1

    scroll = Scrollbar(frame4, orient="vertical", command=canvas.yview)
    scroll2 = Scrollbar(frame4, orient="horizontal", command=canvas.xview)
    canvas.configure(yscrollcommand=scroll.set, xscrollcommand=scroll2.set)

    scroll.pack(fill='y', side=RIGHT)
    scroll2.pack(fill='x', side=BOTTOM)
    canvas.pack(side=LEFT, expand=True, fill='both')


# function to create new window
def openNewWindow():
    for widgets in container1.winfo_children():
        widgets.destroy()
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
        temp_frame_1 = Frame(first_button)
        temp_frame_1.pack(padx=10, pady=10, fill='x')
        size_x_m = Label(temp_frame_1, text="Liczba wierszy: ")
        size_x_m.pack(padx=10, pady=5, fill='x', side=LEFT)
        size_1 = Entry(temp_frame_1)
        size_1.pack(padx=10, pady=5, fill='x')

        temp_frame_2 = Frame(first_button)
        temp_frame_2.pack(padx=10, pady=10, fill='x')
        size_y_m = Label(temp_frame_2, text="Liczba kolumn: ")
        size_y_m.pack(padx=10, pady=5, fill='x', side=LEFT)
        size_2 = Entry(temp_frame_2)
        size_2.pack(padx=10, pady=5, fill='x')

        def create_matrix():
            cre_matrix = Toplevel(window)
            cre_matrix.iconbitmap('./cash_icon.ico')
            cre_matrix.title("Tworzenie własnej macierzy")
            matrix_size_x = int(size_1.get())
            matrix_size_y = int(size_2.get())

            if matrix_size_x > 300 or matrix_size_x < 4:
                messagebox.showwarning("Warning", "Zły rozmiar macierzy. Max: 300, Min: 4 ")
                cre_matrix.destroy()
                return

            if matrix_size_y > 300 or matrix_size_y < 4:
                messagebox.showwarning("Warning", "Zły rozmiar macierzy. Max: 300, Min: 4 ")
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
                            x = int(values[i_x * matrix_size_y + j_x])
                            matrix_[i_x][j_x] = x

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
            b.grid(row=(matrix_size_x + 1), column=(matrix_size_y - 1) // 2 - 1, columnspan=3, sticky=E + W)

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
        L2_m = Label(third_button, text="Rozmiar osobnika: ")
        L2_m.pack(padx=5, pady=5, fill='x')
        E2_m = Entry(third_button)
        E2_m.pack(padx=5, pady=5, fill='x')
        L1_m = Label(third_button, text="Maksymalna wartość: ")
        L1_m.pack(padx=5, pady=5, fill='x')
        E1_m = Entry(third_button)
        E1_m.pack(padx=5, pady=5, fill='x')
        L3_m = Label(third_button, text="Gęstości macierzy: ")
        L3_m.pack(padx=5, pady=5, fill='x')
        E3_m = Entry(third_button)
        E3_m.pack(padx=5, pady=5, fill='x')

        def generate_matrix():
            global matrix_
            max_generated_value = int(E1_m.get())
            size_of_specimen = int(E2_m.get())
            density = int(E3_m.get())

            if max_generated_value > max_value_of_spec or max_generated_value < min_value_of_spec:
                messagebox.showinfo("Warning", "Zła wartość. Max: 500, Min: 1")
                return
            if size_of_specimen > max_size_of_spec or size_of_specimen < min_size_of_spec:
                messagebox.showwarning("Warning", 'Zły rozmiar. Max: 30, Min: 4')
                return
            if density > 100 or density < 10:
                messagebox.showwarning("Warning", 'Zły wartość. Max: 100, Min: 10')
                return

            matrix_ = functions.generate_initial_matrix(max_generated_value, size_of_specimen, density)

            cols_m = np.sum(matrix_, axis=0)
            rows_m = np.sum(matrix_, axis=1)
            Table(container1, matrix_, cols_m, rows_m, len(matrix_), len(matrix_[0]))

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
temp_frame_mu = Frame(value_frame)
temp_frame_mu.pack(fill='x')
E3_1 = Entry(temp_frame_mu, width=10)
E3_1.pack(fill='x', side=LEFT, expand=True)
lab_x = Label(temp_frame_mu, text='x')
lab_x.pack(padx=10, side=LEFT)
E3 = Entry(temp_frame_mu, width=10)
E3.pack(fill='x', side=LEFT, expand=True)

L4 = Label(value_frame, text="Liczba mutacji")
L4.pack(fill='x', expand=True)
E4 = Entry(value_frame)
E4.pack(fill='x', expand=True)


def is_checked():
    if CheckVar1.get() == 1:
        elite_si.config(state='normal')
    elif CheckVar1.get() == 0:
        elite_si.config(state='disabled')
    else:
        messagebox.showerror('PythonGuides', 'Something went wrong!')


CheckVar1 = IntVar()
C1 = Checkbutton(lf2, text="Elita", variable=CheckVar1, onvalue=1, offvalue=0, command=is_checked)
C1.pack(padx=10, pady=5, fill='x', expand=True)
elite_si = Entry(lf2)
elite_si.config(state='disabled')
elite_si_lab = Label(lf2, text="Rozmiar elity: ")
elite_si_lab.pack(side=LEFT)
elite_si.pack(padx=10, pady=5, side=BOTTOM)

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
    radio = ttk.Radiobutton(lf1, text=method, value=grid_column + 1, variable=selected_method, command=sel)
    radio.grid(column=grid_column, row=0, ipadx=10, ipady=10)

    grid_column += 1


def plot_quality(plot_quality_, matrix_size):
    iteration_ = int(itera_entry.get())
    figure1 = plt.Figure(figsize=(6, 5))
    a = figure1.add_subplot(111)
    size_ = max(matrix_size[0], matrix_size[1]) ** 2
    x_axis = [0]
    y_axis = [size_]
    for quali in plot_quality_:
        x_axis.append(quali[0])
        y_axis.append(size_ - quali[1])
    x_axis.append(iteration_)
    y_axis.append(size_ - plot_quality_[-1][1])

    a.step(x_axis, y_axis)
    a.set_ylabel("Jakość najlepszego rozwiązania")
    a.set_xlabel("Numer iteracji")
    a.set_title("")
    a.grid()
    line1 = FigureCanvasTkAgg(figure1, frame3)
    line1.get_tk_widget().pack()
    line1.draw()


def clear_frame():
    for widgets in frame3.winfo_children():
        widgets.destroy()
    for widgets in container2.winfo_children():
        widgets.destroy()
    for widgets in frame4.winfo_children():
        widgets.destroy()


def start_algorithm():
    clear_frame()
    global matrix_
    size_of_elite = 0
    size_population_ = int(E1.get())

    if matrix_ is None:
        messagebox.showinfo("Warning", "Macierz początkowa nie jest zdefiniowana!")
        return

    if size_population_ > 50 or size_population_ < 1:
        messagebox.showinfo("Warning", "Zły rozmiar populacji. Max:50, Min:1")
        return

    number_mutation_ = int(E4.get())
    if number_mutation_ > 50 or number_mutation_ < 0:
        messagebox.showinfo("Warning", "Zła liczba mutacji. Max: 50, Min:0")
        return

    number_crossover_ = int(E2.get())
    if number_crossover_ > 50 or number_crossover_ < 0:
        messagebox.showinfo("Warning", "Zła liczba krzyżowania. Max: 50, Min:0")
        return

    if CheckVar1.get() == 1:
        size_of_elite = int(elite_si.get())
    else:
        size_of_elite = 0

    iteration_ = int(itera_entry.get())
    if iteration_ > 10000 or iteration_ < 1:
        messagebox.showinfo("Warning", "Zła liczba iteracji. Max: 10000, Min:1")
        return

    mut_size_y = int(E3.get())
    mut_size_x = int(E3_1.get())

    if mut_size_x > len(matrix_) // 2 or mut_size_x < 2:
        messagebox.showinfo("Warning", f"Zły rozmiar mutacji. Max: {len(matrix_) // 2}, Min:2")
        return

    if mut_size_y > len(matrix_[0]) // 2 or mut_size_y < 2:
        messagebox.showinfo("Warning", f"Zły rozmiar mutacji. Max: {len(matrix_[0]) // 2}, Min:2")
        return

    if mut_size_x > min(mut_size_x, mut_size_y) or mut_size_y > min(mut_size_x, mut_size_y):
        messagebox.showinfo("Warning",
                            f"Zły rozmiar mutacji. Max: {min(mut_size_x, mut_size_y)}x{min(mut_size_x, mut_size_y)}")
        return

    size_of_mutation_ = [mut_size_x, mut_size_y]

    start = time.time()
    best_Specimen, quality_ = EvolutionaryAlgorithm(primitive_specimen=matrix_,
                                                    size_of_population=size_population_,
                                                    iterations=iteration_,
                                                    # time=,
                                                    size_of_elite=size_of_elite,
                                                    number_of_mutations=number_mutation_,
                                                    size_of_mutation=size_of_mutation_,
                                                    number_of_crossover=number_crossover_,
                                                    selection_type=selection_)

    time_count = time.time() - start

    best_Specimen_cols = np.sum(best_Specimen.matrix, axis=0)
    best_Specimen_rows = np.sum(best_Specimen.matrix, axis=1)

    best_Specimen.matrix = functions.delete_unexpected_rows_cols(best_Specimen.matrix)
    Table(container2, best_Specimen.matrix, best_Specimen_cols, best_Specimen_rows, len(best_Specimen.matrix),
          len(best_Specimen.matrix[0]), time_count)
    display_score(best_Specimen.matrix)

    plot_quality(quality_, best_Specimen.matrix.shape)
    print("The best Specimen:")
    best_Specimen.display()


start_button = Button(lf, text="Start", command=start_algorithm)
start_button.pack(padx=10, pady=10, expand=True)
pb1 = Progressbar(window, orient=HORIZONTAL, length=285, mode='determinate')
pb1.pack()
window.mainloop()
