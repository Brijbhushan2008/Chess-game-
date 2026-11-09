import tkinter as tk
from tkinter import messagebox

BOARD_SIZE = 8
SQUARE_SIZE = 80

LIGHT_COLOR = "#F0D9B5"
DARK_COLOR = "#B58863"
BG_COLOR = "#2E2E2E"
PANEL_COLOR = "#1E1E1E"
TEXT_COLOR = "#FFFFFF"
HIGHLIGHT_COLOR = "#FFD700"

UNICODE_PIECES = {
    "K": "♔", "Q": "♕", "R": "♖", "B": "♗", "N": "♘", "P": "♙",
    "k": "♚", "q": "♛", "r": "♜", "b": "♝", "n": "♞", "p": "♟",
}

class ChessGame:
    def __init__(self, root):
        self.root = root
        self.root.title("♟ Modern Python Chess")
        self.root.configure(bg=BG_COLOR)

        self.main_frame = tk.Frame(root, bg=BG_COLOR)
        self.main_frame.pack(padx=20, pady=20)

        self.canvas = tk.Canvas(self.main_frame,
                                width=BOARD_SIZE*SQUARE_SIZE,
                                height=BOARD_SIZE*SQUARE_SIZE,
                                highlightthickness=0,
                                bg=BG_COLOR)
        self.canvas.grid(row=0, column=0)

        self.side_panel = tk.Frame(self.main_frame, bg=PANEL_COLOR)
        self.side_panel.grid(row=0, column=1, padx=20, sticky="n")

        self.title_label = tk.Label(self.side_panel,
                                    text="♟ Chess Game",
                                    font=("Segoe UI", 18, "bold"),
                                    bg=PANEL_COLOR,
                                    fg=TEXT_COLOR)
        self.title_label.pack(pady=10)

        self.turn_label = tk.Label(self.side_panel,
                                   text="Turn: White",
                                   font=("Segoe UI", 14),
                                   bg=PANEL_COLOR,
                                   fg="#00FFAA")
        self.turn_label.pack(pady=5)

        self.history_box = tk.Text(self.side_panel,
                                   width=28,
                                   height=20,
                                   bg="#111111",
                                   fg=TEXT_COLOR,
                                   insertbackground=TEXT_COLOR,
                                   relief="flat",
                                   font=("Consolas", 10))
        self.history_box.pack(pady=10)

        self.turn = "white"
        self.drag_data = {"item": None, "row": None, "col": None}
        self.move_history = []
        self.last_move = None

        self.board = self.create_initial_board()
        self.draw_board()

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def create_initial_board(self):
        return [
            ["r","n","b","q","k","b","n","r"],
            ["p","p","p","p","p","p","p","p"],
            ["","","","","","","",""],
            ["","","","","","","",""],
            ["","","","","","","",""],
            ["","","","","","","",""],
            ["P","P","P","P","P","P","P","P"],
            ["R","N","B","Q","K","B","N","R"],
        ]

    def draw_board(self):
        self.canvas.delete("all")

        for row in range(8):
            for col in range(8):
                x1 = col * SQUARE_SIZE
                y1 = row * SQUARE_SIZE
                x2 = x1 + SQUARE_SIZE
                y2 = y1 + SQUARE_SIZE

                color = LIGHT_COLOR if (row + col) % 2 == 0 else DARK_COLOR
                self.canvas.create_rectangle(x1, y1, x2, y2,
                                             fill=color,
                                             outline=color)

                if self.last_move and (row, col) in self.last_move:
                    self.canvas.create_rectangle(x1, y1, x2, y2,
                                                 outline=HIGHLIGHT_COLOR,
                                                 width=4)

                piece = self.board[row][col]
                if piece:
                    self.canvas.create_text(
                        x1 + SQUARE_SIZE//2,
                        y1 + SQUARE_SIZE//2,
                        text=UNICODE_PIECES[piece],
                        font=("Segoe UI Symbol", 40),
                        fill="#222222" if piece.isupper() else "#000000"
                    )

        # Draw coordinates
        for i in range(8):
            self.canvas.create_text(10, i*SQUARE_SIZE + 10,
                                    text=str(8-i),
                                    fill="gray",
                                    anchor="nw",
                                    font=("Segoe UI", 8))

            self.canvas.create_text(i*SQUARE_SIZE + SQUARE_SIZE - 10,
                                    8*SQUARE_SIZE - 10,
                                    text=chr(97+i),
                                    fill="gray",
                                    anchor="se",
                                    font=("Segoe UI", 8))

    def on_press(self, event):
        col = event.x // SQUARE_SIZE
        row = event.y // SQUARE_SIZE
        if 0 <= row < 8 and 0 <= col < 8:
            piece = self.board[row][col]
            if piece and self.correct_turn(piece):
                self.drag_data = {"row": row, "col": col,
                                  "item": self.canvas.find_closest(event.x, event.y)[0]}

    def on_drag(self, event):
        if self.drag_data["item"]:
            self.canvas.coords(self.drag_data["item"], event.x, event.y)

    def on_release(self, event):
        if not self.drag_data["item"]:
            return

        to_col = event.x // SQUARE_SIZE
        to_row = event.y // SQUARE_SIZE
        fr, fc = self.drag_data["row"], self.drag_data["col"]

        if 0 <= to_row < 8 and 0 <= to_col < 8:
            if self.is_valid_move(fr, fc, to_row, to_col):
                self.make_move(fr, fc, to_row, to_col)
                self.last_move = [(fr, fc), (to_row, to_col)]
                self.after_move(fr, fc, to_row, to_col)

        self.drag_data = {"item": None, "row": None, "col": None}
        self.draw_board()

    def correct_turn(self, piece):
        return (piece.isupper() and self.turn == "white") or \
               (piece.islower() and self.turn == "black")

    def switch_turn(self):
        self.turn = "black" if self.turn == "white" else "white"
        self.turn_label.config(text=f"Turn: {self.turn.capitalize()}")

    def make_move(self, fr, fc, tr, tc):
        piece = self.board[fr][fc]
        self.board[tr][tc] = piece
        self.board[fr][fc] = ""

        if piece == "P" and tr == 0:
            self.board[tr][tc] = "Q"
        if piece == "p" and tr == 7:
            self.board[tr][tc] = "q"

    def after_move(self, fr, fc, tr, tc):
        move = f"{self.board[tr][tc]}: ({fr},{fc}) → ({tr},{tc})\n"
        self.move_history.append(move)
        self.history_box.insert(tk.END, move)
        self.history_box.see(tk.END)
        self.switch_turn()

    # ===== Move Rules (Unchanged Logic) =====

    def is_valid_move(self, r, c, tr, tc):
        piece = self.board[r][c]
        if not piece:
            return False

        target = self.board[tr][tc]
        color = "white" if piece.isupper() else "black"

        # Prevent capturing own piece
        if target:
            if (piece.isupper() and target.isupper()) or (piece.islower() and target.islower()):
                return False

        dr = tr - r
        dc = tc - c

        # Pawn
        if piece.lower() == 'p':
            direction = -1 if color == "white" else 1
            start_row = 6 if color == "white" else 1

            if dc == 0:
                if dr == direction and not target:
                    return True
                if r == start_row and dr == 2 * direction and not target and not self.board[r + direction][c]:
                    return True
            if abs(dc) == 1 and dr == direction and target:
                return True
            return False

        # Rook
        if piece.lower() == 'r':
            if dr != 0 and dc != 0:
                return False
            step_r = (dr > 0) - (dr < 0)
            step_c = (dc > 0) - (dc < 0)
            cr, cc = r + step_r, c + step_c
            while (cr, cc) != (tr, tc):
                if self.board[cr][cc]:
                    return False
                cr += step_r
                cc += step_c
            return True

        # Knight
        if piece.lower() == 'n':
            return (abs(dr), abs(dc)) in [(2,1),(1,2)]

        # Bishop
        if piece.lower() == 'b':
            if abs(dr) != abs(dc):
                return False
            step_r = (dr > 0) - (dr < 0)
            step_c = (dc > 0) - (dc < 0)
            cr, cc = r + step_r, c + step_c
            while (cr, cc) != (tr, tc):
                if self.board[cr][cc]:
                    return False
                cr += step_r
                cc += step_c
            return True

        # Queen
        if piece.lower() == 'q':
            if dr == 0 or dc == 0 or abs(dr) == abs(dc):
                step_r = (dr > 0) - (dr < 0)
                step_c = (dc > 0) - (dc < 0)
                cr, cc = r + step_r, c + step_c
                while (cr, cc) != (tr, tc):
                    if self.board[cr][cc]:
                        return False
                    cr += step_r
                    cc += step_c
                return True
            return False

        # King
        if piece.lower() == 'k':
            if max(abs(dr), abs(dc)) == 1:
                return True
            return False

        return False

    def valid_pawn(self, fr, fc, tr, tc):
        piece = self.board[fr][fc]
        direction = -1 if piece.isupper() else 1
        start_row = 6 if piece.isupper() else 1

        if fc == tc and self.board[tr][tc] == "":
            if tr - fr == direction:
                return True
            if fr == start_row and tr - fr == 2*direction and \
               self.board[fr + direction][fc] == "":
                return True

        if abs(tc - fc) == 1 and tr - fr == direction and self.board[tr][tc] != "":
            return True

        return False

    def valid_rook(self, fr, fc, tr, tc):
        if fr != tr and fc != tc:
            return False
        return self.clear_path(fr, fc, tr, tc)

    def clear_path(self, fr, fc, tr, tc):
        step_r = (tr - fr) // max(1, abs(tr - fr)) if fr != tr else 0
        step_c = (tc - fc) // max(1, abs(tc - fc)) if fc != tc else 0
        r, c = fr + step_r, fc + step_c
        while (r, c) != (tr, tc):
            if self.board[r][c] != "":
                return False
            r += step_r
            c += step_c
        return True

    def same_color(self, p1, p2):
        return (p1.isupper() and p2.isupper()) or \
               (p1.islower() and p2.islower())


if __name__ == "__main__":
    root = tk.Tk()
    game = ChessGame(root)
    root.mainloop()
