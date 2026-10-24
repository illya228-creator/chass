
# Проверяем, свободны ли клетки между двумя позициями
def is_path_clear(board, start_pos, end_pos):
    sx, sy = start_pos
    ex, ey = end_pos

    # Определяем направление движения по каждой оси
    dx = (ex > sx) - (ex < sx)
    dy = (ey > sy) - (ey < sy)

    # Начинаем со следующей клетки после начальной
    x = sx + dx
    y = sy + dy

    while (x, y) != (ex, ey):
        # Если на пути есть фигура, движение невозможно
        if board[y][x] != "":
            return False

        x += dx
        y += dy

    return True


# Проверяем допустимость хода
def is_valid_move(board, start_pos, end_pos, turn):
    sx, sy = start_pos
    ex, ey = end_pos

    # Проверяем границы доски
    if not (
        0 <= sx < 8 and 0 <= ex < 8
        and 0 <= sy < 8 and 0 <= ey < 8
    ):
        return False

    # Нельзя переместиться на ту же клетку
    if start_pos == end_pos:
        return False

    # Получаем фигуру в начальной клетке
    piece = board[sy][sx]

    if not piece:
        return False

    # Проверяем, принадлежит ли фигура текущему игроку
    current_color = "w" if turn == "white" else "b"

    if piece[0] != current_color:
        return False

    # Проверяем целевую клетку
    target = board[ey][ex]

    # Нельзя брать собственную фигуру
    if target and target[0] == piece[0]:
        return False

    # Расстояние между клетками
    dx = abs(ex - sx)
    dy = abs(ey - sy)

    # -------------------------
    # Пешка
    # -------------------------
    if piece[1] == "p":
        direction = -1 if piece[0] == "w" else 1
        start_row = 6 if piece[0] == "w" else 1

        # Один шаг вперёд на пустую клетку
        if (
            dx == 0
            and ey - sy == direction
            and target == ""
        ):
            return True

        # Два шага с начальной позиции
        if (
            dx == 0
            and sy == start_row
            and ey - sy == 2 * direction
            and target == ""
            and board[sy + direction][sx] == ""
        ):
            return True

        # Взятие чужой фигуры по диагонали
        if (
            dx == 1
            and ey - sy == direction
            and target != ""
            and target[0] != piece[0]
        ):
            return True

        return False

    # -------------------------
    # Конь
    # -------------------------
    if piece[1] == "n":
        return (dx, dy) in ((1, 2), (2, 1))

    # -------------------------
    # Ладья
    # -------------------------
    if piece[1] == "r":
        return (
            (dx == 0 or dy == 0)
            and is_path_clear(board, start_pos, end_pos)
        )

    # -------------------------
    # Слон
    # -------------------------
    if piece[1] == "b":
        return (
            dx == dy
            and is_path_clear(board, start_pos, end_pos)
        )

    # -------------------------
    # Ферзь
    # -------------------------
    if piece[1] == "q":
        straight = dx == 0 or dy == 0
        diagonal = dx == dy

        return (
            (straight or diagonal)
            and is_path_clear(board, start_pos, end_pos)
        )

    # -------------------------
    # Король
    # -------------------------
    if piece[1] == "k":
        return dx <= 1 and dy <= 1

    return False


# Проверяем наличие королей на доске
def check_victory(board):
    has_white_king = any(
        piece == "wk"
        for row in board
        for piece in row
    )

    has_black_king = any(
        piece == "bk"
        for row in board
        for piece in row
    )

    # Если белый король отсутствует, победили чёрные
    if not has_white_king:
        return "Black wins!"

    # Если чёрный король отсутствует, победили белые
    if not has_black_king:
        return "White wins!"

    # Игра продолжается
    return None
