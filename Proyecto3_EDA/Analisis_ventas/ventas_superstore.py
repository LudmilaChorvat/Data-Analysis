import pandas as pd

# Cargar el dataset

df=pd.read_excel('SuperStoreUS-2015.xlsx')

# # Paso 1: Describir el archivo

# # Mostrar las primeras filas para verificar la carga 
# print (df.head())

# # Descrbiri de forma general el dataframe
# print(df.info())

# # Paso 2: Exploracion inicial de los datos

# # Resumen estadístico de las columnas numéricas
# print(df.describe())

# # Verificacion de los valores faltantes
# print(df.isnull().sum())

# print(df.columns)

#Paso 3: Realizar analisis sobre el archivo 

#Calcular las ventas totales o ingresos totales: 

# ingreso_total=df['Ventas'].sum()
# print(f'El ingreso total por parte de las ventas es: ${ingreso_total}')

#Calcular que clase de producto es la que mas influye sobre las ventas totales
#Agrupo los productos segun su categoría y luego sumo todos los valores de sus ventas. 
#Encuentro el máximo. 

# ventas_por_categoria=df.groupby('Categoría de Producto')['Ventas'].sum()

# print(ventas_por_categoria)
# print('-------------------------------------------------------------------')
# categoria_mayor_ventas=ventas_por_categoria.idxmax()
# print(f'La categoría que mas influye sobre las ventas es {categoria_mayor_ventas} con un total de ${ventas_por_categoria.max()}')

#Que region tiene las ventas mas altas? y las mas bajas?
#Agrupamos por región 

# ventas_por_region=df.groupby('Región')['Ventas'].sum()
# print(ventas_por_region)
# print('-------------------------------------------------------------------')

# región_mayor_ventas=ventas_por_region.idxmax()
# print(f'La región con mas ventas es {región_mayor_ventas}, con un total vendido de ${ventas_por_region.max()}')
# print('-------------------------------------------------------------------')

# región_menor_ventas=ventas_por_region.idxmin()
# print(f'La región con mas ventas es {región_menor_ventas}, con un total vendido de ${ventas_por_region.min()}')
# print('-------------------------------------------------------------------')

# 4 Margen de utilidad 
# Margen de utilidad promedio 

# margen_utilidad_promedio=df['Margen Base del Producto'].mean()
# print(f'El margen de utlidad promediop de la tienda es :{margen_utilidad_promedio:,.2F}')
# print('-------------------------------------------------------------------')

# 5 Proyeccion de compras basadas en lo vendido. 
# Para esto nos vamos a basar en los promedios mensuales
# Como vamos a trabajar con tiempo hay que asegurarse que la comuna de fechas esté en formato date time 

df['Fecha de Pedido']=pd.to_datetime(df['Fecha de Pedido'])

# Agrego una columna con el mes y el año del pedido

df['Mes-Año']=df['Fecha de Pedido'].dt.to_period('M')

#Agrupar por mes y calcular la cantidad total vendida

# ventas_mensuales=df.groupby('Mes-Año')['Cantidad Ordenada'].sum()

# #Calcular el promedio de ventas mensuales 

# promedio_ventas_mensual=ventas_mensuales.mean()
# print(f'el promedio de ventas mensuales es : {promedio_ventas_mensual:,.2F} unidades')

# #Proyectar ventas para los proximos 6 meses

# proyeccion=promedio_ventas_mensual*6
# print(f'La proyeccion de ventas para los proximos 6 meses es de: {proyeccion:,.2F} unidades')

# 6 Margen de ganacia por categoría de producto
# Analizar cual es el margen de ganancia por producto en cada categoría para analizar cuales son los mas rentables 
# Agrupo por categoría. Analizo el margen de ganancia promedio 

#
# Analisis de Ventas por Segmentos de Clientes 
# Agrupar los clientes por segmento 
ventas_por_segmento=df.groupby('Segmento de Cliente')['Ventas'].sum()
print(ventas_por_segmento)