import socket
import threading
from tic_tac_toe import TicTacToe
from PyQt6.QtWidgets import QApplication, QMessageBox
import sys

class TicTacToeClient(TicTacToe):
    def __init__(self, host='localhost', port=12345, player='O'):
        super().__init__()
        self.host = host
        self.port = port
        self.player = player
        self.opponent = 'X' 
        self.connected = False
        self.current_player = player
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))
        self.connected = True

        threading.Thread(target=self.receive_data, daemon=True).start()

    def receive_data(self):
        while self.connected:
            try:
                data = self.s.recv(1024).decode()
                if data:
                    self.handle_server_message(data)
            except Exception as e:
                print(f'Error: {e}')
                self.connected = False
                return 

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
            if player == self.opponent:
                self.current_player = self.player
            else:
                self.current_player = self.opponent

    def make_move(self, idx):
        def move():
            #print(self.current_player, self.player) 
            if not self.buttons[idx].text() and self.current_player == self.player:
                self.buttons[idx].setText(self.player)
                self.board[idx] = self.player
                self.s.send((str(idx)+','+self.current_player).encode())
                self.current_player = self.opponent
            if self.judge():
                QMessageBox.information(self, "Game Over", f"{self.player} wins!")
                self.reset_game()
            elif '' not in self.board:
                QMessageBox.information(self, "Game Over", "It's a draw!")
                self.reset_game()
        return move

    def reset_game(self):
        self.board = ['']*9
        for button in self.buttons:
            button.setText('')
        self.current_player = 'O'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = TicTacToeClient(player='O')  
    sys.exit(app.exec())
