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
