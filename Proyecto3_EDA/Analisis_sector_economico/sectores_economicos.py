import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Paso 1: Cargar los Datos

# Cargar el archivo excel
file_path = 'remuneracion-neta-sector-actividad-economica-sector-privado.csv'
df = pd.read_csv(file_path)

print(df.head())
print(df.info())

# Paso 1: Identificación de Datos Ausentes
datos_faltantes = df.isnull().sum()

# Paso 2: Análisis Estadístico Descriptivo
estadisticas_resumen = df.describe()

# Paso 3: Cálculos Relevantes
# 1. Promedio de remuneración neta por sector
promedio_remuneracion = df.mean(numeric_only=True)

# 2. Sector con mayor remuneración neta promedio
sector_mayor_promedio = promedio_remuneracion.idxmax()
mayor_promedio = promedio_remuneracion.max()

# 3. Variación estándar de la remuneración en sectores clave
desviacion_estandar_remuneracion = df.std(numeric_only=True)

# 4. Remuneración máxima y mínima en el sector con mayor variabilidad
sector_mayor_variabilidad = desviacion_estandar_remuneracion.idxmax()
maxima_remuneracion = df[sector_mayor_variabilidad].max()
minima_remuneracion = df[sector_mayor_variabilidad].min()

# 5. Comparación de la remuneración en sectores de alto y bajo riesgo
sectores_alto_riesgo = df[['explotacion_minas_canteras', 'extr_minerales_metaliferos_explotacion_minas_canteras_ncp']]
sectores_bajo_riesgo = df[['serv_culturales_deportivos_otras_act', 'serv_organizaciones_organos_extraterritoriales']]

promedio_alto_riesgo = sectores_alto_riesgo.mean().mean()
promedio_bajo_riesgo = sectores_bajo_riesgo.mean().mean()

# Resultados
resultado = {
    "Datos Faltantes": datos_faltantes,
    "Estadísticas Resumen": estadisticas_resumen,
    "Promedio Remuneración por Sector": promedio_remuneracion.head(),
    "Sector con Mayor Promedio": sector_mayor_promedio,
    "Mayor Promedio": mayor_promedio,
    "Sector con Mayor Variabilidad": sector_mayor_variabilidad,
    "Máxima Remuneración en Sector con Mayor Variabilidad": maxima_remuneracion,
    "Mínima Remuneración en Sector con Mayor Variabilidad": minima_remuneracion,
    "Promedio Remuneración Alto Riesgo": promedio_alto_riesgo,
    "Promedio Remuneración Bajo Riesgo": promedio_bajo_riesgo,
}

print(resultado)


###############
#### Gráficos con Seaborn


# a)  Gráfico de Disperción (Scatter Plot)
# sns.scatterplot(data=df, x='variable_x' , y='variable_y')


# b) Gráfico de Barras (Bar Plot)
# sns.barplot(data=df, x='categoria', y='valor')


# c) Grafico de Línea (Line Plot)
# sns.lineplot(data=df, x='tiempo', y='valor')


# d) Mapa de calor (Heatmap)
# sns.heatmap(data=correlacion, annot=True, cmap='coolwarm')


# e) Gráfico de Violín (Violin Plot)
# sns.violinplot(data=df, x='categoría', y='valor')


# Pair Plot

#sns.pairplot(df)


##### 
# paletas de colores
# sns.color_palette('pastel')
# Estilos de gráficos
# sns.set_style('whitegrid')
# Temas
# sns.set_theme(style='darkgrid')



# Configuración Inicial
sns.set_theme(style='darkgrid')


# # Gráfico de Barras: Promedio de Remuneración por Sector

# plt.figure(figsize=(12, 6))
# sns.barplot(x=promedio_remuneracion.index, y=promedio_remuneracion.values)
# plt.xticks(rotation=90)
# plt.title("Promedio de Remuneración Neta por Sector")
# plt.xlabel("Sector")
# plt.ylabel("Promedio de Remuneración Neta")
# plt.show()



# # # Gráfico de Violín: Distribución en Sectores con Mayor Variabilidad

# plt.figure(figsize=(8, 6))
# sns.violinplot(y=df[sector_mayor_variabilidad])
# plt.title(f"Distribución de Remuneración en {sector_mayor_variabilidad}")
# plt.xlabel("Remuneración")
# plt.show()


# # Mapa de Calor: Correlación entre Sectores de Alto y Bajo Riesgo

# plt.figure(figsize=(8, 6))
# correlacion = df[sectores_alto_riesgo.columns.union(sectores_bajo_riesgo.columns)].corr()
# sns.heatmap(correlacion, annot=True, cmap="coolwarm")
# plt.title("Correlación entre Sectores de Alto y Bajo Riesgo")
# plt.show()



# # Gráfico de Dispersión (Scatter Plot) con Regresión Lineal

# plt.figure(figsize=(8, 6))
# sns.regplot(data=df, x='explotacion_minas_canteras', y='extr_minerales_metaliferos_explotacion_minas_canteras_ncp')
# plt.title("Relación entre Remuneraciones en Sectores de Minería")
# plt.xlabel("Explotación de Minas y Canteras")
# plt.ylabel("Extracción de Minerales Metalíferos y NCP")
# plt.show()




# # Gráfico de Cajas (Box Plot)

# plt.figure(figsize=(10, 6))
# sns.boxplot(data=sectores_bajo_riesgo)
# plt.title("Distribución de Remuneración en Sectores de Bajo Riesgo")
# plt.xlabel("Sector")
# plt.ylabel("Remuneración")
# plt.xticks(rotation=45)
# plt.show()


# # Pair Plot (Gráfico de Pares)

# plt.figure(figsize=(10, 10))
# sns.pairplot(df[sectores_alto_riesgo.columns.union(sectores_bajo_riesgo.columns)])
# plt.suptitle("Gráfico de Pares entre Sectores de Alto y Bajo Riesgo", y=1.02)
# plt.show()


# # Gráfico de Barras Apiladas

# df_barra_apilada = pd.DataFrame({
#     'Alto Riesgo': promedio_alto_riesgo,
#     'Bajo Riesgo': promedio_bajo_riesgo
# }, index=['Promedio Remuneración'])

# df_barra_apilada.plot(kind='bar', stacked=True, figsize=(8, 6), color=['#1f77b4', '#ff7f0e'])
# plt.title("Comparación de Remuneración entre Sectores de Alto y Bajo Riesgo")
# plt.ylabel("Promedio de Remuneración")
# plt.xticks(rotation=0)
# plt.show()





# # Gráfico de Líneas (Line Plot)

# plt.figure(figsize=(8, 6))
# sns.lineplot(data=df, x=df.index, y='explotacion_minas_canteras')
# plt.title("Tendencia de Remuneración en Explotación de Minas y Canteras")
# plt.xlabel("Índice")
# plt.ylabel("Remuneración")
# plt.show()

