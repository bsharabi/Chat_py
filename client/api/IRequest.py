
from datetime import datetime
class IRequest:
    def __init__(self, header: dict = {}, body: dict = {}, req: str = "", fileName: str = "", user: str = "", password: str = "", origin: str = "", toClient: str = "", *args, **kwargs) -> None: 
        self.header = header if header else {
            "req": req, "date": str(datetime.now())}

        self.body = body if body else {"args": args,
                                       "data": kwargs,
                                       "file": fileName,
                                       "form":
                                       {"user": user,
                                        "password": password},
                                       "to": toClient}
        self.origin = origin
    
    def get_req(self):
        '''
        
        
        '''
        pass
    
    def get_data(self):
        pass

    def get_origin(self):
        pass

    def get_date(self):
        pass

    def get_user(self):
        pass

    def get_password(self):
        pass

    def get_toClient(self):
        pass

    def __str__(self):
        pass