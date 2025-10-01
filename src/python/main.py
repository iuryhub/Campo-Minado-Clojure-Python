import time
from game import GameState, init_game, reveal_cell, toggle_flag, count_flags, get_cell


def clear_screen():
    print("\033[2J\033[H", end="")


def print_board(state: GameState):
    print("\n  ", end="")
    for c in range(state.width):
        print(f" {c}", end="")
    print()

    for r in range(state.height):
        print(f"{r:2}", end="")
        for c in range(state.width):
            cell = get_cell(state, r, c)

            if cell.is_flagged:
                print(" 🚩", end="")
            elif not cell.is_revealed:
                print(" ▢", end="")
            elif cell.has_mine:
                print(" 💣", end="")
            elif cell.adjacent_mines == 0:
                print("  ", end="")
            else:
                print(f" {cell.adjacent_mines}", end="")
        print()


def print_status(state: GameState):
    flags = count_flags(state)
    remaining = state.mines_count - flags
    print(f"\n💣 Minas: {state.mines_count}  |  🚩 Bandeiras: {flags}  |  Restantes: {remaining}")


def print_game_over(state: GameState):
    if state.won:
        print("\n🎉 PARABÉNS! Você venceu! 🎉")
    else:
        print("\n💥 BOOM! Você perdeu! 💥")


def get_move():
    print("\nAções: r <linha> <coluna> = revelar | f <linha> <coluna> = bandeira | q = sair")
    cmd = input("Seu movimento: ").strip().lower().split()

    if not cmd:
        return None

    if cmd[0] == 'q':
        return ('quit',)

    if cmd[0] in ['r', 'f'] and len(cmd) == 3:
        try:
            row = int(cmd[1])
            col = int(cmd[2])
            return (cmd[0], row, col)
        except ValueError:
            return None

    return None


def print_welcome():
    print("=" * 50)
    print("        🎮 CAMPO MINADO 💣")
    print("=" * 50)
    print("\nBem-vindo ao Campo Minado!")
    print("Revele todas as células sem minas para vencer.")
    print("\nInstruções:")
    print("  - Digite 'r <linha> <coluna>' para revelar uma célula")
    print("  - Digite 'f <linha> <coluna>' para marcar/desmarcar bandeira")
    print("  - Digite 'q' para sair")
    print("\nNúmeros indicam quantas minas estão adjacentes.")
    print("=" * 50)


def print_error(message: str):
    print(f"\n❌ {message}")


def main():
    print_welcome()
    width = 8
    height = 8
    mines = 10
    seed = int(time.time())
    state = init_game(width, height, mines, seed)
    while not state.game_over:
        clear_screen()
        print_board(state)
        print_status(state)
        move = get_move()
        if move is None:
            print_error("Movimento inválido!")
            input("Pressione ENTER para continuar...")
            continue
        if move[0] == 'quit':
            print("\nSaindo...")
            return
        action, row, col = move
        if action == 'r':
            state = reveal_cell(state, row, col, seed)
        elif action == 'f':
            state = toggle_flag(state, row, col)

    clear_screen()
    print_board(state)
    print_status(state)
    print_game_over(state)
    print()


if __name__ == "__main__":
    main()

