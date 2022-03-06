import sys
sys.path.append("./Client")
from datetime import datetime
from api.IFriends import IFriend
from api.IClient import Iclient
import pygame as pg
from pygame import *
from types import SimpleNamespace
from tkinter import Label
import threading
WIDTH, HEIGHT = (800, 600)
REFRASH = 60
FIELD_WIDTH, FIELD_HEIGHT = (590, 175)
MSG_WIDTH, MSG_HEIGHT = (590, 355)
CLIENT_LIST_WIDTH, CLIENT_LIST_HEIGHT = (180, 540)
FILE_LIST_WIDTH, FILE_LIST_HEIGHT = (180, 540)

SEND_BUTTON_WIDTH, SEND_BUTTON_HEIGHT = (70, 30)
LOADING_BAR_WIDTH, LOADING_BAR_HEIGHT = (500, 30)
GET_FILE_BUTTON_WIDTH, GET_FILE_BUTTON_HEIGHT = (100, 30)
STOP_BUTTON_WIDTH, STOP_BUTTON_HEIGHT = (70, 30)

BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT = (150, 30)


# ------------------------------- View -------------------------------------


class GUI_Panel():

    def __init__(self, client: Iclient):
        pg.init()
        pg.font.init()
        pg.mixer.init()
        self.client = client
        self.GuiController = Selector_server(client)

    def __call__(self):
        client = self.client
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    client.close_connection_TCP()
                elif event.type == pg.KEYDOWN:
                    self.GuiController.handleButtonPress(event)
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if 1 <= event.button <= 2:
                        self.GuiController.handleClick()
                elif event.type == pg.MOUSEWHEEL:
                    self.GuiController.handleWheel(event)
            if self.GuiController.shouldAdvance():
                self.GuiController = self.GuiController.getNextViewController()

            self.GuiController.draw_screen()
        return running

    def __del__(self):
        print("Client view is distroy")


class Label:
    '''Initilaize'''

    def __init__(self, text_field: str = '', text_font: font = None) -> None:
        self.text = text_field
        self.font = text_font
        self.active = True

    def draw_label(self, surface: Surface, pos: tuple[float, float], color: Color = Color(70, 50, 111), center_text: bool = False) -> None:
        if self.active:
            if center_text:
                title_srf = self.font.render(
                    self.text, True, color)
                title_rect = title_srf.get_rect(center=pos)
                surface.blit(title_srf, title_rect)
            else:
                surface.blit(self.font.render(self.text, True, color), pos)


class Rectangle:

    def __init__(self, position: tuple[int, int], size_box: tuple[int, int]) -> None:
        self.rect: Rect = Rect(position, size_box)
        self.position = position

    '''Checks if the mouse is in the field '''

    def has_mouse(self):
        mouse_pos = pg.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)

    def gradientRect(self, window, left_colour, right_colour, target_rect):
        """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
        colour_rect = pg.Surface(
            (2, 2))                                   # tiny! 2x2 bitmap
        pg.draw.line(colour_rect, left_colour,  (0, 0),
                     (0, 1))            # left colour line
        pg.draw.line(colour_rect, right_colour, (1, 0),
                     (1, 1))            # right colour line
        colour_rect = pg.transform.smoothscale(
            colour_rect, (target_rect.width, target_rect.height))  # stretch!
        # paint it
        window.blit(colour_rect, target_rect)

    '''Draws the rectangle on Surface'''

    def draw_rect(self, surface: Surface, color: Color) -> None:
        pg.draw.rect(surface, color, self.rect, border_radius=4)


class RectLabel:
    def __init__(self, rect_label: Rectangle, lable: Label, color: Color = (204, 204, 204), text_color: Color = (0, 0, 0)) -> None:
        self.color = color
        self.label = lable
        self.rect = rect_label
        self.text_color = text_color

    def draw_rectLabel(self, surface):
        self.rect.draw_rect(surface, self.color)
        self.rect.rect.topleft = self.rect.position
        self.label.draw_label(
            surface, self.rect.rect.topleft, self.text_color, False)
        pass


class Button:

    def __init__(self, rect_button: Rectangle, text_button: Label, hover_color: Color = (0, 0, 255), text_color: Color = (0, 255, 0), rect_color: Color = (255, 0, 0)):
        self.rect_button = rect_button
        self.text_button = text_button
        self.hover_color = hover_color
        self.text_color = text_color
        self.rect_color = rect_color
        self.active = False

    '''Check if the mouse hovers over the Rectangle Button'''

    def mouse_hover(self) -> bool:
        mouse_pos = pg.mouse.get_pos()
        return self.rect_button.rect.collidepoint(mouse_pos)

    '''Check if the mouse cliked on the Rectangle Button'''

    '''Draws the rectangle button on the Surface'''

    def draw_button(self, surface, center: bool = False):
        button_color = self.rect_color
        if self.mouse_hover():
            button_color = self.hover_color
        if self.active:
            button_color = (146, 181, 233)
        self.color_now = button_color
        self.rect_button.draw_rect(surface, button_color)
        self.rect_button.rect.topleft = self.rect_button.position
        self.text_button.draw_label(
            surface, self.rect_button.rect.center, self.text_color, center)


class RectangleList:

    def __init__(self, rect_list_Button: list[Button], rect: Rectangle) -> None:
        self.rectListButton = rect_list_Button
        self.rect = rect
        self.y = 0
        self.p = 10

    def scroll(self, y):
        self.y += y

    def has_mouse(self):
        return self.rect.has_mouse()

    def draw_scerrn(self, surf: Surface):
        self.rect.draw_rect(surf, (255, 255, 255))
        for client in self.rectListButton:
            client.draw_button(surf, True)
            self.p += 55
            pass


class InputField:

    def __init__(self, label: Label, rect_angle: Rectangle):

        self.lable = label
        self.rect_angle = rect_angle
        self.length = len(label.text)
        self.ready = False
        self.active = False

    def has_mouse(self):
        return self.rect_angle.has_mouse()

    def handle_Key_Press(self, event):
        if event.key == pg.K_RETURN:
            self.ready = True
        if event.key == pg.K_BACKSPACE and self.length <= len(self.lable.text[:-1]):
            self.lable.text = self.lable.text[:-1]
        elif event.key != pg.K_BACKSPACE:
            if event.key == 32:
                self.lable.text += ' '
            else:
                self.lable.text += pg.key.name(event.key)

    def draw_InputField(self, surface, panelColor, textColor):
        if self.active:
            temp = panelColor
            panelColor = textColor
            textColor = temp
        self.rect_angle.draw_rect(surface, panelColor)
        pos = self.rect_angle.position
        self.lable.draw_label(surface, pos, textColor)


class GuiController:

    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        display.set_caption("Whats'up Client Chat ")
        self.palette = {
            "gray": (192, 192, 192),
            "white": (255, 255, 255),
            "light-green": (64, 213, 47),
            "green": (175, 237, 169),
            "red": (255, 0, 0),
            "purple": (70, 50, 111),
            "light-red": (252, 87, 87),
            "black": (0, 0, 0)
        }
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("Arial", 24, bold=True)

    def shouldAdvance(self):

        # override this
        pass

    def getNextViewController(self):

        # override this
        pass

    def handleClick(self):

        # override this
        pass

    def handleButtonPress(self, event):

        # override this
        pass

    def handleWheel(self, event):

        # override this
        pass

    def draw_screen(self):

        # override this
        pass

    def __del__(self):
        # print("Viewer controller is distroy")
        pass


class Selector_server(GuiController):

    def __init__(self, client: Iclient):

        super().__init__()

        self.client = client

        self.screen = pg.display.set_mode((400, 200), depth=32)
        display.set_caption("Connec to server")

        self.time_err = Label("Time out Error - try again ", self.font)
        self.time_err.active = False

        self.ip_Label = Label("Host:", self.font)
        txt_Label = Label("localhost", self.font)

        ip_Panel = Rectangle((100, 100), (250, 32))
        self.ip_Field = InputField(txt_Label, ip_Panel)

        self.port_Label = Label("Port:", self.font)
        txt_port_label = Label("3000", self.font)

        portPanel = Rectangle((100, 50), (250, 32))
        self.port_field = InputField(txt_port_label, portPanel)

        submitLabel = Label("Connect ", self.font)
        submitPanel = Rectangle((100, 150), (100, 32))
        self.submitButton = Button(
            submitPanel, submitLabel, self.palette["green"], self.palette["light-green"], self.palette["white"])

        self.ready = False

    def handleClick(self):

        self.port_field.active = True if self.port_field.has_mouse() else False
        self.ip_Field.active = True if self.ip_Field.has_mouse() else False

        if self.submitButton.mouse_hover():
            self.ready = True

    def handleButtonPress(self, event):

        self.time_err.active = False

        if self.port_field.active:
            self.port_field.handle_Key_Press(event)
        if self.ip_Field.active:
            self.ip_Field.handle_Key_Press(event)

    def handleWheel(self, event):
        pass

    def shouldAdvance(self):

        if self.ready:
            self.client.port = int(self.port_field.lable.text)
            self.client.host = str(self.ip_Field.lable.text)
            Succeeded = self.client.connect_to_TCP()
            if Succeeded:
                return True
            self.time_err.active = True
            self.ready = not self.ready
        return False

    def getNextViewController(self):
        return ClientLogin(self.client)

    def draw_screen(self):

        self.screen.fill(self.palette["white"])
        self.time_err.draw_label(self.screen, (100, 20), Color(255, 0, 0))

        self.port_field.draw_InputField(
            self.screen, self.palette["green"], self.palette["light-green"])
        x, y = self.port_field.rect_angle.rect.topleft
        self.port_Label.draw_label(self.screen, (x-50, y), (0, 0, 0))

        self.ip_Field.draw_InputField(
            self.screen, self.palette["green"], self.palette["light-green"])
        x, y = self.ip_Field.rect_angle.rect.topleft
        self.ip_Label.draw_label(self.screen, (x-50, y), (0, 0, 0))

        self.submitButton.draw_button(self.screen, True)

        pg.display.update()
        self.clock.tick(REFRASH)


class ClientLogin(GuiController):

    def __init__(self, client: Iclient):
        super().__init__()
        self.client = client
        self.screen = pg.display.set_mode((400, 300), depth=32)
        display.set_caption("Login")

        self.err_msg = Label("", self.font)
        self.err_msg.active = False

        self.nameLabel = Label("Username:", self.font)

        textLabel = Label("", self.font)
        namePanel = Rectangle((100, 100), (200, 32))
        self.nameField = InputField(textLabel, namePanel)

        self.passLabel = Label("password:", self.font)

        textLabel = Label("", self.font)
        passPanel = Rectangle((100, 200), (200, 32))
        self.passField = InputField(textLabel, passPanel)

        submitLabel = Label("Register", self.font)
        submitPanel = Rectangle((100, 250), (100, 32))

        self.registerButton = Button(
            submitPanel, submitLabel, self.palette["green"], self.palette["light-green"], self.palette["white"])

        submitLabel = Label("Login", self.font)
        submitPanel = Rectangle((220, 250), (100, 32))
        self.submitButton = Button(
            submitPanel, submitLabel, self.palette["green"], self.palette["light-green"], self.palette["white"])
        self.register = False
        self.ready = False

    def handleClick(self):

        self.nameField.active = True if self.nameField.has_mouse()else False
        self.passField.active = True if self.passField.has_mouse()else False

        if self.submitButton.mouse_hover():
            self.ready = True
        if self.registerButton.mouse_hover():
            self.register = True

    def handleButtonPress(self, event):
        self.err_msg.active = False

        if self.nameField.active:
            self.nameField.handle_Key_Press(event)
        if self.passField.active:
            self.passField.handle_Key_Press(event)

    def shouldAdvance(self):
        self.client.name = Name = str(self.nameField.lable.text)
        Password = str(self.passField.lable.text)
        if self.ready:
            Succeeded, msg = self.client.login(
                "login", name=Name, password=Password)
            if Succeeded:
                return True
            self.err_msg.text = msg
            self.err_msg.active = True
        elif self.register:
            Succeeded, msg = self.client.register(
                "register", name=Name, password=Password)
            self.err_msg.text = msg
            self.err_msg.active = True

        self.ready = False
        self.register = False
        return False

    def getNextViewController(self):
        th: threading.Thread = threading.Thread(target=self.client.response)
        th.start()
        return Chat(self.client)

    def draw_screen(self):

        self.screen.fill(self.palette["white"])

        self.nameField.draw_InputField(
            self.screen, self.palette["green"], self.palette["light-green"])
        x, y = self.nameField.rect_angle.rect.topleft
        self.nameLabel.draw_label(self.screen, (x, y-40), (0, 0, 0))

        self.passField.draw_InputField(
            self.screen, self.palette["green"], self.palette["light-green"])
        x, y = self.passField.rect_angle.rect.topleft
        self.passLabel.draw_label(self.screen, (x, y-40), (0, 0, 0))

        self.submitButton.draw_button(self.screen, True)

        self.registerButton.draw_button(self.screen, True)

        x = self.screen.get_rect().center[0]
        self.err_msg.draw_label(self.screen, (x, 25), (0, 0, 0), True)

        pg.display.update()
        self.clock.tick(REFRASH)

    def handleWheel(self, event):
        pass


class ChatRoom(GuiController):

    def __init__(self, name: str, client: Iclient):

        super().__init__()

        self.down = 0

        self.client = client

        self.friend: IFriend = client.friends.get(name)

        self.msg_list: list[RectLabel] = []

        self.clientName = name
        # create new text-box for log server
        self.chat_box_from = Rectangle(
            (CLIENT_LIST_WIDTH+20, 10), (MSG_WIDTH, MSG_HEIGHT))

        chat_box_to = Rectangle(
            (CLIENT_LIST_WIDTH+20, MSG_HEIGHT+20), (FIELD_WIDTH, FIELD_HEIGHT))

        label_box = Label(f"", self.font)

        self.input_box = InputField(label_box, chat_box_to)

        self.send_button = Button(
            rect_button=Rectangle(
                (WIDTH-80, CLIENT_LIST_HEIGHT+20), (SEND_BUTTON_WIDTH, SEND_BUTTON_HEIGHT)),
            text_button=Label("Send", self.font),
            hover_color=Color(self.palette["green"]),
            rect_color=Color(self.palette["light-green"]),
            text_color=Color(self.palette["black"])
        )

        try:
            self.add_msg()
        except:
            pass

    def add_msg(self):
        self.msg_list.clear()
        try:
            x = 0
            messages, f, t = self.friend.read("msg")
            for message in messages:
                rect = Rectangle(
                    (210, 335+x), ((len(message["msg"])+len(message["date"]))*11, 28))
                colorMsg = (204, 204, 204) if message["fromClient"] == self.clientName else (
                    193, 255, 166)
                date = message["date"]
                msg = message["msg"]
                msg_label = f"{msg} {date}"
                self.msg_list.append(RectLabel(rect, Label(
                    msg_label, self.font), colorMsg, (0, 0, 0)))
                x -= 30
        except Exception as e:
            print(e)

        pass

    def handleWheel(self, event):
        pass

    def shouldAdvance(self):
        pass

    def getNextViewController(self):
        pass

    def handleClick(self):
        if self.send_button.mouse_hover() and self.friend.isConnect:
            toClient = self.clientName
            msg = self.input_box.lable.text if toClient != "Friends Group" else f"{self.client.name}:" + \
                self.input_box.lable.text
            self.input_box.lable.text = ''
            dateT = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            self.friend.write("msg", msg=msg, fromClient=self.client.name,
                              toClient=self.clientName, date=dateT)
            request = "sendMsg" if toClient != "Friends Group" else "sendMsgALL"
            self.client.request(req=request, toClient=toClient, msg=msg)
            try:
                self.add_msg()
            except:
                pass
        self.input_box.active = self.input_box.has_mouse()

    def handleButtonPress(self, event):
        if self.input_box.active:
            self.input_box.handle_Key_Press(event)

    def draw_screen(self):

        self.chat_box_from.draw_rect(self.screen, self.palette["white"])
        self.input_box.draw_InputField(
            self.screen, self.palette["white"], self.palette["green"])

        self.send_button.draw_button(self.screen, True)

        limit = len(self.msg_list)-14 if (len(self.msg_list)-14) > 0 else 0
        for msg in self.msg_list[limit:]:
            msg.draw_rectLabel(self.screen)

        pg.display.update()
        self.clock.tick(REFRASH)


class Chat(GuiController):

    def __init__(self, client: Iclient):

        super().__init__()
        self.mc = client.mc
        self.client = client
        self.count_friend = 0
        self.menu_side_friend: list[Button] = []
        self.chat_room: dict[str, ChatRoom] = {}
        self.show_chat = ChatRoom("Friends Group", client)
        self.left_pos_button = 10
        self.client_list_online = Rectangle(
            (10, 10), (CLIENT_LIST_WIDTH, CLIENT_LIST_HEIGHT))
        self.clientList = RectangleList([], self.client_list_online)
        self.chat_room_label = Label("Welcome ", self.font)

        self.get_file_button = Button(
            rect_button=Rectangle((LOADING_BAR_WIDTH+20, CLIENT_LIST_HEIGHT+20),
                                  (GET_FILE_BUTTON_WIDTH, GET_FILE_BUTTON_HEIGHT)),
            text_button=Label("File List", self.font),
            hover_color=Color(self.palette["green"]),
            rect_color=Color(self.palette["light-green"]),
            text_color=Color(self.palette["black"])
        )
        self.stop_button = Button(
            rect_button=Rectangle((LOADING_BAR_WIDTH+40+GET_FILE_BUTTON_WIDTH, CLIENT_LIST_HEIGHT+20),
                                  (STOP_BUTTON_WIDTH, STOP_BUTTON_HEIGHT)),
            text_button=Label("Stop", self.font),
            hover_color=Color(self.palette["green"]),
            rect_color=Color(self.palette["light-green"]),
            text_color=Color(self.palette["black"])
        )
        self.download_c=0
        self.get_file_active = False
        self.loading_bar = Rectangle(
            (10, CLIENT_LIST_HEIGHT+20), (LOADING_BAR_WIDTH, LOADING_BAR_HEIGHT))
        self.load_list_friend()

    def load_list_friend(self, f: int = 0, t: int = 10):
        self.chat_room: dict[str, ChatRoom] = {}
        self.menu_side_friend.clear()
        self.left_pos_button = 10
        friends: list[IFriend] = list(self.client.friends.values())
        for friend in friends[f:t]:
            name = friend.name
            if name not in self.chat_room:
                with threading.Lock():
                    self.chat_room[name] = ChatRoom(name, self.client)
            button = Button(
                rect_button=Rectangle((10, self.left_pos_button), (180, 50)),
                text_button=Label(name, self.font),
                hover_color=Color(
                    self.palette["light-green"])if friend.isConnect else Color(self.palette["light-red"]),
                rect_color=Color(
                    self.palette["green"] if friend.isConnect else Color(self.palette["red"])),
                text_color=Color(self.palette["black"])
            )
            self.left_pos_button += 55
            self.menu_side_friend.append(button)
        self.clientList.rectListButton = self.menu_side_friend
        self.count_friend = len(friends)

    def shouldAdvance(self):
        if self.get_file_active:
            self.get_file_active = False
            return True
        self.clientList.rect.has_mouse()

    def getNextViewController(self):
        return Choser(self.client)

    def handleWheel(self, event):
        if self.clientList.has_mouse():
            f = self.clientList.y
            if 0 <= f <= self.count_friend:
                self.clientList.scroll(event.y)
                self.load_list_friend(f, f+10)
            else:
                self.clientList.y = 0
                pass

    def handleClick(self):
        if self.get_file_button.mouse_hover():
            self.client.request(req="getFilesList")

            self.get_file_active = True if len(
                self.client.file_list) > 0 else False

        self.show_chat.handleClick()
        if self.client_list_online.has_mouse():
            for client in self.menu_side_friend:
                if client.mouse_hover():
                    name = client.text_button.text
                    client.active = True
                    self.show_chat = self.chat_room[name]
                    self.chat_room_label.active = False
                else:
                    client.active = False
        pass

    def handleButtonPress(self, event):
        self.show_chat.handleButtonPress(event)
        pass

    def draw_screen(self):
        if self.client.mc != self.mc:
            self.load_list_friend(0, 10)
            self.show_chat.add_msg()
            self.mc = self.client.mc
        self.screen.fill(self.palette["gray"])
        self.get_file_button.draw_button(self.screen, True)
        self.stop_button.draw_button(self.screen, True)
        self.loading_bar.draw_rect(self.screen, self.palette["white"])
        if self.client.download_start:
            if self.client.download_file_count_pack==0:
                pics=LOADING_BAR_WIDTH
                self.client.download_start=False
            else:
                pics = LOADING_BAR_WIDTH/self.client.download_file_count_pack
            self.loading_bar.gradientRect(self.screen, (0, 255, 0), (0, 100, 0), pg.Rect(
                (10, CLIENT_LIST_HEIGHT+20), (pics, LOADING_BAR_HEIGHT)))
        self.clientList.draw_scerrn(self.screen)
        if not self.chat_room_label.active:
            self.show_chat.draw_screen()
        center = self.screen.get_rect().center
        self.chat_room_label.draw_label(self.screen, center, (0, 0, 0))
        pg.display.flip()
        pg.display.update()
        self.clock.tick(REFRASH)

    def __del__(self):
        print("Chat is destroyed.")


class Choser(GuiController):

    def __init__(self, client: Iclient):
        super().__init__()
        self.screen = pg.display.set_mode(
            (FILE_LIST_WIDTH+20, FILE_LIST_HEIGHT+60))
        self.client = client
        self.back_button = Button(
            rect_button=Rectangle((20, CLIENT_LIST_HEIGHT+20),
                                  (BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT)),
            text_button=Label("Back to chat", self.font),
            hover_color=Color(self.palette["green"]),
            rect_color=Color(self.palette["light-green"]),
            text_color=Color(self.palette["black"])
        )
        self.count_file = 0
        self.back_active = False

        self.menu_side_files: list[Button] = []
        self.file_list_rect = Rectangle(
            (10, 10), (FILE_LIST_WIDTH, FILE_LIST_HEIGHT))

        self.file_List = RectangleList([], self.file_list_rect)
        self.load_fileList()

    def load_fileList(self):
        self.menu_side_files.clear()
        self.left_pos_button = 10
        files: list[str] = self.client.file_list
        for friend in files:
            name = friend
            button = Button(
                rect_button=Rectangle((10, self.left_pos_button), (180, 50)),
                text_button=Label(name, self.font),
                hover_color=Color(self.palette["light-green"]),
                rect_color=Color(self.palette["green"]),
                text_color=Color(self.palette["black"])
            )
            self.left_pos_button += 55
            self.menu_side_files.append(button)
        self.file_List.rectListButton = self.menu_side_files
        self.count_file = len(files)

    def shouldAdvance(self):
        if self.back_active:
            self.back_active = False
            return True
        # override this
        pass

    def getNextViewController(self):
        return Chat(self.client)

    def handleClick(self):
        if self.back_button.mouse_hover():
            self.back_active = True
        if self.file_list_rect.has_mouse():
            for file in self.menu_side_files:
                if file.mouse_hover():
                    name = file.text_button.text
                    self.back_active = True
                    self.client.request(req="getFile", fileName=name)

    def handleButtonPress(self, event):
        pass

    def handleWheel(self, event):
        pass

    def draw_screen(self):
        self.screen.fill(self.palette["gray"])
        self.file_list_rect.draw_rect(self.screen, (255, 255, 255))
        self.back_button.draw_button(self.screen, True)
        self.file_List.draw_scerrn(self.screen)
        pg.display.update()
        self.clock.tick(REFRASH)
        pass

    def __del__(self):
        print("Viewer controller is distroy")
        pass
