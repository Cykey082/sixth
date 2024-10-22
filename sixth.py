class chess:
    types=["number"]*10+["barrier"]+["direction"]*4
    names=["0","1","2","3","4","5","6","7","8","9","barrier","up","down","left","right"]
    names_display=["0","1","2","3","4","5","6","7","8","9","×","↑","↓","←","→"]
    values=[0,1,2,3,4,5,6,7,8,9,0,0,0,0,0]
    def __init__(self,belong:str="",index:int=None):
        self.belong=belong
        self.type=chess.types[index]
        self.name=chess.names[index]
        self.name_display=chess.names_display[index]
        self.value=chess.values[index]
        self.pos="hand"
        pass
    pass

class player:
    def __init__(self,name:str=''):
        self.name=name
        self.score=0
        self.chess=[]
        for i in range(15):
            self.chess.append(chess(self.name,i))
            pass
        pass
    pass

class sixth:
    def __init__(self):
        self.player1=player("player1")
        self.player2=player("player2")
        self.board=[[None]*5]*4
        self.current_player=self.player1
        self.next_player=self.player2
        pass
    def round(self):
        self.current_player,self.next_player=self.next_player,self.current_player
        pass
    def preput(self,chess:chess,row:int,column:int):
        answer=[]
        if row<0 or row>3 or column<0 or column>4:
            return ["error","Invalid range"]
        if chess.pos!="hand":
            if chess.pos=="board" or chess.type!="number" or self.current_player.chess[0].pos!="hand":
                return ["error","Invalid chess"]
            else:
                answer.append("revive")
        if chess.type=="number":
            if self.board[row][column]!=None:
                if self.board[row][column].belong==self.current_player.name:
                    return ["error","Invalid put"]
                if self.board[row][column].type=="number" and chess.value<=self.board[row][column].value:
                    return ["error","Invalid swap"]
                return answer+["swap","put",row,column,chess]
            else:
                return answer+["put",row,column,chess]
        elif chess.type=="barrier":
            if self.board[row][column]!=None:
                return ["error","Invalid put"]
            return answer+["put",row,column,chess]
        elif chess.type=="direction":
            if self.board[row][column]==None:
                return ["error","Invalid move"]
            if chess.name=="up":
                if row==0 or self.board[row-1][column]!=None:
                    return ["error","Invalid move"]
                return answer+["move",row,column,chess]
            elif chess.name=="down":
                if row==3 or self.board[row+1][column]!=None:
                    return ["error","Invalid move"]
                return answer+["move",row,column,chess]
            elif chess.name=="left":
                if column==0 or self.board[row][column-1]!=None:
                    return ["error","Invalid move"]
                return answer+["move",row,column,chess]
            elif chess.name=="right":
                if column==4 or self.board[row][column+1]!=None:
                    return ["error","Invalid move"]
                return answer+["move",row,column,chess]
            pass
        pass
    def put(self,args:list):
        if args[0]=="error":
            return []
        if args[0]=="revive":
            args[-1].pos="hand"
            self.current_player.chess[0].pos="tomb"
            args=args[1:]
        if args[0]=="swap":
            self.board[args[1]][args[2]].status="hand"
            self.board[args[1]][args[2]]=None
            args=args[1:]
        if args[0]=="put":
            self.board[args[1]][args[2]]=args[3]
            args[3].pos="board"
            return[(args[1],args[2])]
        if args[0]=="move":
            pass
        return []

