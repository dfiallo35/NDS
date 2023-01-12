class ParserObj:
    def __init__(self, type:str, **kwargs):
        self.type= type
        self.__dict__.update(kwargs)
    
    def __str__(self):
        return str(self.__dict__)
    
    def get(self, key: str):
        return self.__dict__.get(key)