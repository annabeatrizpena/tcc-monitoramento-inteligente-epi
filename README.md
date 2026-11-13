# Sistema Inteligente de Monitoramento de Segurança Industrial utilizando Visão Computacional e YOLO11

**Intelligent Industrial Safety Monitoring System Using Computer Vision and YOLO11**

---

## 🇧🇷 Português

### Sobre o projeto

Este projeto consiste no desenvolvimento de um sistema inteligente de monitoramento de segurança industrial utilizando técnicas de visão computacional e o modelo YOLO11 para identificação automática de condições inseguras relacionadas ao uso de Equipamentos de Proteção Individual (EPIs).

O sistema utiliza imagens capturadas por uma câmera para identificar pessoas e verificar a ausência de equipamentos de proteção, especificamente capacetes e óculos de segurança. O protótipo também permite delimitar uma Região de Interesse (ROI), aplicar confirmação temporal das ocorrências, registrar evidências e armazenar os dados em um banco de dados SQLite.

O projeto foi desenvolvido como parte do Trabalho de Conclusão de Curso (TCC) de Engenharia da Computação.

### Funcionalidades

- Captura de imagens por câmera.
- Detecção de pessoas utilizando YOLO11.
- Identificação de ausência de capacete de segurança.
- Identificação de ausência de óculos de proteção.
- Delimitação de Região de Interesse (ROI).
- Confirmação temporal de condições inseguras.
- Geração de alertas visuais.
- Registro automático de ocorrências.
- Armazenamento de evidências em imagens.
- Banco de dados SQLite para histórico de ocorrências.
- Dashboard interativo para visualização e análise dos registros.

### Tecnologias utilizadas

- **Python:** linguagem principal de desenvolvimento.
- **YOLO11 (Ultralytics):** detecção de objetos e equipamentos de proteção.
- **OpenCV:** captura e processamento de imagens.
- **Streamlit:** desenvolvimento do painel de monitoramento.
- **SQLite:** armazenamento das ocorrências.
- **Pandas:** manipulação e organização dos dados.
- **Plotly:** geração de gráficos interativos.

### Estrutura do projeto

```text
TCC_YOLO_EPI/
│
├── main.py
├── dashboard.py
├── testecamera.py
├── requirements.txt
├── roi_config.json
├── yolo11n.pt
│
├── modelo/
│   └── weights.pt
│
├── relatorios/
│   └── gerar_relatorio.py
│
└── README.md
```

### Instalação e execução

**1. Clone o repositório:**

```bash
git clone https://github.com/annabeatrizpena/tcc-monitoramento-inteligente-epi.git
```

**2. Acesse a pasta do projeto:**

```bash
cd tcc-monitoramento-inteligente-epi
```

**3. Crie um ambiente virtual:**

```bash
python -m venv venv
```

**4. Ative o ambiente virtual (Windows):**

```powershell
.\venv\Scripts\Activate.ps1
```

**5. Instale as dependências:**

```bash
pip install -r requirements.txt
```

**6. Execute o sistema de monitoramento:**

```bash
python main.py
```

**7. Execute o dashboard:**

Em outro terminal, com o ambiente virtual ativado:

```bash
streamlit run dashboard.py
```

### Modelos de detecção

O projeto utiliza dois arquivos de pesos:

- `yolo11n.pt`: modelo YOLO11n utilizado como modelo base.
- `modelo/weights.pt`: pesos do modelo personalizado utilizado no projeto.

### Armazenamento de dados

As ocorrências identificadas são armazenadas localmente em um banco de dados SQLite. As imagens utilizadas como evidências também são armazenadas no ambiente de execução.

Esses arquivos locais não são disponibilizados no repositório público.

### Objetivo acadêmico

O objetivo deste trabalho é demonstrar a aplicação da visão computacional como ferramenta de apoio ao monitoramento de segurança industrial, contribuindo para a identificação de condições inseguras e para o registro de ocorrências relacionadas à ausência de EPIs.

**Autora:** Anna Beatriz Pena  
**Curso:** Engenharia da Computação  
**Projeto:** Trabalho de Conclusão de Curso (TCC)

---

## 🇺🇸 English

### About the Project

This project consists of developing an intelligent industrial safety monitoring system using computer vision techniques and the YOLO11 model to automatically identify unsafe conditions related to the use of Personal Protective Equipment (PPE).

The system processes images captured by a camera to detect people and identify missing protective equipment, specifically safety helmets and protective goggles. The prototype also allows the definition of a Region of Interest (ROI), temporal confirmation of detected events, evidence capture, and data storage in an SQLite database.

The project was developed as part of a Bachelor's Degree in Computer Engineering Final Year Project.

### Features

- Camera image capture.
- Person detection using YOLO11.
- Safety helmet absence detection.
- Protective goggles absence detection.
- Region of Interest (ROI) configuration.
- Temporal confirmation of unsafe conditions.
- Visual alerts.
- Automatic incident logging.
- Evidence image capture and storage.
- SQLite database for incident history.
- Interactive dashboard for monitoring and data visualization.

### Technologies Used

- **Python:** main programming language.
- **YOLO11 (Ultralytics):** object and PPE detection.
- **OpenCV:** image capture and processing.
- **Streamlit:** interactive monitoring dashboard.
- **SQLite:** incident data storage.
- **Pandas:** data manipulation and organization.
- **Plotly:** interactive data visualization.

### Project Structure

The project is organized into Python scripts, model weights, configuration files, and reporting utilities.

### Installation and Execution

**1. Clone the repository:**

```bash
git clone https://github.com/annabeatrizpena/tcc-monitoramento-inteligente-epi.git
```

**2. Navigate to the project directory:**

```bash
cd tcc-monitoramento-inteligente-epi
```

**3. Create a virtual environment:**

```bash
python -m venv venv
```

**4. Activate the virtual environment (Windows):**

```powershell
.\venv\Scripts\Activate.ps1
```

**5. Install dependencies:**

```bash
pip install -r requirements.txt
```

**6. Run the monitoring system:**

```bash
python main.py
```

**7. Run the dashboard:**

In another terminal, with the virtual environment activated:

```bash
streamlit run dashboard.py
```

### Detection Models

The project uses two model weight files:

- `yolo11n.pt`: YOLO11n base model.
- `modelo/weights.pt`: custom model weights used in the project.

### Data Storage

Detected incidents are stored locally in an SQLite database. Evidence images are also saved in the local execution environment.

These local files are not included in the public repository.

### Academic Purpose

The purpose of this project is to demonstrate the application of computer vision as a supporting tool for industrial safety monitoring, helping identify unsafe conditions and record incidents related to missing Personal Protective Equipment.

**Author:** Anna Beatriz Pena  
**Degree Program:** Computer Engineering  
**Project:** Final Year Project

---

**Repository:** https://github.com/annabeatrizpena/tcc-monitoramento-inteligente-epi
