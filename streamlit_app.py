import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

df = pd.read_csv('C:/Users/Usuario/Downloads/art/5gr.csv', encoding='latin1')

# Limpieza de datos
df.drop_duplicates(inplace=True)
df.fillna(df.mean(numeric_only=True), inplace=True)

# Funciones para mostrar gráficos

def mostrar_distribucion_goles_totales():
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df['FT Team 1'] + df['FT Team 2'], bins=50, kde=True, ax=ax)
    ax.set_title('Distribución de Goles Totales')
    ax.set_xlabel('Goles Totales')
    ax.set_ylabel('Frecuencia')
    st.pyplot(fig)

def mostrar_distribucion_por_paises():
    counts = df['Country'].value_counts().nlargest(10)
    labels = counts.index
    colors = sns.color_palette('tab10', len(counts))

    fig, ax = plt.subplots(figsize=(10, 6))
    wedges, texts, autotexts = ax.pie(counts, autopct='%1.1f%%', startangle=90, pctdistance=0.85, colors=colors)
    
    ax.set_title('Distribución por Países (Top 10)')
    ax.axis('equal')  # Asegura que el gráfico sea circular
    
    # Ajustar la leyenda
    ax.legend(wedges, labels, title="Países", loc="center left", bbox_to_anchor=(1, 0.5))
    
    st.pyplot(fig)

def mostrar_evolucion_goles_por_anio():
    fig, ax = plt.subplots(figsize=(10, 6))
    df_grouped = df.groupby('Year')[['FT Team 1', 'FT Team 2']].sum()
    df_grouped.plot(kind='line', ax=ax)
    ax.set_title('Evolución de Goles por Año')
    ax.set_xlabel('Año')
    ax.set_ylabel('Total de Goles')
    st.pyplot(fig)

def mostrar_matriz_correlacion():
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm', ax=ax)
    ax.set_title('Matriz de Correlación')
    st.pyplot(fig)

def mostrar_puntos_por_equipo():
    puntos_por_equipo = df.groupby('Team 1')['Team 1 (pts)'].sum().nlargest(16)
    colors = sns.color_palette('tab20', len(puntos_por_equipo))
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(range(len(puntos_por_equipo)), puntos_por_equipo.values, color=colors)
    ax.set_title('Puntos por Equipo (Top 16)')
    ax.set_xlabel('Equipo')
    ax.set_ylabel('Puntos')
    
    # Añadir etiquetas de los puntos en las barras
    for bar, value in zip(bars, puntos_por_equipo.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{value}', ha='center', va='bottom')

    # Quitar las etiquetas de x-ticks y poner números
    ax.set_xticks(range(len(puntos_por_equipo)))
    ax.set_xticklabels([])

    # Agregar leyenda
    ax.legend(bars, puntos_por_equipo.index, title="Equipos", loc="center left", bbox_to_anchor=(1, 0.5))
    
    st.pyplot(fig)

def mostrar_grafico_ganados_por_equipo():
    ganados_por_equipo = df['Team 1'].value_counts().nlargest(10)
    labels = ganados_por_equipo.index
    colors = sns.color_palette('tab10', len(ganados_por_equipo))

    fig, ax = plt.subplots(figsize=(10, 6))
    wedges, texts, autotexts = ax.pie(ganados_por_equipo, autopct='%1.1f%%', startangle=90, pctdistance=0.85, colors=colors)
    
    # Dibujar el círculo central para crear el efecto de anillo
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig.gca().add_artist(centre_circle)
    
    ax.set_title('Partidos Ganados por Equipo (Top 10)')
    ax.axis('equal')  # Asegura que el gráfico sea circular
    
    # Ajustar la leyenda
    ax.legend(wedges, labels, title="Equipos", loc="center left", bbox_to_anchor=(1, 0.5))
    
    st.pyplot(fig)

# Configuración de la interfaz gráfica de Streamlit
st.title("Reportes de Fútbol")

if st.button('Distribución de Goles Totales'):
    mostrar_distribucion_goles_totales()

if st.button('Distribución por Países'):
    mostrar_distribucion_por_paises()

if st.button('Evolución de Goles por Año'):
    mostrar_evolucion_goles_por_anio()

if st.button('Matriz de Correlación'):
    mostrar_matriz_correlacion()

if st.button('Puntos por Equipo'):
    mostrar_puntos_por_equipo()

if st.button('Anillo de Partidos Ganados'):
    mostrar_grafico_ganados_por_equipo()
