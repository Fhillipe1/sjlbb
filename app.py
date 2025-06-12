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
    page_icon="🍔", # Ícone que aparece na aba do navegador
    layout="wide"
)

# --- 2. CSS Customizado para Estilo e Cards ---
# Injeta CSS diretamente na aplicação Streamlit.
# O 'unsafe_allow_html=True' é necessário para permitir a renderização de HTML/CSS.
st.markdown("""
<style>
/* Estilo geral do corpo da aplicação Streamlit */
.stApp {
    background-color: #0E1117; /* Cor de fundo principal, corresponde ao config.toml */
    color: #FAFAFA; /* Cor do texto padrão, corresponde ao config.toml */
}

/* Estilização do Título Principal */
.main-title {
    font-size: 3.8em; /* Tamanho da fonte maior */
    font-weight: 800; /* Extra bold */
    text-align: center; /* Centraliza o texto */
    color: #FFFFFF; /* Cor branca para alto contraste */
    text-shadow: 2px 2px 6px rgba(0,0,0,0.5); /* Sombra sutil para profundidade */
    margin-bottom: 0.2em; /* Espaço abaixo do título */
    padding-top: 0.5em; /* Espaço acima do título */
}

/* Estilização do Subtítulo/Nome da Empresa */
.subtitle {
    font-size: 1.8em; /* Tamanho da fonte do subtítulo */
    text-align: center; /* Centraliza o texto */
    color: #FF4B4B; /* Cor primária do tema para destaque */
    margin-top: -0.2em; /* Ajusta a margem para ficar mais próximo do título principal */
    margin-bottom: 1.5em; /* Espaço abaixo do subtítulo */
    font-weight: 600; /* Semi-bold */
}

/* Estilo para os Cards de Métricas (KPIs) */
/* Seleciona o contêiner de cada métrica Streamlit (st.metric) */
div[data-testid="stMetric"] {
    background-color: #1E202B; /* Cor de fundo do card, ligeiramente mais clara que o fundo principal */
    border-radius: 12px; /* Cantos arredondados */
    padding: 25px; /* Espaçamento interno */
    margin-bottom: 25px; /* Espaço entre os cards e outros elementos */
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3); /* Sombra mais pronunciada para efeito de elevação */
    border: 1px solid #333642; /* Borda sutil */
    text-align: center; /* Centraliza o conteúdo (label e valor) dentro do card */
    min-height: 130px; /* Altura mínima para os cards */
    display: flex; /* Usa flexbox para alinhamento */
    flex-direction: column; /* Coloca itens em coluna */
    justify-content: center; /* Centraliza verticalmente */
    align-items: center; /* Centraliza horizontalmente */
}

/* Estilo para o Label (título) dentro do Card da Métrica */
div[data-testid="stMetricLabel"] > div {
    font-size: 1.2em; /* Tamanho da fonte do label */
    color: #BBBBBB; /* Cor mais clara para o label */
    font-weight: 500; /* Peso da fonte */
    margin-bottom: 8px; /* Espaço entre o label e o valor */
}

/* Estilo para o Valor dentro do Card da Métrica */
div[data-testid="stMetricValue"] {
    font-size: 3em; /* Tamanho da fonte do valor (bem maior) */
    font-weight: bold; /* Negrito */
    color: #FF4B4B; /* Cor primária do tema para o valor */
    /* Formata o valor para não quebrar linha */
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* Estilo para os gráficos Plotly (para que se pareçam com cards também) */
.stPlotlyChart {
    background-color: #1E202B; /* Cor de fundo igual a dos cards */
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
    margin-bottom: 25px;
    border: 1px solid #333642;
}

/* Ajustes para elementos da Sidebar (filtros) para combinar com o tema */
.st-emotion-cache-1pxazr7 div.stSelectbox,
.st-emotion-cache-1pxazr7 div.stMultiSelect,
.st-emotion-cache-1pxazr7 div.stDateInput,
.st-emotion-cache-1pxazr7 div.stTextInput {
    background-color: #262730; /* Cor de fundo secundária do config.toml */
    border-radius: 8px;
    padding: 8px;
    border: 1px solid #333642;
}

/* Garante que o texto dos títulos e parágrafos na sidebar tenha a cor correta */
.st-emotion-cache-1pxazr7 h1, .st-emotion-cache-1pxazr7 h2, .st-emotion-cache-1pxazr7 h3,
.st-emotion-cache-1pxazr7 h4, .st-emotion-cache-1pxazr7 h5, .st-emotion-cache-1pxazr7 h6,
.st-emotion-cache-1pxazr7 p, .st-emotion-cache-1pxazr7 label {
    color: #FAFAFA !important; /* !important para garantir a aplicação */
}

/* Estilo para botões (se houver, para combinar com o tema) */
.stButton>button {
    background-color: #FF4B4B;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
}
.stButton>button:hover {
    background-color: #E03A3A;
}

</style>
""", unsafe_allow_html=True) # ESSENCIAL para que o Streamlit renderize o HTML e CSS


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
st.sidebar.header("Filtros")

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
# Usando as classes CSS personalizadas para o título e subtítulo
st.markdown("<h1 class='main-title'>🍔 Dashboard Faturamento Madrugada</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='subtitle'>La Brasa Burger Aracaju</h2>", unsafe_allow_html=True)
st.markdown("Análise detalhada do desempenho de vendas no período da madrugada (00:00 - 05:00).")

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
    st.dataframe(df_filtered)
