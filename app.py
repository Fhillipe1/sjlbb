# app.py

# Importa as bibliotecas necessárias
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime # Para lidar com objetos de tempo

# --- 1. Configurações da Página Streamlit ---
# Define o título da página, o ícone e o layout.
# O layout 'wide' utiliza toda a largura disponível da tela, o que é ótimo para dashboards.
st.set_page_config(
    page_title="Dashboard La Brasa Burger - Faturamento Madrugada",
    page_icon="https://site.labrasaburger.com.br/wp-content/uploads/2021/09/logo.png",  # Ícone personalizado
    layout="wide"
)

# --- 2. CSS Customizado para Estilo e Cards ---
# Injeta CSS diretamente na aplicação Streamlit.
# O 'unsafe_allow_html=True' é necessário para permitir a renderização de HTML/CSS.
st.markdown("""
<style>
/* --- Estilo Global --- */
.stApp {
    background: linear-gradient(135deg, #181A23 0%, #23263A 100%);
    color: #FAFAFA;
    font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
    letter-spacing: 0.01em;
}

/* --- Scrollbar customizada --- */
::-webkit-scrollbar {
    width: 10px;
    background: #23263A;
}
::-webkit-scrollbar-thumb {
    background: #FF4B4B;
    border-radius: 8px;
}

/* --- Título Principal --- */
.main-title {
    font-size: 4em;
    font-weight: 900;
    text-align: center;
    color: #FFF;
    text-shadow: 0 6px 32px #FF4B4B44, 0 2px 8px #000A;
    margin-bottom: 0.2em;
    padding-top: 0.5em;
    letter-spacing: 0.03em;
    background: linear-gradient(90deg, #FF4B4B 10%, #FFB347 90%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* --- Subtítulo --- */
.subtitle {
    font-size: 2em;
    text-align: center;
    color: #FFB347;
    margin-top: -0.2em;
    margin-bottom: 1.5em;
    font-weight: 700;
    letter-spacing: 0.02em;
    text-shadow: 0 2px 8px #0006;
}

/* --- Cards de Métricas (KPIs) --- */
div[data-testid="stMetric"] {
    background: linear-gradient(120deg, #23263A 60%, #181A23 100%);
    border-radius: 18px;
    padding: 32px 18px 28px 18px;
    margin-bottom: 28px;
    box-shadow: 0 8px 32px 0 #FF4B4B22, 0 2px 8px #000A;
    border: 1.5px solid #FF4B4B33;
    text-align: center;
    min-height: 140px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    transition: box-shadow 0.2s;
}
div[data-testid="stMetric"]:hover {
    box-shadow: 0 12px 40px 0 #FFB34733, 0 4px 16px #000A;
    border-color: #FFB34799;
}

/* Label do Card */
div[data-testid="stMetricLabel"] > div {
    font-size: 1.25em;
    color: #FFB347;
    font-weight: 600;
    margin-bottom: 10px;
    letter-spacing: 0.01em;
    text-shadow: 0 1px 4px #0004;
}

/* Valor do Card */
div[data-testid="stMetricValue"] {
    font-size: 3.2em;
    font-weight: 900;
    color: #FF4B4B;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    text-shadow: 0 2px 12px #FF4B4B33, 0 1px 4px #0008;
    letter-spacing: 0.01em;
}

/* --- Cards de Gráficos --- */
.card-plotly {
    background: linear-gradient(120deg, #23263A 60%, #181A23 100%);
    border-radius: 18px;
    padding: 28px 18px 18px 18px;
    margin-bottom: 28px;
    box-shadow: 0 8px 32px 0 #FF4B4B22, 0 2px 8px #000A;
    border: 1.5px solid #FF4B4B33;
    transition: box-shadow 0.2s;
    min-height: 420px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: stretch;
}
.card-plotly:hover {
    box-shadow: 0 12px 40px 0 #FFB34733, 0 4px 16px #000A;
    border-color: #FFB34799;
}
.card-plotly h5, .card-plotly h4, .card-plotly h3, .card-plotly h2, .card-plotly h1 {
    color: #FFB347;
    margin-bottom: 0.7em;
    margin-top: 0;
    font-weight: 700;
    letter-spacing: 0.01em;
    text-shadow: 0 1px 4px #0004;
}
.card-plotly .stPlotlyChart {
    background: transparent !important;
    border-radius: 12px;
    box-shadow: none;
    border: none;
    padding: 0;
    margin: 0;
}

/* --- Gráficos Plotly (fallback para fora do card) --- */
.stPlotlyChart {
    background: linear-gradient(120deg, #23263A 60%, #181A23 100%);
    border-radius: 16px;
    padding: 22px 10px 18px 10px;
    box-shadow: 0 8px 32px 0 #FF4B4B22, 0 2px 8px #000A;
    margin-bottom: 28px;
    border: 1.5px solid #FF4B4B33;
    transition: box-shadow 0.2s;
}
.stPlotlyChart:hover {
    box-shadow: 0 12px 40px 0 #FFB34733, 0 4px 16px #000A;
    border-color: #FFB34799;
}

/* --- Sidebar (Filtros) --- */
.st-emotion-cache-1pxazr7 {
    background: linear-gradient(135deg, #181A23 0%, #23263A 100%);
    border-right: 2px solid #FF4B4B33;
}
.st-emotion-cache-1pxazr7 div.stSelectbox,
.st-emotion-cache-1pxazr7 div.stMultiSelect,
.st-emotion-cache-1pxazr7 div.stDateInput,
.st-emotion-cache-1pxazr7 div.stTextInput {
    background: #23263A;
    border-radius: 10px;
    padding: 10px;
    border: 1.5px solid #FFB34755;
    color: #FAFAFA;
    font-weight: 500;
    margin-bottom: 10px;
}
.st-emotion-cache-1pxazr7 h1, .st-emotion-cache-1pxazr7 h2, .st-emotion-cache-1pxazr7 h3,
.st-emotion-cache-1pxazr7 h4, .st-emotion-cache-1pxazr7 h5, .st-emotion-cache-1pxazr7 h6,
.st-emotion-cache-1pxazr7 p, .st-emotion-cache-1pxazr7 label {
    color: #FFB347 !important;
    font-weight: 600;
    letter-spacing: 0.01em;
}

/* --- Botões --- */
.stButton>button {
    background: linear-gradient(90deg, #FF4B4B 60%, #FFB347 100%);
    color: #FFF;
    border-radius: 10px;
    border: none;
    padding: 12px 28px;
    font-weight: bold;
    font-size: 1.1em;
    box-shadow: 0 2px 8px #FF4B4B33;
    transition: background 0.2s, box-shadow 0.2s;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #FFB347 60%, #FF4B4B 100%);
    box-shadow: 0 4px 16px #FFB34733;
}

/* --- Tabela de Dados --- */
.stDataFrame {
    background: #23263A;
    border-radius: 14px;
    border: 1.5px solid #FFB34755;
    box-shadow: 0 4px 16px #FFB34722;
    font-size: 1.08em;
}
.stDataFrame th {
    background: #FF4B4B;
    color: #FFF;
    font-weight: 700;
    border-radius: 8px 8px 0 0;
    letter-spacing: 0.01em;
}
.stDataFrame td {
    background: #23263A;
    color: #FAFAFA;
    border-radius: 0 0 8px 8px;
}

/* --- Tooltip customizado para hover em cards e gráficos --- */
div[data-testid="stMetric"]:hover,
.card-plotly:hover,
.stPlotlyChart:hover {
    cursor: pointer;
}

/* --- Pequenos detalhes para inputs e seleção --- */
input, select, textarea {
    background: #23263A !important;
    color: #FAFAFA !important;
    border-radius: 8px !important;
    border: 1.5px solid #FFB34755 !important;
    font-size: 1em !important;
    font-weight: 500 !important;
}

/* --- Remove outline azul padrão dos inputs ao focar --- */
input:focus, select:focus, textarea:focus {
    outline: 2px solid #FFB347 !important;
    border-color: #FFB347 !important;
}

/* --- Ajuste para links --- */
a {
    color: #FFB347;
    text-decoration: underline;
}
a:hover {
    color: #FF4B4B;
    text-decoration: none;
}
</style>
""", unsafe_allow_html=True)


# --- 3. Carregamento e Tratamento dos Dados ---

# O 'st.cache_data' armazena em cache os resultados da função,
# o que acelera a aplicação se os dados não mudarem.
@st.cache_data
def load_data():
    # Carrega a planilha Excel. O engine 'openpyxl' é necessário para arquivos .xlsx.
    df = pd.read_excel("data/Vendas por período.xlsx", engine='openpyxl')

    # Lista de colunas a serem removidas conforme sua solicitação
    columns_to_drop = [
        "Pedido", "Código da loja", "Nome da loja", "Tipo do pedido", "Turno",
        "Canal de venda", "Número do pedido no parceiro", "Consumidor",
        "Tem cupom", "Esta cancelado", "Itens", "Entrega", "Entregador",
        "Bairro", "CEP", "Acréscimo", "Motivo de acréscimo", "Desconto",
        "Motivo do desconto"
    ]
    df = df.drop(columns=columns_to_drop)

    # Converte a coluna 'Data da venda' para o tipo datetime, lidando com possíveis erros
    df['Data da venda'] = pd.to_datetime(df['Data da venda'], errors='coerce')

    # Remove linhas onde 'Data da venda' se tornou NaT (Not a Time) após a conversão
    df.dropna(subset=['Data da venda'], inplace=True)

    # Cria as colunas 'Data' e 'Hora' a partir de 'Data da venda'
    df['Data'] = df['Data da venda'].dt.date
    df['Hora'] = df['Data da venda'].dt.time

    # Filtra os dados para manter apenas os horários entre 00:00 e 05:00
    start_time = datetime.time(0, 0, 0)
    end_time = datetime.time(5, 0, 0)
    df = df[ (df['Hora'] >= start_time) & (df['Hora'] <= end_time) ]

    # Garante que 'Total' seja numérico
    df['Total'] = pd.to_numeric(df['Total'], errors='coerce')
    # Remove linhas com valores nulos no 'Total' após a conversão
    df.dropna(subset=['Total'], inplace=True)

    return df

# Carrega os dados tratados
df = load_data()

# --- 4. Sidebar para Filtros ---
with st.sidebar:
    st.markdown(
        """
        <div style='text-align:center; margin-bottom: 1.5em;'>
            <img src='https://site.labrasaburger.com.br/wp-content/uploads/2021/09/logo.png' style='width:90px; margin-bottom:0.5em;' />
            <h2 style='color:#FF4B4B; margin-bottom:0.2em;'>Filtros</h2>
            <p style='color:#BBBBBB; font-size:1.1em;'>Personalize sua análise</p>
        </div>
        """, unsafe_allow_html=True
    )

# Filtro de Data
# Pega a data mínima e máxima disponível nos dados
min_date = df['Data'].min()
max_date = df['Data'].max()

# Permite ao usuário selecionar um intervalo de datas
date_range = st.sidebar.date_input(
    "Selecione o Período",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Garante que date_range tenha dois elementos (início e fim)
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    # Se apenas uma data for selecionada, defina o fim como a mesma data
    start_date = date_range[0]
    end_date = date_range[0]

# Filtra o DataFrame com base nas datas selecionadas
df_filtered = df[(df['Data'] >= start_date) & (df['Data'] <= end_date)]

# Adiciona um filtro para o método de pagamento
st.sidebar.subheader("Filtrar por Método de Pagamento")
payment_methods = df_filtered['Pagamento'].unique().tolist()
selected_payment_methods = st.sidebar.multiselect(
    "Selecione as Formas de Pagamento",
    options=payment_methods,
    default=payment_methods
)

# Aplica o filtro de método de pagamento
df_filtered = df_filtered[df_filtered['Pagamento'].isin(selected_payment_methods)]

# --- 5. Título Principal do Dashboard ---
# Título principal estilizado com logo e destaque visual
st.markdown(f"""
<div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 1.5em;">
    <img src="https://site.labrasaburger.com.br/wp-content/uploads/2021/09/logo.png" style="width:110px; margin-bottom: 0.2em; border-radius: 18px; box-shadow: 0 4px 24px #FF4B4B33, 0 1px 8px #000A;" />
    <h1 class="main-title" style="margin-bottom: 0.1em; font-size: 3.5em;">
        Dashboard Faturamento Madrugada
    </h1>
    <h2 class="subtitle" style="margin-top: -0.3em; color:#FFB347;">
        La Brasa Burger <span style="color:#BBBBBB;">Aracaju</span>
    </h2>
    <p style="font-size:1.18em; color:#BBBBBB; margin-top:0.3em;">
        <span style="background:rgba(255,75,75,0.10); border-radius:10px; padding:0.5em 1.3em; box-shadow:0 2px 8px #FFB34722;">
            Análise detalhada do desempenho de vendas <b style="color:#FF4B4B;">00:00 - 05:00</b>
        </span>
    </p>
</div>
""", unsafe_allow_html=True)

# --- 6. Métricas Chave (Key Performance Indicators - KPIs) ---
# Inicializa as variáveis para evitar erro de referência se o DataFrame filtrado estiver vazio
total_revenue = 0.0
total_orders = 0

if df_filtered.empty:
    st.warning("Nenhum dado encontrado para os filtros selecionados. Tente ajustar os filtros.")
else:
    # Calcula o faturamento total e o número de pedidos SOMENTE SE houver dados
    total_revenue = df_filtered['Total'].sum()
    total_orders = df_filtered.shape[0] # Número de linhas = número de pedidos

# Exibe as métricas em colunas para um layout organizado
# Estão fora do 'else' para garantir que os cards sempre apareçam, mesmo com valores zero
col1, col2 = st.columns(2)

with col1:
    # st.metric será automaticamente estilizado pelo CSS div[data-testid="stMetric"]
    st.metric(label="Faturamento Total (Madrugada)", value=f"R$ {total_revenue:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
with col2:
    # st.metric será automaticamente estilizado pelo CSS div[data-testid="stMetric"]
    st.metric(label="Total de Pedidos (Madrugada)", value=f"{total_orders:,}".replace(",", "."))

# --- 7. Gráficos ---
# Os gráficos só serão renderizados se houver dados, então permanecem dentro do 'else'
if not df_filtered.empty: # Condição para garantir que os gráficos só apareçam com dados
    st.subheader("Visualizações do Faturamento")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("##### Faturamento Diário no Período da Madrugada")
        daily_revenue = df_filtered.groupby('Data')['Total'].sum().reset_index()
        fig_line = px.line(
            daily_revenue,
            x='Data',
            y='Total',
            title='Faturamento Total por Dia',
            labels={'Total': 'Faturamento (R$)', 'Data': 'Data'},
            markers=True
        )
        fig_line.update_traces(line_color='#FF4B4B') # Cor neutra para linha
        fig_line.update_layout(hovermode="x unified")
        st.plotly_chart(fig_line, use_container_width=True)


    with col4:
        st.markdown("##### Distribuição do Faturamento por Forma de Pagamento")
        payment_revenue = df_filtered.groupby('Pagamento')['Total'].sum().reset_index()
        fig_pie = px.pie(
            payment_revenue,
            values='Total',
            names='Pagamento',
            title='Faturamento por Forma de Pagamento',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#000000', width=1)))
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("##### Número de Pedidos e Faturamento por Hora na Madrugada")
    df_filtered['Hora_Str'] = df_filtered['Hora'].apply(lambda x: x.strftime('%H:00'))

    hourly_summary = df_filtered.groupby('Hora_Str').agg(
        Contagem_de_Pedidos=('Hora_Str', 'size'),
        Faturamento_Total=('Total', 'sum')
    ).reset_index()

    hourly_summary['Hora_Str'] = pd.Categorical(hourly_summary['Hora_Str'],
                                              categories=[f'{h:02d}:00' for h in range(6)],
                                              ordered=True)
    hourly_summary = hourly_summary.sort_values('Hora_Str')

    fig_bar_hourly = px.bar(
        hourly_summary,
        x='Hora_Str',
        y='Contagem_de_Pedidos',
        title='Contagem de Pedidos e Faturamento por Hora (Madrugada)',
        labels={'Hora_Str': 'Hora', 'Contagem_de_Pedidos': 'Número de Pedidos'},
        color='Contagem_de_Pedidos',
        color_continuous_scale=px.colors.sequential.Bluyl,
        hover_data={'Faturamento_Total': ':.2f'}
    )
    fig_bar_hourly.update_traces(
        hovertemplate="""
        <b>Hora</b>: %{x}<br>
        <b>Número de Pedidos</b>: %{y}<br>
        <b>Faturamento Total</b>: R$ %{customdata[0]:,.2f}
        <extra></extra>
        """,
        customdata=hourly_summary[['Faturamento_Total']].values
    )

    fig_bar_hourly.update_layout(xaxis_title="Hora", yaxis_title="Número de Pedidos")
    st.plotly_chart(fig_bar_hourly, use_container_width=True)

    # --- 8. Tabela de Dados (Amostra) ---
    st.subheader("Dados Detalhados (Amostra)")

    # Seleciona as colunas e renomeia para exibir nomes mais amigáveis com ícones
    df_display = df_filtered.copy()
    df_display = df_display.rename(columns={
        "Data": "📅 Data",
        "Hora": "⏰ Hora",
        "Pagamento": "💳 Forma de Pagamento",
        "Total": "💰 Valor Total (R$)"
    })

    # Formata as colunas de data, hora e valor
    df_display["📅 Data"] = df_display["📅 Data"].apply(lambda x: x.strftime("%d/%m/%Y"))
    df_display["⏰ Hora"] = df_display["⏰ Hora"].apply(lambda x: x.strftime("%H:%M"))
    df_display["💰 Valor Total (R$)"] = df_display["💰 Valor Total (R$)"].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    # Mostra apenas as principais colunas com ícones
    columns_to_show = ["📅 Data", "⏰ Hora", "💳 Forma de Pagamento", "💰 Valor Total (R$)"]
    st.dataframe(
        df_display[columns_to_show].reset_index(drop=True),
        use_container_width=True,
        hide_index=True
    )
