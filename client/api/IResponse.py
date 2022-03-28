
from datetime import datetime
class IResponse:

    def __init__(self, header: dict = {}, body: dict = {}, res: str = "", origin: str = "", *args, **kwargs) -> None:
        self.header = header if header else {
            "res": res, "date": str(datetime.now())}
        self.body = body if body else {"args": args, "data": kwargs}
        self.origin = origin


    def get_body(self)->dict:
        '''
        The function returns the message body
        @return dict 
        '''
    
  
    def get_res(self)->str:
        # override this
        '''
        return the response from response object
        '''
    
    def get_data(self)->dict:
        # override this
        '''
        return the date from response
        '''
        pass

    def get_origin(self)->str:
       # override this
        '''
        return the origin from response
        '''

    def get_date(self)->str:
        # override this
        '''
        return the date from response
        '''

    def __str__(self)->str:
        # override this  
        '''
        return the details of response 
        '''
        pass