
class ObjectParser:

    def __init__(self):
        self.vertex = []
        self.faces = []
        

    def __parse_vertex__(self, line):
        coords = line[1:].split()
        vertex = tuple(float(v) for v in coords)
        self.vertex.append(vertex)


    def __parse_face__(self, line): #by Claude.ai
        """Parse uma linha de face (f v1/vt1/vn1 v2/vt2/vn2 v3/vt3/vn3 ...)"""
        # Remove o 'f' do início
        elements = line.split()[1:]
        # Extrai apenas os índices dos vértices (primeiro número antes de cada '/')
        vertex_indices = []
        for element in elements:
            # Pega o primeiro número antes de '/' ou o número todo se não houver '/'
            vertex_idx = int(element.split('/')[0]) - 1  # OBJ usa indexação 1-based
            vertex_indices.append(vertex_idx)
        self.faces.append(vertex_indices)


    def read_file(self, filename:str):
        with open(filename, "r") as file:
            for l in file:
                if l.startswith("v "):
                    self.__parse_vertex__(l)
                
                elif l.startswith("f "):
                    self.__parse_face__(l)

        return self.vertex, self.faces


