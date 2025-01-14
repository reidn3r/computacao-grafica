from object import Object, Plane
import numpy as np

def main():

    obj = Object('./model/cube.obj')
    vertex, faces = (obj.getVertex(), obj.getFaces())

    print(obj.getNs())
    print(obj.getNv())
    print(obj.getNvps(0))


    pl = Plane(((0, 0, 0), (0, 0, 1), (1, 0, 0)), (0,0,0))

    print(pl.calculate_normal())

if __name__ == "__main__":
    pov = (0, 0, 1)

    main()