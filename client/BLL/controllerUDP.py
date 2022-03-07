import os

from .UDP_function import Client,FileException,SocketException,WindowSizeException
from .Setting_Simulation import *

def Client_Start(file_name,count):
    '''
    A function that initializes the client server to receive a file
    '''
    server_ip = "127.0.0.1"
    server_port = 531
    client_ip = "127.0.0.1"
    client_port = 800
    window_size = 12
    seq_num_bits = 16
    timeout = 10
    client_data_folder = os.path.join(os.getcwd(), "Client/downloads")

    try:
        client = Client(client_ip,
                        client_port, server_ip,
                        server_port,
                        seq_num_bits,
                        window_size,
                        client_data_folder,file_name,timeout,count=count)
        

        client.thread.start()


    except SocketException as e:
        print(e)
    except FileException as e:
        print(e)
    except WindowSizeException as e:
        print(e)
    except Exception as e:
        print(e)
    

    print("Start download")
