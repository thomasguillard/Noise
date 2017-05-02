import tingbot
from tingbot import *

import point
from point import *

import random
from random import *

import math
from math import *

import vector
from vector import *

import remap
from remap import *

size = screen.width*2 # Get rid of *2

grid = [[] for i in xrange(size)]

# setup code here

for col in xrange(size):
    for row in xrange(size):
        angle = int(random()*2*math.pi)
        x = math.cos(angle)
        y = math.sin(angle)
        grid[col].append(Point(col, row, Vector(x, y, 0)))
        
def blend(t):
    return 6 * math.pow(t, 5) - 15 * math.pow(t, 4) + 10 * math.pow(t, 3)

def noise2D(x, y):
    i = int(floor(x))
    j = int(floor(y))

    g00 = grid[i][j].g
    g10 = grid[i+1][j].g
    g01 = grid[i][j+1].g
    g11 = grid[i+1][j+1].g
    
    u = x - i
    v = y - j

    n00 = g00.dot(Vector(u, v, 0))
    n10 = g10.dot(Vector(u-1, v, 0))
    n01 = g01.dot(Vector(u, v-1, 0))
    n11 = g11.dot(Vector(u-1, v-1, 0))
    
    nx0 = n00 * (1-blend(u)) + n10 * blend(u)
    nx1 = n01 * (1-blend(u)) + n11 * blend(u)

    nxy = nx0 * (1-blend(v)) + nx1 * blend(v)

    return nxy

pos = 0
increase = True
increment = 0.1
offset = 1

def displayball():
    global pos, increase, increment, offset
    if increase:
        if pos < size - increment - offset - 1:
            pos += increment
        else:
            increase = False
    else:
        if pos > 0 + increment + offset:
            pos -= increment
        else:
            increase = True

    #screen.text(noise2D(pos, 0))
    screen.circle(
        xy = (  screen.width/2+noise2D(pos, 0)*screen.width/2,
                screen.height/2+noise2D(pos + offset,0)*screen.height/2),
        size = 10,
        color='blue'
    )

mylist = [[] for i in xrange(size)]
flatList = []

frame = 0

frequency = floor(50)

def process():
    for px in xrange(screen.width):
        for py in xrange(screen.height):
            v = noise2D((px)/frequency,py/frequency)
            mylist[px].append(v)
            flatList.append(v)

    minimum = min(flatList)
    maximum = max(flatList)

    print minimum
    print maximum

    for px in xrange(screen.width):
        for py in xrange(screen.height):
            mylist[px][py] = remap(mylist[px][py], minimum, maximum, 0, 255)
            flatList[px+py*screen.width] = remap(flatList[px+py*screen.width], minimum, maximum, 0, 255)

    new_minimum = min(flatList)
    new_maximum = max(flatList)

    print new_minimum
    print new_maximum

process()

@every(seconds=1.0/30)
def loop():
    # drawing code here
    screen.fill(color='black')
    
    for px in xrange(screen.width):
        for py in xrange(screen.height):
            screen.rectangle(
                xy = (px, py),
                size = [1]*2,
                align = 'topleft',
                color = tuple([mylist[px][py]]*3)
            )
    
    '''
    global frame, mylist, flatList,frequency
    screen.text(frame,color='red')
    frame+=1
    frequency-=1
    del mylist[:]
    mylist = [[] for i in xrange(size)]
    del flatList[:]
    process()
    '''
    '''
    displayball()
    '''
tingbot.run()
