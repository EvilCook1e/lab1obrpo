import pygame
from .const import *
from .direction import Direction
from .element import Element


class Infrastructure:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode([WIDTH * SCALE, HEIGHT * SCALE])
        pygame.display.set_caption("Змейка")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, SCALE)

    def is_quit_event(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

    def get_pressed_key(self) -> Direction | None:
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            return Direction.UP
        if key[pygame.K_RIGHT]:
            return Direction.RIGHT
        if key[pygame.K_DOWN]:
            return Direction.DOWN
        if key[pygame.K_LEFT]:
            return Direction.LEFT
        return None

    def fill_screen(self) -> None:
        self.screen.fill(SCREEN_COLOR)

    def draw_element(self, e: Element, color: str) -> None:
        pygame.draw.rect(
            self.screen,
            pygame.Color(color),
            (e.x * SCALE, e.y * SCALE, ELEMENT_SIZE, ELEMENT_SIZE),
            0,
            ELEMENT_RADIUS
        )

    def draw_score(self, score: int) -> None:
        self.screen.blit(
            self.font.render(f'Score: {score}', True, pygame.Color(SCORE_COLOR)),
            (5, 5)
        )

    def draw_game_over(self) -> None:
        message = self.font.render('GAME OVER', True, pygame.Color(GAME_OVER_COLOR))
        self.screen.blit(
            message,
            message.get_rect(center=((WIDTH // 2) * SCALE, (HEIGHT // 2) * SCALE))
        )

    def update_and_tick(self) -> None:
        pygame.display.update()
        self.clock.tick(FPS)

    def quit(self) -> None:
        pygame.quit()

    def get_player_name(self) -> str:
        name = ""
        input_active = True
        cursor_timer = 0

        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return ""
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if name.strip():
                            input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        return ""
                    else:
                        if len(name) < MAX_PLAYER_NAME and event.unicode.isprintable():
                            name += event.unicode

            self.screen.fill(INPUT_BG_COLOR)

            title = self.font.render("ВВЕДИТЕ ВАШЕ ИМЯ", True, pygame.Color(INPUT_COLOR))
            title_rect = title.get_rect(center=((WIDTH * SCALE) // 2, (HEIGHT * SCALE) // 2 - 60))
            self.screen.blit(title, title_rect)

            hint = self.font.render("Enter - подтвердить, Esc - отмена", True, pygame.Color('gray'))
            hint_rect = hint.get_rect(center=((WIDTH * SCALE) // 2, (HEIGHT * SCALE) // 2 + 60))
            self.screen.blit(hint, hint_rect)

            input_rect = pygame.Rect(
                (WIDTH * SCALE) // 2 - 150,
                (HEIGHT * SCALE) // 2 - 15,
                300,
                40
            )
            pygame.draw.rect(self.screen, (50, 50, 50), input_rect)
            pygame.draw.rect(self.screen, pygame.Color(INPUT_ACTIVE_COLOR), input_rect, 2)

            display_name = name
            cursor_timer += 1
            if (cursor_timer // 30) % 2 == 0:
                display_name += "|"

            name_surface = self.font.render(display_name, True, pygame.Color(INPUT_ACTIVE_COLOR))
            name_rect = name_surface.get_rect(center=input_rect.center)
            self.screen.blit(name_surface, name_rect)

            length_hint = self.font.render(
                f"{len(name)}/{MAX_PLAYER_NAME}",
                True,
                pygame.Color('gray')
            )
            self.screen.blit(length_hint, (input_rect.right - 50, input_rect.bottom + 5))

            pygame.display.update()
            self.clock.tick(FPS)

        return name.strip()

    def draw_scoreboard(self, scoreboard, highlight_score: int = None) -> None:
        records = scoreboard.get_records()

        header = self.font.render("ТАБЛИЦА РЕКОРДОВ", True, pygame.Color(TABLE_HEADER_COLOR))
        header_rect = header.get_rect(center=((WIDTH * SCALE) // 2, 40))
        self.screen.blit(header, header_rect)

        rank_header = self.font.render("N", True, pygame.Color(TABLE_HEADER_COLOR))
        name_header = self.font.render("Имя", True, pygame.Color(TABLE_HEADER_COLOR))
        score_header = self.font.render("Очки", True, pygame.Color(TABLE_HEADER_COLOR))

        self.screen.blit(rank_header, (50, 90))
        self.screen.blit(name_header, (100, 90))
        self.screen.blit(score_header, (400, 90))

        pygame.draw.line(
            self.screen,
            pygame.Color(TABLE_HEADER_COLOR),
            (40, 115),
            (WIDTH * SCALE - 40, 115),
            1
        )

        y_offset = 130
        for i, record in enumerate(records):
            if highlight_score is not None and record.score == highlight_score:
                color = TABLE_HIGHLIGHT_COLOR
            else:
                color = TABLE_ROW_COLOR

            rank_text = self.font.render(str(i + 1), True, pygame.Color(color))
            self.screen.blit(rank_text, (50, y_offset))

            name_text = self.font.render(record.name, True, pygame.Color(color))
            self.screen.blit(name_text, (100, y_offset))

            score_text = self.font.render(str(record.score), True, pygame.Color(color))
            self.screen.blit(score_text, (400, y_offset))

            y_offset += 35

        if not records:
            empty_text = self.font.render("Нет рекордов", True, pygame.Color('gray'))
            empty_rect = empty_text.get_rect(center=((WIDTH * SCALE) // 2, (HEIGHT * SCALE) // 2))
            self.screen.blit(empty_text, empty_rect)

        hint = self.font.render("Нажмите любую клавишу для продолжения", True, pygame.Color('gray'))
        hint_rect = hint.get_rect(center=((WIDTH * SCALE) // 2, HEIGHT * SCALE - 40))
        self.screen.blit(hint, hint_rect)

    def wait_for_key(self) -> None:
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    waiting = False
            self.clock.tick(FPS)