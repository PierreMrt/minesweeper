from tkinter import *
from functions import *
import time
from functools import partial
import os
from winsound import *
import threading

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


class Interface(Frame):

    def __init__(self, size):
        # Options
        self.size = size
        self.bombs = nb_bombs(self.size)
        self.table = []

        # Main window creation
        self.main_window = Tk()
        self.main_window.title('Demineur extreme')
        # self.main_window.geometry('300x400')

        # Frames creation
        self.game_frame = Game(self.main_window, self.size, self.bombs)
        self.menu_frame = MenuFrame(self.main_window, self.game_frame, self.size)

        self.main_window.mainloop()


class MenuFrame(Frame):

    def __init__(self, main_window, game_frame, size):
        super(MenuFrame, self).__init__()
        self.main_window = main_window
        self.game_frame = game_frame

        # Creation of the frame for the file menu
        self.menu_frame = Frame(self.main_window)
        self.menu_frame.grid(row=0, column=0)

        self.size = size

        # Menu creation inside of menu_frame
        file_menu = Menubutton(self.menu_frame, text='≡ Menu', activebackground='grey', relief=RAISED)
        file_menu.grid(row=0, column=0)

        drop_down = Menu(file_menu, tearoff=False)
        drop_down_size = Menu(drop_down, tearoff=False)
        drop_down_score = Menu(drop_down, tearoff=False)

        # Create elements to put in drop_down_size
        drop_down_size.add_command(label='Petit: 8 x 8', command=partial(self.change_size, 8))
        drop_down_size.add_command(label='Moyen: 12 x 12', command=partial(self.change_size, 12))
        drop_down_size.add_command(label='Grand: 20 x 20', command=partial(self.change_size, 20))

        # Create elements to put in drop_down_score
        # drop_down_score.add_command(label='Petit: 8 x 8', command=partial(show_high_scores, 8))
        # drop_down_score.add_command(label='Moyen: 12 x 12', command=partial(show_high_scores, 12))
        # drop_down_score.add_command(label='Grand: 20 x 20', command=partial(show_high_scores, 20))

        # Create size submenu
        drop_down.add_cascade(label='Taille', menu=drop_down_size)

        # Create highscores submenu
        drop_down.add_command(label='Highscores', command=show_high_scores)

        drop_down.add_command(label='Restart', command=partial(self.change_size, self.size))

        file_menu.configure(menu=drop_down)

    def change_size(self, size):
        self.main_window.destroy()
        Interface(size)


class Game(Frame):

    def __init__(self, main_window, size, bombs):
        super(Game, self).__init__()
        self.main_window = main_window

        # Frame creation inside of main_window
        self.game_frame = Frame(self.main_window, borderwidth=10)
        self.game_frame.grid(row=1, column=0)

        # Creation of sub frame inside of game_frame
        self.info_frame = Frame(self.game_frame, borderwidth=5)
        self.info_frame.grid(row=0, column=0)

        self.table_frame = Frame(self.game_frame)
        self.table_frame.grid(row=1, column=0)
        self.pop_up_frame = Frame(self.game_frame)
        self.pop_up_frame.grid(row=2, column=0)

        # Declaration of variables used for the game
        self.table = []
        self.size = size
        self.bombs = bombs

        self.unveiled = 0
        self.revealed = []
        self.right_clicked = []

        self.timer = time.time()
        self.loss = False
        self.button_score = 0

        self.update_score()
        self.table_creation()

    def table_creation(self):
        self.table = initialize_table(self.size, self.bombs, self.table)

        for row in range(self.size):
            for column in range(self.size):
                button = Button(self.table_frame, text=' ', command=partial(self.button_left_click, row,
                                                                            column), width=2, height=1)
                button.grid(row=row, column=column)
                button.bind('<Button-3>', partial(self.button_right_click, row, column))

    def update_score(self):
        missing = int(self.bombs) - len(self.right_clicked)

        try:
            # If there is already a button, destroy it
            self.button_score.destroy()
        except AttributeError:
            pass

        self.button_score = Button(self.info_frame, text=f'Bombes restantes: {missing}', bg='lavender', relief=SUNKEN)
        self.button_score.grid(row=0, column=0)

    def button_left_click(self, row, column):
        if self.table[row][column] == '☼':
            for row in range(self.size + 1):
                for column in range(self.size):
                    self.loss = True
                    self.color(row, column)

            # Defeat pop-up
            self.pop_up()

        elif self.table[row][column] == ' ':
            check_xy_axis(self, row, column, self.size, self.table)

        else:
            self.color(row, column)

    def button_right_click(self, row, column, *args):

        if [row, column] not in self.right_clicked:
            self.right_clicked.append([row, column])
            text = '☺'

        elif [row, column] in self.right_clicked:
            self.right_clicked.remove([row, column])
            text = ' '

        button = Button(self.table_frame, text=text, command=partial(self.button_left_click, row, column), width=2, height=1)
        button.grid(row=row, column=column)
        button.bind('<Button-3>', partial(self.button_right_click, row, column))

        self.update_score()

    def color(self, row, column):

        if (row, column) not in self.revealed and 0 <= row < self.size and 0 <= column < self.size:
            bg = 'SystemButtonFace'
            try:
                cell = self.table[row][column]

                if cell == '☼':
                    fg = 'black'
                    bg = 'red'
                elif cell == ' ':
                    fg = 'grey'
                elif cell == '1':
                    fg = 'blue'
                elif cell == '2':
                    fg = 'green'
                elif cell == '3':
                    fg = 'red'
                elif cell == '4':
                    fg = 'navy'
                elif cell >= '5':
                    fg = 'red4'

                my_font = "{courier regular} 9 bold"
                button = Button(self.table_frame, text=self.table[row][column], bg=bg, foreground=fg, font=my_font,
                                relief=SUNKEN, width=2, height=1)
                try:
                    button.grid(row=row, column=column)
                except TclError:
                    pass

                self.revealed.append((row, column))

                self.unveiled += 1

                if self.loss:
                    pass

                else:
                    if self.unveiled == (self.size * self.size) - self.bombs:
                        # Victory pop-up
                        self.pop_up()
                        self.destroy()

            except IndexError:
                pass

        else:
            pass

    def pop_up(self):
        # Calculate time taken
        timer = time.time() - self.timer
        timer = (round(timer, 2))

        if self.loss:
            text = 'Enorme défaite'
            sound = 'loss_sound.wav'

        else:
            text = 'Glorieuse victoire !!\n' \
                   'Temps : ' + str(timer) + 's'
            sound = 'win_sound.wav'

        self.play_sound(sound)

        champ_label = Label(self.pop_up_frame, text=text)
        champ_label.grid(row=0, column=0)

        button = Button(self.pop_up_frame, text='restart', command=self.restart)
        button.grid(row=1, column=0)

        if not self.loss:
            check_high_scores(timer, self.size)

    @staticmethod
    def play_sound(sound):
        threading.Thread(target=(lambda: PlaySound(DIR_PATH + '/assets/' + sound, SND_FILENAME))).start()

    def restart(self):
        self.game_frame.destroy()
        self.game_frame = Game(self.main_window, self.size, self.bombs)


class NamePopUp(Frame):

    def __init__(self, timer, list_score, size):
        self.name_prompt = Tk()
        self.prompt_frame = Frame(self.name_prompt, borderwidth=10)
        self.prompt_frame.grid(row=0, column=0)

        self.label = Label(self.prompt_frame, text='Top 10 ! Dis moi ton nom:')
        self.label.grid(row=0, column=0)

        self.entry = Entry(self.prompt_frame)
        self.entry.grid(row=1, column=0)

        self.button = Button(self.prompt_frame, text='Ok', width=10, command=self.check_name)
        self.button.grid(row=2, column=0)

        self.name = 0
        self.size = size
        self.timer = timer
        self.list_score = list_score

        self.name_prompt.mainloop()

    def check_name(self):
        self.name = self.entry.get()
        expression = r'^[A-Za-z0-9 ]{3,10}$'

        if re.search(expression, self.name) is not None:
            self.name_prompt.destroy()
            self.add_score()
        else:
            self.entry.config(bg='red')
            self.label.config(text='Entre 3 et 8 lettres ou chiffres.')

        def add_score(self):
            self.list_score.append((self.name, self.timer))
            list_score = sorted(self.list_score, key=lambda tup: tup[1])
            if len(list_score) > 10:
                del list_score[-1]
            self.write_score(list_score, self.size)

    @staticmethod
    def write_score(list_score, size):
        with open(DIR_PATH + '/score/' + str(size), 'wb+') as score_file:
            my_pickler = pickle.Pickler(score_file)
            my_pickler.dump(list_score)


if __name__ == '__main__':
    default_size = 8
    interface = Interface(default_size)
