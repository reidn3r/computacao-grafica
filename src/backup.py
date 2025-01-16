from object import Object, Plane, Projection
import numpy as np
import cv2

# Variáveis globais para controle do POV e arraste
is_dragging = False
last_mouse_pos = None
pov = [4, 4, 4]  # Ponto de vista inicial

def draw_projection(image, vertices, faces, scale=20):
    # Calcular o centro da projeção
    avg_x = sum(vertex[0] for vertex in vertices) / len(vertices)
    avg_y = sum(vertex[1] for vertex in vertices) / len(vertices)
    offset = (image.shape[1] // 2 - int(avg_x * scale), image.shape[0] // 2 - int(avg_y * scale))

    for face in faces:
        for i in range(len(face)):
            start_idx = face[i]
            end_idx = face[(i + 1) % len(face)]

            start_vertex = vertices[start_idx]
            end_vertex = vertices[end_idx]

            start_point = (
                int(start_vertex[0] * scale + offset[0]),
                int(start_vertex[1] * scale + offset[1]),
            )
            end_point = (
                int(end_vertex[0] * scale + offset[0]),
                int(end_vertex[1] * scale + offset[1]),
            )

            cv2.line(image, start_point, end_point, (255, 255, 255), 1)

def mouse_callback(event, x, y, flags, param):
    global is_dragging, last_mouse_pos, pov
    if event == cv2.EVENT_LBUTTONDOWN:  # Início do clique e arraste
        is_dragging = True
        last_mouse_pos = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE and is_dragging:  # Arrastando
        dx, dy = x - last_mouse_pos[0], y - last_mouse_pos[1]
        pov[0] += dx * 0.1  # Ajuste a sensibilidade conforme necessário
        pov[1] -= dy * 0.1
        last_mouse_pos = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:  # Fim do arraste
        is_dragging = False

def main():
    global pov
    # Carregar o cubo
    obj = Object('./model/Mcube.obj')
    vertex, faces = obj.getVertex(), obj.getFaces()

    # Definir o plano de projeção
    plane = Plane(((0, 1, 0), (0, 0, 1), (1, 0, 0)), (-1, -1, -1))

    # Criar uma janela e configurar o callback do mouse
    cv2.namedWindow("Projeção")
    cv2.setMouseCallback("Projeção", mouse_callback)

    while True:
        # Criar projeção com o POV atualizado
        projection = Projection(obj, plane, tuple(pov))
        projected_vertices = projection.project()

        # Criar uma imagem para visualizar a projeção
        image = np.zeros((500, 500), dtype=np.uint8)

        # Desenhar a projeção na imagem
        draw_projection(image, projected_vertices, faces)

        # Mostrar a imagem
        cv2.imshow("Projeção", image)

        # Verificar se a tecla 'q' foi pressionada para sair
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
