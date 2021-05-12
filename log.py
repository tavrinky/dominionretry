

# so that people aren't coupled to printing 

class Log(object):
    def log(self, msg: str) -> None: 
        pass 

class PrintLog(Log):
    def __init__(self): 
        pass 

    def log(self, msg): 
        print(msg) 

    