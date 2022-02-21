
import re

def isConnected(func):
    def wrapper(*args, **kwargs):
        self=args[0]
        if self.connected:
            return func(*args, **kwargs)
        else:
            return False
    return wrapper

def valid_token(func):
    print("valid_token")
    def wrapper(*args, **kwargs):
        if args[1] :
            return func(*args, **kwargs)
        return False
    return wrapper

def valid_login(func):
    def wrapper(self,name,password):
        if self.connected:
            if re.match("^[a-zA-Z0-9_.-]+$", name):
                return func(self,name,password),""
            return False,"name not Valid"
        return False
    return wrapper

