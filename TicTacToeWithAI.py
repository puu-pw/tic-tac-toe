import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = ""  
        self.game_over = False
        
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(root, text=" ", font=("Arial", 20), width=5, height=2,
                                               command=lambda i=i, j=j: self.player_move(i, j))
                self.buttons[i][j].grid(row=i, column=j)
        
        
        self.choose_symbol()

    def choose_symbol(self):
        symbol = messagebox.askquestion("Pick your starting phase", "Do you want to play first?")
        if symbol == "yes":
            self.current_player = "X"
        else:
            self.current_player = "O"
            self.ai_move()  
    
    def player_move(self, row, col):
        if self.current_player == "" or self.game_over:
            return
        
        if self.board[row][col] == " ":
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            
            if self.check_winner(self.board):
                self.end_game(f"Player {self.current_player} wins!")
            elif self.is_full(self.board):
                self.end_game("It's a tie!")
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                if self.current_player == "O":
                    self.ai_move()
    
    def ai_move(self):
        if self.current_player == "" or self.game_over:
            return
        
        move = self.find_best_move()
        if move:
            self.board[move[0]][move[1]] = "O"
            self.buttons[move[0]][move[1]].config(text="O")
        
        if self.check_winner(self.board):
            self.end_game("AI wins!")
        elif self.is_full(self.board):
            self.end_game("It's a tie!")
        else:
            self.current_player = "X"
    
    def find_best_move(self):
        best_val = -float('inf')
        best_move = None
        
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    self.board[i][j] = "O"
                    move_val = self.minimax(self.board, 0, False)
                    self.board[i][j] = " "
                    if move_val > best_val:
                        best_move = (i, j)
                        best_val = move_val
        return best_move

    def minimax(self, board, depth, is_max):
        score = self.evaluate(board)

        if score == 10:
            return score - depth

        if score == -10:
            return score + depth

        if self.is_full(board):
            return 0

        if is_max:
            best = -float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == " ":
                        board[i][j] = "O"
                        best = max(best, self.minimax(board, depth + 1, not is_max))
                        board[i][j] = " "
            return best
        else:
            best = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == " ":
                        board[i][j] = "X"
                        best = min(best, self.minimax(board, depth + 1, not is_max))
                        board[i][j] = " "
            return best

    def evaluate(self, board):
        for row in range(3):
            if board[row][0] == board[row][1] == board[row][2]:
                if board[row][0] == "O":
                    return 10
                elif board[row][0] == "X":
                    return -10

        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col]:
                if board[0][col] == "O":
                    return 10
                elif board[0][col] == "X":
                    return -10

        if board[0][0] == board[1][1] == board[2][2]:
            if board[0][0] == "O":
                return 10
            elif board[0][0] == "X":
                return -10

        if board[0][2] == board[1][1] == board[2][0]:
            if board[0][2] == "O":
                return 10
            elif board[0][2] == "X":
                return -10

        return 0
    
    def check_winner(self, board):
        score = self.evaluate(board)
        if score == 10 or score == -10:
            return True
        return False
    
    def is_full(self, board):
        for row in board:
            if " " in row:
                return False
        return True
    
    def end_game(self, message):
        messagebox.showinfo("Tic-Tac-Toe", message)
        self.reset_board()
    
    def reset_board(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=" ")
        self.current_player = ""
        self.game_over = False
        
        
        self.choose_symbol()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
