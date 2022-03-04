import sys
sys.path.append("./Client")

from BLL.Client import *
from UIL.GUI import GUI_Panel

if __name__=="__main__":
    client= Client()
    gui= GUI_Panel(client)
    gui()
   