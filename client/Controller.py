import threading
from Client import *
from GUI import GUI_Panel


if __name__=="__main__":
    client= Client()
    gui= GUI_Panel(client)
    gui()
    print("hellllllo")
   
    pass