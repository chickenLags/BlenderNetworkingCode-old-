import bge, time

controller = bge.logic.getCurrentController()
own = controller.owner
increase = controller.sensors['Increase']
decrease = controller.sensors['Decrease']

if increase.status == 1:
    own['prop'] += 1
if decrease.status == 1:
    own['prop'] -= 1 
    
if own['prop'] > 5:
    own['prop'] = 5
elif own['prop'] < 1:
    own['prop'] = 1

own.text = str(own['prop'])

