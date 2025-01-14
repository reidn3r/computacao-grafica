import numpy as np
import cv2

# Função para calcular o vetor normal ao plano
def calcular_vetor_normal(p1, p2, p3):
    vetor1 = np.array(p2) - np.array(p1)
    vetor2 = np.array(p3) - np.array(p2)
    normal = np.cross(vetor1, vetor2)
    return normal / np.linalg.norm(normal)

# Função para calcular a matriz de projeção perspectiva
def matriz_projecao(c, n, d):
    a, b, c_ = c
    d0 = np.dot(c, n)
    matriz = np.array([
        [d + a * n[0], a * n[1], a * n[2], -a * d0],
        [b * n[0], d + b * n[1], b * n[2], -b * d0],
        [c_ * n[0], c_ * n[1], d + c_ * n[2], -c_ * d0],
        [n[0], n[1], n[2], d0]
    ])
    return matriz

# Função para projetar os pontos
def projetar_pontos(pontos, matriz):
    pontos_h = np.hstack((pontos, np.ones((pontos.shape[0], 1))))
    pontos_proj = np.dot(pontos_h, matriz.T)
    pontos_proj /= pontos_proj[:, -1].reshape(-1, 1)  # Coordenadas homogêneas para cartesianas
    return pontos_proj[:, :2]  # Apenas coordenadas 2D

# Configuração inicial
ponto_vista = [10, 10, 10]
p1, p2, p3 = [0, 0, 0], [1, 0, 0], [0, 1, 0]
vertices = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 1]])
superficies = [[0, 1, 2], [1, 2, 3]]

# Cálculo
vetor_normal = calcular_vetor_normal(p1, p2, p3)
matriz_persp = matriz_projecao(ponto_vista, vetor_normal, 1)
pontos_proj = projetar_pontos(vertices, matriz_persp)

# Desenho do objeto projetado
altura, largura = 500, 500
imagem = np.zeros((altura, largura, 3), dtype=np.uint8)
for face in superficies:
    pts = np.array([pontos_proj[i] * [largura / 2, altura / 2] + [largura / 2, altura / 2] for i in face], np.int32)
    cv2.polylines(imagem, [pts], isClosed=True, color=(255, 255, 255), thickness=2)

cv2.imshow("Projecao Perspectiva", imagem)
cv2.waitKey(0)
cv2.destroyAllWindows()
