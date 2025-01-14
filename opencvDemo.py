import cv2
import numpy as np

# Criação de uma imagem em branco (500x500, 3 canais para RGB)
image = np.zeros((500, 500, 3), dtype=np.uint8)

# Desenhar uma linha
cv2.line(image, (50, 50), (450, 50), (0, 255, 0), 5)

# Desenhar um retângulo
cv2.rectangle(image, (50, 100), (200, 300), (255, 0, 0), -1)

# Desenhar um círculo
cv2.circle(image, (300, 200), 50, (0, 0, 255), -1)  # -1 preenche o círculo

# Desenhar um polígono
points = np.array([[250, 350], [300, 400], [350, 350], [300, 300]], np.int32)
points = points.reshape((-1, 1, 2))
cv2.polylines(image, [points], isClosed=True, color=(255, 255, 0), thickness=2)

# Desenhar um texto
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(image, 'OpenCV Drawing', (50, 400), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

# Mostrar a imagem
cv2.imshow("Drawing Example", image)

# Aguarde até que uma tecla seja pressionada e feche as janelas
cv2.waitKey(0)
cv2.destroyAllWindows()
