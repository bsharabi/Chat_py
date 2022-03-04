import sys
sys.path.append("./Server")
import threading
import json
from pygame import *
import pygame as pg
from BLL.TCP_server import Iserver
WIDTH, HEIGHT = (800, 600)
REFRASH = 60

# ------------------------------- View -------------------------------------


class GUI_Panel():

    def __init__(self, server: Iserver):
        pg.init()
        pg.font.init()
        pg.mixer.init()
        self.server = server
        self.GuiController = GuiController(server)
        self.down = 19
        self.mc=0
        self.up = 0

    def scroll_mouse(self, op):
        self.down += op
        self.up += op

    def __call__(self):
        running = self.server.connect_to_TCP()
        server_thread = threading.Thread(target=self.server)
        if not running:
            return
        server_thread.start()
        while running:
            for e in pg.event.get():
                if e.type == QUIT:
                    running = not self.server.close_connection_TCP()
                elif e.type == pg.MOUSEBUTTONDOWN:
                    if self.GuiController.shouldExit():
                        running = not self.server.close_connection_TCP()
                        return
                if e.type == pg.MOUSEWHEEL:
                    if e.y == -1:
                        self.scroll_mouse(1)
                    elif e.y == 1:
                        if self.down > 19:
                            self.scroll_mouse(-1)
            ##TODO check if this same log 
            if self.mc!=self.server.mc:
                log_list, self.up, self.down = self.server.read_file_log(
                    f=self.up, to=self.down)
                self.mc=self.server.mc

            self.GuiController.add_log(log_list)
            self.GuiController.draw_screen()

    def __del__(self):
        print("Server distroy")


class Label:

    def __init__(self, text_field: str = '', text_font: font = None) -> None:
        self.text = text_field
        self.font = text_font
        self.active = True

    def draw_label(self, surface: Surface, pos: tuple[float, float], color: Color = Color(0, 0, 0), center_text: bool = False) -> None:
        if self.active:
            if center_text:
                title_srf = self.font.render(
                    self.text, True, Color(70, 50, 111))
                title_rect = title_srf.get_rect(center=pos)
                surface.blit(title_srf, title_rect)
            else:
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

    def draw_button(self, surface, center: bool = False):
        button_color = self.hover_color
        text_color = self.click_color
        if self.mouse_listener():
            button_color = self.click_color
            text_color = self.hover_color
        self.rect_button.draw_rect(surface, button_color)
        self.text_button.draw_label(
            surface, self.rect_button.rect.center, text_color, center)


class GuiController:

    def __init__(self, server: Iserver):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), depth=32)
        display.set_caption("Server")

        self.server = server
        self.palette = {
            "gray": (192, 192, 192),
            "white": (255, 255, 255),
            "light-green": (64, 213, 47),
            "green": (175, 237, 169),
            "red": (255, 0, 0)
        }
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("Arial", 24)
        self.log_list: list[Label] = []

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
        self.port_label = Label(
            f"Listening on port {self.server.port}", self.font)

    def shouldExit(self):
        return self.quitButton.mouse_listener()

    def add_log(self, logs: list):
        self.log_list.clear()
        for log in logs:
            log = Label(log["log"], self.font)
            self.log_list.append(log)

    def draw_screen(self):
        self.screen.fill(self.palette["gray"])
        self.cmd_server.draw_rect(self.screen, self.palette["white"])
        self.port_label.draw_label(
            self.screen, (300, 0), self.palette["light-green"])
        self.quitButton.draw_button(self.screen, True)

        x = 0
        limit = len(self.log_list)-19 if (len(self.log_list)-19) > 0 else 0
        for log in self.log_list[limit:]:
            log.draw_label(self.screen, (30, 40+x), (0, 0, 0,))
            x += 25

        pg.display.update()
        self.clock.tick(REFRASH)

    def __del__(self):
        print("Viewer controller is distroy")
