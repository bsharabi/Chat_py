
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
    
    def get_req(self) -> str:
        # override this
        '''
        return request from header
        '''
        pass
    
    def get_data(self) -> dict[str,str]:
        # override this
        '''
        return dict of data request
        '''
        pass

    def get_origin(self)->str:
        # override this
        '''
        return origin from request
        '''
        pass

    def get_date(self)->str:
        # override this
        '''
        return the date from request
        '''
        pass

    def get_user(self)->str:
        # override this   
        '''
        return the user name from requst,
        if user does't exist return ""
        '''
        pass

    def get_password(self)->str:
        # override this
        '''
        return the user password from requst,
        if password does't exist return ""
        '''
        pass

    def get_toClient(self)->str:
        '''
        return the user name of client 
        '''
        pass
    
    def get_file_name(self)->str:
        # override this
        '''
        return the file name from request,
        if file name does't exist return ""
        '''
        pass

    def __str__(self):
        # override this  
        '''
        return the details of request 
        '''
        pass