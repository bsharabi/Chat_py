class IClient:

    def __init__(self, name: str, connection=None) -> None:
        self.name = name
        self.connection = connection
        self.isConnect = True
        

    def __eq__(self, connection):
        pass

    def __repr__(self) -> str:
        pass