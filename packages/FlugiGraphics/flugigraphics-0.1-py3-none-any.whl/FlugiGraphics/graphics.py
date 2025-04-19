import pygame

KEY_BACKSPACE = pygame.K_BACKSPACE
KEY_CAPSLOCK = pygame.K_CAPSLOCK
KEY_DELETE = pygame.K_DELETE
KEY_DOWN = pygame.K_DOWN
KEY_END = pygame.K_END
KEY_ENTER = pygame.K_RETURN
KEY_ESCAPE = pygame.K_ESCAPE
KEY_F1 = pygame.K_F1
KEY_F2 = pygame.K_F2
KEY_F3 = pygame.K_F3
KEY_F4 = pygame.K_F4
KEY_F5 = pygame.K_F5
KEY_F6 = pygame.K_F6
KEY_F7 = pygame.K_F7
KEY_F8 = pygame.K_F8
KEY_F9 = pygame.K_F9
KEY_F10 = pygame.K_F10
KEY_F11 = pygame.K_F11
KEY_F12 = pygame.K_F12
KEY_F13 = pygame.K_F13
KEY_F14 = pygame.K_F14
KEY_F15 = pygame.K_F15
KEY_HOME = pygame.K_HOME
KEY_INSERT = pygame.K_INSERT
KEY_LEFT_ALT = pygame.K_LALT
KEY_LEFT_CONTROL = pygame.K_LCTRL
KEY_LEFT = pygame.K_LEFT
KEY_LEFT_SHIFT = pygame.K_LSHIFT
KEY_LEFT_SUPER = pygame.K_LSUPER  # LWIN is known as LSUPER in Pygame
KEY_MENU = pygame.K_MENU
KEY_NUMLOCK = pygame.K_NUMLOCK
KEY_PAGE_DOWN = pygame.K_PAGEDOWN
KEY_PAGE_UP = pygame.K_PAGEUP
KEY_RIGHT_ALT = pygame.K_RALT
KEY_RIGHT_CONTROL = pygame.K_RCTRL
KEY_RIGHT = pygame.K_RIGHT
KEY_RIGHT_SHIFT = pygame.K_RSHIFT
KEY_RIGHT_SUPER = pygame.K_RSUPER  # RWIN is known as RSUPER in Pygame
KEY_SCROLLLOCK = pygame.K_SCROLLOCK
KEY_SPACE = pygame.K_SPACE
KEY_TAB = pygame.K_TAB
KEY_UP = pygame.K_UP

BTN_LEFT = 1
BTN_RIGHT = 3
BTN_MIDDLE = 2

class Event:
    def __init__(self, event):
        self.type = None
        self.keycode = None
        self.button = None
        self.pos_x = None
        self.pos_y = None

        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            self.type = 'ev_key'
            self.keycode = event.key if event.type == pygame.KEYDOWN else -event.key
        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            self.type = 'ev_mouse'
            self.button = event.button if event.type == pygame.MOUSEBUTTONDOWN else -event.button
            self.pos_x, self.pos_y = event.pos
        elif event.type == pygame.MOUSEMOTION:
            self.type = 'ev_mouse'
            self.pos_x, self.pos_y = event.pos
            self.button = 0  # No button action for motion
        elif event.type == pygame.USEREVENT:  # Assuming custom or timer events
            self.type = 'ev_timer'
            # Add additional logic if needed
        # Handle other types as needed

class BaseGraphics:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.buffer = pygame.Surface((width, height), pygame.SRCALPHA)
        self.current_pos = (0, 0)
        self.current_color = (255, 255, 255)

    def move(self, x, y):
        new_x = self.current_pos[0] + x
        new_y = self.current_pos[1] + y
        if 0 <= new_x < self.width and 0 <= new_y < self.height:
            self.current_pos = (new_x, new_y)

    def move_to(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.current_pos = (x, y)

    def color(self, color):
        self.current_color = color

    def dot(self):
        self.buffer.set_at(self.current_pos, self.current_color)

    def draw_line(self, start_pos, end_pos, color, width=1):
        pygame.draw.line(self.buffer, color, start_pos, end_pos, width)

    def line_to(self, x, y):
        self.draw_line(self.current_pos, (x, y), self.current_color)
        self.current_pos = (x, y)

    def line(self, x, y, width=1):
        end_pos = (self.current_pos[0] + x, self.current_pos[1] + y)
        self.draw_line(self.current_pos, end_pos, self.current_color, width)
        self.current_pos = end_pos

    def box(self, width, height):
        rect = pygame.Rect(self.current_pos, (width, height))
        pygame.draw.rect(self.buffer, self.current_color, rect)
        self.current_pos = (self.current_pos[0] + width, self.current_pos[1] + height)

    def box_to(self, x, y):
        width = x - self.current_pos[0]
        height = y - self.current_pos[1]
        self.box(width, height)
        self.current_pos = (x, y)

    def text(self, x, y, text, font_name='Arial', size=24, color=(255, 255, 255)):
        font = pygame.font.SysFont(font_name, size)
        text_surface = font.render(text, True, color)
        self.buffer.blit(text_surface, (x, y))

class FlugiGraphics(BaseGraphics):
    def __init__(self, width, height):
        super().__init__(width, height)
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True

    def get_events(self):
        return [Event(event) for event in pygame.event.get()]

    def refresh(self):
        self.screen.blit(self.buffer, (0, 0))
        pygame.display.flip()

    def is_quit_event(self, event):
        return event.type == pygame.QUIT

    def tick(self, fps):
        self.clock.tick(fps)

    def quit(self):
        pygame.quit()

    def show_mouse(self, show):
        pygame.mouse.set_visible(show)

    def move_mouse(self, x, y):
        pygame.mouse.set_pos(x, y)

class Canvas(BaseGraphics):
    def draw_to(self, target_surface, x, y):
        target_surface.blit(self.buffer, (x, y))

    def set_pixel(self, x, y, color):
        self.buffer.set_at((x, y), color)

    def save(self, filename):
        pygame.image.save(self.buffer, filename)

    def transparent(self, is_transparent):
        if is_transparent:
            self.buffer = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        else:
            self.buffer = pygame.Surface((self.width, self.height))

    def load_font(self, filename, fontsize, antialias=True):
        self.font = pygame.font.Font(filename, fontsize)
        self.antialiasing = antialias

    def antialias(self, is_antialias):
        self.antialiasing = is_antialias