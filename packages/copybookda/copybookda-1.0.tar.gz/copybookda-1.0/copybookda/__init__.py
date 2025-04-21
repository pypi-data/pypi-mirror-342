__author__ = 'DavidYdin'
__version__ = '1.0'
__email__ = 'David.2280@yandex.ru'
from turtle import *
from pyautogui import *
from keyboard import *
speed(0)
setup(1.0,1.0)
up()
X=0
Y=0
a = 0
moveTo(1000, 500)
while a == 0:
    if is_pressed('space') == True:
        down()
    else:
        up()
    x, y = position()
    X+=x-1000
    Y+=y-500
    goto(X, -Y)
    moveTo(1000, 500)
    if is_pressed('esc') == True:
        a = 1