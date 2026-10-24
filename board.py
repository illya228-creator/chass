
import os
import pygame

# Размеры игрового окна
WIDTH = 800
HEIGHT = 800

# Параметры шахматной доски
ROWS = 8
COLS = 8
SQUARE_SIZE = WIDTH // COLS

# Частота обновления экрана
FPS = 60

# Цвета клеток и выделения
LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Определяем путь к папке с изображениями
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Названия файлов всех шахматных фигур
PIECE_FILES = {
    "wp": "wp.png",  # Белая пешка
    "bp": "bp.png",  # Чёрная пешка
    "wr": "wr.png",  # Белая ладья
    "br": "br.png",  # Чёрная ладья
    "wn": "wn.png",  # Белый конь
    "bn": "bn.png",  # Чёрный конь
    "wb": "wb.png",  # Белый слон
    "bb": "bb.png",  # Чёрный слон
    "wq": "wq.png",  # Белый ферзь
    "bq": "bq.png",  # Чёрный ферзь
    "wk": "wk.png",  # Белый король
    "bk": "bk.png",  # Чёрный король
}


# Загружаем изображения фигур
def load_pieces():
    images = {}

    for name, filename in PIECE_FILES.items():
        path = os.path.join(ASSETS_DIR, filename)

        # Проверяем, существует ли изображение
        if not os.path.isfile(path):
            raise FileNotFoundError(
                f"Не найден файл фигуры: {path}"
            )

        # Загружаем изображение с прозрачностью
        image = pygame.image.load(path).convert_alpha()

        # Подгоняем изображение под размер клетки
        images[name] = pygame.transform.smoothscale(
            image, (SQUARE_SIZE, SQUARE_SIZE)
        )

    return images


# Рисуем шахматную доску
def draw_board(screen):
    for row in range(ROWS):
        for col in range(COLS):
            # Чередуем светлые и тёмные клетки
            color = (
                LIGHT_BROWN
                if (row + col) % 2 == 0
                else DARK_BROWN
            )

            pygame.draw.rect(
                screen,
                color,
                (
                    col * SQUARE_SIZE,
                    row * SQUARE_SIZE,
                    SQUARE_SIZE,
                    SQUARE_SIZE,
                ),
            )


# Рисуем все фигуры на доске
def draw_pieces(screen, board, images):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]

            # Пустые клетки не требуют отрисовки
            if piece:
                screen.blit(
                    images[piece],
                    (
                        col * SQUARE_SIZE,
                        row * SQUARE_SIZE,
                    ),
                )


# Подсвечиваем выбранную фигуру
def draw_selected(screen, position):
    if position is None:
        return

    col, row = position

    pygame.draw.rect(
        screen,
        GREEN,
        (
            col * SQUARE_SIZE,
            row * SQUARE_SIZE,
            SQUARE_SIZE,
            SQUARE_SIZE,
        ),
        3,  # Толщина рамки
    )
