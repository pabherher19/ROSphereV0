import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import time

# Configuración de la página
st.set_page_config(
    page_title="ROSphere Monitor",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Personalización CSS mejorada
st.markdown("""
<style>
    /* Estilos generales */
    .main {
        background-color: #000000;
        color: white;
        padding: 0 !important;
        margin: 0 !important;
    }
    .stButton button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 8px 15px;
        text-align: center;
        display: inline-block;
        font-size: 14px;
        margin: 2px;
        cursor: pointer;
    }
    
    /* Sidebar con fondo oscuro */
    [data-testid="stSidebar"] {
        background-color: #121212;
    }
    
    /* Celdas de parámetros con fondo azul marino */
    .param-box {
        background-color: #0a1e3d;
        color: white;
        border-radius: 5px;
        padding: 6px 10px;
        margin-bottom: 8px;
        text-align: center;
    }
    
    /* Títulos */
    h1 {
        color: white;
        font-size: 24px;
        margin-bottom: 5px;
        padding-bottom: 0;
    }
    h2, h3, h4, p, div {
        color: white;
        margin-top: 0;
        margin-bottom: 3px;
        padding-top: 0;
        padding-bottom: 0;
    }
    
    /* Cronómetro */
    .timer-display {
        background-color: #0a1e3d;
        color: white !important;
        padding: 5px 10px;
        border-radius: 5px;
        text-align: center;
        font-size: 16px;
        margin-bottom: 8px;
    }
    
    /* Valores de parámetros */
    .slider-value {
        font-size: 22px;
        font-weight: bold;
        text-align: center;
        padding: 3px 8px;
        border-radius: 4px;
        margin-top: 0;
        color: white;
    }
    
    /* Sliders */
    .stSlider {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        margin-top: 0 !important;
        margin-bottom: 4px !important;
    }
    
    /* Dividers */
    hr {
        margin-top: 5px;
        margin-bottom: 5px;
        border: 0;
        border-top: 1px solid #333;
    }
    
    /* Ajustar sidebar */
    .css-1d391kg {
        padding-top: 0.5rem;
    }
    
    /* Eliminar padding excesivo */
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0 !important;
        max-width: 100% !important;
    }
    
    /* Ajustar labels de sliders */
    .stSlider p {
        color: white !important;
        font-weight: bold !important;
        margin-bottom: 0 !important;
    }
    
    /* Celdas de título con fondo azul marino */
    .metric-title {
        background-color: #0a1e3d;
        color: white;
        padding: 5px 10px;
        border-radius: 5px 5px 0 0;
        text-align: center;
        font-weight: bold;
        margin-bottom: 0;
        font-size: 16px;
    }
    
    /* Para pantallas más pequeñas */
    .main .block-container {
        padding: 0 !important;
        margin: 0 !important;
    }
    .stPlotlyChart {
        margin-bottom: 0 !important;
    }
    
    /* Ocultar elementos no deseados */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Selector de pacientes con texto oscuro */
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: white;
        color: #333333 !important;
    }
    
    .stSelectbox div[data-baseweb="select"] span {
        color: #333333 !important;
    }
    
    /* Para los elementos del dropdown */
    div[data-baseweb="popover"] div[role="listbox"] {
        background-color: white;
    }
    
    div[data-baseweb="popover"] div[role="option"] {
        color: #333333 !important;
    }
</style>
""", unsafe_allow_html=True)

# Funciones para crear los gráficos (versión más compacta)
def create_gauge_chart(value, title, min_val, max_val, thresholds, container_width=400, container_height=150):
    colors = ['#32CD32', '#FFD700', '#FF4500']
    
    # Calcular rangos basados en thresholds
    ranges = []
    for i in range(len(thresholds)):
        if i == 0:
            ranges.append([min_val, thresholds[i]])
        else:
            ranges.append([thresholds[i-1], thresholds[i]])
    if thresholds:
        ranges.append([thresholds[-1], max_val])
    
    fig = go.Figure()
    
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 16, 'color': 'white'}},
        gauge={
            'axis': {'range': [min_val, max_val], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "white", 'thickness': 0.15},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 0,
            'steps': [
                {'range': ranges[0], 'color': colors[0]},
                {'range': ranges[1], 'color': colors[1]},
                {'range': ranges[2], 'color': colors[2]},
            ],
            'threshold': {
                'line': {'color': "white", 'width': 2},
                'thickness': 0.75,
                'value': value
            }
        },
        number={'font': {'size': 36, 'color': 'white'}}
    ))
    
    fig.update_layout(
        width=container_width,
        height=container_height,
        margin=dict(l=10, r=10, t=10, b=0),
        paper_bgcolor='rgba(48, 48, 48, 1)',
        font={'color': "white", 'family': "Arial"},
    )
    
    return fig

def create_trend_graph(x_data, y_data, title, container_width=400, container_height=60):
    fig = go.Figure()
    
    # Añadir la línea de tendencia
    fig.add_trace(go.Scatter(
        x=x_data, 
        y=y_data,
        mode='lines+markers',
        line=dict(color='red', width=2),
        marker=dict(size=4, color='red'),
        name=title
    ))
    
    # Configurar el diseño
    fig.update_layout(
        title=None,
        width=container_width,
        height=container_height,
        margin=dict(l=10, r=10, t=0, b=20),
        paper_bgcolor='rgba(48, 48, 48, 1)',
        plot_bgcolor='rgba(48, 48, 48, 1)',
        font={'color': "white", 'family': "Arial"},
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(75, 75, 75, 1)',
            zeroline=False,
            title=None,
            tickfont=dict(size=8)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(75, 75, 75, 1)',
            zeroline=False,
            title=None,
            tickfont=dict(size=8)
        )
    )
    
    return fig

def create_risk_gauge(risk_probability, container_width=700, container_height=180):
    # Colores para los rangos de riesgo
    risk_colors = [
        {'range': [0, 60], 'color': 'green'},
        {'range': [60, 80], 'color': 'yellow'},
        {'range': [80, 90], 'color': 'orange'},
        {'range': [90, 100], 'color': 'red'}
    ]
    
    # Determinar si estamos por encima o por debajo del umbral
    is_risk = risk_probability < 65
    arrow_color = 'red' if is_risk else 'green'
    threshold_text = "<65%" if is_risk else ">65%"
    
    # Crear una figura con subplots - uno para el medidor y otro para la información
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "indicator"}, {"type": "indicator"}]],
        column_widths=[0.8, 0.2]
    )
    
    # Añadir el medidor principal con nuevas marcas y colores
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=risk_probability,
            title={
                'text': "Riesgo SatO2 <65% 10min",
                'font': {'size': 16, 'color': 'white'}
            },
            gauge={
                'axis': {
                    'range': [0, 100],
                    'tickwidth': 1,
                    'tickcolor': "white",
                    'tickvals': [0, 60, 80, 90, 100],  # Nuevas marcas
                    'ticktext': ['0', '60', '80', '90', '100']
                },
                'bar': {'color': "white", 'thickness': 0.15},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 0,
                'steps': risk_colors,  # Nuevos colores
                'threshold': {
                    'line': {'color': "white", 'width': 2},
                    'thickness': 0.75,
                    'value': risk_probability
                }
            },
            number={
                'font': {'size': 40, 'color': 'white'},
                'suffix': '%'
            }
        ),
        row=1, col=1
    )
    
    # Mostrar solo el cálculo del % SatO2 <65% en 10min
    fig.add_trace(
        go.Indicator(
            mode="number",
            value=risk_probability,
            title={
                'text': f"<span style='color:{arrow_color};font-size:22px;'>{threshold_text}</span>",
                'font': {'size': 16, 'color': 'white'}
            },
            number={
                'font': {'size': 36, 'color': 'white'},
                'suffix': '%'
            }
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        width=container_width,
        height=container_height,
        margin=dict(l=10, r=10, t=20, b=0),
        paper_bgcolor='rgba(48, 48, 48, 1)',
        font={'color': "white", 'family': "Arial"},
    )
    
    return fig

def create_performance_metrics_card(metrics, container_width=300, container_height=180):
    fig = go.Figure()
    
    # Crear una tabla para mostrar las métricas
    fig.add_trace(go.Table(
        header=dict(
            values=["<b>Métrica</b>", "<b>Valor</b>"],
            line_color='rgba(48, 48, 48, 1)',
            fill_color='#0a1e3d',  # Azul marino
            align=['left', 'center'],
            font=dict(color='white', size=12),
            height=25
        ),
        cells=dict(
            values=[
                list(metrics.keys()),
                list(metrics.values())
            ],
            line_color='rgba(60, 60, 60, 1)',
            fill_color='rgba(48, 48, 48, 1)',
            align=['left', 'center'],
            font=dict(color='white', size=12),
            height=25
        )
    ))
    
    # Configurar el diseño
    fig.update_layout(
        title={
            'text': "Rendimiento Algoritmo Random Forest",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 14, 'color': 'white'}
        },
        width=container_width,
        height=container_height,
        margin=dict(l=5, r=5, t=30, b=5),
        paper_bgcolor='rgba(48, 48, 48, 1)',
    )
    
    return fig

# Inicialización del estado si no existe
if 'simulation_time' not in st.session_state:
    st.session_state.simulation_time = 0
    st.session_state.running = True  # Automáticamente inicia la simulación
    st.session_state.mode = "AUTOMÁTICO"  # Por defecto en AUTOMÁTICO
    st.session_state.map = 75
    st.session_state.co = 5.0
    st.session_state.svv = 12
    st.session_state.pvv = 11
    st.session_state.trend_data = {
        'map': [],
        'co': [],
        'svv': [],
        'pvv': [],
        'risk': []
    }
    st.session_state.x_data = list(range(0, 10))  # Inicializar con 10 puntos

# Título de la aplicación (más compacto)
st.markdown("<h1 style='text-align: center; margin: 0; padding: 0;'>ROSphere Monitor</h1>", unsafe_allow_html=True)

# Contenido de la barra lateral (más compacto)
with st.sidebar:
    st.markdown("<h3 style='margin-top:0'>Control de Simulación</h3>", unsafe_allow_html=True)
    
    # Selector de modo (Manual/Automático)
    st.markdown("<div style='margin-bottom: 2px;'>Modo de operación</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        manual_btn = st.button("MANUAL", use_container_width=True, 
                               type="primary" if st.session_state.mode == "MANUAL" else "secondary")
        if manual_btn:
            st.session_state.mode = "MANUAL"
            st.session_state.running = False  # Detener la simulación en modo manual
    with col2:
        auto_btn = st.button("AUTOMÁTICO", use_container_width=True,
                             type="primary" if st.session_state.mode == "AUTOMÁTICO" else "secondary")
        if auto_btn:
            st.session_state.mode = "AUTOMÁTICO"
            st.session_state.running = True  # Iniciar la simulación en modo automático
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Selector de paciente (lista expandida)
    st.markdown("<div style='margin-bottom: 3px;'>Paciente</div>", unsafe_allow_html=True)
    patient_options = [f"Paciente {i}" for i in range(1, 21)]
    patient = st.selectbox("Seleccionar paciente", patient_options, label_visibility="collapsed")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Controles de parámetros (organizados en 2x2)
    st.markdown("<div style='margin-bottom: 2px;'>Parámetros de simulación</div>", unsafe_allow_html=True)
    
    # Primera fila de parámetros
    param_col1, param_col2 = st.columns(2)
    
    with param_col1:
        # MAP control
        st.markdown("<div class='param-box'>MAP (mmHg)</div>", unsafe_allow_html=True)
        st.session_state.map = st.slider("MAP (mmHg)", 40, 140, st.session_state.map, label_visibility="collapsed")
        st.markdown(f"<div class='slider-value'>{st.session_state.map}</div>", unsafe_allow_html=True)
    
    with param_col2:
        # CO control
        st.markdown("<div class='param-box'>CO (L/min)</div>", unsafe_allow_html=True)
        st.session_state.co = st.slider("CO (L/min)", 1.0, 10.0, float(st.session_state.co), 0.1, label_visibility="collapsed")
        st.markdown(f"<div class='slider-value'>{st.session_state.co:.2f}</div>", unsafe_allow_html=True)
    
    # Segunda fila de parámetros
    param_col3, param_col4 = st.columns(2)
    
    with param_col3:
        # SVV control
        st.markdown("<div class='param-box'>SVV (%)</div>", unsafe_allow_html=True)
        st.session_state.svv = st.slider("SVV (%)", 0, 25, st.session_state.svv, label_visibility="collapsed")
        st.markdown(f"<div class='slider-value'>{st.session_state.svv}</div>", unsafe_allow_html=True)
    
    with param_col4:
        # PVV control
        st.markdown("<div class='param-box'>PVV (%)</div>", unsafe_allow_html=True)
        st.session_state.pvv = st.slider("PVV (%)", 0, 25, st.session_state.pvv, label_visibility="collapsed")
        st.markdown(f"<div class='slider-value'>{st.session_state.pvv}</div>", unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Mostrar tiempo de simulación con nuevo estilo
    st.markdown(f"""
    <div class='timer-display'>
        ⏱️ Tiempo: {st.session_state.simulation_time:.1f} segundos
    </div>
    """, unsafe_allow_html=True)
    
    # Botones de control
    col1, col2 = st.columns(2)
    with col1:
        if st.button("INICIAR", use_container_width=True, type="primary" if st.session_state.running else "secondary"):
            st.session_state.running = True
    with col2:
        if st.button("DETENER", use_container_width=True, type="primary" if not st.session_state.running else "secondary"):
            st.session_state.running = False
    
    # Estado actual
    if st.session_state.running:
        status = "Simulación en curso"
    else:
        status = "Simulación detenida"
    st.markdown(f"<div style='color: #A0A0A0; margin-top: 5px;'>{status}</div>", unsafe_allow_html=True)

# Botón de actualizar simulación en el área principal
st.button("ACTUALIZAR SIMULACIÓN", type="primary", use_container_width=True)

# Función para generar datos de tendencia
def update_trend_data():
    time_factor = st.session_state.simulation_time / 10
    
    # Solo mantener los últimos 10 puntos para cada tendencia
    if len(st.session_state.trend_data['map']) >= 10:
        for key in st.session_state.trend_data:
            st.session_state.trend_data[key].pop(0)
    
    # Agregar nuevos valores
    st.session_state.trend_data['map'].append(st.session_state.map)
    st.session_state.trend_data['co'].append(st.session_state.co)
    st.session_state.trend_data['svv'].append(st.session_state.svv)
    st.session_state.trend_data['pvv'].append(st.session_state.pvv)
    
    # Calcular riesgo basado en los parámetros actuales
    risk_score = 100 - min(100, max(0, (st.session_state.map - 60) + (st.session_state.co * 10) - 
                                   (st.session_state.svv * 0.5) - (st.session_state.pvv * 0.5)))
    st.session_state.trend_data['risk'].append(risk_score)
    
    return risk_score

# Métricas para el modelo
metrics = {
    "AUC": "0.93",
    "F1-Score": "0.89",
    "Precisión": "0.88",
    "Sensibilidad": "0.88",
    "Especificidad": "0.90",
    "Exactitud": "0.89"
}

# Calcular el riesgo actual
risk_score = update_trend_data() if st.session_state.running else st.session_state.trend_data['risk'][-1] if st.session_state.trend_data['risk'] else 42.5

# Crear contenedores para filas de métricas principales y riesgo
row3_col1, row3_col2 = st.columns([1, 2])

# Fila de métricas
with row3_col1:
    # Tabla de métricas
    st.markdown("<div class='metric-title'>Métricas del Algoritmo</div>", unsafe_allow_html=True)
    st.plotly_chart(create_performance_metrics_card(metrics), use_container_width=True, config={'displayModeBar': False})

with row3_col2:
    # Título del gráfico de riesgo
    st.markdown("<div class='metric-title'>Predicción de Riesgo SatO2 <65% en 10min</div>", unsafe_allow_html=True)
    
    # Mostrar gráfico de riesgo con probabilidad
    st.plotly_chart(create_risk_gauge(risk_score), use_container_width=True, config={'displayModeBar': False})

# Crear contenedores para las filas de gráficos principales
row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

# Primera fila de gráficos
with row1_col1:
    # MAP con título azul marino
    st.markdown("<div class='metric-title'>MAP (mmHg)</div>", unsafe_allow_html=True)
    st.plotly_chart(create_gauge_chart(
        value=st.session_state.map,
        title="",
        min_val=40,
        max_val=140,
        thresholds=[65, 95]
    ), use_container_width=True, config={'displayModeBar': False})
    
    # Gráfico de tendencia MAP
    st.plotly_chart(create_trend_graph(
        x_data=st.session_state.x_data,
        y_data=st.session_state.trend_data['map'],
        title="MAP (mmHg)"
    ), use_container_width=True, config={'displayModeBar': False})

with row1_col2:
    # CO con título azul marino
    st.markdown("<div class='metric-title'>CO (L/min)</div>", unsafe_allow_html=True)
    st.plotly_chart(create_gauge_chart(
        value=st.session_state.co,
        title="",
        min_val=1,
        max_val=10,
        thresholds=[2.5, 7.5]
    ), use_container_width=True, config={'displayModeBar': False})
    
    # Gráfico de tendencia CO
    st.plotly_chart(create_trend_graph(
        x_data=st.session_state.x_data,
        y_data=st.session_state.trend_data['co'],
        title="CO (L/min)"
    ), use_container_width=True, config={'displayModeBar': False})

# Segunda fila de gráficos
with row2_col1:
    # SVV con título azul marino
    st.markdown("<div class='metric-title'>SVV (%)</div>", unsafe_allow_html=True)
    st.plotly_chart(create_gauge_chart(
        value=st.session_state.svv,
        title="",
        min_val=0,
        max_val=25,
        thresholds=[8, 17]
    ), use_container_width=True, config={'displayModeBar': False})
    
    # Gráfico de tendencia SVV
    st.plotly_chart(create_trend_graph(
        x_data=st.session_state.x_data,
        y_data=st.session_state.trend_data['svv'],
        title="SVV (%)"
    ), use_container_width=True, config={'displayModeBar': False})

with row2_col2:
    # PVV con título azul marino
    st.markdown("<div class='metric-title'>PVV (%)</div>", unsafe_allow_html=True)
    st.plotly_chart(create_gauge_chart(
        value=st.session_state.pvv,
        title="",
        min_val=0,
        max_val=25,
        thresholds=[5, 15]
    ), use_container_width=True, config={'displayModeBar': False})
    
    # Gráfico de tendencia PVV
    st.plotly_chart(create_trend_graph(
        x_data=st.session_state.x_data,
        y_data=st.session_state.trend_data['pvv'],
        title="PVV (%)"
    ), use_container_width=True, config={'displayModeBar': False})

# Simulación automática
if st.session_state.running:
    # Incrementar el tiempo de simulación
    st.session_state.simulation_time += 0.1
    
    # Simular cambios pequeños en los parámetros si está en modo automático
    if st.session_state.mode == "AUTOMÁTICO":
        time_factor = st.session_state.simulation_time / 10
        
        # Pequeña variación sinusoidal en los parámetros
        st.session_state.map = 75 + int(5 * np.sin(time_factor))
        st.session_state.co = 5.0 + 0.5 * np.sin(time_factor + 1)
        st.session_state.svv = 12 + int(2 * np.sin(time_factor + 2))
        st.session_state.pvv = 11 + int(2 * np.sin(time_factor + 3))
    
    # Breve pausa para simulación más realista
    time.sleep(0.1)
    
    # Usar st.rerun() en lugar de st.experimental_rerun()
    st.rerun()