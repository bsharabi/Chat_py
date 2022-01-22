from base64 import decode
import socket
import threading
from pygame import *
import pygame as pg
WIDTH, HEIGHT = (800, 600)
REFRASH = 60
FIELD_WIDTH, FIELD_HEIGHT = (590, 175)
MSG_WIDTH, MSG_HEIGHT = (590,355)
CLIENT_LIST_WIDTH , CLIENT_LIST_HEIGHT =(180,540)
SEND_BUTTON_WIDTH,SEND_BUTTON_HEIGHT=(70, 30)
LOADING_BAR_WIDTH,LOADING_BAR_HEIGHT=(500, 30)
GET_FILE_BUTTON_WIDTH,GET_FILE_BUTTON_HEIGHT=(45, 30)
PUT_FILE_BUTTON_WIDTH,PUT_FILE_BUTTON_HEIGHT=(45, 30)

# ------------------------------- View -------------------------------------

class GUI_Panel():

    def __init__(self):
        pg.init()
        pg.font.init()
        pg.mixer.init()
        self.GuiController = Selector_server()

    def cmd_console(self):
        pass

    def log_console(self):
        pass

    def __call__(self,socket:socket):
        running = True
        while running:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    self.GuiController.handleButtonPress(event)
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.GuiController.handleClick()
            
            if self.GuiController.shouldAdvance(socket):
                self.GuiController = self.GuiController.getNextViewController()
            
            self.GuiController.draw_screen()
        return running

    def __del__(self):
        print("Server distroy")

class Label:
    
    def __init__(self, text_field: str = '', text_font: font = None) -> None:
        self.text = text_field
        self.font = text_font

    def draw_label(self, surface: Surface, pos: tuple[float, float], color: Color = Color(0, 0, 0),center:bool=True) -> None:
        label_srf=self.font.render(self.text, True, color)
        pos = label_srf.get_rect(center=pos) if center else pos
        surface.blit(label_srf, pos)
   
class Rectangle:

    def __init__(self, position: tuple[int, int], size_box: tuple[int, int]) -> None:
        self.rect: Rect = Rect(position, size_box)
        self.position = position
    
    def has_mouse(self):
        mouse_pos = pg.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)
    
    def draw_rect(self, surface: Surface, color: Color) -> None:
        pg.draw.rect(surface, color, self.rect)

class Button:

    def __init__(self, rect_button: Rectangle, text_button: Label, hover_color: Color = (0, 0, 255), click_color: Color = (0, 255, 0),rect_color: Color = (255, 0, 0)):
        self.rect_button = rect_button
        self.text_button = text_button
        self.hover_color = hover_color
        self.click_color = click_color
        self.rect_color = rect_color


    def mouse_hover(self) -> bool:
        mouse_pos = pg.mouse.get_pos()
        return self.rect_button.rect.collidepoint(mouse_pos)
    
    def mouse_click(self) -> bool:
        for e in pg.event.get(): 
            if e.type == MOUSEBUTTONDOWN:
                return self.mouse_hover()
            elif e.type == MOUSEBUTTONUP:
                mouse_pos = pg.mouse.get_pos()
                if self.rect_button.rect.collidepoint(mouse_pos):
                    pass    
        return False
       
    def mouse_listener(self) -> bool:
        mouse_pos = pg.mouse.get_pos()
        return self.rect_button.rect.collidepoint(mouse_pos)
    
    def draw_button(self, surface):
        button_color = self.hover_color
        text_color = self.rect_color
        if self.mouse_hover():
            button_color = self.rect_color
            text_color = self.hover_color
        if self.mouse_click():
            button_color = self.click_color
            text_color = self.hover_color
        self.rect_button.draw_rect(surface, button_color)
        self.text_button.draw_label(
            surface, self.rect_button.position, text_color)

class InputField:
    
    def __init__(self, label:Label, rect_angle:Rectangle):

        self.lable = label
        self.rect_angle = rect_angle
        self.length=len(label.text)
        self.ready = False
        self.active = False
    
    def has_mouse(self):
        return self.rect_angle.has_mouse()
    
    def handle_Key_Press(self, event):  
        if event.key == pg.K_RETURN:
            self.ready = True
        if event.key == pg.K_BACKSPACE and self.length<=len(self.lable.text[:-1]):
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
        self.lable.draw_label(surface,( self.rect_angle.rect[0] + 15, self.rect_angle.rect[1] + 15), textColor)    

class GuiController:

    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), depth=32)
        display.set_caption("Whats'up Client Chat ")
        self.palette = {
            "gray": (192, 192, 192),
            "white": (255, 255, 255),
            "light-green": (64, 213, 47),
            "green": (175, 237, 169),
            "red": (255, 0, 0)
        }
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("Arial", 24,bold=True)

    def scale(data, min_screen, max_screen, min_data, max_data):
        """
        get the scaled data with proportions min_data, max_data
        relative to min and max screen dimentions
        """
        return ((data - min_data) / (max_data-min_data)) * (max_screen - min_screen) + min_screen

    def shouldAdvance(self, controller):

        #override this
        pass

    def getNextViewController(self):
        
        #override this
        pass

    def handleClick(self):
        
        #override this
        pass

    def handleButtonPress(self, event):
        
        #override this
        pass
    
    def draw_screen(self):

        #override this
        pass
    def __del__(self):
        print("Viewer controller is distroy")

class Selector_server(GuiController):

    def __init__(self):

        super().__init__()
        self.screen = pg.display.set_mode((400,200),depth=32)
        display.set_caption("Connec to server")

        ip_Label = Label("IP: localhost", self.font)
        ip_Panel = Rectangle((100,100), (250,32))
        self.ip_Field = InputField(ip_Label,ip_Panel )

        portLabel = Label("Port: 3000", self.font)
        portPanel = Rectangle((100, 50), (250,32))
        self.port_field = InputField(portLabel, portPanel)

        submitLabel = Label("Connect ", self.font)
        submitPanel = Rectangle((100,150), (100,32))
        self.submitButton = Button(submitPanel, submitLabel, self.palette["green"], self.palette["light-green"])

        self.ready = False

    def handleClick(self):
        
        self.port_field.active = True if self.port_field.has_mouse() else False
        self.ip_Field.active = True if self.ip_Field.has_mouse() else False

        if self.submitButton.mouse_listener():
            self.ready = True
    
    def handleButtonPress(self, event):
        
        if self.port_field.active:
            self.port_field.handle_Key_Press(event)
        if self.ip_Field.active:
            self.ip_Field.handle_Key_Press(event)
            
    def shouldAdvance(self, socket_client):

        if self.ready:
            port_number = int(self.port_field.lable.text.split(": ")[1])
            ip_number=str(self.ip_Field.lable.text.split(": ")[1])
            socket_client.connect((ip_number,port_number ))
            return True
        return False
    
    def getNextViewController(self):
        
        return ClientLogin()
    
    def draw_screen(self):
        
        self.screen.fill(self.palette["white"])
        self.ip_Field.draw_InputField(self.screen,self.palette["green"], self.palette["light-green"])
        self.port_field.draw_InputField(self.screen, self.palette["green"], self.palette["light-green"])
        self.submitButton.draw_button(self.screen)

        pg.display.update()
    
class ClientLogin(GuiController):

    def __init__(self):
        super().__init__()
        self.screen = pg.display.set_mode((400,400), depth=32)
        display.set_caption("Login")

        nameLabel = Label("Username: ", self.font)
        namePanel = Rectangle((100,200), (200,32))
        self.nameField = InputField(nameLabel, namePanel)

        submitLabel = Label("Login", self.font)
        submitPanel = Rectangle((100,350), (100,32))
        self.submitButton = Button(submitPanel, submitLabel, self.palette["green"], self.palette["light-green"])

        self.ready = False

    def handleClick(self):
        
        self.nameField.active = self.nameField.has_mouse()

        if self.submitButton.mouse_listener():
            self.ready = True
    
    def handleButtonPress(self, event):
        
        if self.nameField.active:
            self.nameField.handle_Key_Press(event)
    
    def shouldAdvance(self, controller:socket):

        if self.ready:
            message = "name:" + self.nameField.lable.text.split(":")[1]
            print("name from shouldAdvance login ",message)
            controller.send(message.encode())
            print(f"Sent message \"{message}\"\n")
            response = controller.recv(1024).decode()
            print(f"Got response\"{response}\"\n")
            if response == "available":
                # controller.name = self.nameField.lable.text.split(":")[1]
                return True
        return False
        
    
    def getNextViewController(self):
        
        return ChatRoom()
    
    def draw_screen(self):
        
        self.screen.fill(self.palette["white"])
        self.nameField.draw_InputField(self.screen, self.palette["green"], self.palette["light-green"])
        self.submitButton.draw_button(self.screen)

        pg.display.update()

class ChatRoom(GuiController):
    
    def __init__(self):
        super().__init__()
     # create new text-box for log server
        self.chat_box_from = Rectangle((CLIENT_LIST_WIDTH+20, 10), (MSG_WIDTH, MSG_HEIGHT))
        chat_box_to = Rectangle((CLIENT_LIST_WIDTH+20, MSG_HEIGHT+20), (FIELD_WIDTH, FIELD_HEIGHT))
        label_box=Label("msg:",self.font)
        self.input_box=InputField(label_box,chat_box_to)
        self.client_list_online = Rectangle((10, 10), (CLIENT_LIST_WIDTH, CLIENT_LIST_HEIGHT))
        self.loading_bar= Rectangle((10,CLIENT_LIST_HEIGHT+20 ), (LOADING_BAR_WIDTH, LOADING_BAR_HEIGHT))
        
        # create new button
        self.send_button = Button(
            rect_button=Rectangle((WIDTH-80, CLIENT_LIST_HEIGHT+20), (SEND_BUTTON_WIDTH, SEND_BUTTON_HEIGHT)),
            text_button=Label("Send", self.font),
            hover_color=Color(self.palette["green"]),
            rect_color=Color(self.palette["light-green"]),
            click_color=Color(self.palette["red"])
        )
        
        self.get_file_button = Button(
            rect_button=Rectangle((LOADING_BAR_WIDTH+20, CLIENT_LIST_HEIGHT+20), (GET_FILE_BUTTON_WIDTH, GET_FILE_BUTTON_HEIGHT)),
            text_button=Label("Get", self.font),
            hover_color=Color(self.palette["green"]),
            rect_color=Color(self.palette["light-green"]),
            click_color=Color(self.palette["red"])
        )
        self.put_file_button = Button(
            rect_button=Rectangle((LOADING_BAR_WIDTH+30+GET_FILE_BUTTON_WIDTH, CLIENT_LIST_HEIGHT+20), (PUT_FILE_BUTTON_WIDTH, PUT_FILE_BUTTON_HEIGHT)),
            text_button=Label("Put", self.font),
            hover_color=Color(self.palette["green"]),
            rect_color=Color(self.palette["light-green"]),
            click_color=Color(self.palette["red"])
        )
    
    def shouldAdvance(self, controller):

        #override this
        pass

    def getNextViewController(self):
        
        #override this
        pass

    def handleClick(self):
        self.input_box.active = self.input_box.has_mouse()
        pass

    def handleButtonPress(self, event):
        
        if self.input_box.active:
            self.input_box.handle_Key_Press(event)
            
    def draw_screen(self):
        self.screen.fill(self.palette["gray"])
        self.chat_box_from.draw_rect(self.screen, self.palette["white"])
        self.input_box.draw_InputField(self.screen, self.palette["white"],self.palette["green"])
        self.client_list_online.draw_rect(self.screen, self.palette["white"])
        self.loading_bar.draw_rect(self.screen, self.palette["white"])
        self.send_button.draw_button(self.screen)
        self.get_file_button.draw_button(self.screen)
        self.put_file_button.draw_button(self.screen)

        pg.display.update()
        self.clock.tick(REFRASH)

    