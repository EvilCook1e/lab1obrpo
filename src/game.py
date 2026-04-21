from .infrastructure import Infrastructure
from .snake import Snake
from .utils import *
from .const import *
from .scoreboard import ScoreBoard


class Game:
    def __init__(self, infrastructure: Infrastructure) -> None:
        self.infrastructure = infrastructure
        self.scoreboard = ScoreBoard()
        self.reset_game()

    def reset_game(self) -> None:
        head = gen_center_element()
        self.snake = Snake(head)
        self.apple = gen_apple(self.snake)
        self.tick_counter = 0
        self.snake_speed_delay = INITIAL_SPEED_DELAY
        self.is_running = True
        self.is_game_over = False
        self.score = 0

    def process_events(self) -> None:
        if self.infrastructure.is_quit_event():
            self.is_running = False
        new_direction = self.infrastructure.get_pressed_key()
        if new_direction is not None:
            self.snake.set_direction(new_direction)

    def update_state(self) -> None:
        if self.is_game_over:
            return
        self.tick_counter += 1

        if not self.tick_counter % self.snake_speed_delay:
            head = self.snake.get_new_head()
            if is_good_head(head, self.snake):
                self.snake.enqueue(head)
                if head == self.apple:
                    self.score += 1
                    self.apple = gen_apple(self.snake)
                else:
                    self.snake.dequeue()
            else:
                self.is_game_over = True
                self.handle_game_over()

    def handle_game_over(self) -> None:
        if self.scoreboard.is_high_score(self.score) and self.score > 0:
            player_name = self.infrastructure.get_player_name()
            if player_name:
                self.scoreboard.add_record(player_name, self.score)

    def show_scoreboard(self) -> None:
        self.infrastructure.fill_screen()
        self.infrastructure.draw_scoreboard(self.scoreboard, self.score)
        self.infrastructure.update_and_tick()
        self.infrastructure.wait_for_key()

    def render(self) -> None:
        self.infrastructure.fill_screen()
        for e in self.snake.deque:
            self.infrastructure.draw_element(e, SNAKE_COLOR)

        self.infrastructure.draw_element(self.apple, APPLE_COLOR)
        self.infrastructure.draw_score(self.score)

        if self.is_game_over:
            self.infrastructure.draw_game_over()

        self.infrastructure.update_and_tick()

    def loop(self) -> None:
        while self.is_running:
            self.process_events()
            self.update_state()
            self.render()

        self.show_scoreboard()
        self.infrastructure.quit()