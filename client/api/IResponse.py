
from datetime import datetime
class IResponse:

    def __init__(self, header: dict = {}, body: dict = {}, res: str = "", origin: str = "", *args, **kwargs) -> None:
        self.header = header if header else {
            "res": res, "date": str(datetime.now())}
        self.body = body if body else {"args": args, "data": kwargs}
        self.origin = origin

    def get_res(self):
        pass

    def get_data(self):
        pass

    def get_origin(self):
        pass

    def get_date(self):
        pass

    def get_body(self):
        pass

    def __str__(self):
        pass