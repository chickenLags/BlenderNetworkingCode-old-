import socket, sys, pickle

###SERVER###

class Server:
    def __init__(self):
        self.host = socket.gethostname()
        self.port = 5000
        self.s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s_udp.settimeout(1)
        self.s_udp.bind((self.host, self.port))
        self.connections = []
        self.players = []
        print("starting server...")
        self.run()

    def receive(self): # format data = [category, c_id, msg]
        try:
            data = pickle.loads(self.s_udp.recv(1024))
            return data
        except:
            pass
        
        

    def send(self, category, c_id, msg):
        to_send = pickle.dumps([category, msg])

        if c_id == "all":
            for con in self.connections:
                self.s_udp.sendto(to_send, con)
        else:
            self.s_udp.sendto(to_send, self.connections[c_id])

        print("sent to", c_id, pickle.loads(to_send))
        


        

    def run(self):
        while True:
            cmd = self.receive()
            
            if cmd == None:
                pass
            elif cmd[0] == "id_request":
                print("cibbugfyfd")
                if cmd[2] in self.connections:
                    self.send("id_assign", self.connections.index(cmd[2]), self.connections.index(cmd[2]))
                else:
                    self.connections.append(cmd[2])
                    self.send("id_assign", self.connections.index(cmd[2]), self.connections.index(cmd[2]))
            elif cmd[0] == "update":
                if len(self.players) > cmd[1]:
                    self.players[cmd[1]] = cmd[2]
                else:
                    self.players.append(cmd[2])
                    
                self.send("update", "all", self.players)

class Player:
    def __init__(self, position, orientation):
        self.position = position
        self.orientation = orientation

server = Server()


        
