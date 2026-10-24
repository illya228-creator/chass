
import pygame

# Импортируем функции из трёх остальных модулей
from board import (
    WIDTH,
    HEIGHT,
    SQUARE_SIZE,
    FPS,
    BLACK,
    WHITE,
    load_pieces,
    draw_board,
    draw_pieces,
    draw_selected,
)
from pieces import create_board, move_piece
from game_logic import is_valid_move, check_victory


# Главная функция игры
def main():
    # Инициализируем Pygame
    pygame.init()

    # Создаём игровое окно
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess")

    # Создаём таймер для ограничения FPS
    clock = pygame.time.Clock()

    # Загружаем изображения шахматных фигур
    images = load_pieces()

    # Создаём доску с начальной расстановкой
    board = create_board()

    # Начальное состояние игры
    selected_piece = None
    turn = "white"
    running = True
    victory_message = None

    # Главный игровой цикл
    while running:
        clock.tick(FPS)

        # Обрабатываем события пользователя
        for event in pygame.event.get():

            # Закрытие окна
            if event.type == pygame.QUIT:
                running = False

            # Обрабатываем нажатие левой кнопки мыши
            elif (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and victory_message is None
            ):
                # Получаем координаты курсора
                x, y = event.pos

                # Преобразуем координаты окна в координаты доски
                col = x // SQUARE_SIZE
                row = y // SQUARE_SIZE

                # Получаем позицию выбранной клетки
                clicked = (col, row)

                # Первый клик: выбираем свою фигуру
                if selected_piece is None:
                    piece = board[row][col]

                    # Проверяем цвет выбранной фигуры
                    current_color = (
                        "w" if turn == "white" else "b"
                    )

                    if piece and piece[0] == current_color:
                        selected_piece = clicked

                # Второй клик: пытаемся выполнить ход
                else:
                    if is_valid_move(
                        board,
                        selected_piece,
                        clicked,
                        turn,
                    ):
                        # Выполняем перемещение фигуры
                        move_piece(
                            board,
                            selected_piece,
                            clicked,
                        )

                        # Передаём ход другому игроку
                        turn = (
                            "black"
                            if turn == "white"
                            else "white"
                        )

                        # Сбрасываем выделение
                        selected_piece = None

                    else:
                        # Если нажали на другую свою фигуру,
                        # выбираем её вместо предыдущей
                        piece = board[row][col]
                        current_color = (
                            "w" if turn == "white" else "b"
                        )

                        if piece and piece[0] == current_color:
                            selected_piece = clicked
                        else:
                            selected_piece = None

        # Проверяем, завершилась ли игра
        victory_message = check_victory(board)

        # Рисуем доску
        draw_board(screen)

        # Рисуем фигуры
        draw_pieces(screen, board, images)

        # Подсвечиваем выбранную клетку
        draw_selected(screen, selected_piece)

        # Если есть победитель, показываем сообщение
        if victory_message:
            # Создаём полупрозрачное затемнение
            overlay = pygame.Surface(
                (WIDTH, HEIGHT),
                pygame.SRCALPHA,
            )
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            # Создаём текст победы
            font = pygame.font.Font(None, 68)
            text = font.render(
                victory_message,
                True,
                WHITE,
            )

            # Размещаем сообщение по центру окна
            text_rect = text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2)
            )
            screen.blit(text, text_rect)

        # Обновляем экран
        pygame.display.flip()

    # Корректно закрываем Pygame
    pygame.quit()


# Запускаем игру при запуске main.py
if __name__ == "__main__":
    main()
