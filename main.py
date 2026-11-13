
from ultralytics import YOLO
import cv2
import os
import time
from datetime import datetime
from banco.database import criar_banco, registrar_ocorrencia
import json
from pathlib import Path
from collections import deque

# Inicializa o banco de dados
criar_banco()

# Carrega o modelo treinado
model = YOLO("modelo/weights.pt")

# Abre a webcam
camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)



# Arquivo onde a ROI sera armazenada
arquivo_roi = Path(__file__).resolve().parent / "roi_config.json"

# Captura uma imagem inicial da camera
sucesso, frame_inicial = camera.read()

if not sucesso:
    camera.release()
    raise RuntimeError("Nao foi possivel capturar a imagem inicial.")

altura_frame, largura_frame = frame_inicial.shape[:2]

# Verifica se ja existe uma ROI salva
usar_roi_salva = False

if arquivo_roi.exists():
    with open(arquivo_roi, "r", encoding="utf-8") as arquivo:
        dados_roi = json.load(arquivo)

    if (
        dados_roi.get("largura_frame") == largura_frame
        and dados_roi.get("altura_frame") == altura_frame
    ):
        usar_roi_salva = True
        print("ROI salva encontrada!")
    else:
        print("Resolucao diferente. Selecione uma nova ROI.")

if usar_roi_salva:
    print("Pressione R para redefinir a ROI ou outra tecla para continuar.")

    imagem_previa = frame_inicial.copy()

    cv2.rectangle(
        imagem_previa,
        (dados_roi["x1"], dados_roi["y1"]),
        (dados_roi["x2"], dados_roi["y2"]),
        (0, 255, 0),
        2
    )

    cv2.imshow("Configuracao da ROI", imagem_previa)
    tecla = cv2.waitKey(0) & 0xFF
    cv2.destroyWindow("Configuracao da ROI")

    usar_roi_salva = tecla != ord("r")

if usar_roi_salva:
    x1_roi = dados_roi["x1"]
    y1_roi = dados_roi["y1"]
    x2_roi = dados_roi["x2"]
    y2_roi = dados_roi["y2"]

else:
    # Permite selecionar uma nova ROI
    selecao = cv2.selectROI(
        "Selecione a area monitorada",
        frame_inicial,
        fromCenter=False,
        showCrosshair=True
    )

    cv2.destroyWindow("Selecione a area monitorada")

    x_roi, y_roi, largura_roi, altura_roi = map(int, selecao)

    if largura_roi == 0 or altura_roi == 0:
        camera.release()
        raise RuntimeError("Nenhuma area foi selecionada.")

    x1_roi = x_roi
    y1_roi = y_roi
    x2_roi = x_roi + largura_roi
    y2_roi = y_roi + altura_roi

    # Salva a configuracao
    dados_roi = {
        "x1": x1_roi,
        "y1": y1_roi,
        "x2": x2_roi,
        "y2": y2_roi,
        "largura_frame": largura_frame,
        "altura_frame": altura_frame
    }

    with open(arquivo_roi, "w", encoding="utf-8") as arquivo:
        json.dump(dados_roi, arquivo, indent=4)

    print("Nova ROI salva com sucesso!")


if not camera.isOpened():
    print("ERRO: nao foi possivel abrir a webcam.")
    raise SystemExit

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Sistema de monitoramento de EPI iniciado!")
print("Pressione Q para encerrar.")


# Pasta onde as evidencias serao armazenadas
pasta_evidencias = "evidencias"
os.makedirs(pasta_evidencias, exist_ok=True)

# Intervalo minimo entre registros (segundos)
intervalo_registro = 45

# Controle do ultimo registro
ultimo_registro = 0

# Tempo minimo para confirmar a ausencia de EPI
tempo_confirmacao = 3

tolerancia_deteccao = 0.5

ultima_deteccao = {
    "CAPACETE AUSENTE": None,
    "OCULOS AUSENTES": None
}

# Percentual minimo de deteccoes para confirmar ausencia
percentual_minimo_deteccoes = 0.70

# Historico recente de deteccoes de cada EPI
historico_deteccoes = {
    "CAPACETE AUSENTE": deque(),
    "OCULOS AUSENTES": deque()
}

# Temporizador independente para cada EPI
inicio_ausencia = {
    "CAPACETE AUSENTE": None,
    "OCULOS AUSENTES": None
}

try:
    while True:
        ret, frame = camera.read()

        if not ret:
            print("ERRO: nao foi possivel capturar a imagem.")
            break

        # Executa a deteccao de EPI
        results = model.predict(
            source=frame,
            imgsz=640,
            conf=0.50,
            verbose=False
        )

        # Desenha as caixas de deteccao
        frame_detectado = frame.copy()

        # Desenha a area monitorada
        cv2.rectangle(
            frame_detectado,
            (x1_roi, y1_roi),
            (x2_roi, y2_roi),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame_detectado,
            "AREA MONITORADA",
            (x1_roi, max(y1_roi - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 0),
            2
        )

       
        
        
        # Identifica pessoas e ausencias de EPI
        pessoas = []
        epis_ausentes = []

        for box in results[0].boxes:
            classe_id = int(box.cls[0])
            classe_nome = model.names[classe_id]

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            if classe_nome.lower() == "person":
                pessoas.append((x1, y1, x2, y2))

            elif classe_nome == "no_helmet":
                epis_ausentes.append(
                    ("CAPACETE AUSENTE", x1, y1, x2, y2)
                )

            elif classe_nome == "no_goggle":
                epis_ausentes.append(
                    ("OCULOS AUSENTES", x1, y1, x2, y2)
                )

     
        # Seleciona pessoas com pelo menos 30% da caixa na ROI
        pessoas_monitoradas = []

        percentual_minimo = 0.30

        for px1, py1, px2, py2 in pessoas:

            # Calcula a area total da caixa da pessoa
            largura_pessoa = max(0, px2 - px1)
            altura_pessoa = max(0, py2 - py1)
            area_pessoa = largura_pessoa * altura_pessoa

            if area_pessoa == 0:
                continue

            # Calcula a intersecao com a ROI
            inter_x1 = max(px1, x1_roi)
            inter_y1 = max(py1, y1_roi)
            inter_x2 = min(px2, x2_roi)
            inter_y2 = min(py2, y2_roi)

            largura_inter = max(0, inter_x2 - inter_x1)
            altura_inter = max(0, inter_y2 - inter_y1)

            area_intersecao = largura_inter * altura_inter

            # Percentual da pessoa dentro da ROI
            percentual_sobreposicao = (
                area_intersecao / area_pessoa
            )

            
            # Define a identificacao visual da pessoa
            
            if percentual_sobreposicao >= percentual_minimo:
                pessoas_monitoradas.append(
                    (px1, py1, px2, py2)
                )

                cor_pessoa = (0, 255, 0)
                texto_pessoa = "PESSOA MONITORADA"
            else:
                cor_pessoa = (0, 165, 255)
                texto_pessoa = "FORA DA ROI"

            # Desenha a caixa de identificacao
            cv2.rectangle(
                frame_detectado,
                (px1, py1),
                (px2, py2),
                cor_pessoa,
                3
            )

            # Define a posicao do texto
            posicao_texto_y = max(py1 - 10, 20)

            # Exibe o status da pessoa
            cv2.putText(
                frame_detectado,
                texto_pessoa,
                (px1, posicao_texto_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                cor_pessoa,
                2
            )

        # Associa cada ausencia a uma pessoa monitorada
        alertas_detectados = set()

        for epi, ex1, ey1, ex2, ey2 in epis_ausentes:
            centro_epi_x = (ex1 + ex2) // 2
            centro_epi_y = (ey1 + ey2) // 2

            for px1, py1, px2, py2 in pessoas_monitoradas:

                # Verifica se o centro da deteccao do EPI
                # esta dentro da caixa da pessoa
                pertence_pessoa = (
                    px1 <= centro_epi_x <= px2
                    and py1 <= centro_epi_y <= py2
                )

                if pertence_pessoa:
                    alertas_detectados.add(epi)
                    
                    # Define a cor da deteccao de EPI ausente
                    cor_epi = (0, 0, 255)

                    # Desenha a caixa do EPI ausente
                    cv2.rectangle(
                        frame_detectado,
                        (ex1, ey1),
                        (ex2, ey2),
                        cor_epi,
                        2
                    )

                    # Exibe o nome do EPI ausente
                    cv2.putText(
                        frame_detectado,
                        epi,
                        (ex1, max(ey1 - 8, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.50,
                        cor_epi,
                        2
                    )
                    break

        percentuais_epi = {}
       
        # Atualiza os temporizadores e o historico
        tempo_atual = time.monotonic()
        alertas = []

        for epi in inicio_ausencia:
            detectado = epi in alertas_detectados

            # Guarda o resultado do frame atual
            historico_deteccoes[epi].append(
                (tempo_atual, detectado)
            )

            # Mantem somente os ultimos 3 segundos
            while (
                historico_deteccoes[epi]
                and tempo_atual - historico_deteccoes[epi][0][0]
                > tempo_confirmacao
            ):
                historico_deteccoes[epi].popleft()

            # Atualiza a ultima deteccao
            if detectado:
                ultima_deteccao[epi] = tempo_atual

                if inicio_ausencia[epi] is None:
                    inicio_ausencia[epi] = tempo_atual

            elif ultima_deteccao[epi] is not None:
                tempo_sem_deteccao = (
                    tempo_atual - ultima_deteccao[epi]
                )

                if tempo_sem_deteccao > tolerancia_deteccao:
                    inicio_ausencia[epi] = None
                    ultima_deteccao[epi] = None
                    historico_deteccoes[epi].clear()

            # Calcula o percentual de frames positivos
            total_frames = len(historico_deteccoes[epi])

            if total_frames > 0:
                frames_positivos = sum(
                    1 for _, presente in historico_deteccoes[epi]
                    if presente
                )
                percentual = frames_positivos / total_frames
            else:
                percentual = 0
            percentuais_epi[epi] = percentual

            # Confirma somente apos 3 segundos
            # e com pelo menos 70% de deteccoes
            if (
                inicio_ausencia[epi] is not None
                and ultima_deteccao[epi] is not None
                and tempo_atual - inicio_ausencia[epi] >= tempo_confirmacao
                and tempo_atual - ultima_deteccao[epi] <= tolerancia_deteccao
                and percentual >= percentual_minimo_deteccoes
            ):
                alertas.append(epi)

        ausencia_confirmada = len(alertas) > 0




        # Exibe o alerta somente apos a confirmacao
        if ausencia_confirmada:

           
            # Ajusta a altura da faixa conforme os alertas
            altura_faixa = 65 + (len(alertas) * 30)

            # Desenha a faixa vermelha
            cv2.rectangle(
                frame_detectado,
                (0, 0),
                (frame_detectado.shape[1], altura_faixa),
                (0, 0, 200),
                -1
            )

            # Titulo principal
            cv2.putText(
                frame_detectado,
                "ALERTA: EPI AUSENTE!",
                (15, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                (255, 255, 255),
                2
            )

            # Exibe cada EPI ausente
            for indice, epi in enumerate(alertas):
                cv2.putText(
                    frame_detectado,
                    epi,
                    (15, 70 + indice * 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (255, 255, 255),
                    2
                )


            # Verifica se ja passou o intervalo entre registros
            tempo_atual = time.time()

            if tempo_atual - ultimo_registro >= intervalo_registro:

                # Gera data e hora da ocorrencia
                data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

                # Define o nome do arquivo
                nome_arquivo = f"alerta_{data_hora}.jpg"

                # Caminho completo da imagem
                caminho = os.path.join(pasta_evidencias, nome_arquivo)

                # Salva a imagem com as deteccoes e o alerta
                salvo = cv2.imwrite(caminho, frame_detectado)

                
                if salvo:
                    print(f"Evidencia salva: {caminho}")

                    # Registra os EPIs ausentes no banco
                    
                    registrar_ocorrencia(
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        ", ".join(sorted(set(alertas))),
                        caminho,
                        round(percentuais_epi["CAPACETE AUSENTE"] * 100, 2),
                        round(percentuais_epi["OCULOS AUSENTES"] * 100, 2)
                    )


                    ultimo_registro = tempo_atual

                else:
                    print("ERRO: nao foi possivel salvar a evidencia.")



        # Exibe os percentuais de deteccao na webcam
        altura_frame, largura_frame = frame_detectado.shape[:2]

        indicadores = [
            ("CAPACETE", percentuais_epi["CAPACETE AUSENTE"]),
            ("OCULOS", percentuais_epi["OCULOS AUSENTES"])
        ]

        for indice, (nome_epi, percentual) in enumerate(indicadores):
            texto = f"{nome_epi}: {percentual * 100:.0f}%"

            posicao_y = altura_frame - 48 + indice * 24

            # Fundo escuro para facilitar a leitura
            cv2.rectangle(
                frame_detectado,
                (5, posicao_y - 18),
                (205, posicao_y + 5),
                (30, 30, 30),
                -1
            )

            cv2.putText(
                frame_detectado,
                texto,
                (12, posicao_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                2
            )

        # Mostra a webcam
        cv2.imshow(
            "TCC - Monitoramento de EPI",
            frame_detectado
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    camera.release()
    cv2.destroyAllWindows()
    print("Sistema encerrado.")
