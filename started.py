 import bge

controller = bge.logic.getCurrentController()
own = controller.owner
started = controller.sensors['Message']

if started.status == 1:
    own.text = "started"
