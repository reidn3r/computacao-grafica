from object import Object, Plane, Projection
import numpy as np
import cv2

def draw_projection(image, vertices, faces, scale=10, offset=(250, 250)):
    # Verifique se o número de vértices projetados é suficiente
    num_vertices = len(vertices)
    print(num_vertices)
    
    for face in faces:
        for i in range(len(face)):
            # Pega o índice do vértice atual e o próximo
            start_idx = face[i]
            end_idx = face[(i + 1) % len(face)]  # O próximo vértice (circular)

            # Verifique se os índices são válidos
            if start_idx >= num_vertices or end_idx >= num_vertices:
                print(f"Índice fora de alcance: start_idx={start_idx}, end_idx={end_idx}")
                continue  # Pula essa face se o índice for inválido

            # Vértices para desenhar a linha
            start_vertex = vertices[start_idx]
            end_vertex = vertices[end_idx]

            print(start_vertex, end_vertex)

            # Ajuste para a escala e deslocamento da projeção
            start_point = (int(start_vertex[0] * -scale), int(start_vertex[1] * -scale))
            end_point = (int(end_vertex[0] * -scale), int(end_vertex[1] * -scale))

            # Desenha a linha entre os vértices
            cv2.line(image, start_point, end_point, (255, 255, 255), 1)  # Linha branca



def main():
    # Carregar o cubo
    obj = Object('./model/cube.obj')
    vertex, faces = obj.getVertex(), obj.getFaces()

    print("Número de Superfícies:", obj.getNs())
    print("Número de Vértices:", obj.getNv())
    print("Número de Vértices na Superfície 0:", obj.getNvps(0))

    # Definir o plano de projeção
    plane = Plane(((0,1,0), (0,0,1), (1,0,0)), (-1,-1,-1)) # ((0,1,0), (0,0,1), (1,0,0)), (-1,-1,-1) ((0,0,0), (1,0,0), (0,1,0)), (0,0,-1)

    print("Vetor Normal ao Plano:", plane.calculate_normal())

    # Definir o ponto de vista
    pov = (4,4,4)

    # Criar projeção
    projection = Projection(obj, plane, pov)
    projected_vertices = projection.project()
    print(projected_vertices)

    # Criar uma imagem para visualizar a projeção
    image = np.zeros((500, 500), dtype=np.uint8)

    print(faces)

    # Desenhar a projeção na imagem
    draw_projection(image, projected_vertices, faces)

    # Mostrar a imagem
    cv2.imshow("Projeção", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
