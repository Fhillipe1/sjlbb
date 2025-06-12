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

# --- 2. Carregamento e Tratamento dos Dados ---

# Define o caminho do arquivo de dados.
# O 'st.cache_data' armazena em cache os resultados da função,
# o que acelera a aplicação se os dados não mudarem.
@st.cache_data
def load_data():
    # Carrega a planilha Excel. O engine 'openpyxl' é necessário para arquivos .xlsx.
    # CORRIGIDO: Nome do arquivo agora é 'Vendas por período.xlsx'
    df = pd.read_excel("data/Vendas por período.xlsx", engine='openpyxl')

    # Lista de colunas a serem removidas conforme sua solicitação
    # CORRIGIDO: Removida 'Forma de pagamento' e garantida que 'Pagamento' seja mantida
    columns_to_drop = [
        "Pedido", "Código da loja", "Nome da loja", "Tipo do pedido", "Turno",
        "Canal de venda", "Número do pedido no parceiro", "Consumidor",
        "Tem cupom", "Esta cancelado", "Itens", "Entrega", "Entregador",
        "Bairro", "CEP", "Acréscimo", "Motivo de acréscimo", "Desconto",
        "Motivo do desconto"
    ]
    # Remove as colunas especificadas
    df = df.drop(columns=columns_to_drop)

    # Converte a coluna 'Data da venda' para o tipo datetime, lidando com possíveis erros
    df['Data da venda'] = pd.to_datetime(df['Data da venda'], errors='coerce')

    # Remove linhas onde 'Data da venda' se tornou NaT (Not a Time) após a conversão
    df.dropna(subset=['Data da venda'], inplace=True)

    # Cria as colunas 'Data' e 'Hora' a partir de 'Data da venda'
    df['Data'] = df['Data da venda'].dt.date
    df['Hora'] = df['Data da venda'].dt.time

    # Filtra os dados para manter apenas os horários entre 00:00 e 05:00
    # Cria um objeto de tempo para 00:00:00 e 05:00:00
    start_time = datetime.time(0, 0, 0) # Usando datetime.time
    end_time = datetime.time(5, 0, 0)   # Usando datetime.time

    # Aplica o filtro de horário
    df = df[ (df['Hora'] >= start_time) & (df['Hora'] <= end_time) ]

    # Garante que 'Total' seja numérico
    # CORRIGIDO: Coluna 'Total'
    df['Total'] = pd.to_numeric(df['Total'], errors='coerce')
    # Remove linhas com valores nulos no 'Total' após a conversão
    df.dropna(subset=['Total'], inplace=True)


    return df

# Carrega os dados tratados
df = load_data()

# --- 3. Sidebar para Filtros ---
st.sidebar.header("Filtros")

# Filtro de Data
# Pega a data mínima e máxima disponível nos dados
min_date = df['Data'].min()
max_date = df['Data'].max()

# Permite ao usuário selecionar um intervalo de datas
date_range = st.sidebar.date_input(
    "Selecione o Período",
    value=(min_date, max_date), # Valor inicial exibido
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
# CORRIGIDO: Usando a coluna 'Pagamento'
st.sidebar.subheader("Filtrar por Método de Pagamento")
payment_methods = df_filtered['Pagamento'].unique().tolist()
selected_payment_methods = st.sidebar.multiselect(
    "Selecione as Formas de Pagamento",
    options=payment_methods,
    default=payment_methods # Seleciona todas por padrão
)

# Aplica o filtro de método de pagamento
# CORRIGIDO: Usando a coluna 'Pagamento'
df_filtered = df_filtered[df_filtered['Pagamento'].isin(selected_payment_methods)]

# --- 4. Título Principal do Dashboard ---
st.title("🍔 Dashboard Faturamento Madrugada - La Brasa Burger Aracaju")
st.markdown("Análise detalhada do desempenho de vendas no período da madrugada (00:00 - 05:00).")

# Verifica se há dados após os filtros
if df_filtered.empty:
    st.warning("Nenhum dado encontrado para os filtros selecionados. Tente ajustar os filtros.")
else:
    # --- 5. Métricas Chave (Key Performance Indicators - KPIs) ---
    st.subheader("Métricas de Faturamento")

    # Calcula o faturamento total e o número de pedidos
    # CORRIGIDO: Usando a coluna 'Total'
    total_revenue = df_filtered['Total'].sum()
    total_orders = df_filtered.shape[0] # Número de linhas = número de pedidos

    # Exibe as métricas em colunas para um layout organizado
    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="Faturamento Total (Madrugada)", value=f"R$ {total_revenue:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        # Formata o valor para R$ com duas casas decimais e separador de milhar
        # A gambiarra .replace(",", "X").replace(".", ",").replace("X", ".") é para formatar para padrão BR
    with col2:
        st.metric(label="Total de Pedidos (Madrugada)", value=f"{total_orders:,}".replace(",", "."))

    # --- 6. Gráficos ---
    st.subheader("Visualizações do Faturamento")

    # Layout de colunas para os gráficos
    col3, col4 = st.columns(2)

    with col3:
        # Gráfico de Linha: Faturamento por Data
        st.markdown("##### Faturamento Diário no Período da Madrugada")
        # Agrupa os dados por data e soma o valor total do pedido
        # CORRIGIDO: Usando a coluna 'Total'
        daily_revenue = df_filtered.groupby('Data')['Total'].sum().reset_index()
        fig_line = px.line(
            daily_revenue,
            x='Data',
            y='Total', # CORRIGIDO: Coluna 'Total'
            title='Faturamento Total por Dia',
            labels={'Total': 'Faturamento (R$)', 'Data': 'Data'}, # CORRIGIDO: Label 'Total'
            markers=True # Adiciona marcadores nos pontos de dados
        )
        fig_line.update_traces(line_color='#FF4B4B') # Cor neutra para linha
        fig_line.update_layout(hovermode="x unified") # Melhora a interatividade do hover
        st.plotly_chart(fig_line, use_container_width=True)


    with col4:
        # Gráfico de Pizza: Distribuição de Faturamento por Forma de Pagamento
        st.markdown("##### Distribuição do Faturamento por Forma de Pagamento")
        # CORRIGIDO: Usando a coluna 'Pagamento'
        payment_revenue = df_filtered.groupby('Pagamento')['Total'].sum().reset_index()
        fig_pie = px.pie(
            payment_revenue,
            values='Total', # CORRIGIDO: Coluna 'Total'
            names='Pagamento', # CORRIGIDO: Coluna 'Pagamento'
            title='Faturamento por Forma de Pagamento',
            hole=0.4, # Cria um gráfico de donut
            color_discrete_sequence=px.colors.qualitative.Pastel # Uma paleta de cores suave
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#000000', width=1)))
        st.plotly_chart(fig_pie, use_container_width=True)

    # Gráfico de Barras: Pedidos por Hora da Madrugada
    st.markdown("##### Número de Pedidos e Faturamento por Hora na Madrugada")
    # Extrai a hora como uma string para agrupar facilmente
    df_filtered['Hora_Str'] = df_filtered['Hora'].apply(lambda x: x.strftime('%H:00'))

    # Agrupa os dados por hora, contando os pedidos e somando o faturamento
    hourly_summary = df_filtered.groupby('Hora_Str').agg(
        Contagem_de_Pedidos=('Hora_Str', 'size'), # Conta o número de pedidos
        Faturamento_Total=('Total', 'sum')       # Soma o faturamento
    ).reset_index()

    # Garante a ordem correta das horas para exibição
    hourly_summary['Hora_Str'] = pd.Categorical(hourly_summary['Hora_Str'],
                                              categories=[f'{h:02d}:00' for h in range(6)], # Horas de 00 a 05
                                              ordered=True)
    hourly_summary = hourly_summary.sort_values('Hora_Str')

    fig_bar_hourly = px.bar(
        hourly_summary,
        x='Hora_Str',
        y='Contagem_de_Pedidos', # O eixo Y continua sendo a contagem de pedidos
        title='Contagem de Pedidos e Faturamento por Hora (Madrugada)',
        labels={'Hora_Str': 'Hora', 'Contagem_de_Pedidos': 'Número de Pedidos'},
        color='Contagem_de_Pedidos', # Colore as barras com base na contagem
        color_continuous_scale=px.colors.sequential.Bluyl, # Uma escala de cor suave
        # Inclui o faturamento total na tooltip (informação ao passar o mouse)
        hover_data={
            'Faturamento_Total': ':.2f' # Formata o faturamento para 2 casas decimais
        }
    )
    # Atualiza o template da tooltip para exibir Faturamento com R$ e separador de milhar
    fig_bar_hourly.update_traces(
        hovertemplate="""
        <b>Hora</b>: %{x}<br>
        <b>Número de Pedidos</b>: %{y}<br>
        <b>Faturamento Total</b>: R$ %{customdata[0]:,.2f}
        <extra></extra>
        """,
        customdata=hourly_summary[['Faturamento_Total']].values # Passa Faturamento_Total como customdata
    )


    fig_bar_hourly.update_layout(xaxis_title="Hora", yaxis_title="Número de Pedidos")
    st.plotly_chart(fig_bar_hourly, use_container_width=True)

    # --- 7. Tabela de Dados (Opcional, para debug ou visualização detalhada) ---
    st.subheader("Dados Detalhados (Amostra)")
    st.dataframe(df_filtered) # Mostra as primeiras 10 linhas dos dados filtrados