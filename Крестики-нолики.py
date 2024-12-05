import tkinter as tk
from tkinter import messagebox
import random


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Крестики-Нолики")
        self.center_window(340, 350)

        # Переменные для отслеживания состояния игры
        self.current_player = "X"  # Игрок
        self.bot_player = "O"  # Бот
        self.board = [""] * 9
        self.buttons = []

        # Создание кнопок для игрового поля
        self.create_buttons()

        # Кнопка для сброса игры
        self.reset_button = tk.Button(root, text="Сбросить", command=self.reset_game)
        self.reset_button.grid(row=3, column=0, columnspan=3)

        # Информация о текущем игроке
        self.info_label = tk.Label(root, text=f"Текущий игрок: {self.current_player}", font=("Arial", 14))
        self.info_label.grid(row=4, column=0, columnspan=3)

    def center_window(self, width, height):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.geometry(f'{width}x{height}+{x}+{y}')


    def create_buttons(self):
        """Создание кнопок для игрового поля."""
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self.root, text="", font=("Arial", 24), width=5, height=2,
                                   command=lambda index=i * 3 + j: self.player_move(index))
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)

    def player_move(self, index):
        """Обрабатывает ход игрока и обновляет состояние игры."""
        if self.board[index] == "" and not self.check_winner():
            self.board[index] = self.current_player
            self.buttons[index // 3][index % 3].config(text=self.current_player)
            if self.check_winner():
                messagebox.showinfo("Игра окончена", f"Игрок {self.current_player} выиграл!")
                return
            elif "" not in self.board:
                messagebox.showinfo("Игра окончена", "Ничья!")
                return
            else:
                # Меняем игрока на бота
                self.current_player = self.bot_player
                self.update_info()
                self.bot_move()

    def bot_move(self):
        """Ход бота."""
        index = self.best_move()
        if index is not None:
            self.board[index] = self.bot_player
            self.buttons[index // 3][index % 3].config(text=self.bot_player)
            if self.check_winner():
                messagebox.showinfo("Игра окончена", f"Бот {self.bot_player} выиграл!")
            elif "" not in self.board:
                messagebox.showinfo("Игра окончена", "Ничья!")
            else:
                # Меняем бота обратно на человека
                self.current_player = "X"
                self.update_info()

    def best_move(self):
        """Находит лучший ход для бота, даже на пустой доске."""
        if "" not in self.board: # проверка на заполненность
            return None

        # Выигрышный ход (первым)
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = self.bot_player
                if self.check_winner():
                    self.board[i] = ""
                    return i
                self.board[i] = ""

        # Блокировка выигрыша игрока (первым)
        if self.board[4] == "": #Центр доски - стратегически важный
            return 4  # Захват центра на первом ходу

        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "X"  # Игрок ходит "X"
                if self.check_winner():
                    self.board[i] = ""
                    return i
                self.board[i] = ""

        # Если ни выигрышного хода, ни блокировки нет, выбираем угол или край
        corners = [0, 2, 6, 8]
        edges = [1, 3, 5, 7]
        available_corners = [c for c in corners if self.board[c] == ""]
        available_edges = [e for e in edges if self.board[e] == ""]

        if available_corners:
            return random.choice(available_corners)
        elif available_edges:
            return random.choice(available_edges)
        else: #Should never happen because we checked if board is full
            return None

    def check_winner(self):
        """Проверяет наличие победителя."""
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # строки
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # столбцы
            (0, 4, 8), (2, 4, 6)              # диагонали
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != "":
                return True
        return False

    def reset_game(self):
        """Сбрасывает игру к начальному состоянию."""
        self.board = [""] * 9
        for row in self.buttons:
            for button in row:
                button.config(text="")
        self.current_player = "X"
        self.update_info()

    def update_info(self):
        """Обновляет информацию о текущем игроке."""
        self.info_label.config(text=f"Текущий игрок: {self.current_player}")


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
