from object import Object, Plane, Projection
import numpy as np
import cv2

pov = [20, 10, 30]  # Ponto de vista inicial

# Carregar o cubo
obj = Object('./model/dante.obj')
vertex, faces = obj.getVertex(), obj.getFaces()

# Definir o plano de projeção
plane = Plane(((1,0,0),(0,0,0),(0,1,0)), (0,0,0))
print('\nNormal do plano:')
print(plane.normal)

# Criar uma janela e configurar o callback do mouse
cv2.namedWindow("Projeção")

# Criar projeção com o POV atualizado
projection = Projection(obj, plane, tuple(pov))
projected_vertices = projection.project()
projected_viewport = projection.toViewport((-7,9),(-5,7),(0,32),(0,24),(2,2))

print('\nViewport:')
print(projected_viewport)

# Criar uma imagem para visualizar a projeção
image = np.zeros((500, 500), dtype=np.uint8)

# Desenhar a projeção na imagem
# draw_projection(image, projected_vertices, faces)

# Mostrar a imagem
cv2.imshow("Projeção", image)
