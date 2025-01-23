from object import Object, Plane, Projection, flip
import numpy as np
import cv2

def draw_projection(image, projected_viewport, faces, scale=10):
    # Calcular o centro da projeção

    for face in faces:
        for i in range(len(face)):
            start_idx = face[i]
            end_idx = face[(i + 1) % len(face)]

            start_point = (
                int(projected_viewport[0][start_idx] * scale),
                int(projected_viewport[1][start_idx] * scale),
            )
            end_point = (
                int(projected_viewport[0][end_idx] * scale),
                int(projected_viewport[1][end_idx] * scale),
            )

            cv2.line(image, start_point, end_point, (255, 255, 255), 1)

pov = [20, 10, 30]  # Ponto de vista inicial

# Carregar o cubo
obj = Object('./model/dante.obj')
vertex, faces = obj.getVertex(), obj.getFaces()

# Definir o plano de projeção
plane = Plane(((1,0,0),(0,0,0),(0,1,0)), (0,0,0))
print('\nNormal do plano:')
print(plane.normal)

# Criar uma janela e configurar o callback do mouse
cv2.namedWindow("Viewport")

# Criar projeção com o POV atualizado
projection = Projection(obj, plane, tuple(pov))
projected_vertices = projection.project()
projected_viewport = projection.toViewport((-7,9),(-5,7),(0,32),(0,24),(2,2))

print('\nViewport:')
print(projected_viewport)

# Criar uma imagem para visualizar a projeção
image = np.zeros((320, 320), dtype=np.uint8)

# Desenhar a projeção na imagem
draw_projection(image, flip(projected_viewport), faces)

# Mostrar a imagem
cv2.imshow("Viewport", image)

cv2.waitKey(0)
