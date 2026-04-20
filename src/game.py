from .infrastructure import Infrastructure
from .snake import Snake
from .utils import *
from .const import *

class Game:
    def __init__(self, infrastracture: Infrastructure) -> None:
        self.infrastracture = infrastracture
        head = gen_center_element()
        self.snake = Snake(head)
        self.apple = gen_apple(self.snake)
        self.tick_counter = 0
        self.snake_speed_delay = NITIAL_SPEED_DELAY
        self.is_running = True
        self.is_game_over = False
        self.score = 0

    def process_events(self) -> None:
        if self.infrastracture.is_quit_event():
            self.is_running = False
        new_direction = self.infrastracture.get_pressed_key()
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

    def render(self) ->  None:
        self.infrastracture.fill_screen()
        for e in self.snake.deque:
            self.infrastracture.draw_element(e, SNAKE_COLOR)
        
        self.infrastracture.draw_element(self.apple, APPLE_COLOR)
        self.infrastracture.draw_score(self.score)

        if self.is_game_over:
            self.infrastracture.draw_game_over()
        
        self.infrastracture.update_and_tick()


    def loop(self):
        while self.is_running:
            self.process_events()
            self.update_state()
            self.render()
        self.infrastracture.quit()