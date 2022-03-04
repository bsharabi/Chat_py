import unittest
from Server.api.IRequest import *
class TestServer(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
    def test_write_file(self, *args, **kwargs):
        pass

    def test_read_file_log(self, f=0, to=19) -> list[str]:
        pass

    def test_connect_to_TCP(self):
        pass

    def test_close_connection_TCP(self):
        pass

    def test_registar(self,req:IRequest,connection):
        pass
    
    def test_login(self,req:IRequest,connection):
        pass
    
    def test_send_msg(self:IRequest,req,connection):
        pass
        
    def test_send_msg_to_all(self:IRequest,req,connection):
        pass

if __name__ == '__main__':
    unittest.main()