import pyglet
from pyglet import shapes
import pygletDef as gui
from pyglet.window import key, mouse


window = pyglet.window.Window(resizable=True, width=1500, height=800)
window.set_caption('Light Configure - Layout')#Layout, Display, Sequence, Render

red = (150,0,0)
lightRed = (255,0,0)
orange = (255,150,0)
green = (0,200,0)
light_green = (0,255,0)
blue = (0,0,200)
purple = (144,34,199)
brown = (117,79,45)
black = (0,0,0)
white = (255,255,255)
lightGrey2 = (185,185,185)
lightGrey = (100,100,100)
darkGrey = (50,50,50)

layoutScreen = gui.layoutScreen()
displayScreen = gui.displayScreen()

backGround = shapes.Rectangle(0, 0, window.width, window.height, color=lightGrey)

#-----Button Object Define-----#
fileButton = gui.Button([255,255,255], 12, [0,0,0,175], "File")

layoutButton = gui.Button([150,150,150], 15, [255,255,255,255], "Layout")
sequenceButton = gui.Button([150,150,150], 15, [255,255,255,255], "Sequence")
renderButton = gui.Button([150,150,150], 15, [255,255,255,255], "Render")
displayButton = gui.Button([150,150,150], 15, [255,255,255,255], "Display")

fps_display = pyglet.window.FPSDisplay(window=window)

@window.event
def on_draw():
    window.clear()

    #Background Update and Draw
    backGround.width = window.width
    backGround.height = window.height
    backGround.draw()

    #-----Button Location Updates-----#
    fileButton.updateLoc(0,window.height-20,40,20)

    layoutButton.updateLoc(5,window.height-55,100,30)
    sequenceButton.updateLoc(110,window.height-55,100,30)
    renderButton.updateLoc(215,window.height-55,100,30)
    displayButton.updateLoc(320,window.height-55,100,30)

    #-----Button Draw Calls-----#
    fileButton.draw()

    layoutButton.draw()
    sequenceButton.draw()
    renderButton.draw()
    displayButton.draw()
    
    #-----Drawing Different Screens and Changing Button Colors-----#
    if window.caption.replace("Light Configure - ", "") == "Layout":
        layoutButton.rect.color=[50,50,50]
        sequenceButton.rect.color=[150,150,150]
        renderButton.rect.color=[150,150,150]
        displayButton.rect.color=[150,150,150]

        layoutScreen.runTime(window.width, window.height)

    if window.caption.replace("Light Configure - ", "") == "Sequence":
        layoutButton.rect.color=[150,150,150]
        sequenceButton.rect.color=[50,50,50]
        renderButton.rect.color=[150,150,150]
        displayButton.rect.color=[150,150,150]

    if window.caption.replace("Light Configure - ", "") == "Render":
        layoutButton.rect.color=[150,150,150]
        sequenceButton.rect.color=[150,150,150]
        renderButton.rect.color=[50,50,50]
        displayButton.rect.color=[150,150,150]

    if window.caption.replace("Light Configure - ", "") == "Display":
        layoutButton.rect.color=[150,150,150]
        sequenceButton.rect.color=[150,150,150]
        renderButton.rect.color=[150,150,150]
        displayButton.rect.color=[50,50,50]

        displayScreen.runTime(window.width, window.height)

    fps_display.draw()



@window.event
def on_key_press(symbol, modifiers):
    if window.caption.replace("Light Configure - ", "") == "Display":
        displayScreen.keysPress(symbol)

    # Symbolic names:
    if symbol == key.RETURN:
        print("enter")

    #if symbol == 96:
        #print('`')

@window.event
def on_mouse_press(x, y, button, modifiers):
    if window.caption.replace("Light Configure - ", "") == "Layout":
        layoutScreen.actionInput(x, y, button, modifiers)
    if window.caption.replace("Light Configure - ", "") == "Display":
        displayScreen.actionInput(x, y, button, modifiers)

    if button == 1:
        if layoutButton.isOver(x,y):
            window.set_caption('Light Configure - Layout')
        elif sequenceButton.isOver(x,y):
            window.set_caption('Light Configure - Sequence')
        elif renderButton.isOver(x,y):
            window.set_caption('Light Configure - Render')
        elif displayButton.isOver(x,y):
            window.set_caption('Light Configure - Display')
        

@window.event
def on_mouse_motion(x, y, dx, dy):
    if window.caption.replace("Light Configure - ", "") == "Layout":
        layoutScreen.mouseMotion(x,y)
    if window.caption.replace("Light Configure - ", "") == "Display":
        displayScreen.mouseMotion(x,y)

    layoutButton.over = layoutButton.isOver(x,y)
    sequenceButton.over = sequenceButton.isOver(x,y)
    renderButton.over = renderButton.isOver(x,y)
    displayButton.over = displayButton.isOver(x,y)

pyglet.app.run()