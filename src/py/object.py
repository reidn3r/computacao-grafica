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
        v1 = np.array(p1) - np.array(p2)
        v2 = np.array(p3) - np.array(p2)

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
        self.projected_vertices = []

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
            [n[0], n[1], n[2], -d1]
        ])

        print(f'd0: {d0} d1: {d1} d:{d}')
        print('\nMatriz de projeção:')
        print(projection_matrix)
        print('\nVértices:')
        print(self.obj.getVertex())

        transposed_object = np.array(self.obj.vertex).T # Transpõe matrix dos vérticess
        projected_vertices = np.dot(projection_matrix, transposed_object)

        m = projected_vertices.shape[0]
        n = projected_vertices.shape[1]
        for line in range(m):
            for collum in range(n):
                projected_vertices[line][collum] /= projected_vertices[m-1][collum]
        print('\nCoordenadas homgêneas:')
        print(projected_vertices)

        projected_vertices = projected_vertices[:2] # Remove as coordenadas que z e w
        print('\nRemove Z e W:')
        print(projected_vertices)

        # Multiplicando apenas as coordenadas y por -1
        projected_vertices[1] *= -1
        print('\nCoordenadas refletidas:')
        print(projected_vertices)

        self.projected_vertices = projected_vertices

        # Retorna os vértices projetados
        return projected_vertices

    def toViewport(self, X, Y, U, V, S):
        Xmax, Xmin = X[0], X[1]
        Ymax, Ymin = Y[0], Y[1]
        Umax, Umin = U[0], U[1]
        Vmax, Vmin = V[0], V[1]
        Sx, Sy = S[0], S[1]

        # Lista para armazenar as coordenadas de dispositivo
        deviceCoordinates = self.projected_vertices.copy()

        # O PROBLEMA TA AQUIIIIIIIIIIIIIIIIIIIII!!!!!!!!!!!!!!!!!!!!!!!!
        m = deviceCoordinates.shape[0]
        for i in range(m):
            deviceCoordinates[0][i] = (Sx * self.projected_vertices[0][i]) - (Sx * Xmin)
        
        for i in range(m):
            deviceCoordinates[1][i] = -(Sy * self.projected_vertices[1][i]) - (Sy * Ymin)

        return np.array(deviceCoordinates)
