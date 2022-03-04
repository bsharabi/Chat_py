import sys
sys.path.append("./Client")
from base64 import decode
import threading
import json
from tkinter import Label
from types import SimpleNamespace
from turtle import pos
from pygame import *
import pygame as pg
from api.IClient  import Iclient
from api.IFriends  import IFriend

WIDTH, HEIGHT = (800, 600)
REFRASH = 60
FIELD_WIDTH, FIELD_HEIGHT = (590, 175)
MSG_WIDTH, MSG_HEIGHT = (590, 355)
CLIENT_LIST_WIDTH, CLIENT_LIST_HEIGHT = (180, 540)
SEND_BUTTON_WIDTH, SEND_BUTTON_HEIGHT = (70, 30)
LOADING_BAR_WIDTH, LOADING_BAR_HEIGHT = (500, 30)
GET_FILE_BUTTON_WIDTH, GET_FILE_BUTTON_HEIGHT = (45, 30)
PUT_FILE_BUTTON_WIDTH, PUT_FILE_BUTTON_HEIGHT = (45, 30)

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
                elif event.type == pg.MOUSEBUTTONDOWN :
                    if 1<=event.button<= 2:
                        self.GuiController.handleClick()
                elif event.type == pg.MOUSEWHEEL:
                        self.GuiController.handleWheel(event)
            if self.GuiController.shouldAdvance():
                self.GuiController = self.GuiController.getNextViewController()

            self.GuiController.draw_screen()
        return running

    def __del__(self):
        print("Server distroy")



        
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

    '''Draws the rectangle on Surface'''

    def draw_rect(self, surface: Surface, color: Color) -> None:
        pg.draw.rect(surface, color, self.rect)

class RectLabel():
    def __init__(self,rect_label: Rectangle,lable: Label,color:Color=(204,204,204),text_color:Color=(0,0,0)) -> None:
        self.color=color
        self.label=lable
        self.rect=rect_label
        self.text_color=text_color
        
        
    def draw_rectLabel(self,surface,pos):
        self.rect.rect.update(pos[0],pos[1])
        self.rect.draw_rect(surface, self.color)
        self.rect.rect.topleft = self.rect.position
        self.label.draw_label(
            surface, self.rect.rect.center, self.text_color, False)
        pass
        
class Button:

    def __init__(self, rect_button: Rectangle, text_button: Label, hover_color: Color = (0, 0, 255), text_color: Color = (0, 255, 0), rect_color: Color = (255, 0, 0)):
        self.rect_button = rect_button
        self.text_button = text_button
        self.hover_color = hover_color
        self.text_color = text_color
        self.rect_color = rect_color

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
            if event.key== 32:
                self.lable.text +=' '
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
            "light-red": (252, 87, 87)
        }
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("Arial", 24, bold=True)

    def scale(data, min_screen, max_screen, min_data, max_data):
        """
        get the scaled data with proportions min_data, max_data
        relative to min and max screen dimentions
        """
        return ((data - min_data) / (max_data-min_data)) * (max_screen - min_screen) + min_screen

    def shouldAdvance(self, client):

        # override this
        pass

    def getNextViewController(self):

        # override this
        pass

    def handleClick(self, client):

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
        print("Viewer controller is distroy")

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

        submitLabel = Label("Registar", self.font)
        submitPanel = Rectangle((100, 250), (100, 32))

        self.registarButton = Button(
            submitPanel, submitLabel, self.palette["green"], self.palette["light-green"], self.palette["white"])

        submitLabel = Label("Login", self.font)
        submitPanel = Rectangle((220, 250), (100, 32))
        self.submitButton = Button(
            submitPanel, submitLabel, self.palette["green"], self.palette["light-green"], self.palette["white"])
        self.registar = False
        self.ready = False

    def handleClick(self):

        self.nameField.active = True if self.nameField.has_mouse()else False
        self.passField.active = True if self.passField.has_mouse()else False

        if self.submitButton.mouse_hover():
            self.ready = True
        if self.registarButton.mouse_hover():
            self.registar = True

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
        elif self.registar:
            Succeeded, msg = self.client.register(
                "registar", name=Name, password=Password)
            self.err_msg.text = msg
            self.err_msg.active = True

        self.ready = False
        self.registar = False
        return False

    def getNextViewController(self):
        threading.Thread(target=self.client.response).start()
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

        self.registarButton.draw_button(self.screen, True)

        x = self.screen.get_rect().center[0]
        self.err_msg.draw_label(self.screen, (x, 25), (0, 0, 0), True)

        pg.display.update()
        self.clock.tick(REFRASH)

    def handleWheel(self, event):
        pass

class ChatRoom(GuiController):

    def __init__(self, name: str,client:Iclient):
        
        super().__init__()
        
        self.down=0
        
        self.client=client
        
        self.friend:IFriend=client.friends.get(name)
        
        self.msg_list:list[RectLabel]=[]
        
        self.clientName = name
        # create new text-box for log server
        self.chat_box_from = Rectangle(
            (CLIENT_LIST_WIDTH+20, 10), (MSG_WIDTH, MSG_HEIGHT))
        
        chat_box_to = Rectangle(
            (CLIENT_LIST_WIDTH+20, MSG_HEIGHT+20), (FIELD_WIDTH, FIELD_HEIGHT))
        
        label_box = Label(f"", self.font)
        
        self.input_box = InputField(label_box, chat_box_to)

        self.loading_bar = Rectangle(
            (10, CLIENT_LIST_HEIGHT+20), (LOADING_BAR_WIDTH, LOADING_BAR_HEIGHT))

        self.send_button = Button(
            rect_button=Rectangle(
                (WIDTH-80, CLIENT_LIST_HEIGHT+20), (SEND_BUTTON_WIDTH, SEND_BUTTON_HEIGHT)),
            text_button=Label("Send", self.font),
            hover_color=Color(self.palette["green"]),
            rect_color=Color(self.palette["light-green"]),
            text_color=Color(self.palette["red"])
        )

        self.get_file_button = Button(
            rect_button=Rectangle((LOADING_BAR_WIDTH+20, CLIENT_LIST_HEIGHT+20),
                                  (GET_FILE_BUTTON_WIDTH, GET_FILE_BUTTON_HEIGHT)),
            text_button=Label("Get", self.font),
            hover_color=Color(self.palette["green"]),
            rect_color=Color(self.palette["light-green"]),
            text_color=Color(self.palette["red"])
        )
                
        self.put_file_button = Button(
            rect_button=Rectangle((LOADING_BAR_WIDTH+30+GET_FILE_BUTTON_WIDTH,
                                  CLIENT_LIST_HEIGHT+20), (PUT_FILE_BUTTON_WIDTH, PUT_FILE_BUTTON_HEIGHT)),
            text_button=Label("Put", self.font),
            hover_color=Color(self.palette["green"]),
            rect_color=Color(self.palette["light-green"]),
            text_color=Color(self.palette["red"])
        )
        try:
            self.add_msg()
        except:
            pass

    def add_msg(self):
        self.msg_list.clear()
        try:
            messages,f,t=self.friend.read("msg")
            for message in messages:
                rect=Rectangle((0,0),(10,len(message)))
                self.msg_list.append(RectLabel(rect, Label(message["msg"],self.font),(204,204,204),(0,0,0)))
        except:
            pass
        
        pass
    
    def handleWheel(self, event):
        pass

    def shouldAdvance(self):
        pass
    
    def getNextViewController(self):
        pass

    def handleClick(self):
        if self.send_button.mouse_hover():
            toClient = self.clientName
            msg = f"{self.client.name}: "+self.input_box.lable.text
            self.input_box.lable.text=''
            self.friend.write("msg",msg=msg)
            self.client.request(req="sendMsg",toClient=toClient,msg=msg)
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

        self.loading_bar.draw_rect(self.screen, self.palette["white"])
        self.send_button.draw_button(self.screen, True)
        self.get_file_button.draw_button(self.screen, True)
        self.put_file_button.draw_button(self.screen, True)
        x = 0
        limit = len(self.msg_list)-14 if (len(self.msg_list)-14) > 0 else 0
        for msg in self.msg_list[limit:]:
            msg.draw_rectLabel(self.screen,(210, 335+x))
            # msg.draw_label(self.screen, (210, 335+x), (0, 0, 0))
            x -= 25
        pg.display.update()
        self.clock.tick(REFRASH)

class Chat(GuiController):

    def __init__(self, client: Iclient):

        super().__init__()
        self.mc = client.mc
        self.client = client
        self.count_friend=0
        self.menu_side_friend: list[Button] = []
        self.chat_room: dict[str, ChatRoom] = {}
        self.show_chat = ChatRoom("ALL",client)
        self.left_pos_button = 10
        self.client_list_online = Rectangle(
            (10, 10), (CLIENT_LIST_WIDTH, CLIENT_LIST_HEIGHT))
        self.clientList = RectangleList([], self.client_list_online)
        self.chat_room_label = Label("Hello There click ", self.font)
        self.refresh = False
        self.refresh_button = Button(
            rect_button=Rectangle((LOADING_BAR_WIDTH+140, CLIENT_LIST_HEIGHT+20),
                                  (GET_FILE_BUTTON_WIDTH, GET_FILE_BUTTON_HEIGHT)),
            text_button=Label("Get", self.font),
            hover_color=Color(self.palette["light-green"]),
            rect_color=Color(self.palette["green"]),
            text_color=Color(self.palette["purple"])
        )
        self.load_list_friend()
        # self.client.observ.append(self.load_list_friend)

    def load_list_friend(self, f: int = 0, t: int = 10):
        self.chat_room: dict[str, ChatRoom] = {}
        self.menu_side_friend.clear()
        self.left_pos_button = 10
        friends: list[ IFriend] = list(self.client.friends.values())
        for friend in friends[f:t]:
            name=friend.name
            if name not in self.chat_room:
                self.chat_room[name] = ChatRoom(name,self.client)
            button = Button(
                rect_button=Rectangle((10, self.left_pos_button), (180, 50)),
                text_button=Label(name, self.font),
                hover_color=Color(
                    self.palette["light-green"])if friend.isConnect else Color(self.palette["light-red"]),
                rect_color=Color(
                    self.palette["green"] if friend.isConnect else Color(self.palette["red"])),
                text_color=Color(self.palette["purple"])
            )
            self.left_pos_button += 55
            self.menu_side_friend.append(button)
        self.clientList.rectListButton = self.menu_side_friend
        self.count_friend=len(friends)

    def shouldAdvance(self):
        if self.refresh:
            self.refresh = False
        self.clientList.rect.has_mouse()

    def getNextViewController(self):
        return Selector_server()

    def handleWheel(self, event):
        if self.clientList.has_mouse():
            f = self.clientList.y
            if 0<=f<=self.count_friend:
                self.clientList.scroll(event.y)
                self.load_list_friend(f, f+10)
            else:
                self.clientList.y=0
                pass
    
    def handleClick(self):

        self.show_chat.handleClick()

        if self.refresh_button.mouse_hover():
            self.refresh = True
        for client in self.menu_side_friend:
            if client.mouse_hover():
                name = client.text_button.text
                self.show_chat = self.chat_room[name]
                self.chat_room_label.active = False

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
        self.clientList.draw_scerrn(self.screen)
        self.refresh_button.draw_button(self.screen, True)
        if not self.chat_room_label.active:
            self.show_chat.draw_screen()
        center = self.screen.get_rect().center
        self.chat_room_label.draw_label(self.screen, center, (0, 0, 0))

        pg.display.update()
        self.clock.tick(REFRASH)

    def __del__(self):
        print("Chat is destroyed.")