import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
from typing import List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class Color(Enum):
    WHITE = "white"
    BLACK = "black"

class PieceType(Enum):
    PAWN = "pawn"
    KNIGHT = "knight"
    BISHOP = "bishop"
    ROOK = "rook"
    QUEEN = "queen"
    KING = "king"

@dataclass
class Piece:
    type: PieceType
    color: Color
    
    def __str__(self):
        symbols = {
            PieceType.PAWN: ('♙', '♟'),
            PieceType.KNIGHT: ('♘', '♞'),
            PieceType.BISHOP: ('♗', '♝'),
            PieceType.ROOK: ('♖', '♜'),
            PieceType.QUEEN: ('♕', '♛'),
            PieceType.KING: ('♔', '♚')
        }
        return symbols[self.type][0 if self.color == Color.WHITE else 1]

class DiplomaticChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Diplomatic Chess - International Relations Simulator")
        self.root.configure(bg='#1e293b')
        
        # Game state
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_player = Color.WHITE
        self.selected_square = None
        self.valid_moves = []
        self.move_count = 0
        self.game_status = "active"
        self.military_strength = {Color.WHITE: 39, Color.BLACK: 39}
        self.diplomatic_log = []
        self.is_ai_thinking = False
        
        # UI Elements
        self.square_buttons = [[None for _ in range(8)] for _ in range(8)]
        self.setup_ui()
        self.initialize_board()
        self.update_display()
        
    def setup_ui(self):
        """Setup the GUI layout"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#1e293b')
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Title
        title_frame = tk.Frame(main_frame, bg='#1e293b')
        title_frame.pack(pady=(0, 10))
        
        title = tk.Label(
            title_frame,
            text="👑 DIPLOMATIC CHESS 🛡️",
            font=('Arial', 24, 'bold'),
            bg='#1e293b',
            fg='#f1f5f9'
        )
        title.pack()
        
        subtitle = tk.Label(
            title_frame,
            text="International Relations Strategy Simulator",
            font=('Arial', 12),
            bg='#1e293b',
            fg='#94a3b8'
        )
        subtitle.pack()
        
        # Content container
        content_frame = tk.Frame(main_frame, bg='#1e293b')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Info
        left_panel = tk.Frame(content_frame, bg='#334155', width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Strategic Intelligence
        intel_frame = tk.LabelFrame(
            left_panel,
            text="📊 Strategic Intelligence",
            font=('Arial', 11, 'bold'),
            bg='#334155',
            fg='#f1f5f9',
            relief=tk.RIDGE,
            bd=2
        )
        intel_frame.pack(padx=10, pady=10, fill=tk.X)
        
        self.current_player_label = tk.Label(
            intel_frame,
            text="Current Turn: WHITE",
            font=('Arial', 10),
            bg='#334155',
            fg='#60a5fa',
            anchor='w'
        )
        self.current_player_label.pack(fill=tk.X, padx=5, pady=2)
        
        self.move_count_label = tk.Label(
            intel_frame,
            text="Move Count: 0",
            font=('Arial', 10),
            bg='#334155',
            fg='#f1f5f9',
            anchor='w'
        )
        self.move_count_label.pack(fill=tk.X, padx=5, pady=2)
        
        self.status_label = tk.Label(
            intel_frame,
            text="Status: ACTIVE",
            font=('Arial', 10),
            bg='#334155',
            fg='#4ade80',
            anchor='w'
        )
        self.status_label.pack(fill=tk.X, padx=5, pady=2)
        
        # Military Strength
        military_frame = tk.LabelFrame(
            left_panel,
            text="⚔️ Military Strength",
            font=('Arial', 11, 'bold'),
            bg='#334155',
            fg='#f1f5f9',
            relief=tk.RIDGE,
            bd=2
        )
        military_frame.pack(padx=10, pady=10, fill=tk.X)
        
        self.white_strength_label = tk.Label(
            military_frame,
            text="⚪ White Nation: 39",
            font=('Arial', 10),
            bg='#334155',
            fg='#60a5fa',
            anchor='w'
        )
        self.white_strength_label.pack(fill=tk.X, padx=5, pady=2)
        
        self.white_progress = ttk.Progressbar(
            military_frame,
            length=250,
            mode='determinate',
            maximum=39
        )
        self.white_progress['value'] = 39
        self.white_progress.pack(fill=tk.X, padx=5, pady=2)
        
        self.black_strength_label = tk.Label(
            military_frame,
            text="⚫ Black Nation: 39",
            font=('Arial', 10),
            bg='#334155',
            fg='#ef4444',
            anchor='w'
        )
        self.black_strength_label.pack(fill=tk.X, padx=5, pady=(10, 2))
        
        self.black_progress = ttk.Progressbar(
            military_frame,
            length=250,
            mode='determinate',
            maximum=39
        )
        self.black_progress['value'] = 39
        self.black_progress.pack(fill=tk.X, padx=5, pady=2)
        
        # Diplomatic Log
        log_frame = tk.LabelFrame(
            left_panel,
            text="📜 Diplomatic Log",
            font=('Arial', 11, 'bold'),
            bg='#334155',
            fg='#f1f5f9',
            relief=tk.RIDGE,
            bd=2
        )
        log_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        log_scroll = tk.Scrollbar(log_frame)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(
            log_frame,
            height=10,
            width=30,
            bg='#1e293b',
            fg='#cbd5e1',
            font=('Arial', 9),
            yscrollcommand=log_scroll.set,
            wrap=tk.WORD,
            relief=tk.FLAT
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        log_scroll.config(command=self.log_text.yview)
        
        # Control buttons
        control_frame = tk.Frame(left_panel, bg='#334155')
        control_frame.pack(padx=10, pady=10, fill=tk.X)
        
        self.reset_button = tk.Button(
            control_frame,
            text="🔄 New Summit",
            font=('Arial', 11, 'bold'),
            bg='#3b82f6',
            fg='white',
            activebackground='#2563eb',
            activeforeground='white',
            relief=tk.RAISED,
            bd=3,
            command=self.reset_game,
            cursor='hand2'
        )
        self.reset_button.pack(fill=tk.X)
        
        # Right panel - Chess board
        board_container = tk.Frame(content_frame, bg='#1e293b')
        board_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        board_frame = tk.Frame(board_container, bg='#334155', relief=tk.RIDGE, bd=3)
        board_frame.pack(padx=20, pady=20)
        
        # Column labels
        col_label_frame = tk.Frame(board_frame, bg='#334155')
        col_label_frame.grid(row=0, column=1, columnspan=8)
        for i in range(8):
            label = tk.Label(
                col_label_frame,
                text=chr(97 + i),
                font=('Arial', 12, 'bold'),
                bg='#334155',
                fg='#94a3b8',
                width=5
            )
            label.pack(side=tk.LEFT)
        
        # Chess squares
        for row in range(8):
            # Row label
            row_label = tk.Label(
                board_frame,
                text=str(8 - row),
                font=('Arial', 12, 'bold'),
                bg='#334155',
                fg='#94a3b8',
                width=2
            )
            row_label.grid(row=row + 1, column=0)
            
            for col in range(8):
                color = '#cbd5e1' if (row + col) % 2 == 0 else '#64748b'
                btn = tk.Button(
                    board_frame,
                    text='',
                    font=('Arial', 32),
                    width=3,
                    height=1,
                    bg=color,
                    activebackground=color,
                    relief=tk.FLAT,
                    command=lambda r=row, c=col: self.on_square_click(r, c)
                )
                btn.grid(row=row + 1, column=col + 1, padx=1, pady=1)
                self.square_buttons[row][col] = btn
        
        # Educational note
        edu_frame = tk.Frame(board_container, bg='#334155', relief=tk.RIDGE, bd=2)
        edu_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        edu_label = tk.Label(
            edu_frame,
            text="📖 Educational Connection: This chess game demonstrates diplomatic decision-making in international relations\nthrough strategic gameplay, territorial control, and power projection.",
            font=('Arial', 9),
            bg='#334155',
            fg='#94a3b8',
            wraplength=600,
            justify=tk.LEFT
        )
        edu_label.pack(padx=10, pady=10)
    
    def initialize_board(self):
        """Setup standard chess starting position"""
        back_row = [PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP, PieceType.QUEEN,
                    PieceType.KING, PieceType.BISHOP, PieceType.KNIGHT, PieceType.ROOK]
        
        for col in range(8):
            self.board[0][col] = Piece(back_row[col], Color.BLACK)
            self.board[1][col] = Piece(PieceType.PAWN, Color.BLACK)
            self.board[6][col] = Piece(PieceType.PAWN, Color.WHITE)
            self.board[7][col] = Piece(back_row[col], Color.WHITE)
        
        self.add_log("🌍 International chess summit initiated")
        self.add_log("White Nation vs Black Nation")
    
    def add_log(self, message):
        """Add message to diplomatic log"""
        self.diplomatic_log.append(message)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
    
    def update_display(self):
        """Update all UI elements"""
        # Update board squares
        for row in range(8):
            for col in range(8):
                btn = self.square_buttons[row][col]
                piece = self.board[row][col]
                
                # Base color
                base_color = '#cbd5e1' if (row + col) % 2 == 0 else '#64748b'
                
                # Highlight selected square
                if self.selected_square and self.selected_square == (row, col):
                    btn.config(bg='#fbbf24', activebackground='#fbbf24')
                # Highlight valid moves
                elif (row, col) in self.valid_moves:
                    if piece:
                        btn.config(bg='#ef4444', activebackground='#ef4444')
                    else:
                        btn.config(bg='#4ade80', activebackground='#4ade80')
                else:
                    btn.config(bg=base_color, activebackground=base_color)
                
                # Set piece symbol
                btn.config(text=str(piece) if piece else '')
        
        # Update labels
        player_text = f"Current Turn: {self.current_player.value.upper()}"
        if self.is_ai_thinking:
            player_text += " 🤔"
        self.current_player_label.config(
            text=player_text,
            fg='#60a5fa' if self.current_player == Color.WHITE else '#ef4444'
        )
        
        self.move_count_label.config(text=f"Move Count: {self.move_count}")
        self.status_label.config(text=f"Status: {self.game_status.upper()}")
        
        # Update military strength
        self.white_strength_label.config(text=f"⚪ White Nation: {self.military_strength[Color.WHITE]}")
        self.white_progress['value'] = self.military_strength[Color.WHITE]
        
        self.black_strength_label.config(text=f"⚫ Black Nation: {self.military_strength[Color.BLACK]}")
        self.black_progress['value'] = self.military_strength[Color.BLACK]
        
        self.root.update()
    
    def on_square_click(self, row, col):
        """Handle square click"""
        if self.game_status != "active" or self.is_ai_thinking:
            return
        
        piece = self.board[row][col]
        
        if self.selected_square:
            if (row, col) in self.valid_moves:
                # Execute move
                self.execute_move(self.selected_square, (row, col))
                self.selected_square = None
                self.valid_moves = []
                
                # Let AI move
                if self.game_status == "active" and self.current_player == Color.BLACK:
                    self.root.after(500, self.make_ai_move)
            elif piece and piece.color == self.current_player:
                # Select different piece
                self.selected_square = (row, col)
                self.valid_moves = self.get_valid_moves_for_piece(row, col)
            else:
                # Deselect
                self.selected_square = None
                self.valid_moves = []
        elif piece and piece.color == self.current_player:
            # Select piece
            self.selected_square = (row, col)
            self.valid_moves = self.get_valid_moves_for_piece(row, col)
        
        self.update_display()
    
    def get_valid_moves_for_piece(self, row, col):
        """Get all valid moves for piece at position"""
        piece = self.board[row][col]
        if not piece:
            return []
        
        moves = []
        for to_row in range(8):
            for to_col in range(8):
                if self.is_valid_move((row, col), (to_row, to_col)):
                    moves.append((to_row, to_col))
        return moves
    
    def is_valid_move(self, from_pos, to_pos):
        """Check if move is valid"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.board[from_row][from_col]
        if not piece or piece.color != self.current_player:
            return False
        
        target = self.board[to_row][to_col]
        if target and target.color == piece.color:
            return False
        
        # Movement rules
        if piece.type == PieceType.PAWN:
            return self._is_valid_pawn_move(from_pos, to_pos)
        elif piece.type == PieceType.KNIGHT:
            return self._is_valid_knight_move(from_pos, to_pos)
        elif piece.type == PieceType.BISHOP:
            return self._is_valid_bishop_move(from_pos, to_pos)
        elif piece.type == PieceType.ROOK:
            return self._is_valid_rook_move(from_pos, to_pos)
        elif piece.type == PieceType.QUEEN:
            return self._is_valid_queen_move(from_pos, to_pos)
        elif piece.type == PieceType.KING:
            return self._is_valid_king_move(from_pos, to_pos)
        
        return False
    
    def _is_valid_pawn_move(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        piece = self.board[from_row][from_col]
        target = self.board[to_row][to_col]
        
        direction = -1 if piece.color == Color.WHITE else 1
        start_row = 6 if piece.color == Color.WHITE else 1
        
        if to_col == from_col and not target:
            if to_row == from_row + direction:
                return True
            if from_row == start_row and to_row == from_row + 2 * direction:
                if not self.board[from_row + direction][from_col]:
                    return True
        
        if abs(to_col - from_col) == 1 and to_row == from_row + direction and target:
            return True
        
        return False
    
    def _is_valid_knight_move(self, from_pos, to_pos):
        row_diff = abs(to_pos[0] - from_pos[0])
        col_diff = abs(to_pos[1] - from_pos[1])
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
    
    def _is_valid_bishop_move(self, from_pos, to_pos):
        if abs(to_pos[0] - from_pos[0]) != abs(to_pos[1] - from_pos[1]):
            return False
        return self._is_path_clear(from_pos, to_pos)
    
    def _is_valid_rook_move(self, from_pos, to_pos):
        if from_pos[0] != to_pos[0] and from_pos[1] != to_pos[1]:
            return False
        return self._is_path_clear(from_pos, to_pos)
    
    def _is_valid_queen_move(self, from_pos, to_pos):
        return self._is_valid_rook_move(from_pos, to_pos) or self._is_valid_bishop_move(from_pos, to_pos)
    
    def _is_valid_king_move(self, from_pos, to_pos):
        return abs(to_pos[0] - from_pos[0]) <= 1 and abs(to_pos[1] - from_pos[1]) <= 1
    
    def _is_path_clear(self, from_pos, to_pos):
        row_dir = 0 if to_pos[0] == from_pos[0] else (1 if to_pos[0] > from_pos[0] else -1)
        col_dir = 0 if to_pos[1] == from_pos[1] else (1 if to_pos[1] > from_pos[1] else -1)
        
        curr_row, curr_col = from_pos[0] + row_dir, from_pos[1] + col_dir
        while (curr_row, curr_col) != to_pos:
            if self.board[curr_row][curr_col]:
                return False
            curr_row += row_dir
            curr_col += col_dir
        return True
    
    def get_all_valid_moves(self, color):
        """Get all valid moves for a color"""
        moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    for to_row in range(8):
                        for to_col in range(8):
                            saved_player = self.current_player
                            self.current_player = color
                            if self.is_valid_move((row, col), (to_row, to_col)):
                                moves.append(((row, col), (to_row, to_col)))
                            self.current_player = saved_player
        return moves
    
    def get_piece_value(self, piece_type):
        values = {
            PieceType.PAWN: 1, PieceType.KNIGHT: 3, PieceType.BISHOP: 3,
            PieceType.ROOK: 5, PieceType.QUEEN: 9, PieceType.KING: 0
        }
        return values[piece_type]
    
    def make_ai_move(self):
        """AI makes a move"""
        self.is_ai_thinking = True
        self.update_display()
        
        moves = self.get_all_valid_moves(Color.BLACK)
        if not moves:
            self.game_status = "stalemate"
            self.add_log("🤝 Strategic stalemate reached!")
            messagebox.showinfo("Game Over", "Stalemate! Diplomatic deadlock!")
            self.is_ai_thinking = False
            self.update_display()
            return
        
        capture_moves = []
        center_moves = []
        
        for move in moves:
            from_pos, to_pos = move
            target = self.board[to_pos[0]][to_pos[1]]
            
            if target:
                value = self.get_piece_value(target.type)
                capture_moves.append((move, value))
            
            if 3 <= to_pos[0] <= 4 and 3 <= to_pos[1] <= 4:
                center_moves.append(move)
        
        if capture_moves:
            capture_moves.sort(key=lambda x: x[1], reverse=True)
            selected_move = capture_moves[0][0]
            self.add_log(f"🎯 Black: Territorial acquisition (Value: {capture_moves[0][1]})")
        elif center_moves and random.random() > 0.3:
            selected_move = random.choice(center_moves)
            self.add_log("🏛️ Black: Strategic positioning")
        else:
            selected_move = random.choice(moves)
            self.add_log("🛡️ Black: Defensive maneuver")
        
        self.execute_move(selected_move[0], selected_move[1])
        self.is_ai_thinking = False
        self.update_display()
    
    def execute_move(self, from_pos, to_pos):
        """Execute a move"""
        piece = self.board[from_pos[0]][from_pos[1]]
        captured = self.board[to_pos[0]][to_pos[1]]
        
        self.board[to_pos[0]][to_pos[1]] = piece
        self.board[from_pos[0]][from_pos[1]] = None
        
        if captured:
            self.military_strength[Color.WHITE if piece.color == Color.BLACK else Color.BLACK] -= \
                self.get_piece_value(captured.type)
        
        self.move_count += 1
        self.current_player = Color.BLACK if self.current_player == Color.WHITE else Color.WHITE
        
        # Check game end
        next_moves = self.get_all_valid_moves(self.current_player)
        if not next_moves:
            self.game_status = "checkmate"
            winner = "Black" if self.current_player == Color.WHITE else "White"
            self.add_log(f"🏆 {winner} achieves victory!")
            messagebox.showinfo("Game Over", f"{winner} Nation achieves total strategic dominance!")
    
    def reset_game(self):
        """Reset the game"""
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_player = Color.WHITE
        self.selected_square = None
        self.valid_moves = []
        self.move_count = 0
        self.game_status = "active"
        self.military_strength = {Color.WHITE: 39, Color.BLACK: 39}
        self.diplomatic_log = []
        self.is_ai_thinking = False
        
        self.log_text.delete('1.0', tk.END)
        self.initialize_board()
        self.update_display()

def main():
    root = tk.Tk()
    root.geometry("1200x800")
    root.resizable(True, True)
    app = DiplomaticChessGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()