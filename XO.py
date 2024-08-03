import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QMessageBox
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
from random import randrange

class TicTacToe(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()
        self.board = [[3 * j + i + 1 for i in range(3)] for j in range(3)]
        self.board[1][1] = 'X'
        self.human_turn = True
        self.update_buttons()

    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.setWindowTitle('Tic Tac Toe')
        self.setStyleSheet("background-color: #f0f0f0;")
        self.buttons = [[QPushButton('') for _ in range(3)] for _ in range(3)]

        for row in range(3):
            for col in range(3):
                self.buttons[row][col].setFixedSize(100, 100)
                self.buttons[row][col].clicked.connect(self.make_move)
                self.grid.addWidget(self.buttons[row][col], row, col)
                self.buttons[row][col].setStyleSheet("""
                    QPushButton {
                        font-size: 24px;
                        background-color: #ffffff;
                        border: 1px solid #cccccc;
                    }
                    QPushButton:pressed {
                        background-color: #cccccc;
                    }
                """)

        self.setGeometry(300, 300, 320, 320)
        self.show()

    @pyqtSlot()
    def make_move(self):
        button = self.sender()
        idx = self.grid.indexOf(button)
        row, col = divmod(idx, 3)

        if self.board[row][col] in ['X', 'O']:
            QMessageBox.information(self, "Invalid Move", "This field is already occupied.")
            return

        if self.human_turn:
            self.board[row][col] = 'O'
            self.buttons[row][col].setStyleSheet("""
                QPushButton {
                    font-size: 24px;
                    background-color: #ffcccc;
                    border: 1px solid #ff6666;
                }
            """)
            self.human_turn = False
        self.update_buttons()
        
        victor = self.victory_for('O')
        if victor:
            self.end_game("You won!")
            return

        self.computer_move()
        self.update_buttons()
        
        victor = self.victory_for('X')
        if victor:
            self.end_game("Computer wins!")
            return

    def update_buttons(self):
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 'X':
                    self.buttons[row][col].setText('X')
                    self.buttons[row][col].setStyleSheet("""
                        QPushButton {
                            font-size: 24px;
                            background-color: #ccccff;
                            border: 1px solid #6666ff;
                        }
                    """)
                elif self.board[row][col] == 'O':
                    self.buttons[row][col].setText('O')
                else:
                    self.buttons[row][col].setText('')

    def make_list_of_free_fields(self):
        free = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] not in ['O', 'X']:
                    free.append((row, col))
        return free

    def victory_for(self, sgn):
        cross1 = cross2 = True
        for rc in range(3):
            if self.board[rc][0] == sgn and self.board[rc][1] == sgn and self.board[rc][2] == sgn:
                return True
            if self.board[0][rc] == sgn and self.board[1][rc] == sgn and self.board[2][rc] == sgn:
                return True
            if self.board[rc][rc] != sgn:
                cross1 = False
            if self.board[rc][2 - rc] != sgn:
                cross2 = False
        if cross1 or cross2:
            return True
        return False

    def computer_move(self):
        free = self.make_list_of_free_fields()
        if free:
            this = randrange(len(free))
            row, col = free[this]
            self.board[row][col] = 'X'
            self.human_turn = True

    def end_game(self, message):
        # Create a QMessageBox instance
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Game Over")
        
        # Load and set the image
        pixmap = QPixmap("comp.jpg")  # Make sure this file is in the same directory as your script
        msg_box.setIconPixmap(pixmap)
        
        # Set the message text
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.button(QMessageBox.Ok).setText("Close")
        
        # Show the message box
        msg_box.exec_()
        self.close()

def main():
    app = QApplication(sys.argv)
    ex = TicTacToe()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
