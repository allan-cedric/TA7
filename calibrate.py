#!/usr/bin/env python3
import numpy as np
import cv2 as cv

# Para a leitura dos arquivos de imagem:
import glob


# Prepara a criteria:
# Define a precisao, numeros de iteracoes a serem feitos e outras informacoes
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepara os pontos de objeto, (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
# Nosso referencial vai ser os quadrados de um tabuleiro de xadrez, o grid 7x6:
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Listas dos pontos de objeto e pontos de imagem,
# conseguidos a partir das fotos tiradas:
objpoints = [] # (Ponto 3d no mundo real)
imgpoints = [] # (Ponto 2d na imagem)

# Abre os arquivos num iteravel:
images = glob.glob('pictures/*.png')

# Contagem das fotos salvas:
count = 1


# ENCONTRA OS PONTOS DE IMAGEM E DE OBJETO:
for fname in images:
    # Le a imagem
    img = cv.imread(fname)
    # Converte pra escala cinza
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Tenta encontrar os cantos do tabuleiro
    ret, corners = cv.findChessboardCorners(gray, (7,6), None)

    # Se achou:
    if ret == True:
        # Armazena os pontos de objeto e de imagem encontrados:
        objpoints.append(objp)
        imgpoints.append(corners)
        # Desenha os cantos e salva o resultado:
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        cv.drawChessboardCorners(img, (7,6), corners2, ret)
        cv.imwrite('results/result{}.png'.format(count), img)
        count += 1

# CALIBRA A CAMERA A PARTIR DOS VALORES ENCONTRADOS:
# OBTEM VALORES DE INTERESSE:
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print("Matriz da camera:\n{}".format(mtx))
print("Coeficiente de distorcao:\n{}".format(dist))
print("Vetores de rotacao:\n{}".format(rvecs))
print("Vetores de translacao:\n{}".format(tvecs))

# APLICANDO OS VALORES ENCONTRADOS:
# TIRANDO A DISTORCAO DA IMAGEM:

# Le uma imagem qualquer
img = cv.imread('pictures/chessboard1.png')
# Pega seus parametros
h, w = img.shape[:2]
# Atualiza e refina amatriz da camera pela imagem
newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 0, (w,h))

# Obtem a imagem desdistorcida
dst = cv.undistort(img, mtx, dist, None, newcameramtx)
# Corta a imagem apenas pela Region Of Interest
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
# Salva o resultado
cv.imwrite('results/calibresult.png', dst)

# Feedback: Obtem a precisao dos calculos que acabamos de fazer:
# (Quanto menor o erro total, melhor)

mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
    mean_error += error
print( "Erro total: {}".format(mean_error/len(objpoints)) )
cv.destroyAllWindows()