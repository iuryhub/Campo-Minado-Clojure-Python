
from typing import List, Tuple, Optional
from dataclasses import dataclass, replace
from random import Random


@dataclass(frozen=True)
class Cell:
    has_mine: bool
    is_revealed: bool
    is_flagged: bool
    adjacent_mines: int

@dataclass(frozen=True)
class GameState:
    width: int
    height: int
    board: Tuple[Tuple[Cell, ...], ...]
    game_over: bool
    won: bool
    mines_count: int

def create_empty_board(width: int, height: int) -> Tuple[Tuple[Cell, ...], ...]:
    cell = Cell(has_mine=False, is_revealed=False, is_flagged=False, adjacent_mines=0)
    return tuple(tuple(cell for _ in range(width)) for _ in range(height))

def get_neighbors(row: int, col: int, height: int, width: int) -> List[Tuple[int, int]]:
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = row + dr, col + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def place_mines(board: Tuple[Tuple[Cell, ...], ...], mines_count: int, seed: int, first_click: Optional[Tuple[int, int]] = None) -> Tuple[Tuple[Cell, ...], ...]:
    height = len(board)
    width = len(board[0])
    rng = Random(seed)
    available = [(r, c) for r in range(height) for c in range(width)]
    if first_click:
        fr, fc = first_click
        forbidden = {first_click} | set(get_neighbors(fr, fc, height, width))
        available = [pos for pos in available if pos not in forbidden]
    mine_positions = set(rng.sample(available, min(mines_count, len(available))))
    new_board = []
    for r in range(height):
        row = []
        for c in range(width):
            cell = board[r][c]
            if (r, c) in mine_positions:
                cell = replace(cell, has_mine=True)
            row.append(cell)
        new_board.append(tuple(row))

    return tuple(new_board)

def calculate_adjacent_mines(board: Tuple[Tuple[Cell, ...], ...]) -> Tuple[Tuple[Cell, ...], ...]:
    height = len(board)
    width = len(board[0])

    new_board = []
    for r in range(height):
        row = []
        for c in range(width):
            cell = board[r][c]
            if not cell.has_mine:
                neighbors = get_neighbors(r, c, height, width)
                mine_count = sum(1 for nr, nc in neighbors if board[nr][nc].has_mine)
                cell = replace(cell, adjacent_mines=mine_count)
            row.append(cell)
        new_board.append(tuple(row))

    return tuple(new_board)

def init_game(width: int, height: int, mines_count: int, seed: int) -> GameState:
    board = create_empty_board(width, height)
    return GameState(
            width=width,
            height=height,
            board=board,
            game_over=False,
            won=False,
            mines_count=mines_count
            )

def is_first_move(state: GameState) -> bool:
    for row in state.board:
        for cell in row:
            if cell.is_revealed:
                return False
    return True

def reveal_cell(state: GameState, row: int, col: int, seed: int) -> GameState:
    if state.game_over or not (0 <= row < state.height and 0 <= col < state.width):
        return state

    cell = state.board[row][col]

    if cell.is_revealed or cell.is_flagged:
        return state
    board = state.board
    if is_first_move(state):
        board = place_mines(board, state.mines_count, seed, (row, col))
        board = calculate_adjacent_mines(board)
    new_board = list(list(row_cells) for row_cells in board)
    new_board[row][col] = replace(cell, is_revealed=True)
    if board[row][col].has_mine:
        for r in range(state.height):
            for c in range(state.width):
                if new_board[r][c].has_mine:
                    new_board[r][c] = replace(new_board[r][c], is_revealed=True)

        board_tuple = tuple(tuple(row_cells) for row_cells in new_board)
        return replace(state, board=board_tuple, game_over=True, won=False)
    if board[row][col].adjacent_mines == 0:
        board_tuple = tuple(tuple(row_cells) for row_cells in new_board)
        temp_state = replace(state, board=board_tuple)

        for nr, nc in get_neighbors(row, col, state.height, state.width):
            temp_state = reveal_cell(temp_state, nr, nc, seed)

        return temp_state

    board_tuple = tuple(tuple(row_cells) for row_cells in new_board)
    new_state = replace(state, board=board_tuple)
    return check_win(new_state)

def toggle_flag(state: GameState, row: int, col: int) -> GameState:
    if state.game_over or not (0 <= row < state.height and 0 <= col < state.width):
        return state

    cell = state.board[row][col]

    if cell.is_revealed:
        return state

    new_board = list(list(row_cells) for row_cells in state.board)
    new_board[row][col] = replace(cell, is_flagged=not cell.is_flagged)
    board_tuple = tuple(tuple(row_cells) for row_cells in new_board)

    new_state = replace(state, board=board_tuple)
    return check_win(new_state)


def check_win(state: GameState) -> GameState:
    if state.game_over:
        return state
    unrevealed_safe = 0
    for row in state.board:
        for cell in row:
            if not cell.has_mine and not cell.is_revealed:
                unrevealed_safe += 1
    if unrevealed_safe == 0:
        return replace(state, game_over=True, won=True)

    return state


def count_flags(state: GameState) -> int:
    count = 0
    for row in state.board:
        for cell in row:
            if cell.is_flagged:
                count += 1
    return count


def get_cell(state: GameState, row: int, col: int) -> Optional[Cell]:
    if 0 <= row < state.height and 0 <= col < state.width:
        return state.board[row][col]
    return None
