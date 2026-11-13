# Sistema Inteligente de Monitoramento de Segurança Industrial utilizando Visão Computacional e YOLO11

## Sobre o projeto

Este projeto consiste no desenvolvimento de um sistema inteligente de monitoramento de segurança industrial utilizando técnicas de visão computacional e inteligência artificial.

A solução utiliza o modelo YOLO11 para identificar pessoas e detectar a ausência de Equipamentos de Proteção Individual (EPIs), contribuindo para a identificação de condições potencialmente inseguras em ambientes industriais.

O sistema foi desenvolvido como Trabalho de Conclusão de Curso (TCC) de Engenharia da Computação.

## Objetivo

Desenvolver um protótipo capaz de monitorar imagens capturadas por uma câmera, identificar situações de ausência de EPIs e registrar ocorrências para auxiliar no acompanhamento das condições de segurança.

## Funcionalidades

- Captura de imagens por câmera.
- Detecção de pessoas utilizando YOLO11.
- Identificação de ausência de capacete.
- Identificação de ausência de óculos de proteção.
- Delimitação de Região de Interesse (ROI).
- Confirmação temporal das condições detectadas.
- Geração de registros de ocorrências.
- Armazenamento de evidências.
- Dashboard para visualização e acompanhamento dos registros.

## Tecnologias utilizadas

- Python
- YOLO11
- Ultralytics
- OpenCV
- Streamlit
- SQLite
- Pandas
- Plotly

## Estrutura do projeto

```text
TCC_YOLO_EPI/
├── main.py
├── dashboard.py
├── testecamera.py
├── roi_config.json
├── requirements.txt
├── yolo11n.pt
├── modelo/
│   └── weights.pt
└── relatorios/
    └── gerar_relatorio.py
```

## Instalação e execução

### 1. Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
```

### 2. Acessar a pasta

```bash
cd tcc-monitoramento-inteligente-epi
```

### 3. Criar ambiente virtual

```bash
python -m venv venv
```

### 4. Ativar o ambiente virtual

Windows:

```bash
venv\Scripts\activate
```

### 5. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 6. Executar o sistema de monitoramento

```bash
python main.py
```

### 7. Acessar o dashboard

```bash
streamlit run dashboard.py
```

## Desenvolvimento acadêmico

Projeto desenvolvido no âmbito do curso de Engenharia da Computação, com foco na aplicação de sistemas inteligentes e inteligência artificial à segurança industrial.

## Status do projeto

Em desenvolvimento.

## Autoria

Trabalho de Conclusão de Curso – Engenharia da Computação.