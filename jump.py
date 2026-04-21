import pygame
import random
import sys
import struct
import os
from dataclasses import dataclass
from typing import List, Optional

pygame.init()

WIDTH = 800
HEIGHT = 400
GROUND = HEIGHT - 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Прыгун")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)


@dataclass
class Record:
    name: str
    score: int
    MAX_NAME_LENGTH: int = 20

    def __post_init__(self):
        if len(self.name) > self.MAX_NAME_LENGTH:
            self.name = self.name[:self.MAX_NAME_LENGTH]


class ScoreBoard:
    def __init__(self, filename: str = "jump_records.dat", max_records: int = 10):
        self.filename = filename
        self.max_records = max_records
        self.records: List[Record] = []
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self.filename):
            self.records = []
            return

        self.records = []
        try:
            with open(self.filename, 'rb') as f:
                while True:
                    name_bytes = f.read(40)
                    score_bytes = f.read(4)
                    if len(name_bytes) < 40 or len(score_bytes) < 4:
                        break
                    try:
                        name = name_bytes.decode('utf-16le').rstrip('\x00')
                    except UnicodeDecodeError:
                        continue
                    score = struct.unpack('<i', score_bytes)[0]
                    self.records.append(Record(name=name, score=score))
        except (IOError, struct.error):
            self.records = []
        self._sort()

    def _save(self) -> None:
        try:
            with open(self.filename, 'wb') as f:
                for record in self.records[:self.max_records]:
                    name_encoded = record.name.encode('utf-16le')
                    name_padded = name_encoded.ljust(40, b'\x00')
                    score_encoded = struct.pack('<i', record.score)
                    f.write(name_padded)
                    f.write(score_encoded)
        except IOError:
            pass

    def _sort(self) -> None:
        self.records.sort(key=lambda r: r.score, reverse=True)

    def add_record(self, name: str, score: int) -> bool:
        if not self.is_high_score(score):
            return False
        new_record = Record(name=name, score=score)
        self.records.append(new_record)
        self._sort()
        if len(self.records) > self.max_records:
            self.records = self.records[:self.max_records]
        self._save()
        return True

    def is_high_score(self, score: int) -> bool:
        if len(self.records) < self.max_records:
            return True
        return score > self.records[-1].score

    def get_records(self) -> List[Record]:
        return self.records.copy()


def get_player_name(current_score: int) -> str:
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
                    if len(name) < 20 and event.unicode.isprintable():
                        name += event.unicode

        screen.fill((30, 30, 30))

        title = font.render("ВВЕДИТЕ ВАШЕ ИМЯ", True, (255, 255, 0))
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
        screen.blit(title, title_rect)

        score_text = font.render(f"Ваш счёт: {current_score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
        screen.blit(score_text, score_rect)

        hint = small_font.render("Enter - подтвердить, Esc - отмена", True, (128, 128, 128))
        hint_rect = hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
        screen.blit(hint, hint_rect)

        input_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 15, 300, 40)
        pygame.draw.rect(screen, (50, 50, 50), input_rect)
        pygame.draw.rect(screen, (255, 255, 255), input_rect, 2)

        display_name = name
        cursor_timer += 1
        if (cursor_timer // 30) % 2 == 0:
            display_name += "|"

        name_surface = font.render(display_name, True, (255, 255, 255))
        name_rect = name_surface.get_rect(center=input_rect.center)
        screen.blit(name_surface, name_rect)

        length_hint = small_font.render(f"{len(name)}/20", True, (128, 128, 128))
        screen.blit(length_hint, (input_rect.right - 40, input_rect.bottom + 5))

        pygame.display.update()
        clock.tick(60)

    return name.strip()


def draw_scoreboard(scoreboard: ScoreBoard, highlight_score: int = None) -> None:
    records = scoreboard.get_records()

    screen.fill((30, 30, 30))

    header = font.render("ТАБЛИЦА РЕКОРДОВ", True, (0, 255, 255))
    header_rect = header.get_rect(center=(WIDTH // 2, 50))
    screen.blit(header, header_rect)

    rank_header = small_font.render("N", True, (0, 255, 255))
    name_header = small_font.render("Имя", True, (0, 255, 255))
    score_header = small_font.render("Очки", True, (0, 255, 255))

    screen.blit(rank_header, (150, 100))
    screen.blit(name_header, (200, 100))
    screen.blit(score_header, (550, 100))

    pygame.draw.line(screen, (0, 255, 255), (130, 125), (650, 125), 1)

    y_offset = 140
    for i, record in enumerate(records):
        if highlight_score is not None and record.score == highlight_score:
            color = (255, 255, 0)
        else:
            color = (255, 255, 255)

        rank_text = small_font.render(str(i + 1), True, color)
        screen.blit(rank_text, (150, y_offset))

        name_text = small_font.render(record.name, True, color)
        screen.blit(name_text, (200, y_offset))

        score_text = small_font.render(str(record.score), True, color)
        screen.blit(score_text, (550, y_offset))

        y_offset += 30

    if not records:
        empty_text = small_font.render("Нет рекордов", True, (128, 128, 128))
        empty_rect = empty_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(empty_text, empty_rect)

    hint = small_font.render("Нажмите любую клавишу для продолжения", True, (128, 128, 128))
    hint_rect = hint.get_rect(center=(WIDTH // 2, HEIGHT - 40))
    screen.blit(hint, hint_rect)

    pygame.display.update()


def wait_for_key() -> None:
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.KEYDOWN:
                waiting = False
        clock.tick(60)


def game_over_screen(score: int, scoreboard: ScoreBoard) -> None:
    if scoreboard.is_high_score(score) and score > 0:
        player_name = get_player_name(score)
        if player_name:
            scoreboard.add_record(player_name, score)

    screen.fill((255, 255, 255))
    game_over_text = font.render("ИГРА ОКОНЧЕНА", True, (255, 0, 0))
    score_text = font.render(f"Ваш счёт: {score}", True, (0, 0, 0))
    restart_text = small_font.render("Нажмите ПРОБЕЛ чтобы играть снова", True, (0, 0, 0))
    records_text = small_font.render("Нажмите R для просмотра рекордов", True, (0, 0, 0))

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 80))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 30))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))
    screen.blit(records_text, (WIDTH // 2 - records_text.get_width() // 2, HEIGHT // 2 + 60))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                elif event.key == pygame.K_r:
                    draw_scoreboard(scoreboard, score)
                    wait_for_key()
                    screen.fill((255, 255, 255))
                    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 80))
                    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 30))
                    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))
                    screen.blit(records_text, (WIDTH // 2 - records_text.get_width() // 2, HEIGHT // 2 + 60))
                    pygame.display.update()


def run_game() -> None:
    dino_x = 80
    dino_y = GROUND - 40
    dino_width = 30
    dino_height = 40
    dino_vel_y = 0
    is_jumping = False

    cactus_x = WIDTH
    cactus_width = 20
    cactus_height = 30
    cactus_speed = 7

    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, score
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not is_jumping:
                    is_jumping = True
                    dino_vel_y = -15

        if is_jumping:
            dino_vel_y += 1
            dino_y += dino_vel_y
            if dino_y >= GROUND - dino_height:
                dino_y = GROUND - dino_height
                is_jumping = False

        cactus_x -= cactus_speed
        if cactus_x < -cactus_width:
            cactus_x = WIDTH
            score += 1
            if score % 5 == 0:
                cactus_speed += 1

        dino_rect = pygame.Rect(dino_x, dino_y, dino_width, dino_height)
        cactus_rect = pygame.Rect(cactus_x, GROUND - cactus_height, cactus_width, cactus_height)

        if dino_rect.colliderect(cactus_rect):
            running = False

        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 0), (0, GROUND, WIDTH, 3))
        pygame.draw.rect(screen, (0, 0, 0), (dino_x, dino_y, dino_width, dino_height))
        pygame.draw.circle(screen, (255, 255, 255), (dino_x + 25, dino_y + 10), 3)
        pygame.draw.circle(screen, (0, 0, 0), (dino_x + 25, dino_y + 10), 1)
        pygame.draw.rect(screen, (0, 150, 0), (cactus_x, GROUND - cactus_height, cactus_width, cactus_height))
        pygame.draw.rect(screen, (0, 150, 0), (cactus_x + 5, GROUND - cactus_height - 15, 10, 15))

        text = font.render(f"Счёт: {score}", True, (0, 0, 0))
        screen.blit(text, (10, 10))

        pygame.display.update()
        clock.tick(60)

    return True, score


def main() -> None:
    scoreboard = ScoreBoard("jump_records.dat")

    while True:
        play_again, score = run_game()
        if not play_again:
            break
        game_over_screen(score, scoreboard)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()