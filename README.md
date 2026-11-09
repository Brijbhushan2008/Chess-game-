# ♟ Modern Python Chess

A sleek, feature-rich, and interactive graphical chess game built completely from scratch using Python and `tkinter`. Designed with a modern dark-mode interface, smooth drag-and-drop piece mechanics, and robust move-validation logic.

---

## ✨ Key Features

- **Modern Minimalist UI:** Custom dark-themed layout (`#2E2E2E` and `#1E1E1E` styling) featuring crisp Unicode chess pieces and subtle coordinate markers.
- **Fluid Piece Mechanics:** Supports intuitive click-and-drag piece movement powered by dynamic canvas binding.
- **Complete Rule Enforcement:** Built-in move validation algorithms covering movement and path-checking for all standard chess pieces:
  - ♙ **Pawns:** Single/double step initial moves, diagonal captures.
  - ♖ **Rooks:** Straight-line horizontal and vertical movement with clear path verification.
  - ♘ **Knight:** L-shaped jumping mechanics.
  - ♗ **Bishop:** Diagonal movement with obstruction checking.
  - ♕ **Queen:** Combined orthogonal and diagonal mobility.
  - ♔ **King:** Single-square directional movement.
- **Smart Move History Tracker:** A live scrollable side-panel log that records every turn's coordinate changes and piece movements in real time.
- **Dynamic Turn Indicator:** Real-time visual status indicator highlighting whose turn it is to play.
- **Automatic Pawn Promotion:** Automatically promotes any pawn that reaches the final rank into a Queen.
- **Visual Feedback:** Highlights the source and destination squares of the last played move.

---

## 🚀 Getting Started

### Prerequisites
Make sure you have **Python 3.x** installed on your system. 
*(Note: `tkinter` comes pre-installed with standard Python distributions on Windows and macOS).*

---

## 🕹️ How to Play

1. **White moves first.** White pieces are represented by uppercase symbols (`K, Q, R, B, N, P`), and Black pieces by lowercase symbols (`k, q, r, b, n, p`).
2. **Dragging Pieces:** Click and hold down the left mouse button on any of your pieces, drag it across the board to a target square, and release to drop it.
3. **Validating Moves:** If a move violates standard chess rules or attempts to jump/capture friendly pieces, the piece will snap back to its original position.
4. **Tracking Progress:** Check the side panel to view the live history log and monitor turn updates.

---

## 🛠️ Code Architecture

The application is built within a single core class (`ChessGame`) managing state and event loops:
* **Board Representation:** An $8 \times 8$ matrix tracking piece characters.
* **Event Handlers:** Uses `<ButtonPress-1>`, `<B1-Motion>`, and `<ButtonRelease-1>` bindings to handle smooth dragging coordinates on a Tkinter `Canvas`.
* **Validation Engine:** Modular mathematical checks (`is_valid_move`, `clear_path`) ensuring clean, bug-free move validation without heavy third-party dependencies.

