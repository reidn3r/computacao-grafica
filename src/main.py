from object import Object
import numpy as np

def main():
    '''
        * Dados do Objeto
        * v: coordenadas dos vertices
    '''
    obj = Object('./model/cube.obj')
    vertex, faces = (obj.getVertex(), obj.getFaces())

    print(obj.getNs())
    print(obj.getNv())
    print(obj.getNvps(0))

    p1, p2, p3 = (0, 0, 0), (1, 1, 1), (2, 2, 2)
    r0 = p2
    '''
        * Cálculos
    '''
    return

if __name__ == "__main__":
    pov = (0, 0, 1)

    main()