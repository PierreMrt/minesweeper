from random import randint
import pickle
import re
import os
from minesweeper import *


def unveil_around(self, row, column):
    for x in range(- 1, 2):
        for y in range(- 1, 2):
            Game.color(self, row + y, column + x)


def check_xy_axis(self, row, column, size, table):

    range_parameters1 = [(size - column, 1), (- column, - 1)]
    range_parameters2 = [(size - row, 1), (row, - 1)]
    for elt1 in range_parameters1:
        for x in range(0, elt1[0], elt1[1]):
            if table[row][column + x] == ' ':
                for elt2 in range_parameters2:
                    for y in range(0, elt2[0]):
                        cell = table[row + (y * elt2[1])][column + x]
                        if cell == ' ':
                            unveil_around(self, row + (y * elt2[1]), column + x)
                        else:
                            break

            else:
                break

    range_parameters1 = [(size - row, 1), (- row, - 1)]
    range_parameters2 = [(size - column, 1), (column, - 1)]
    for elt1 in range_parameters1:
        for y in range(0, elt1[0], elt1[1]):
            if table[row + y][column] == ' ':
                for elt2 in range_parameters2:
                    for x in range(0, elt2[0]):
                        cell = table[row + y][column + (x * elt2[1])]
                        if cell == ' ':
                            unveil_around(self, row + y, column + (x * elt2[1]))
                        else:
                            break

            else:
                break


# Table related functions
def nb_bombs(size):
    if size == 8:
        bombs = 10
    elif size == 12:
        bombs = 25
    elif size == 20:
        bombs = 60
    else:
        bombs = round(size + size / 4, 0)

    return bombs


def initialize_table(size, bombs, table):
    for i in range(size):
        table.append([' '] * size)

    # Bombs ('☼') placement
    i = 1
    while i <= bombs:
        x = randint(0, size - 1)
        y = randint(0, size - 1)
        if table[y][x] != '☼':
            table[y][x] = '☼'
            i += 1
        else:
            continue

    # Number of bombs around calculation
    y = 0
    for lines in table:
        x = 0
        for elt in lines:
            if elt == '☼':
                x += 1
                continue
            else:
                table[y][x] = str(count(x, y, table, size))
                x += 1
        y += 1

    return table


def count(x, y, table, size):
    """ Put a number on each cells.
        - This number corresponds to the number of adjacent bombs (aka: x) (also in diagonal)
        - When this number is 0, put a blank instead
    """
    nb = 0
    for i in range(-1, 2):
        for index in range(-1, 2):
            if x + i > size - 1 or x + i < 0 or y + index < 0 or index > size - 1:
                continue
            else:
                try:
                    if table[y + index][x + i] == '☼':
                        nb += 1
                except IndexError:
                    continue

    if nb == 0:
        nb = ' '

    return nb


# Score related functions
def read_score(size):
    with open(DIR_PATH + '/score/' + str(size), 'rb+') as score_file:
        my_pickler = pickle.Unpickler(score_file)
        list_score = my_pickler.load()

    return list_score


def check_high_scores(timer, size):
    if size == 8 or size == 12 or size == 20:
        try:
            list_score = read_score(size)
        except FileNotFoundError:
            list_score = []
            NamePopUp.write_score(list_score, size)
        except EOFError:
            list_score = []

        if len(list_score) == 0:
            NamePopUp(timer, list_score, size)
        else:
            for elt in list_score:
                if len(list_score) < 10 or timer < elt[1]:
                    NamePopUp(timer, list_score, size)


def show_high_scores():
    score_window = Tk()
    score_window.title('Scores')
    score_frame = Frame(score_window, borderwidth=15)
    score_frame.grid(row=0, column=0)

    label_title = Label(score_frame, text='Meilleurs scores de tous les temps', font="Verdana 10 underline")
    label_title.grid(row=0, columnspan=3, sticky=W+E+N+S, pady=5)

    ind_score_file = []
    for i, file in enumerate(os.listdir(DIR_PATH + "/score")):
        ind_score_file.append(int(file))

    for i, size in enumerate(sorted(ind_score_file, reverse=False)):
        try:
            list_score = read_score(size)
        except FileNotFoundError:
            list_score = []
        text = ''
        for index in range(0, 10):
            nb = index + 1
            try:
                text += f'{nb}. {list_score[index][0]}: {list_score[index][1]}\n'
            except IndexError:
                text += f'{nb}.\n'

        label_title = Label(score_frame, text=f'{size} x {size}')
        label_title.grid(row=1, column=i)
        label = Label(score_frame, text=text, justify=LEFT, relief=GROOVE, padx=10)
        label.grid(row=2, column=i)


    # try:
    #     list_score = read_score(size)
    # except FileNotFoundError:
    #     list_score = []
    # text = ''
    # for index in range(0, 10):
    #     nb = index + 1
    #     try:
    #         text += f'{nb}. {list_score[index][0]}: {list_score[index][1]}\n'
    #     except IndexError:
    #         text += f'{nb}.\n'
    #
    # label = Label(score_frame, text=text, justify=LEFT, relief=GROOVE, padx=10)
    # label.grid(row=index, column=0)
