class Game:

    def __init__(self, bge, UC, pickle):
        self.UC = UC
        self.bge = bge
        self.scene = self.bge.logic.getCurrentScene() 
        self.char = self.scene.objects['char.001']
        self.char['tikking'] = False
                
                
        #initializatie van belangrijke classen
        self.players = Players(self.UC.myId, bge)
        self.stones = Stones(self.UC.myId, bge)
        self.doors = []

    def run(self):
        # here the code can choose to normally update the position or
        # to let the server know to change another player into
        # a tikker. --- decision depends on whether the tikking 
        # property is true --- 
        # if it is then it is reset and executed
        # otherwise a normal update is done.
        
        
        tikking = self.char['tikking']


            # here a normal player position update will be made;
            # this means that the client will send the server, his 
            # position, orientation and the position of his stone.
        if not tikking:
            stone = [0,0,0]
            try:
                stone = self.scene.objects['bullet.000']
                stone = list(stone.worldPosition)
            except:
                pass
                # prepares a var for holding this players orientation in picklable languague
            ori = [] 
            for x in list(self.char.worldOrientation):
                ori.append(list(x))
            
                #sends standard position update
            self.UC.send("my_position", [[self.char.position.x, 
                                        self.char.position.y, 
                                        self.char.position.z], ori, stone])
                                        
                
                
                
            # here the tik_notification will be sent together with the id.
            # the id will first be calculated based on who is closest to
            # this player at the moment.
        elif tikking:
            print("im tikking!")
                # reset property
            self.char.attrDict['tikking'] = False
                # calculate closest and send its id to server
            the_id_of_tikked = self.players.closest_player(self.char.position)
            self.UC.send(["tik_notification", the_id_of_tikked])
            
         
         
            
            
        # Here the client receives an answer after sending out a message of its own
        # The received message is an update of the current status of the board OR 
        # the announcement that the game is ending together with the winning team. 
            
        data = self.UC.receive()
        #print("got to receive data in def run")
        if data != None:
            cat = data[0]
            msg = data[1]
            if cat == "map_update" and self.UC.myId is not 9999:
                players = msg['players'] # [[[0,0], ori], ...
                stones = msg['stones'] # [] or [position, velocity], [position, velocity]]
                self.doors = msg['doors'] # ["name": 0, "name": 1, "name":0]
                tikkers = msg["tikkers"] 
                for x in range(0, len(self.players.players)):
                    if tikkers[x] is 1 and self.players.tikkers[x] is not 1:
                        self.players.tikkers[x] = 1
                        if x is not self.UC.myId:
                            self.players.players[x].set_tikker(True)
                        else:
                            self.becomeTikker()
                    
                        
                # parse data here
                
                self.players.update(players)
                self.stones.update(stones)


            elif cat == "game_finished":
                return "game_finished"
            
    def becomeTikker(self):
        self.char.color = [255, 0, 0, 1]
        pass
            
class Stones:
    def __init__(self, myId, bge):
        self.stones = []
        self.myId = myId
        for x in range(0, 5):
            create_model = True
            if x == self.myId:
                create_model = False
            self.add(Stone(x, create_model, bge))
    
    def add(self, stone):
        self.stones.append(stone)
        
    def update(self, stones):
        for x in range(0, 5):
            if x != self.myId:
                self.stones[x].update(stones[x])

class Stone:
    def __init__(self, myId, create_model, bge):
        self.bge = bge
        self.scene = self.bge.logic.getCurrentScene()
        if create_model:
            self.object = self.scene.addObject("bullet.001", "bullet.001", 0)
            self.object.worldPosition = [0,0,-200]
            
    def update(self, position):
        self.object.worldPosition = position
            
class Players:
    
    def __init__(self, myId, bge):
        self.players = []
        self.tikkers = [0, 0, 0, 0, 0]
        self.myId = myId
        print("got to playes.init")
        for x in range(0, 5):
            create_model = True
            if x == self.myId:
                create_model = False
            self.add(Player(x, create_model, bge))
            
        
    def add(self, player):
        self.players.append(player)
    
    def update(self, players):
        for x in range(0,5):
            if x != self.myId: 
                self.players[x].update(players[x])
                
    def closest_player(self, position):
        closest_player = None
        for player in self.players:
            id, distance = player.distance_to(position)
            if closest_player == None:
                closest_player = [id, distance]
            elif closest_player[1] > distance:
                closest_player = [id, distance]
        
        return closest_player
                
        

class Player:
    def __init__(self, i, create_model, bge):
        self.bge = bge
        self.scene = self.bge.logic.getCurrentScene()
        if create_model:
            self.object = self.scene.addObject("mpchar", "mpchar", 0)
            self.object.worldPosition = [0,0,-200]
            # the standard color should be blue since thats the default material. 
            self.object.color = [255, 0, 0, 1]
            
            
            
        self.ID = i
    
    def update(self, position):
        self.object.worldPosition = position[0]
        self.object.worldOrientation = position[1]
        
    def set_tikker(self, tikker):
        print("player", self.ID, "has become a tikker!")
        self.scene.objects['Cube'].color = [255, 0, 0, 1] #rgba
        #should check how to get a child element from the main element. 
        
    def distance_to(self, position):
        distance_x = self.object.worldPosition.x -position.x
        squared_x = distance_x * distance_x
        
        distance_y = self.object.worldPosition.y - position.y
        squared_y = distance_y * distance_y
        
        sqr_distance_sum = squared_x + squared_y
        
        # DEBUG MSG
        print(self.ID, sqr_distance_sum)
        return [self.ID, sqr_distance_sum]
            
        