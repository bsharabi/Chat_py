import sys
sys.path.append("./Client")
import multiprocessing.pool  

from BLL.Client import *
from UIL.GUI import GUI_Panel
import threading
def usres(x):
    client= Client()
    gui= GUI_Panel(client)
    gui()


if __name__=="__main__":
    countUser= int(input())
    p = multiprocessing.Pool(countUser)
    xs = p.map(usres, range(countUser))
    
    
        
    if input():
        exit()
   