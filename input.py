class Input:
    
    def __init__(self, bge):
        self.bge = bge
        self.keyboard = bge.logic.keyboard
        self.just_activated = bge.logic.KX_INPUT_JUST_ACTIVATED
        
        
    def run(self):
        if self.keyboard.events[self.bge.events.ESCKEY] == self.just_activated:
                print("leaving game")
                return "leaving_game"