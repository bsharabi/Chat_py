import os
import sys

from Server.api.IResponse import IResponse
sys.path.append("Server")
sys.path.append("./Server")
sys.path.append(".")
from BLL._server_functions import FileException
from BLL._server_functions import Server
from BLL._server_functions import SocketException
from BLL._server_functions import WindowSizeException
from BLL._shared_functions import *


def Server_Start(res_:IResponse):
    server_settings = read_args(workingDir + "/Server/BLL/server.in")

    server_ip = "localhost"
    server_port = int(server_settings['server_port'])
    window_size = int(server_settings['window_size'])
    seq_num_bits = 16
    max_segment_size = 32736

    try:
        path = workingDir + "/Server/files"
        print(path)
        print(os.getcwd())
        if not os.path.isdir(path):
            os.mkdir(path)
        server = Server(server_ip, server_port, seq_num_bits,
                        window_size, max_segment_size, server_data_folder=path)
        file_name=res_.get_data()["file_name"]
        file_name=os.path.join(os.getcwd(), f"Server/files/{file_name}")
        count=server.get_count_packet(file_name=file_name)
        
        server.thread.start()
        return True,count
    except SocketException as e:
        print(e)
        return False,0
    except FileException as e:
        print(e)
        return False,0
    except WindowSizeException as e:
        print(e)
        return False,0
    except Exception as e:
        print(e)
        return False,0
        
    

