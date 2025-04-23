import sys

try:
    import pygame
except:
    print("PyGame is not installed.")
    sys.exit()

from pygame import mixer

class MiniEngine:
    def __init__(self, pix_size=10, pix_per_x=64, pix_per_y=64, title="MiniEngine", icon_path=None):
        pygame.init()
        self.pix_size = pix_size
        self.width = pix_per_x * pix_size
        self.height = pix_per_y * pix_size
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.NOFRAME)
        pygame.display.set_caption(title)
        if icon_path:
            try:
                icon = pygame.image.load(icon_path)
                pygame.display.set_icon(icon)
            except:
                print("Icon load failed.")
        else:
            pygame.display.set_icon(pygame.Surface((32, 32)))
        self.buffer = {}
        self._keys_state = None
        self._mouse_buttons_state = None
        self.running = True
        self.clock = pygame.time.Clock()
        mixer.init()

    def draw_pixel(self, x, y, color):
        self.buffer[(x, y)] = color

    def clear(self):
        self.buffer.clear()

    def update(self):
        self.screen.fill((0, 0, 0))
        for (x, y), color in self.buffer.items():
            pygame.draw.rect(self.screen, color, (x * self.pix_size, y * self.pix_size, self.pix_size, self.pix_size))
        pygame.display.flip()
        self._handle_events()
        self._update_key_state()
        self._update_mouse_button_state()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _update_key_state(self):
        self._keys_state = pygame.key.get_pressed()

    def _update_mouse_button_state(self):
        self._mouse_buttons_state = pygame.mouse.get_pressed()

    def is_key_pressed(self, key_name):
        if self._keys_state is not None:
            try:
                key_code = pygame.key.key_code(key_name)
                return self._keys_state[key_code]
            except pygame.error:
                print(f"Unknown key: {key_name}.")
                return False
        return False

    def is_mouse_button_pressed(self, button):
        if self._mouse_buttons_state is not None:
            if 1 <= button <= 3:
                return self._mouse_buttons_state[button - 1]
            else:
                print(f"Unknown mouse button: {button}. Use 1, 2, or 3.")
                return False
        return False

    def get_mouse_pos(self):
        mx, my = pygame.mouse.get_pos()
        return mx // self.pix_size, my // self.pix_size

    def play_sound(self, path):
        try:
            sound = mixer.Sound(path)
            sound.play()
        except:
            print("Error playing sound.")

    def is_running(self):
        return self.running

    def tick(self, fps=60):
        self.clock.tick(fps)

    def quit(self):
        pygame.quit()