import streamlit as st
import pandas as pd
import math
from pathlib import Path
import altair as alt
import numpy as np

from st_aggrid import AgGrid


# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    layout='wide',
    initial_sidebar_state='expanded',
    page_title='Profile dashboard',
    page_icon=':📊:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# functions.

@st.cache_data
def get_gdp_data():
    """Grab GDP data from a CSV file.
    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/gdp_data.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME)

    MIN_YEAR = 2000
    MAX_YEAR = 2022

    gdp_df = raw_gdp_df.melt(
        ['Country Code'],
        [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        'Year',
        'GDP',
    )

    # Convert years from string to integers
    gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])

    return gdp_df

gdp_df = get_gdp_data()

# ----------------------------------------------------
# Set the title that appears at the top of the page.
'''
# 📊 Dashboard de Clientes 
Información de principales clientes
'''

# Datos financieros de ejemplo para cuatro empresas de tecnología
data = {
    'Empresa': ['Apple', 'Microsoft', 'Amazon', 'Google'],
    'Ingresos Totales': [365.82, 168.09, 469.82, 257.64],
    'EBITDA': [109.68, 94.96, 59.23, 91.68],
    'Total Patrimonio': [134.05, 118.70, 144.47, 256.97],
    'Deuda Neta': [10.03, 50.24, 57.54, -123.45],  # Nota: -123.45 indica que Google tiene más efectivo que deuda
    'Valor Acción': [145.09, 299.35, 3524.74, 2725.60],
    'Variación Acción': [34.5, 27.6, 13.4, 28.2]
}
data1 = {
    'Empresa': ['Apple', 'Apple', 'Microsoft', 'Microsoft', 'Amazon', 'Amazon', 'Google', 'Google'],
    'Ejecutivo': ['Tim Cook', 'Luca Maestri', 'Satya Nadella', 'Amy Hood', 'Andy Jassy', 'Brian Olsavsky', 'Sundar Pichai', 'Ruth Porat'],
    'Cargo': ['CEO', 'CFO', 'CEO', 'CFO', 'CEO', 'CFO', 'CEO', 'CFO']
}

data2 = {
    'Empresa': ['Apple']*10 + ['Microsoft']*10 + ['Amazon']*10 + ['Google']*10,
    'Proyecto': [
        'Project Titan', 'Apple Glasses', 'HealthKit Expansion', 'Apple Car', 'ARKit Enhancements',
        'M1 Chip Development', 'iOS 16', 'macOS Monterey', 'Apple Music Expansion', 'HomePod Improvements',
        'Azure Quantum', 'Project xCloud', 'Microsoft Mesh', 'Windows 11', 'Surface Duo 2',
        'HoloLens 3', 'Azure AI', 'Microsoft Viva', 'Power BI Enhancements', 'Teams Integration',
        'Amazon Go Expansion', 'Project Kuiper', 'Amazon Pharmacy', 'AWS Graviton', 'Alexa for Business',
        'Amazon Scout', 'Amazon Fresh', 'Prime Air', 'Amazon Pay Expansion', 'Amazon Luna',
        'Waymo Self-Driving', 'Google Fiber Expansion', 'Google Health', 'Stadia Enhancements', 'DeepMind AI',
        'Google Photos', 'Google Workspace', 'Pixel Phone Development', 'YouTube Premium Expansion', 'Google Assistant'
    ],
    'Estado': [
        'planificado', 'en construcción', 'activo', 'planificado', 'en construcción', 
        'activo', 'planificado', 'en construcción', 'activo', 'planificado',
        'activo', 'planificado', 'en construcción', 'activo', 'planificado',
        'en construcción', 'activo', 'planificado', 'en construcción', 'activo',
        'planificado', 'en construcción', 'activo', 'planificado', 'en construcción',
        'activo', 'planificado', 'en construcción', 'activo', 'planificado',
        'en construcción', 'activo', 'planificado', 'en construcción', 'activo',
        'planificado', 'en construcción', 'activo', 'planificado', 'en construcción'
    ]
}

# Datos de ingresos por región para cuatro empresas de tecnología
data3 = {
    'Empresa': ['Apple']*4 + ['Microsoft']*4 + ['Amazon']*4 + ['Google']*4,
    'Región': [1, 2, 3, 4]*4,
    'Zona': ['A', 'A', 'B', 'B']*4,
    'Ingresos': [
        90.0, 110.0, 80.0, 85.82, 
        45.0, 55.0, 35.0, 33.09, 
        120.0, 150.0, 100.0, 99.82, 
        60.0, 70.0, 50.0, 77.64
    ],
    'Tipo': ['regulado', 'dedicado', 'regulado', 'dedicado']*4
}

data4 = {
    'Empresa': ['Apple', 'Apple', 'Apple', 'Microsoft', 'Microsoft', 'Microsoft', 'Amazon', 'Amazon', 'Amazon', 'Google', 'Google', 'Google'],
    'Título': [
        'Apple lanza el nuevo iPhone 14', 'Apple anuncia avances en IA', 'Apple Music supera los 100 millones de suscriptores',
        'Microsoft presenta Windows 12', 'Microsoft adquiere empresa de ciberseguridad', 'Microsoft Teams integra nuevas funciones',
        'Amazon lanza servicio de entrega con drones', 'Amazon Prime Video gana premio', 'Amazon abre nuevo centro logístico',
        'Google mejora su motor de búsqueda', 'Google lanza nueva versión de Android', 'Google Cloud expande sus servicios'
    ],
    'Resumen': [
        'El nuevo iPhone 14 incluye mejoras significativas en la cámara y el rendimiento.', 
        'Apple ha revelado nuevos avances en inteligencia artificial que mejorarán sus productos.', 
        'Apple Music ha alcanzado un hito importante con más de 100 millones de suscriptores.',
        'Microsoft ha anunciado oficialmente el lanzamiento de Windows 12 con nuevas características.', 
        'Microsoft ha adquirido una empresa líder en ciberseguridad para fortalecer su oferta.', 
        'Microsoft Teams ahora incluye funciones mejoradas para la colaboración en remoto.',
        'Amazon ha iniciado un servicio de entrega utilizando drones en áreas seleccionadas.', 
        'Amazon Prime Video ha ganado un premio por su contenido original y de alta calidad.', 
        'Amazon ha inaugurado un nuevo centro logístico para mejorar sus tiempos de entrega.',
        'Google ha implementado mejoras significativas en su motor de búsqueda para ofrecer resultados más precisos.', 
        'Google ha lanzado la nueva versión de Android con múltiples mejoras y nuevas características.', 
        'Google Cloud ha ampliado sus servicios para incluir más opciones de almacenamiento y computación.'
    ]
}

# Generar datos de facturación para 12 meses
meses = pd.date_range(start='2023-01-01', periods=12, freq='M').strftime('%Y-%m')
empresas = ['Apple', 'Microsoft', 'Amazon', 'Google']
facturacion = {empresa: np.random.uniform(50, 150, 12).tolist() for empresa in empresas}

# Crear DataFrame
data5 = {
    'Mes': np.tile(meses, len(empresas)),
    'Empresa': np.repeat(empresas, len(meses)),
    'Facturación': np.concatenate([facturacion[empresa] for empresa in empresas])
}

# Crear un DataFrame
df = pd.DataFrame(data)
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)
df3 = pd.DataFrame(data3)
df4 = pd.DataFrame(data4)
df5 = pd.DataFrame(data5)

with st.sidebar:
    st.title('Customer profile')
    empresa_seleccionada = st.selectbox('Selecciona una empresa', df['Empresa'])

# Filtrar datos para la empresa seleccionada
datos_empresa = df[df['Empresa'] == empresa_seleccionada]
#datos_empresa = datos_empresa.T
#datos_empresa.columns = ['KPI', 'USD M']
datos_ejecutivos = df1[df1['Empresa'] == empresa_seleccionada]
datos_proyectos = df2[df2['Empresa'] == empresa_seleccionada]
datos_regiones = df3[df3['Empresa'] == empresa_seleccionada]

st.markdown('<hr style="border:2px solid blue;">', unsafe_allow_html=True)

# Crear tres columnas con el tamaño especificado
col1, col2, col3 = st.columns([1, 2, 1])

st.markdown("""
    <style>
    .col-container {
        display: flex;
        justify-content: space-between;
    }
    .col {
        flex: 1;
        padding: 10px;
    }
    .col + .col {
        border-left: 2px solid lightgray;
    }
    </style>
    """, unsafe_allow_html=True)

# Contenido de la primera columna
with col1:
    # Título
    #st.title('Perfil Financiero')
    st.write('**Indicadores financieros:**')
    st.dataframe(datos_empresa.drop(columns=['Empresa', 'Valor Acción', 'Variación Acción']).T)

    #############################
    st.markdown('<hr style="border:2px solid blue;">', unsafe_allow_html=True)
    #############################

    # Mostrar métricas del valor de la acción y la variación
    valor_accion = datos_empresa['Valor Acción'].values[0]
    variacion_accion = datos_empresa['Variación Acción'].values[0]
    st.metric(label="Valor acción (USD)", value=f"${valor_accion}",delta=f"{variacion_accion}%")

    #############################
    st.markdown('<hr style="border:2px solid blue;">', unsafe_allow_html=True)
    #############################

    source = pd.DataFrame({"category": [1, 2, 3, 4, 5, 6], "value": [4, 6, 10, 3, 7, 8]})

    chart = alt.Chart(source).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="value", type="quantitative"),
        color=alt.Color(field="category", type="nominal"),
    )

    tab1, tab2 = st.tabs(["Versión 1", "Versión 2"])

    with tab1:
        st.altair_chart(chart, theme="streamlit", use_container_width=True)
    with tab2:
        st.altair_chart(chart, theme=None, use_container_width=True)

    st.write(f'**Principales Ejecutivos:**')
    st.dataframe(datos_ejecutivos.drop(columns=['Empresa']), hide_index=True)

with col2:
    # Crear gráfico de líneas
    chart = alt.Chart(df5).mark_line().encode(
        x=alt.X('Mes:T', axis=alt.Axis(title='Mes', labelAngle=-45)),
        y=alt.Y('Facturación:Q', axis=alt.Axis(title='Facturación - USD M')),
        color='Empresa:N'
    ).properties(
        title='Facturación 12 Meses'
    )

    # Mostrar el gráfico en Streamlit
    st.altair_chart(chart, use_container_width=True)

    #############################
    st.markdown('<hr style="border:2px solid blue;">', unsafe_allow_html=True)
    #############################

    # Multiselector de zonas
    zonas_seleccionadas = st.multiselect('Selecciona las zonas', sorted(datos_regiones['Zona'].unique()))

    # Filtrar datos por zonas seleccionadas
    if zonas_seleccionadas:
        datos_filtrados_zonas = datos_regiones[datos_regiones['Zona'].isin(zonas_seleccionadas)]
    else:
        datos_filtrados_zonas = datos_regiones[datos_regiones['Zona'] != ' ']  # Excluir totales

    # Multiselector de tipos
    tipos_seleccionados = st.multiselect('Selecciona los tipos', sorted(datos_regiones['Tipo'].unique()))

    # Filtrar datos por tipos seleccionados
    if tipos_seleccionados:
        datos_filtrados_tipo = datos_filtrados_zonas[datos_filtrados_zonas['Tipo'].isin(tipos_seleccionados)]
    else:
        datos_filtrados_tipo = datos_filtrados_zonas  # Mostrar todos los datos si no se selecciona ningún tipo

    # Crear gráfico de ingresos filtrados por región
    chart1 = alt.Chart(datos_filtrados_tipo).mark_bar().encode(
        x=alt.X('Región:O', axis=alt.Axis(title='Número de Región')),
        y=alt.Y('Ingresos:Q', axis=alt.Axis(title='Ingresos en USD M')),   color='Empresa:N'
        ).properties(
        title='Ingresos por Región, Zona y Tipo'
    )

    # Mostrar el gráfico en Streamlit
    st.altair_chart(chart1, use_container_width=True)

with col3:
    # Contar la cantidad de proyectos por estado
    estado_counts = datos_proyectos['Estado'].value_counts().reset_index()
    estado_counts.columns = ['Estado', 'Cantidad']

    # Crear gráfico de barras
    chart2 = alt.Chart(estado_counts).mark_bar().encode(
        x=alt.X('Estado', sort=None, axis=alt.Axis(title='Estado')),
        y=alt.Y('Cantidad', axis=alt.Axis(title='n° de Proyectos')),
        color='Estado'
    ).properties(
        title='# Proyectos por Estado'
    )

    # Mostrar el gráfico en Streamlit
    st.altair_chart(chart2, use_container_width=True)

    #############################
    st.markdown('<hr style="border:2px solid blue;">', unsafe_allow_html=True)
    #############################


    #st.write(f'Principales Proyectos:', datos_proyectos.drop(columns=['Empresa']), hide_index=True)
    st.write(f'**Principales Proyectos:**')
    st.dataframe(datos_proyectos.drop(columns=['Empresa']), hide_index=True)

    # Insertar una línea horizontal azul para separar información
    st.markdown('<hr style="border:2px solid blue;">', unsafe_allow_html=True)

    # Mostrar datos de noticias destacadas sin el índice
    st.write(f'**Noticias destacadas**:')
    datos_noticias = df4[df4['Empresa'] == empresa_seleccionada]
    #st.dataframe(datos_noticias.drop(columns=['Empresa']).reset_index(drop=True))
    for index, row in datos_noticias.iterrows():
        st.write(f"**{row['Título']}**")
        st.write(row['Resumen'])
        st.markdown("---") 
######################################

