from vec2 import vec2
import pandas as pd
from math import cos, sin



def transpose(v: vec2):
    return pd.DataFrame([[1, 0, v.x],
                         [0, 1, v.y],
                         [0, 0,  1 ]])

def rotation(rad: float):
    return pd.DataFrame([[cos(rad), -sin(rad), 0],
                         [sin(rad),  cos(rad), 0],
                         [   0,         0,     1]])

def scale(v: vec2):
    return pd.DataFrame([[v.x, 0,  0],
                         [ 0, v.y, 0],
                         [ 0,  0,  1]])

def to_homogenous(v: vec2):
    return pd.DataFrame([[v.x], 
                         [v.y],
                         [ 1 ]])

def identity():
    return pd.DataFrame([[1, 0, 0],
                         [0, 1, 0],
                         [0, 0, 1]])

def chain_transforms(*args):
    acc = identity()
    for arg in args:
        acc = arg.dot(acc)
    return acc

def from_homogenous(df: pd.DataFrame) -> vec2:
    x, y, w = df.iloc[0, 0], df.iloc[1, 0], df.iloc[2, 0]
    return vec2(x / w, y / w)

def apply_transform_to_point(p: vec2, transform):
    return from_homogenous(transform.dot(to_homogenous(p)))

def apply_transform_to_points(pl: list[vec2], transform):
    return [apply_transform_to_point(p, transform) for p in pl]

