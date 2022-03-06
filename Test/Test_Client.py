import sys
sys.path.append(".")

sys.path.append("Client")
sys.path.append("Server")
import shutil
import time
import unittest
from os import path
import os
from Server.BLL.TCP_server import TCPServer
from Client.BLL.Client import Client
from Server.DAL.DataBase import mongodb
import threading
import time
import randomname

class TestClient(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.client = Client(name="barak")
        
    def test_connect_to_TCP(self):
        ans = self.client.connect_to_TCP()
        self.assertEqual(ans, False)
        db=mongodb("Chat-py")
        serverTest = TCPServer(db)
        serverTest.connect_to_TCP()
        threading.Thread(target=serverTest).start()
        time.sleep(2)
        ans = self.client.connect_to_TCP()
        self.assertTrue(ans)
        serverTest.close_connection_TCP()

    def test_connect_to_UDP(self):
        ans = self.client.connect_to_UDP()
        self.assertTrue(ans)

    def test_close_TCP(self):
        db=mongodb("Chat-py")
        serverTest = TCPServer(db)
        serverTest.connect_to_TCP()
        threading.Thread(target=serverTest).start()
        time.sleep(2)
        ans = self.client.connect_to_TCP()
        self.assertTrue(ans)
        ans = self.client.close_connection_TCP()
        self.assertTrue(ans)
        serverTest.close_connection_TCP()

    def test_close_UDP(self):
        ans = self.client.connect_to_UDP()
        self.assertTrue(ans)

    def test_data_directory(self):
        path_=path.join(os.getcwd(),"Client\data")
        shutil.rmtree(path_, ignore_errors=True)
        ans = path.isdir(path_)
        self.assertEqual(ans, False)
        ans = self.client.create_data_directory()
        self.assertEqual(ans, True)
        ans = path.isdir(path_)
        self.assertEqual(ans, True)

    def test_login(self):
        
        db=mongodb("Chat-py")
        serverTest = TCPServer(db)
        serverTest.connect_to_TCP()
        threading.Thread(target=serverTest).start()
        time.sleep(5)
        self.client.connect_to_TCP()
        
        ans = self.client.login(req="login", user="barak", password="12")
        self.assertEqual(ans, (False, "Failure"))
        
        ans = self.client.login(req="login", user="barak__", password="12")
        self.assertEqual(ans, (False, "Failure"))
        
        ans = self.client.login(req="login", user="barak", password="1")
        self.assertEqual(ans, (True, "Success"))

        ans = self.client.login(req="login", user="barak", password="1")
        self.assertEqual(ans, (False, "Client connected"))

        self.client.close_connection_TCP()
        serverTest.close_connection_TCP()
    
    def test_register(self):
        db=mongodb("Chat-py")
        serverTest = TCPServer(db)
        serverTest.connect_to_TCP()
        threading.Thread(target=serverTest).start()
        self.client.connect_to_TCP()
        time.sleep(5)
    
        ans = self.client.register(req="register", user="barak", password="12")
        self.assertEqual(ans, (False, "User exist"))
        
        ans = self.client.register(req="register", user=randomname.get_name(), password="12")
        self.assertEqual(ans, (True, "Success"))
        
        ans = self.client.register(req="register", user="barak", password="1")
        self.assertEqual(ans, (False, "User exist"))

        self.client.close_connection_TCP()
        serverTest.close_connection_TCP()
 
    def __del__(self):
        # self.serverTest.close_connection_TCP()
        print("Test destroyed, Goodbye!")
        # exit()

if __name__ == '__main__':
    unittest.main()
