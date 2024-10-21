class chess:
    types=["number","barrier","direction"]
    names=["0","1","2","3","4","5","6","7","8","9","barrier","up","down","left","right"]
    values=[0,1,2,3,4,5,6,7,8,9,0,0,0,0,0]
    def __init__(self,belong:str="",index:int=None):
        self.belong=belong
        self.type=chess.types[index]
        self.name=chess.names[index]
        self.value=chess.values[index]
        pass
    pass

class player:
    def __init__(self,name:str='',color:str='',score:int=0):
        self.name=name
        self.color=color
        self.score=score
        for i in range(15):
            self.chess.append(chess())
            pass
        pass
    pass

class sixth:
    pass

