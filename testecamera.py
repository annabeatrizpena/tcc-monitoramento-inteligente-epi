import cv2

camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)

if not camera.isOpened():
    print("ERRO: câmera não abriu.")
    exit()

print("Câmera aberta com sucesso.")

while True:
    ret, frame = camera.read()

    if not ret:
        print("ERRO: não foi possível capturar a imagem.")
        break

    cv2.imshow("Teste da Webcam", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()