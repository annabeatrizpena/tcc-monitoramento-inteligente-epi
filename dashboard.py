
import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path

# Configuracao da pagina
st.set_page_config(
    page_title="Monitoramento de EPI",
    page_icon="🦺",
    layout="wide"
)

# Caminhos do projeto
PASTA_PROJETO = Path(__file__).resolve().parent
CAMINHO_BANCO = PASTA_PROJETO / "banco" / "ocorrencias.db"



# Cabecalho do dashboard
st.markdown(
    """
<div style="background-color:#14263D; padding:30px; border-radius:12px; margin-bottom:20px;">
    <h1 style="color:white; margin:0; font-size:32px;">
        🦺 Sistema de Monitoramento de EPI
    </h1>
    <p style="color:#D6E2F0; margin-top:12px; margin-bottom:0; font-size:16px;">
        Monitoramento inteligente de segurança industrial utilizando visão computacional e YOLO11
    </p>
</div>
    """,
    unsafe_allow_html=True
)



st.divider()

# Consulta o banco de dados
def carregar_ocorrencias():
    with sqlite3.connect(CAMINHO_BANCO) as conexao:
        dados = pd.read_sql_query(
            """
            
SELECT
    id,
    data_hora,
    epi_ausente,
    caminho_imagem,
    percentual_capacete,
    percentual_oculos
FROM ocorrencias
ORDER BY id DESC

            """,
            conexao
        )
    return dados

# Botao para atualizar os registros
if st.button("🔄 Atualizar Ocorrências"):
    st.rerun()

dados = carregar_ocorrencias()


# Filtro por tipo de EPI
st.subheader("Filtros de Pesquisa")

if not dados.empty:
    tipos_epi = sorted({
        alerta.strip()
        for registro in dados["epi_ausente"]
        for alerta in registro.split(",")
    })

    epi_selecionado = st.selectbox(
        "Selecione o tipo de EPI:",
        ["Todos"] + tipos_epi
    )

    if epi_selecionado != "Todos":
        dados = dados[
            dados["epi_ausente"].apply(
                lambda registro: epi_selecionado in [
                    alerta.strip()
                    for alerta in registro.split(",")
                ]
            )
        ]


# Filtro por periodo
if not dados.empty:
    # Converte as datas do banco para o formato de data
    dados["data_convertida"] = pd.to_datetime(
        dados["data_hora"]
    ).dt.date

    data_minima = dados["data_convertida"].min()
    data_maxima = dados["data_convertida"].max()

    periodo = st.date_input(
        "Selecione o periodo:",
        value=(data_minima, data_maxima),
        min_value=data_minima,
        max_value=data_maxima,
        format="DD/MM/YYYY"
    )

    # Aplica o filtro quando duas datas forem selecionadas
    if isinstance(periodo, tuple) and len(periodo) == 2:
        data_inicial, data_final = periodo

        dados = dados[
            (dados["data_convertida"] >= data_inicial) &
            (dados["data_convertida"] <= data_final)
        ]


st.divider()


# Indicadores de seguranca
st.subheader("📊 Indicadores de Segurança")

# Calcula os indicadores
total_ocorrencias = len(dados)

tipos_alertas = set()

if not dados.empty:
    for registro in dados["epi_ausente"]:
        for alerta in registro.split(","):
            tipos_alertas.add(alerta.strip())

total_tipos = len(tipos_alertas)

# Cria dois cartoes de indicadores
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.metric(
            label="🚨 Total de Ocorrências",
            value=total_ocorrencias
        )

with col2:
    with st.container(border=True):
        st.metric(
            label="🦺 Tipos de EPIs Ausentes",
            value=total_tipos
        )


st.divider()

# Historico
st.subheader("Historico de Ocorrencias")

if dados.empty:
    st.info("Nenhuma ocorrencia registrada.")
else:
    
    # Prepara os dados para exibicao no historico
    tabela_historico = dados[
        [
            "id",
            "data_hora",
            "epi_ausente",
            "percentual_capacete",
            "percentual_oculos"
        ]
    ].copy()

    # Renomeia as colunas
    tabela_historico = tabela_historico.rename(columns={
        "id": "ID",
        "data_hora": "Data e Hora",
        "epi_ausente": "EPI Ausente",
        "percentual_capacete": "Capacete (%)",
        "percentual_oculos": "Oculos (%)"
    })

    st.dataframe(
        tabela_historico,
        use_container_width=True,
        hide_index=True
    )

# Grafico de ocorrencias por tipo de EPI
st.subheader("Ocorrências por Tipo de EPI")

if not dados.empty:
    lista_alertas = []

    for registro in dados["epi_ausente"]:
        for alerta in registro.split(","):
            lista_alertas.append(alerta.strip())

    contagem = pd.Series(lista_alertas).value_counts()

    st.bar_chart(contagem)

else:
    st.info("Ainda não existem dados para o gráfico.")


# ==========================================
# EVIDENCIAS FOTOGRAFICAS
# ==========================================

# Grafico de evolucao diaria das ocorrencias
st.divider()
st.subheader("📈 Evolução Diária das Ocorrências")

if not dados.empty:
    dados_grafico = dados.copy()

    # Converte a data e hora para apenas a data
    dados_grafico["dia"] = pd.to_datetime(
        dados_grafico["data_hora"]
    ).dt.date

    # Conta as ocorrencias registradas por dia
    ocorrencias_por_dia = (
        dados_grafico.groupby("dia")
        .size()
        .reset_index(name="Ocorrencias")
    )

    # Exibe o grafico de linhas
    st.line_chart(
        ocorrencias_por_dia,
        x="dia",
        y="Ocorrencias"
    )

else:
    st.info(
        "Não existem ocorrências para o período selecionado."
    )


st.subheader("📸 Evidências Fotográficas")

if dados.empty:
    st.info("Nenhuma evidência disponível.")

else:
    for _, ocorrencia in dados.iterrows():

        # Localiza a imagem registrada
        caminho = PASTA_PROJETO / ocorrencia["caminho_imagem"].replace("\\", "/")

        titulo = (
            f"🚨 Ocorrência #{ocorrencia['id']} "
            f"| {ocorrencia['data_hora']}"
        )

        # Cria um painel para cada ocorrencia
        with st.expander(titulo):

            col_imagem, col_dados = st.columns([2, 1])

            # Fotografia
            with col_imagem:

                if caminho.is_file():
                    st.image(
                        str(caminho),
                        caption="Imagem registrada pelo YOLO11",
                        width="stretch"
                    )

                else:
                    st.warning("Imagem não encontrada.")
                    st.write(f"Caminho: {caminho}")

            # Informacoes da ocorrencia
            with col_dados:

                st.markdown("#### Detalhes da ocorrência")

                st.write(f"**ID:** {ocorrencia['id']}")

                st.write(
                    f"**Data e hora:** {ocorrencia['data_hora']}"
                )

               
                st.write(
                    f"**EPI ausente:** {ocorrencia['epi_ausente']}"
                )

                # Percentuais registrados na ocorrencia
                percentual_capacete = ocorrencia["percentual_capacete"]
                percentual_oculos = ocorrencia["percentual_oculos"]

                if pd.notna(percentual_capacete):
                    st.write(
                        f"**Deteccoes de ausencia de capacete:** "
                        f"{percentual_capacete:.1f}%"
                    )
                else:
                    st.write(
                        "**Deteccoes de ausencia de capacete:** Nao registrado"
                    )

                if pd.notna(percentual_oculos):
                    st.write(
                        f"**Deteccoes de ausencia de oculos:** "
                        f"{percentual_oculos:.1f}%"
                    )
                else:
                    st.write(
                        "**Deteccoes de ausencia de oculos:** Nao registrado"
                    )

                st.warning("Condição insegura detectada")

