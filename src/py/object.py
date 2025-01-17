import numpy as np

DEBUG = True

class Plane:
    def __init__(self, points, r0):
        try:
            self.points = (points[0], points[1], points[2])
        except Exception:
            print(f"Informe ao menos 3 pontos, cabaço! {Exception}")
        
        self.r0 = r0
        self.normal = self.calculate_normal()  # Calcula o vetor normal na inicialização

    def calculate_normal(self):
        # Obtenha os pontos
        p1, p2, p3 = self.points

        # Vetores diretores do plano
        v1 = np.array(p2) - np.array(p1)
        v2 = np.array(p3) - np.array(p1)

        # Produto vetorial para obter o vetor normal
        normal = np.cross(v1, v2)

        # Normalização do vetor (opcional, depende da aplicação)
        normal_magnitude = np.linalg.norm(normal)
        if normal_magnitude != 0:
            normal = normal / normal_magnitude

        return normal


class Object:

    def __init__(self, filename: str):
        self.vertex = [] 
        self.faces = []

        try:
            self.__readFile__(filename)
        except Exception as e:
            print(f"Erro ao ler arquivo: {e}")

        self.NV = len(self.vertex)
        self.NS = len(self.faces)
        self.NVPS = [len(face) for face in self.faces]

    def __parse_vertex__(self, line):
        coords = line[1:].split()
        vertex = tuple(float(v) for v in coords)
        self.vertex.append(vertex)

    def __parse_face__(self, line):
        """Parse uma linha de face (f v1/vt1/vn1 v2/vt2/vn2 v3/vt3/vn3 ...)"""
        elements = line.split()[1:]
        vertex_indices = []
        for element in elements:
            vertex_idx = int(element.split('/')[0]) - 1  # OBJ usa indexação 1-based
            vertex_indices.append(vertex_idx)
        self.faces.append(vertex_indices)

    def __readFile__(self, filename: str):
        with open(filename, "r") as file:
            for l in file:
                if l.startswith("v "):
                    self.__parse_vertex__(l)
                elif l.startswith("f "):
                    self.__parse_face__(l)

    def getVertex(self):
        return self.vertex
    
    def getFaces(self):
        return self.faces
    
    def getNv(self):
        return self.NV
    
    def getNs(self):
        return self.NS
    
    def getNvps(self, face):
        return self.NVPS[face]

class Projection:
    def __init__(self, obj: Object, pl: Plane, pov):
        self.obj = obj
        self.pl = pl
        self.pov = np.array(pov)  # Ponto de vista (a, b, c)

    def project(self):
        # Vetor normal ao plano
        n = self.pl.normal

        # Cálculo de d0 e d1
        d0 = self.pl.r0[0]*n[0] + self.pl.r0[1]*n[1] + self.pl.r0[2]*n[2]
        d1 = self.pov[0]*n[0] + self.pov[1]*n[1] + self.pov[2]*n[2]
        d = d0 - d1 

        # Construção da matriz de projeção perspectiva
        a, b, c = self.pov
        projection_matrix = np.array([
            [d + a * n[0], a * n[1], a * n[2], -a * d0],
            [b * n[0], d + b * n[1], b * n[2], -b * d0],
            [c * n[0], c * n[1], d + c * n[2], -c * d0],
            [n[0], n[1], n[2], 1.0]
        ])
        # projection_matrix = np.array([
        #     [d1 - a * n[0], -a * n[1], -a * n[2], a * d0],
        #     [-b * n[0], d1 - b * n[1], -b * n[2], b * d0],
        #     [-c * n[0], -c * n[1], d1 - c * n[2], c * d0],
        #     [0,0,0,d1]
        # ])

        if DEBUG:
            print(f'd0: {d0} d1: {d1} d:{d}')
            print(projection_matrix)
            print(self.obj.getVertex())

        # Projeção dos vértices do objeto
        projected_vertices = []
        for vertex in self.obj.getVertex():
            # Converter para coordenadas homogêneas
            vertex_h = np.array([*vertex, 1])  # Adiciona o 1 para homogênea
            print(vertex_h)

            # Aplicar a matriz de projeção
            proj_h = np.dot(projection_matrix, vertex_h)
            print(proj_h)

            # Converter de coordenadas homogêneas para cartesianas
            if abs(proj_h[3]) > 1e-10:  # Evitar divisão por zero
                proj_cartesian = proj_h[:3] / proj_h[3]
            else:
                proj_cartesian = proj_h[:3]

            projected_vertices.append(proj_cartesian)

        # Retorna os vértices projetados
        return projected_vertices
