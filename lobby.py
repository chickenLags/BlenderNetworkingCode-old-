class Lobby:
    def __init__(self, UC, ras, bge):
        self.UC = UC
        self.ras = ras
        self.bge = bge
        self.ras.showMouse(True)
        self.taken_ids = []
        self.started = False
        self.txt_start = bge.logic.getCurrentScene().objects['txt_start']
        self.waiters = 0

    def run(self):
        if str(self.bge.logic.getCurrentScene()) == "menu_scene":
            return "menu_scene"
        if not self.started:
            if self.txt_start.text == "started":
                self.started = True
                self.ras.showMouse(False)
                print("connecting with server to find other players")
        else:
            #request lobby until received id
            if self.UC.myId == 9999:
                self.UC.send("lobby_request", [self.UC.my_ip, self.UC.my_port])
                data = self.UC.receive()
                if data != None:
                    cat = data[0]
                    msg = data[1]
                    if cat == "id_assign":
                        self.UC.myId = msg

            #display everyone in lobby when id has been received
            else:
                self.UC.send("lobby_update", "empty")
                data = self.UC.receive()
                if data != None:
                    cat = data[0]
                    msg = data[1]
                    if cat == "lobby_update":
                        diff = len(msg) - len(self.taken_ids)
                        if diff > 0:
                            self.add_waiters(diff)
                        self.taken_ids = msg
                    elif cat == "game_start":
                        self.ras.showMouse(False)
                        return "game_start"


    def add_waiters(self, i):
        pos = len(self.taken_ids) -1
        self.object = self.bge.logic.getCurrentScene().addObject("holder", "holder", 0)
        value = (pos * -1.3) + 1.5
        self.object.worldPosition = [5, value, 1]
        if i > 1:
            self.add_waiters(i-1)
            
        