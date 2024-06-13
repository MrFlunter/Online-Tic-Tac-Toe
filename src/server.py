import socket
import threading
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QMessageBox
from PyQt6.QtGui import QFont
import sys

class TicTacToeServer(QWidget):
    def __init__(self, host='localhost', port=12345, is_server=False, player='X'):
        super().__init__()
        self.host = host
        self.port = port
        self.is_server = is_server
        self.player = player
        self.opponent = 'O' 
        self.current_player = 'X'
        self.board = [''] * 9
        self.connected = False

        self.initUI()

        if self.is_server:
            self.start_server()
        else:
            self.start_client()

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

    def start_server(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.host, self.port))
        self.s.listen(1)
        threading.Thread(target=self.accept_connections, daemon=True).start()

    def accept_connections(self):
        print('Waiting for a connection...')
        self.conn, self.addr = self.s.accept()
        print(f'Connected by {self.addr}')
        self.connected = True
        threading.Thread(target=self.receive_data, args=(self.conn,), daemon=True).start()

    def start_client(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))
        self.connected = True
        threading.Thread(target=self.receive_data, args=(self.s,), daemon=True).start()

    def receive_data(self, sock):
        while self.connected:
            try:
                data = sock.recv(1024).decode()
                if data:
                    self.handle_server_message(data)
            except Exception as e:
                print(f'Error: {e}')
                self.connected = False

    def handle_server_message(self, message):
        print(message)
        if self.judge():
            QMessageBox.information(self, "Game Over", f"{self.opponent} wins!")
            self.reset_game()
        elif '' not in self.board:
            QMessageBox.information(self, "Game Over", "It's a draw!")
            self.reset_game()
        else:
            print(message)
            idx, player = message.split(',')
            idx = int(idx)
            self.board[idx] = player
            self.buttons[idx].setText(player)
            self.current_player = self.opponent if player == self.player else self.player

    def make_move(self, idx):
        def move():
            if not self.buttons[idx].text() and self.current_player == self.player:
                self.buttons[idx].setText(self.player)
                self.board[idx] = self.player
                self.send_move(idx)
                self.current_player = self.opponent
            if self.judge():
                QMessageBox.information(self, "Game Over", f"{self.player} wins!")
                self.reset_game()
            elif '' not in self.board:
                QMessageBox.information(self, "Game Over", "It's a draw!")
                self.reset_game()
        return move

    def send_move(self, idx):
        if self.is_server:
            self.conn.send(f'{idx},{self.current_player}'.encode())
        # else:
        #     self.s.send(f'{idx},{self.current_player}'.encode())

    def judge(self):
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6)]
        for cond in win_conditions:
            if self.board[cond[0]] == self.board[cond[1]] == self.board[cond[2]] != '':
                return True
        return False

    def reset_game(self):
        self.board = [''] * 9
        for button in self.buttons:
            button.setText('')
        self.current_player = 'X'

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Start as server (Player X) or client (Player O) based on user input
    #is_server = input('Start the server? (y/n): ').lower() == 'y'
    #player = 'X' if is_server else 'O'

    game = TicTacToeServer(is_server=True, player='X')
    sys.exit(app.exec())
