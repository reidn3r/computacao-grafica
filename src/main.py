from object_parser import ObjectParser
import numpy as np

def main():
    '''
        * Dados do Objeto
        * v: coordenadas dos vertices
    '''
    parser = ObjectParser()
    vertex, faces = parser.read_file("../model/cat.obj")

    nv, ns = len(vertex), len(faces)
    nvps = [len(x) for x in faces]

    p1, p2, p3 = (0, 0, 0), (1, 1, 1), (2, 2, 2)
    r0 = p2
    '''
        * Cálculos
    '''
    return

if __name__ == "__main__":
    pov = (0, 0, 1)

    main()