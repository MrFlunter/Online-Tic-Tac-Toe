import socket
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QMessageBox
from PyQt6.QtGui import QFont 

class TicTacToe(QWidget):
    def __init__(self, playername):
        super().__init__()
        self.playername = playername
        self.initUI()
        self.board = ['']*9
        self.current_player = 'X'
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def initUI(self):
        self.setWindowTitle('Tic Tac Toe')
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.buttons = []
        for i in range(9):
            button = QPushButton('')
            font = QFont()
            font.setPointSize(25)
            button.setFont(font)
            button.setFixedSize(100, 100)
            button.clicked.connect(self.make_move(i))
            self.grid.addWidget(button, i // 3, i % 3)
            self.buttons.append(button)
        self.show()

    def make_move(self, idx):
        def move():
            if not self.buttons[idx].text(): 
                self.buttons[idx].setText(self.current_player)
                self.board[idx] = self.current_player
                if self.judge():
                    QMessageBox.information(self, "Game Over", f"{self.current_player} wins!")
                    self.reset_game()
                elif '' not in self.board:
                    QMessageBox.information(self, "Game Over", "It's a draw!")
                    self.reset_game()
                self.current_player = 'O' if self.current_player == 'X' else 'X'
        return move

    def judge(self):
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6)]
        for cond in win_conditions:
            if self.board[cond[0]] == self.board[cond[1]] == self.board[cond[2]] != '':
                return True
        return False

    def reset_game(self):
        self.board = ['']*9 
        for button in self.buttons:
            button.setText('')

"""
    def run_player(self):
        host = '127.0.0.1'
        port = 12345
        self.s.bind((host, port))
        self.s.listen(1)
        conn, addr = self.s.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                self.handle_data(data.decode())

    def handle_data(self, data):
        idx, player = map(str, data.split(','))
        idx = int(idx)
        self.board[idx] = player
        self.buttons[idx].setText(player)
        if self.judge():
            QMessageBox.information(self, "Game Over", f"{player} wins!")
            self.reset_game()
        elif '' not in self.board:
            QMessageBox.information(self, "Game Over", "It's a draw!")
            self.reset_game()
        self.current_player = 'O' if player == 'X' else 'X'
"""
