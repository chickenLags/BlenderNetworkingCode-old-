import bge

scene = bge.logic.getCurrentScene()
stone = scene.objects['bullet.000']

controller = bge.logic.getCurrentController()
own = controller.owner

if controller.sensors['Mouse'].status == 1 and controller.sensors['Property'].status:
    stone.worldPosition = scene.objects['char.001'].worldPosition
    stone.worldPosition.z += 2
    stone.worldOrientation = scene.objects['char.001'].worldOrientation
    stone.setLinearVelocity([0,-90,0], True)

