import socket, pickle, bge
from udp import Udp_communication
from start import Start
from lobby import Lobby
from game import Game
from input import Input
import Rasterizer as ras


class Main:
    server_ip = "192.168.1.100"
    server_port = 5000

    def __init__(self):
        self.running = True
        self.UC = Udp_communication(socket, pickle, self.server_ip, self.server_port)
        self.state = Start(self.UC, bge, ras)   #THIS JUST FORWARDS TO LOBBY, UPDATE IT.
        self.input = Input(bge)


    def run(self):


        value = self.state.run()
        input_value = self.input.run()
        
        if input_value == None:
            pass
        elif input_value == "leaving_game":
            self.running = False
        
        if value == None:
            pass
        elif value == "lobby":
            self.state = Lobby(self.UC, ras, bge)
        elif value == "game_start":
            bge.logic.sendMessage("change_scene")
            if str(bge.logic.getCurrentScene()) == "game_scene":
                self.state = Game(bge, self.UC, pickle)
        elif "menu_scene":
            print("going back to start!")
            self.state = Start(self.UC, bge, ras)


if __name__ == "__main__":
    main = Main()
    bge.logic.NextFrame()

while main.running:
    main.run()
    bge.logic.NextFrame()
    

main.UC.close()