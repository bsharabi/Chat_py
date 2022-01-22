from pygame import *
import pygame as pg

WIDTH, HEIGHT = (800, 600)
REFRASH = 60

# ------------------------------- View -------------------------------------

class GUI_Panel():

    def __init__(self,port):
        pg.init()
        pg.font.init()
        pg.mixer.init()
        self.GuiController = GuiController(port)

    def cmd_console(self):
        pass

    def log_console(self):
        pass

    def __call__(self):
        running = True
        for e in pg.event.get():
            if e.type == QUIT:
                running = False
            elif e.type == pg.MOUSEBUTTONDOWN:
                running = not self.GuiController.shouldExit()
        self.GuiController.draw_screen()
        return running

    def __del__(self):
        print("Server distroy")

class Label:
    
    def __init__(self, text_field: str = '', text_font: font = None) -> None:
        self.text = text_field
        self.font = text_font

    def draw_label(self, surface: Surface, pos: tuple[float, float], color: Color = Color(0, 0, 0)) -> None:
        surface.blit(self.font.render(self.text, True, color), pos)

class Rectangle:

    def __init__(self, position: tuple[int, int], size_box: tuple[int, int]) -> None:
        self.rect: Rect = Rect(position, size_box)
        self.position = position

    def draw_rect(self, surface: Surface, color: Color) -> None:
        pg.draw.rect(surface, color, self.rect)

class Button:

    def __init__(self, rect_button: Rectangle, text_button: Label, hover_color: Color = (255, 255, 255), click_color: Color = (255, 255, 255)):
        self.rect_button = rect_button
        self.text_button = text_button
        self.hover_color = hover_color
        self.click_color = click_color

    def mouse_listener(self) -> bool:
        mouse_pos = pg.mouse.get_pos()
        return self.rect_button.rect.collidepoint(mouse_pos)

    def draw_button(self, surface):
        button_color = self.hover_color
        text_color = self.click_color
        if self.mouse_listener():
            button_color = self.click_color
            text_color = self.hover_color
        self.rect_button.draw_rect(surface, button_color)
        self.text_button.draw_label(
            surface, self.rect_button.position, text_color)

class GuiController:

    def __init__(self, port):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), depth=32)
        display.set_caption("Server")
        self.palette = {
            "gray": (192, 192, 192),
            "white": (255, 255, 255),
            "light-green": (64, 213, 47),
            "green": (175, 237, 169),
            "red": (255, 0, 0)
        }
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("Arial", 24)

        # create new text-box for log server
        self.cmd_server = Rectangle((20, 30), (760, 500))

        # create new button
        self.quitButton = Button(
            rect_button=Rectangle((20, 550), (200, 40)),
            text_button=Label("Shut Down Server", self.font),
            hover_color=Color(self.palette["green"]),
            click_color=Color(self.palette["light-green"])
        )

        self.log_label = Label("...", self.font)
        self.port_label = Label(f"Listening on port {port}", self.font)

    def shouldExit(self):
        return self.quitButton.mouse_listener()

    def draw_screen(self):
        self.screen.fill(self.palette["gray"])
        self.cmd_server.draw_rect(self.screen, self.palette["white"])
        self.port_label.draw_label(
            self.screen, (300, 0), self.palette["light-green"])
        self.quitButton.draw_button(self.screen)

        pg.display.update()
        self.clock.tick(REFRASH)

    def __del__(self):
        print("Viewer controller is distroy")
