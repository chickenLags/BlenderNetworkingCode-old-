class Start:
    def __init__(self, UC, bge, ras):
        print("intializing")
        self.UC = UC
        self.bge = bge
        self.scene = bge.logic.getCurrentScene()
        self.ras = ras
        self.ras.showMouse(True)
        print("initialized!")


    def run(self):
        test = self.bge.logic.getCurrentScene()
        if self.scene != test:
            self.ras.showMouse(False)
            return "lobby"