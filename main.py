from direct.showbase.ShowBase import ShowBase
from panda3d.core import TextNode, TransparencyAttrib
from panda3d.core import LPoint3, LVector3
from panda3d.core import WindowProperties
from direct.gui.OnscreenText import OnscreenText
from direct.task.Task import Task
from math import sin, cos, pi
from random import randint, choice, random
from direct.interval.MetaInterval import Sequence
from direct.interval.FunctionInterval import Wait, Func
from direct.gui.DirectGui import *
import sys

# Constantes que controlarán el comportamiento del juego. Es bueno agrupar constantes 
# como esta para que se puedan cambiar una vez sin tener que buscar en todas partes 
# donde se usan en el código
SPRITE_POS = 55    # En el campo de visión predeterminado y una profundidad de 55, las 
# dimensiones de la pantalla son 40x30 unidades
SCREEN_X = 21       # La pantalla va de -20 a 20 en X
SCREEN_Y = 16       # La pantalla va de -15 a 15 en Y
TURN_RATE = 360     # Grados que puede girar la nave en 1 segundo
ACCELERATION = 10   # Aceleración de la nave en unidades/seg/seg.
MAX_VEL = 6         # Velocidad máxima del barco en unidades/seg.
MAX_VEL_SQ = MAX_VEL ** 2  # Cuadrado de la velocidad del barco.
DEG_TO_RAD = pi / 180  # Traduce grados a radianes para sen y cos
BULLET_LIFE = 2     # Cuánto tiempo permanecen las balas en la pantalla antes de desaparecer.
BULLET_REPEAT = .2  # Con qué frecuencia se pueden disparar balas
BULLET_SPEED = 10   # Velocidad con la que se mueven las balas
AST_INIT_VEL = 2    # Velocidad de los asteroides más grandes
AST_INIT_SCALE = 3  # Escala inicial de asteroides
AST_VEL_SCALE = 2.2  # Velocidad con la que se rompe el asteroide
AST_SIZE_SCALE = .6  # Cuánto cambia la escala de asteroides cuando se rompe
AST_MIN_SCALE = 1.1  # Si un asteroide es más pequeño que este y es golpeado, 
# desaparece en lugar de dividirse

def loadObject(tex=None, pos=LPoint3(0, 0), depth=SPRITE_POS, scale=1,
               transparency=True):
    # Todos los objetos usan el modelo de avión y se acoplan a la cámara 
    # para que quede frente a la pantalla.
    obj = loader.loadModel("models/plane")
    obj.reparentTo(camera)

    # Establecer la posición inicial y la escala.
    obj.setPos(pos.getX(), depth, pos.getY())
    obj.setScale(scale)

    # Esto le dice a Panda que no se preocupe por el orden en que se dibujan las cosas 
    # (es decir, deshabilite la prueba Z). Esto evita un efecto conocido como Z-fighting.
    obj.setBin("unsorted", 0)
    obj.setDepthTest(False)

    if transparency:
        # Habilita la mezcla de transparencias.
        obj.setTransparency(TransparencyAttrib.MAlpha)

    if tex:
        # Cargue y establezca la textura solicitada.
        tex = loader.loadTexture("textures/" + tex)
        obj.setTexture(tex, 1)

    return obj

class Juego(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        #Modificamos el tamaño de la ventana
        properties = WindowProperties()
        properties.setSize(960, 720)
        self.win.requestProperties(properties)

        # Desactivamos el control de cámara predeterminado basado en el mouse.
        self.disableMouse()

        #Asignamos un color de fondo por defecto en este caso R:52 G:227 B: 1142
        #self.setBackgroundColor((25/255),(144/255),(110/255),1)
        self.setBackgroundColor(0,0,0,1)
        self.bg = loadObject("Fondos/FondoBase.png",scale=130, depth=100,
                            transparency=True)
        
        self.cuadro = loadObject("PisosO/Piso18.png")

        self.keyMap={
            "arriba" : False,
            "abajo" : False,
            "izquierda" : False,
            "derecha" : False
        }
        self.accept("w", self.updateKeyMap, ["arriba", True])
        self.accept("w-up", self.updateKeyMap, ["arriba", False])
        self.accept("s", self.updateKeyMap, ["abajo", True])
        self.accept("s-up", self.updateKeyMap, ["abajo", False])
        self.accept("a", self.updateKeyMap, ["izquierda", True])
        self.accept("a-up", self.updateKeyMap, ["izquierda", False])
        self.accept("d", self.updateKeyMap, ["derecha", True])
        self.accept("d-up", self.updateKeyMap, ["derecha", False])
        self.updateTask = taskMgr.add(self.update, "update")

    def updateKeyMap(self, controlName, controlSate):
        self.keyMap[controlName] = controlSate
        # print(controlName, " accedo a ", controlSate)

    def update(self, task):
        # Get the amount of time since the last update
        dt = globalClock.getDt()

        # If any movement keys are pressed, use the above time
        # to calculate how far to move the character, and apply that.
        if self.keyMap["arriba"]:
            self.bg.setZ(self.bg.getZ()-1)
        if self.keyMap["abajo"]:
            self.bg.setZ(self.bg.getZ()+1)
        if self.keyMap["izquierda"]:
            self.bg.setX(self.bg.getX()+1)
        if self.keyMap["derecha"]:
            self.bg.setX(self.bg.getX()-1)
        return task.cont


app = Juego()
app.run()