import pyglet
from pyglet import shapes
import pygletDef as gui
from pyglet.window import key, mouse

window  = pyglet.window.Window(resizable=True)    
label = pyglet.text.Label('Window 1',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')    
@window.event
def on_draw():
    window.clear()
    
    label.x = window.width//2
    label.y = window.height//2
    
    label.draw()


window1  = pyglet.window.Window(resizable=True)
label1 = pyglet.text.Label('Window 2',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window1.width//2, y=window1.height//2,
                          anchor_x='center', anchor_y='center')
@window1.event
def on_draw():
    window1.clear()

    label1.x = window1.width//2
    label1.y = window1.height//2
    
    label1.draw()

window2  = pyglet.window.Window(resizable=True)
label2 = pyglet.text.Label('Window 3',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window1.width//2, y=window1.height//2,
                          anchor_x='center', anchor_y='center')
@window2.event
def on_draw():
    window2.clear()

    label2.x = window2.width//2
    label2.y = window2.height//2
    
    label2.draw()
    
pyglet.app.run()


