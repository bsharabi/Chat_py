from base64 import decode
import socket
import threading
import json
from types import SimpleNamespace
from turtle import pos
from pygame import *
import pygame as pg
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

    def __init__(self,client):
        pg.init()
        pg.font.init()
        pg.mixer.init()
        self.GuiController = Selector_server()
        self.client=client

    def cmd_console(self):
        pass

    def log_console(self):
        pass

    def __call__(self):
        client=self.client
        running = True  
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    self.GuiController.handleButtonPress(event)
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.GuiController.handleClick(client)

            if self.GuiController.shouldAdvance(client):
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

    '''Checks if the mouse is in the field '''

    def has_mouse(self):
        mouse_pos = pg.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)

    '''Draws the rectangle on Surface'''

    def draw_rect(self, surface: Surface, color: Color) -> None:
        pg.draw.rect(surface, color, self.rect)

class Button:

    def __init__(self, rect_button: Rectangle, text_button: Label, hover_color: Color = (0, 0, 255), click_color: Color = (0, 255, 0), rect_color: Color = (255, 0, 0)):
        self.rect_button = rect_button
        self.text_button = text_button
        self.hover_color = hover_color
        self.click_color = click_color
        self.rect_color = rect_color

    '''Check if the mouse hovers over the Rectangle Button'''

    def mouse_hover(self) -> bool:
        mouse_pos = pg.mouse.get_pos()
        return self.rect_button.rect.collidepoint(mouse_pos)

    '''Check if the mouse cliked on the Rectangle Button'''

    def mouse_click(self) -> bool:
        for e in pg.event.get():
            if e.type == MOUSEBUTTONDOWN:
                return self.mouse_hover()
            elif e.type == MOUSEBUTTONUP:
                mouse_pos = pg.mouse.get_pos()
                if self.rect_button.rect.collidepoint(mouse_pos):
                    pass
        return False
    '''Draws the rectangle button on the Surface'''

    def draw_button(self, surface, center: bool = False):
        button_color = self.hover_color
        text_color = self.rect_color
        if self.mouse_hover():
            button_color = self.rect_color
            text_color = self.hover_color
        if self.mouse_click():
            button_color = self.click_color
            text_color = self.hover_color

        self.rect_button.draw_rect(surface, button_color)
        self.rect_button.rect.topleft = self.rect_button.position
        self.text_button.draw_label(
            surface, self.rect_button.rect.center, text_color, center)

class RectangleList:

    def __init__(self, rect_list: list[Button], rect: Rectangle) -> None:
        self.rectList = rect_list
        self.rect = rect

    def draw_scerrn(self, surf: Surface):
        self.rect.draw_rect(surf, (255, 255, 255))
        for client in self.rectList:
            client.draw_button(surf, True)
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
            print("backspace")
        elif event.key != pg.K_BACKSPACE:
            self.lable.text += pg.key.name(event.key)
            print("else")

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
            "red": (255, 0, 0)
        }
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("Arial", 24, bold=True)

    def scale(data, min_screen, max_screen, min_data, max_data):
        """
        get the scaled data with proportions min_data, max_data
        relative to min and max screen dimentions
        """
        return ((data - min_data) / (max_data-min_data)) * (max_screen - min_screen) + min_screen

    def shouldAdvance(self, controller):

        # override this
        pass

    def getNextViewController(self):

        # override this
        pass

    def handleClick(self,client):

        # override this
        pass

    def handleButtonPress(self, event):

        # override this
        pass

    def draw_screen(self):

        # override this
        pass

    def __del__(self):
        print("Viewer controller is distroy")

class Selector_server(GuiController):

    def __init__(self):

        super().__init__()
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

    def handleClick(self,client):

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

    def shouldAdvance(self, client):

        if self.ready:
            client.port = int(self.port_field.lable.text)
            client.host = str(self.ip_Field.lable.text)
            Succeeded = client.connect_to_server()
            if Succeeded:
                return True
            self.time_err.active = True
            self.ready = not self.ready
        return False

    def getNextViewController(self):
        return ClientLogin()

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

    def __init__(self):
        super().__init__()
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
        
        self.registarButton=Button(
            submitPanel, submitLabel, self.palette["green"], self.palette["light-green"], self.palette["white"])
        
        submitLabel = Label("Login", self.font)
        submitPanel = Rectangle((220, 250), (100, 32))
        self.submitButton = Button(
            submitPanel, submitLabel, self.palette["green"], self.palette["light-green"], self.palette["white"])
        self.registar=False
        self.ready = False

    def handleClick(self,client):

        self.nameField.active =True if  self.nameField.has_mouse()else False
        self.passField.active =True if  self.passField.has_mouse()else False
        
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

    def shouldAdvance(self, controller):
        name=str(self.nameField.lable.text)
        password=str(self.passField.lable.text)
        if self.ready:
            Succeeded,msg = controller.login_to_server(name,password)
            if Succeeded:
                return True
            self.err_msg.text=msg
            self.err_msg.active = True
        elif self.registar:
            Succeeded = controller.Registration(name,password)
            if Succeeded:
                self.err_msg.text="Succsse"
                self.err_msg.active = True
        self.ready = False
        self.registar=False
        return False

    def getNextViewController(self):
        return Chat()

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

class ChatRoom(GuiController):

    def __init__(self,name:str):
        super().__init__()
        self.clientName = name
     # create new text-box for log server
        self.chat_box_from = Rectangle(
            (CLIENT_LIST_WIDTH+20, 10), (MSG_WIDTH, MSG_HEIGHT))
        chat_box_to = Rectangle(
            (CLIENT_LIST_WIDTH+20, MSG_HEIGHT+20), (FIELD_WIDTH, FIELD_HEIGHT))
        label_box = Label("msg:", self.font)
        self.input_box = InputField(label_box, chat_box_to)

        # self.client_list_online = Rectangle(
        #     (10, 10), (CLIENT_LIST_WIDTH, CLIENT_LIST_HEIGHT))
        self.loading_bar = Rectangle(
            (10, CLIENT_LIST_HEIGHT+20), (LOADING_BAR_WIDTH, LOADING_BAR_HEIGHT))

        # create new button
        self.send_button = Button(
            rect_button=Rectangle(
                (WIDTH-80, CLIENT_LIST_HEIGHT+20), (SEND_BUTTON_WIDTH, SEND_BUTTON_HEIGHT)),
            text_button=Label("Send", self.font),
            hover_color=Color(self.palette["green"]),
            rect_color=Color(self.palette["light-green"]),
            click_color=Color(self.palette["red"])
        )

        self.get_file_button = Button(
            rect_button=Rectangle((LOADING_BAR_WIDTH+20, CLIENT_LIST_HEIGHT+20),
                                  (GET_FILE_BUTTON_WIDTH, GET_FILE_BUTTON_HEIGHT)),
            text_button=Label("Get", self.font),
            hover_color=Color(self.palette["green"]),
            rect_color=Color(self.palette["light-green"]),
            click_color=Color(self.palette["red"])
        )
        self.put_file_button = Button(
            rect_button=Rectangle((LOADING_BAR_WIDTH+30+GET_FILE_BUTTON_WIDTH,
                                  CLIENT_LIST_HEIGHT+20), (PUT_FILE_BUTTON_WIDTH, PUT_FILE_BUTTON_HEIGHT)),
            text_button=Label("Put", self.font),
            hover_color=Color(self.palette["green"]),
            rect_color=Color(self.palette["light-green"]),
            click_color=Color(self.palette["red"])
        )

    def shouldAdvance(self, client):
        pass

    def getNextViewController(self):
        pass

    def handleClick(self,client):
        self.input_box.active = self.input_box.has_mouse()
        pass

    def handleButtonPress(self, event):
        if self.input_box.active:
            self.input_box.handle_Key_Press(event)

    def draw_screen(self):
        # self.screen.fill(self.palette["gray"])
        self.chat_box_from.draw_rect(self.screen, self.palette["white"])
        self.input_box.draw_InputField(
            self.screen, self.palette["white"], self.palette["green"])
        # self.client_list_online.draw_rect(self.screen, self.palette["white"])
        self.loading_bar.draw_rect(self.screen, self.palette["white"])
        self.send_button.draw_button(self.screen, True)
        self.get_file_button.draw_button(self.screen, True)
        self.put_file_button.draw_button(self.screen, True)

        pg.display.update()
        self.clock.tick(REFRASH)

class Chat(GuiController):

    def __init__(self):
        super().__init__()
        self.menu_side_friend: list[Button] = []
        self.chat_room:dict[str,ChatRoom]={}
        self.show_chat=ChatRoom("ALL")
        self.left_pos_button = 10
        self.client_list_online = Rectangle(
            (10, 10), (CLIENT_LIST_WIDTH, CLIENT_LIST_HEIGHT))
        self.clientList = RectangleList([], self.client_list_online)
        self.chat_room_label = Label("Hello There click ", self.font)
        self.refresh=False
        self.refresh_button = Button(
            rect_button=Rectangle((LOADING_BAR_WIDTH+140, CLIENT_LIST_HEIGHT+20),
                                  (GET_FILE_BUTTON_WIDTH, GET_FILE_BUTTON_HEIGHT)),
            text_button=Label("Get", self.font),
            hover_color=Color(self.palette["green"]),
            rect_color=Color(self.palette["light-green"]),
            click_color=Color(self.palette["red"])
        )

    def load_list_friend(self,controoler):
        response=controoler.list_of_client_online()
        response = json.loads(response, object_hook=lambda d: SimpleNamespace(**d))
        print(response)
        self.chat_room:dict[str,ChatRoom]={}
        self.menu_side_friend.clear()
        self.left_pos_button=10
        for i in response:
            self.chat_room[f"{i.name}"]=ChatRoom(f"{i.name}")
            button = Button(
                rect_button=Rectangle((10,self.left_pos_button), (180, 50)),
                text_button=Label(f"{i.name}", self.font),
                hover_color=Color(self.palette["green"])if i.online=="True" else Color(self.palette["red"]) ,
                rect_color= Color(self.palette["light-green"]),
                click_color=Color(self.palette["red"])
            )
            self.left_pos_button+=55
            self.menu_side_friend.append(button)
        self.clientList.rectList=self.menu_side_friend

    def shouldAdvance(self, controoler):
        if self.refresh:
            self.load_list_friend(controoler)
            self.refresh=False   
        # controoler.get_msg_from_client()
        
        return False if controoler.connected else True
        

    def getNextViewController(self):
        return Selector_server()

    def handleClick(self,client):
        
        self.show_chat.handleClick(client)
        
        if self.show_chat.send_button.mouse_hover():
            to=self.show_chat.clientName
            msg=self.show_chat.input_box.lable.text
            print(to,msg)
            client.send_msg_to_client(to,msg.split(":")[1])
            

        if self.refresh_button.mouse_hover():
            print("Hdddd")
            self.refresh=True
        for client in self.menu_side_friend:
            if client.mouse_hover():
                name= client.text_button.text
                self.show_chat =self.chat_room[name]
                self.chat_room_label.active=False
           
        pass

    def handleButtonPress(self, event):
        self.show_chat.handleButtonPress(event)
        pass

    def draw_screen(self):
        self.screen.fill(self.palette["gray"])
        self.clientList.draw_scerrn(self.screen)
        self.refresh_button.draw_button(self.screen,True)
        if not self.chat_room_label.active:
            self.show_chat.draw_screen()
        center = self.screen.get_rect().center
        self.chat_room_label.draw_label(self.screen, center, (0, 0, 0))
        pg.display.update()
        self.clock.tick(REFRASH)
        # override this
        pass

    def __del__(self):
        print("Chat is destroyed.")
