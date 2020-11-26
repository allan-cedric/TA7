#!/usr/bin/env python3
import cv2

# Conecta com a webcam:
capture = cv2.VideoCapture(0)

# Retorno da leitura da camera:
success = True

# Contagem de fotos tiradas
count = 1

while success:
    # Le a imagem da camera
    success, image = capture.read()
    
    if success:
        # Mostra a imagem
        cv2.imshow("Window", image)
        # Recebe o input dado
        key=cv2.waitKey(5) & 0xFF

        if chr(key) == 's':
            # Salva a imagem
            cv2.imwrite("pictures/chessboard{}.png".format(count), image)
            count += 1