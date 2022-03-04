from DAL.DataBase import * 
from UIL.View import GUI_Panel
from BLL.TCP_server import TCPServer

if __name__=="__main__":
    db=mongodb("Chat-py")
    server= TCPServer(db)
    gui= GUI_Panel(server)
    gui()
