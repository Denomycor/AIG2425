from vec2 import vec2
import math


def triangle():
    return [
        vec2(math.cos(0),math.sin(0)), 
        vec2(math.cos(math.pi*4/5),math.sin(math.pi*4/5)), 
        vec2(math.cos(math.pi*6/5),math.sin(math.pi*6/5))
    ]

