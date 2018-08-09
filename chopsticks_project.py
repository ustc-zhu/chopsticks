
WIN = 'win'
LOSE = 'lose'
DRAW = 'draw'
UNDECIDED = 'undecided' 

maxnum = 10

def DoMove(Position, Move):#chopsticks Position =(U_L,U_R,O_L,O_R)   
    New_Position = (Position[2], Position[3], (Position[0] + Move[0])%maxnum, (Position[1] + Move[1]) % maxnum)
    return New_Position 

def GenMoves(Position):
    Move = []
    for i in [0,1]:
        for j in [2,3]:
            temp = [0,0]
            if Position[i] % maxnum != 0 and Position[j] % maxnum != 0:
                temp[i] = Position[j]
                Move.append(temp)
    if Move == []:
        Move.append([0,0])
    return Move

def children(Position):
    return list(set([DoMove(Position,Move) for Move in GenMoves(Position)])) #去重


def IsPrimitive(Position):
    return Position[0] % maxnum == 0 and Position[1] % maxnum == 0 or Position[2] % maxnum == 0 and Position[3] % maxnum == 0 

def Primitive(Position):
    return WIN if Position[0] % maxnum == 0 and Position[1] % maxnum == 0 else LOSE

Record = {}
Frontier = []
Remoteness={}

index_state = 0
index_parent = 1
index_children = 2
index_childnum = 3
index_remotetag = 4

#cnt = 0

'''def discovery(Position,Parent):
    global Record
    global Frontier
    global Remoteness, cnt
    "go through all positions"
    cnt = cnt + 1
    if IsPrimitive(Position):     
       Record[Position] = [Primitive(),[Parent],[],0,0] if Parent != [] else [Primitive(),[],[],0,0]
       Frontier.append(Position)
       #print(Frontier)
       Remoteness[Position]=0
    else:
        Children = children(Position)
        Record[Position]=[UNDECIDED,[Parent],Children,len(Children), 0] if Parent != [] else [UNDECIDED,[],Children,len(Children),0]
        for child in Children:
            if child in Record:
                Record[child][index_parent].append(Position)
            else:
                print(child,'   ',cnt)
                discovery(child,Position)
'''
def visit(Position):
    global Record
    global Frontier
    global Remoteness
    stack = [Position]
    Record[Position] = [UNDECIDED, [], [], 0, 0]
    while len(stack) != 0:
        pos = stack.pop()
        if IsPrimitive(pos):     
           #Record[Position] = [Primitive(),[pos],[],0,0] if pos != [] else [Primitive(),[],[],0,0]
           Record[pos][index_state] = Primitive(Position)
           Frontier.append(pos)
           #print(Frontier)
           Remoteness[pos] = [0,[]]
        else:
            Children = children(pos)
            #Record[Position]=[UNDECIDED,[pos],Children,len(Children), 0] if pos != [] else [UNDECIDED,[],Children,len(Children),0]
            Record[pos][index_children] = Children
            Record[pos][index_childnum] = len(Children) 
            for child in Children:
                if child in Record:
                    Record[child][index_parent].append(pos)
                else:
                    Record[child] = [UNDECIDED, [pos], [], 0 ,0]
                    stack.append(child)
    
def solve(Position):
    global Record, Frontier
    #discovery(Position, [])
    visit(Position)
    #step 2
    while len(Frontier) != 0:
        pos = Frontier.pop()
        if Record[pos][index_state] == LOSE:
            for parent in Record[pos][index_parent]:
                if Record[parent][index_state] == UNDECIDED:
                    Record[parent][index_childnum] = Record[parent][index_childnum] - 1
                    Record[parent][index_state] = WIN
                    Frontier.append(parent)
        elif Record[pos][index_state] == WIN:
            for parent in Record[pos][index_parent]:
                if Record[parent][index_state] == UNDECIDED:
                    Record[parent][index_childnum] = Record[parent][index_childnum] - 1
                    if Record[parent][index_childnum] == 0:
                        Record[parent][index_state] = LOSE
                        Frontier.append(parent)
    #step3
    for pos in Record:
        if Record[pos][index_state] == UNDECIDED:
            Record[pos][index_state] = DRAW

inf = 999999999

def generate_Remoteness(Position):
    global Remoteness
    if Position in Remoteness:
        return Remoteness[Position]
    else:
        if Record[Position][index_state] != DRAW:     
            if Record[Position][index_state] == LOSE: # if not leaf and state is losing
                max_remoteness = 0
                #Path_child = (0,0,0,0)
                for child in Record[Position][index_children]:
                    if Record[child][index_remotetag] == 0:
                        Record[child][index_remotetag] = 1
                        tmp_remoteness = generate_Remoteness(child)[0]
                        Record[child][index_remotetag] = 0
                        if max_remoteness < tmp_remoteness:
                            max_remoteness = tmp_remoteness
                            Path_child = child
                Remoteness[Position] = [max_remoteness + 1, Path_child]
            else: #if not leaf and state is winning
                min_remoteness = inf
                for child in Record[Position][index_children]:
                    if Record[child][index_state] == LOSE:
                        #print('now',child)
                        if Record[child][index_remotetag] == 0:
                            Record[child][index_remotetag] = 1
                            tmp_remoteness = generate_Remoteness(child)[0]
                            Record[child][index_remotetag] = 0
                            if min_remoteness > tmp_remoteness:
                                min_remoteness = tmp_remoteness
                                Path_child = child
                Remoteness[Position] = [min_remoteness + 1, Path_child]
        else: 
            for child in Record[Position][index_children]:
                if Record[child][index_state] == DRAW:
                    Path_child = child
                    break
            Remoteness[Position] = [inf, Path_child]
        return Remoteness[Position]


def Get_Remoteness():
    for pos in Record:
        if pos not in Remoteness:
            #print(pos)
            generate_Remoteness(pos)

#if __name__=="__main__":
solve((1,1,1,1))
Get_Remoteness()
    #print(Record)


import tkinter as tk
import time
import math

value_to_color = {WIN:"darkgreen",LOSE:"red",DRAW:"yellow"}

COM = 'computer'
HUMAN='human'


turn = 'player1'
gametype = UNDECIDED

def Name1(name):
    global p1name
    print(name)
    p1name=name

def Name2(name):
    global p2name
    print(name)
    p2name=name

def versusPlayer2():
    print("vs P2")

def versusComp():
    global p2name
    p2name = "Computer"
    print("vs Comp")
    

LARGE_FONT= ("Verdana", 12)
global p1name, p2name, secondplayer
p1name = "Player 1"
p2name = "Player 2"

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, OptionPage, ModeSelectPage, GamePlayPage):
                    
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

#*1 def qf(stringtoprint):
# *1    print(stringtoprint)

def qf(param):
    print(param)

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        # Create a button that reacts when you click
        # *1 If you do it this way, it will run on load, not when you click
        # use lambda function instead
        # button1 = tk.Button(self, text = "Visit Page 1", command = qf("yo!"))
#        button1 = tk.Button(self, text = "New Game", 
 #                           command = lambda: qf("Go to select Mode"))
        button1 = tk.Button(self, text = "New Game", 
                            command = lambda: controller.show_frame(ModeSelectPage))
        button1.pack()

        button2 = tk.Button(self, text = "Option", 
                            command = lambda: controller.show_frame(OptionPage))
        button2.pack()

class OptionPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label1 = tk.Label(self, text = "1P's Name: ")
        label2 = tk.Label(self, text = "2P's Name: ")
        entryName1 = tk.Entry(self)
        entryName2 = tk.Entry(self)
        saveName1 = tk.Button(self, text = "Save",
                              command = lambda: Name1(entryName1.get()))
        print(str(entryName1))
        saveName2 = tk.Button(self, text = "Save", command =lambda: Name2(entryName2.get()))
        button3 = tk.Button(self, text = "Back",
                            command = lambda: controller.show_frame(StartPage))
        
        label1.grid(row = 3, column = 0)
        label2.grid(row = 4, column = 0)
        entryName1.grid(row = 3, column = 1)
        entryName2.grid(row = 4, column = 1)
        saveName1.grid(row = 3, column = 2)
        saveName2.grid(row = 4, column = 2)
        button3.place(x=150 ,y=60)
        
gametype = UNDECIDED
        
        
class ModeSelectPage(tk.Frame):
    
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        button4 = tk.Button(self, text = "1P vs 2P",
                            command = self.vshuman)
        button5 = tk.Button(self, text = "1P vs Computer",
                            command = self.vscom)
        button3 = tk.Button(self, text = "Back",
                            command = lambda: controller.show_frame(StartPage))
        
        button4.pack()
        button5.pack()
        button3.pack()
        
    def vscom(self):
        global gametype
        self.controller.show_frame(GamePlayPage)
        gametype = COM
        
    
    def vshuman(self):
        global gametype
        self.controller.show_frame(GamePlayPage)
        gametype = HUMAN

    
        
p1name = "Player 1"
p2name = "Player 2"

P1 = 'player1' 
P2 = 'player2'

turn = P1
game_position = (1,1,1,1)

arrow_tag1 = 'arrowtag1'
arrow_tag2 = 'arrowtag2'
arrow_tag3 = 'arrowtag3'
arrow_tag4 = 'arrowtag4'
arrow_tag5 = 'arrowtag5'
arrow_tag6 = 'arrowtag6'
arrow_tag7 = 'arrowtag7'
arrow_tag8 = 'arrowtag8'


arrows = []
arrows_move = {}

class GamePlayPage(tk.Frame):
    print("turn:",turn,"position:",game_position)
    
    def __init__(self, parent, controller):
        global turn, game_position
        tk.Frame.__init__(self, parent)
        
        
        c = tk.Canvas(self, width=400, height=300)
        c.pack()
        
    # Function to update text into canvas text
        def UpdateStatus(new_text):
            c.itemconfig(STATUS,text=new_text)

        # Function to generate string for remoteness
        def PredictionStr(game_position):
            if Record[game_position][index_state] != DRAW:
                return turn + "should win\n in "+str(Remoteness[game_position][0])+ " moves"
            else: return "DRAW!!!"
        
        def MoveValueSwap(value):
            if value == DRAW:
                return DRAW
            else:
                return LOSE if value == WIN else WIN     
        
        STATUS = c.create_text(200,30,text="")
        #UpdateStatus(PredictionStr(game_position))
        
        p1_label = c.create_text(75,30, text=p1name)
        p2_label = c.create_text(300,30, text=p2name)
       
        lhand = c.create_text(30,75, text="LH")
        rhand = c.create_text(30,175, text="RH")
    
        left1= c.create_oval(50, 50, 120, 120, fill="grey")
                
        right1= c.create_oval(50, 150, 120, 220, fill="grey")

        left_num_1 = c.create_text(85,85, text=str(game_position[0]))
        c.itemconfig(left_num_1, tags=("left_num_1"+"tag"))
        
        
        right_num_1 = c.create_text(85,185, text=str(game_position[1]))
        c.itemconfig(right_num_1, tags=("right_num_1"+"tag"))

        
        
        # hand visualization for 2p
        lhand2 = c.create_text(360,75, text="LH")
        rhand2 = c.create_text(360,175, text="RH")

        left2= c.create_oval(270, 50, 340, 120, fill="grey")

        right2= c.create_oval(270, 150, 340, 220, fill="grey")

        left_num_2 = c.create_text(305,85, text=str(game_position[2]))
        c.itemconfig(left_num_2, tags=("left_num_2"+"tag"))
        #print(c.gettags(left_num_2))

        right_num_2 = c.create_text(305.5,185, text=str(game_position[3]))
        c.itemconfig(right_num_2, tags=("right_num_2"+"tag"))

       
        
        
        off_arrow_x=130
        off_arrow_y=70

        off_arrow_x2=130
        off_arrow_y2=100

        off_arrow_x3=265
        off_arrow_y3=85

        off_arrow_x4=265
        off_arrow_y4=110

        off_arrow_x6=130
        off_arrow_y6=190

        off_arrow_x5=130
        off_arrow_y5=170

        off_arrow_x8=265
        off_arrow_y8=205

        off_arrow_x7=260
        off_arrow_y7=185

        arr = [0,0, 25,0, 25,-5, 40,8, 25,20, 25,15, 0,15]
        arr2 = [(0,0), (25,0), (25,-5), (40,8), (25,20), (25,15), (0,15)]
        arr3 = list(map(lambda x: (x[0]*2,x[1]*2), arr2))

        def rotate(point, angle):
            px, py = point

            qx = math.cos(angle) * px - math.sin(angle) * py
            qy = math.sin(angle) * px  + math.cos(angle) * py
            return (qx, qy)

        deg45=[]
        for a in range(len(arr2)):
           deg45.append(rotate(arr2[a], math.radians(40))*3)

        deg180=[]
        for a in range(len(arr2)):
           deg180.append(rotate(arr2[a], math.radians(180))*3)

        deg135=[]
        for a in range(len(arr2)):
           deg135.append(rotate(arr2[a], math.radians(135))*3)

        deg315=[]
        for a in range(len(arr2)):
           deg315.append(rotate(arr2[a], math.radians(-45))*3)

        deg225=[]
        for a in range(len(arr2)):
           deg225.append(rotate(arr2[a], math.radians(225))*3)

        #arrows = []
        #arrows_move = {}
        def drawarrows(c):
            global arrows
            global arrows_move
            if turn == P1:
                if game_position[0] %10 != 0 and game_position[2] % 10 != 0: 
                    arrow = c.create_polygon(off_arrow_x,off_arrow_y, 
                                             off_arrow_x+25,off_arrow_y, 
                                             off_arrow_x+25,off_arrow_y-5, 
                                             off_arrow_x+40,off_arrow_y+7.5, 
                                             off_arrow_x+25,off_arrow_y+20, 
                                             off_arrow_x+25,off_arrow_y+15, 
                                             off_arrow_x,off_arrow_y+15,activefill="black")
                    c.itemconfig(arrow, tags=(arrow_tag1))
                    arrows.append(arrow)
                    arrows_move[arrow] = [game_position[2],0]
                if game_position[0] %10 != 0 and game_position[3] % 10 != 0:
                    arrow2 = c.create_polygon(off_arrow_x2+deg45[0][0],off_arrow_y2+deg45[0][1], 
                                             off_arrow_x2+deg45[1][0],off_arrow_y2+deg45[1][1], 
                                             off_arrow_x2+deg45[2][0],off_arrow_y2+deg45[2][1], 
                                             off_arrow_x2+deg45[3][0],off_arrow_y2+deg45[3][1], 
                                             off_arrow_x2+deg45[4][0],off_arrow_y2+deg45[4][1], 
                                             off_arrow_x2+deg45[5][0],off_arrow_y2+deg45[5][1], 
                                             off_arrow_x2+deg45[6][0],off_arrow_y2+deg45[6][1],
                                              activefill="black")
                
                    c.itemconfig(arrow2, tags=(arrow_tag2))
                    arrows.append(arrow2)
                    arrows_move[arrow2] = [game_position[3],0]
                    
                if game_position[1] %10 != 0 and game_position[2] % 10 != 0:
                
                    arrow5 = c.create_polygon(off_arrow_x5+deg315[0][0],off_arrow_y5+deg315[0][1], 
                                             off_arrow_x5+deg315[1][0],off_arrow_y5+deg315[1][1], 
                                             off_arrow_x5+deg315[2][0],off_arrow_y5+deg315[2][1], 
                                             off_arrow_x5+deg315[3][0],off_arrow_y5+deg315[3][1], 
                                             off_arrow_x5+deg315[4][0],off_arrow_y5+deg315[4][1], 
                                             off_arrow_x5+deg315[5][0],off_arrow_y5+deg315[5][1], 
                                             off_arrow_x5+deg315[6][0],off_arrow_y5+deg315[6][1],
                                             activefill="black")
            
                    c.itemconfig(arrow5, tags=(arrow_tag5))
                    arrows.append(arrow5)
                    arrows_move[arrow5] = [0, game_position[2]]
                    
                if game_position[1] %10 != 0 and game_position[3] % 10 != 0:   
                    arrow6 = c.create_polygon(off_arrow_x6,off_arrow_y6, 
                                         off_arrow_x6+25,off_arrow_y6, 
                                         off_arrow_x6+25,off_arrow_y6-5, 
                                         off_arrow_x6+40,off_arrow_y6+7.5, 
                                         off_arrow_x6+25,off_arrow_y6+20, 
                                         off_arrow_x6+25,off_arrow_y6+15, 
                                         off_arrow_x6,off_arrow_y6+15,
                                             activefill="black")
                
                    c.itemconfig(arrow6, tags=(arrow_tag6))
                    arrows.append(arrow6)
                    arrows_move[arrow6] = [0, game_position[3]]
            else:
                if game_position[0] %10 != 0 and game_position[2] % 10 != 0:
                    arrow3 = c.create_polygon(off_arrow_x3+deg180[0][0],off_arrow_y3+deg180[0][1], 
                                             off_arrow_x3+deg180[1][0],off_arrow_y3+deg180[1][1], 
                                             off_arrow_x3+deg180[2][0],off_arrow_y3+deg180[2][1], 
                                             off_arrow_x3+deg180[3][0],off_arrow_y3+deg180[3][1], 
                                             off_arrow_x3+deg180[4][0],off_arrow_y3+deg180[4][1], 
                                             off_arrow_x3+deg180[5][0],off_arrow_y3+deg180[5][1], 
                                             off_arrow_x3+deg180[6][0],off_arrow_y3+deg180[6][1],
                                             activefill="black")
                    
                    c.itemconfig(arrow3, tags=(arrow_tag3))
                    arrows.append(arrow3)
                    arrows_move[arrow3] = [game_position[2],0]
                    
                if game_position[0] %10 != 0 and game_position[3] % 10 != 0:  
                    arrow4 = c.create_polygon(off_arrow_x4+deg135[0][0],off_arrow_y4+deg135[0][1], 
                                             off_arrow_x4+deg135[1][0],off_arrow_y4+deg135[1][1], 
                                             off_arrow_x4+deg135[2][0],off_arrow_y4+deg135[2][1], 
                                             off_arrow_x4+deg135[3][0],off_arrow_y4+deg135[3][1], 
                                             off_arrow_x4+deg135[4][0],off_arrow_y4+deg135[4][1], 
                                             off_arrow_x4+deg135[5][0],off_arrow_y4+deg135[5][1], 
                                             off_arrow_x4+deg135[6][0],off_arrow_y4+deg135[6][1],
                                             activefill="black")
                    
                    c.itemconfig(arrow4, tags=(arrow_tag4))
                    arrows.append(arrow4)
                    arrows_move[arrow4] = [game_position[3],0]
                
                if game_position[1] %10 != 0 and game_position[2] % 10 != 0:
                    
                    arrow7 = c.create_polygon(off_arrow_x7+deg225[0][0],off_arrow_y7+deg225[0][1], 
                                             off_arrow_x7+deg225[1][0],off_arrow_y7+deg225[1][1], 
                                             off_arrow_x7+deg225[2][0],off_arrow_y7+deg225[2][1], 
                                             off_arrow_x7+deg225[3][0],off_arrow_y7+deg225[3][1], 
                                             off_arrow_x7+deg225[4][0],off_arrow_y7+deg225[4][1], 
                                             off_arrow_x7+deg225[5][0],off_arrow_y7+deg225[5][1], 
                                             off_arrow_x7+deg225[6][0],off_arrow_y7+deg225[6][1],
                                             activefill="black")
                    
                    c.itemconfig(arrow7, tags=(arrow_tag7))
                    arrows.append(arrow7)
                    arrows_move[arrow7] = [0, game_position[2]]
                    
                if game_position[1] %10 != 0 and game_position[3] % 10 != 0:   
                    arrow8 = c.create_polygon(off_arrow_x8+deg180[0][0],off_arrow_y8+deg180[0][1], 
                                             off_arrow_x8+deg180[1][0],off_arrow_y8+deg180[1][1], 
                                             off_arrow_x8+deg180[2][0],off_arrow_y8+deg180[2][1], 
                                             off_arrow_x8+deg180[3][0],off_arrow_y8+deg180[3][1], 
                                             off_arrow_x8+deg180[4][0],off_arrow_y8+deg180[4][1], 
                                             off_arrow_x8+deg180[5][0],off_arrow_y8+deg180[5][1], 
                                             off_arrow_x8+deg180[6][0],off_arrow_y8+deg180[6][1],
                                             activefill="black")
                    
                    
                    c.itemconfig(arrow8, tags=(arrow_tag8))
                    arrows.append(arrow8)
                    arrows_move[arrow8] = [0, game_position[3]]
        
        #var=IntVar()
       
        
        def cb(self, event):
            print("variable is", self.var.get())
        #solverbox = tk.Checkbutton(, text="Solve", variable = var, command = cb)
#        solverbox.pack()
        def DoMove2(Position, Move):#chopsticks Position =(U_L,U_R,O_L,O_R)
            #print(turn)
            New_Position = (Position[2], Position[3], (Position[0] + Move[0])%maxnum, (Position[1] + Move[1]) % maxnum)
            return New_Position 
        
        def changeturn():            
            childturn = P1 if turn == P2 else P2
            #time.sleep(2)
            return childturn
        def SetupBoard(position):
            print("#turn:",turn,"#position:",game_position, "#gametype:", gametype)
            drawarrows(c)
            UpdateStatus(PredictionStr(position))
            print("lalalalalala")
            #time.sleep(2)
            if gametype == COM and turn == P2:
                #time.sleep(2)
                for i in range(len(arrows)):
                    child = DoMove2(position,arrows_move[arrows[i]])
                    childturn = changeturn()
                    c.itemconfig(arrows[i], fill=value_to_color[MoveValueSwap(Record[child][index_state])])
                    if child == Remoteness[position][1]:
                        c.itemconfig(arrows[i], outline='black')
                        c.tag_bind(arrows[i], sequence="<Button-1>", func=HandleMove({"move":arrows_move[arrows[i]],"parent":position,"child":child, "turn": childturn}))
        
                
            else:
                for i in range(len(arrows)):
                    child = DoMove2(position,arrows_move[arrows[i]])
                    childturn = changeturn()
                    c.itemconfig(arrows[i], fill=value_to_color[MoveValueSwap(Record[child][index_state])])
                    c.tag_bind(arrows[i], sequence="<Button-1>", func=HandleMove({"move":arrows_move[arrows[i]],"parent":position,"child":child, "turn": childturn}))
        
        def hand_num(turnnow, position):
            if turnnow == P1:
                c.itemconfig(left_num_1, text = str(position[0]))
                c.itemconfig(right_num_1, text = str(position[1]))
                c.itemconfig(left_num_2, text = str(position[2]))
                c.itemconfig(right_num_2, text = str(position[3]))
            else:
                c.itemconfig(left_num_1, text = str(position[2]))
                c.itemconfig(right_num_1, text = str(position[3]))
                c.itemconfig(left_num_2, text = str(position[0]))
                c.itemconfig(right_num_2, text = str(position[1]))
        
        
        def HandleMove(info):
            def HandleMoveHelper(event):
                global game_position,turn,arrows,arrows_move
                position = info["child"]
                turnnow = info["turn"]
                if IsPrimitive(position):
                    hand_num(turnnow, position)
                    UpdateStatus("Game Over!\n "+turnnow+ ' ' + Primitive(position) + "!")
                else:
                    hand_num(turnnow, position)
                    print(arrows)
                    for x in arrows:
                        c.delete(x)
                    arrows = []
                    arrows_move = {}
                    turn = turnnow
                    game_position = position
                    SetupBoard(position)
            return HandleMoveHelper
        
        SetupBoard(game_position)
        

app = App()
app.geometry("400x300")
app.mainloop()
