import sys
from src.tic_tac_toe import TicTacToe
from PyQt6.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TicTacToe("Player 1")
    sys.exit(app.exec())