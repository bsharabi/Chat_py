from os import path
from pydoc import cli
import sys
sys.path.append(".")

sys.path.append("Client")
sys.path.append("Server")
import unittest
from server.api.IRequest import *

import time
import unittest
from server.BLL.TCP_server import TCPServer
from client.BLL.Client import Client
from server.DAL.DataBase import mongodb
import threading
import time
import randomname
class TestServer(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        db=mongodb("Chat-py")
        self.serverTest = TCPServer(db)
        self.client=Client(name="barak")
        


    def test_connect_to_TCP(self):
        ans=self.serverTest.connect_to_TCP()
        self.assertTrue(ans)
        self.serverTest.close_connection_TCP()
        
        self.port=""
        self.host=""
        ans=self.serverTest.connect_to_TCP()
        self.assertFalse(ans)
        
        self.serverTest.close_connection_TCP()

    def test_close_connection_TCP(self):
        self.serverTest.connect_to_TCP()
        ans=self.serverTest.close_connection_TCP()
        self.assertTrue(ans)
        

    def test_registar(self):
        self.serverTest.connect_to_TCP()
        threading.Thread(target=self.serverTest).start()
        self.client.connect_to_TCP()
        time.sleep(5)
    
        ans = self.client.register(req="register", user="barak", password="12")
        self.assertEqual(ans, (False, "User exist"))
        
        ans = self.client.register(req="register", user=randomname.get_name(), password="12")
        self.assertEqual(ans, (True, "Success"))
        
        ans = self.client.register(req="register", user="barak", password="1")
        self.assertEqual(ans, (False, "User exist"))

        self.client.close_connection_TCP()
        self.serverTest.close_connection_TCP()
    
    def test_login(self):
        self.serverTest.connect_to_TCP()
        threading.Thread(target=self.serverTest).start()
        self.client.connect_to_TCP()
        time.sleep(5)
        
        ans = self.client.login(req="login", user="barak", password="12")
        self.assertEqual(ans, (False, "Failure"))
        
        ans = self.client.login(req="login", user="barak", password="1")
        self.assertEqual(ans, (True, "Success"))


        self.client.close_connection_TCP()
        self.serverTest.close_connection_TCP()
    
    def test_send_msg(self):
        client1=Client(name="sagi")
        client2=Client(name="barak")

        self.serverTest.connect_to_TCP()
        threading.Thread(target=self.serverTest).start()
        client1.connect_to_TCP()
        client2.connect_to_TCP()

        time.sleep(5)
        
        ans = client1.login(req="login", password="1")
        self.assertEqual(ans, (True, "Success"))
        
        ans = client2.login(req="login", password="1")
        self.assertEqual(ans, (True, "Success"))
        
        threading.Thread(target=client1.response).start()
        time.sleep(2)
       
        threading.Thread(target=client2.response).start()
        time.sleep(2)
        
        client1.request(req="sendMsg",toClient="barak",msg="hello")
        
        
        client1.close_connection_TCP()
        client2.close_connection_TCP()

        self.serverTest.close_connection_TCP()
        
    def test_send_msg_to_all(self):
        self.serverTest.connect_to_TCP()
        threading.Thread(target=self.serverTest).start()
        
        client1=Client(name="sagi")
        client2=Client(name="barak")
        client3=Client(name="daniel")
        client4=Client(name="mesi")
        client5=Client(name="laor")


        client1.connect_to_TCP()
        client2.connect_to_TCP()
        client3.connect_to_TCP()
        client4.connect_to_TCP()
        client5.connect_to_TCP()
        
        
        time.sleep(6)
        
        ans = client1.login(req="login", password="1")
        self.assertEqual(ans, (True, "Success"))
        
        threading.Thread(target=client1.response).start()
        time.sleep(2)
        
        ans = client2.login(req="login", password="1")
        self.assertEqual(ans, (True, "Success"))
        
        threading.Thread(target=client2.response).start()
        time.sleep(2)
        
        ans = client3.login(req="login", password="1")
        self.assertEqual(ans, (True, "Success"))
        
        threading.Thread(target=client3.response).start()
        time.sleep(2)
        
        ans = client4.login(req="login", password="1")
        self.assertEqual(ans, (True, "Success"))
        
        threading.Thread(target=client4.response).start()
        time.sleep(2)
        
        ans = client5.login(req="login", password="1")
        self.assertEqual(ans, (True, "Success"))
        
        threading.Thread(target=client5.response).start()
        time.sleep(2)
        
        client1.request(req="sendMsgALL",toClient="Friends Group",msg="hello")
        
        client1.close_connection_TCP()
        client2.close_connection_TCP()    
        client3.close_connection_TCP()
        client4.close_connection_TCP()  
        client5.close_connection_TCP()   
        self.serverTest.close_connection_TCP()
    
    def __del__(self):
        self.serverTest.close_connection_TCP()
        

if __name__ == '__main__':
    unittest.main()