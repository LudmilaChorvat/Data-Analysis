import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#Carga del dataset
df=pd.read_csv('personas_2019.csv', sep=';')

###--------Descripcion del archivo------------
# print(df.head())
# print(df.info())
# print(df.isnull().sum())

###--------Análisis del archivo----------------

# Cantidad de personas por sexo.
# Creamos una nueva columna que diferencie los sexos y contamos las personas por sexo.

df['sexo']=df['sexo_id'].map({1: 'Femenino', 2:'Masculino'})
personas_por_sexo=df['sexo'].value_counts()
print('La cantidad de personas por sexo es:')
print(personas_por_sexo)
print('-----------------------------------------------------')

# Promedio de edad 

edad_promedio=df['edad'].mean()
print(f'La edad promedio de las personas dedicadas a la cienca en argentina es: {edad_promedio}')
print('-----------------------------------------------------')

# Número de publicaciones por sexo en el ultimo año

publicaciones_por_sexo=df.groupby('sexo')['producciones_ult_anio'].sum()
print('La cantidad de publicaciones cientificas por sexo es:')
print(publicaciones_por_sexo)
print('-----------------------------------------------------')

# Promedio de publicaciones en los ultimos 4 años

promedio_publicaciones_4anios=df['producciones_ult_4_anios'].mean()
print(f'El promedio de publicaciones por persona en los ultimos 4 años es de: {promedio_publicaciones_4anios}')
print('-----------------------------------------------------')

# Promedio de publicaciones en los ultimos 4 años por rango etario
# Creamos intérvalos etarios:

intervalos_edad=pd.cut(df['edad'], bins=[18, 22, 26, 30, 34, 38, 42, 46, 50, 100], labels=['18-22', '22-26', '26-30', '30-34', '34-38', '38-42', '42-46', '46-50', '50+'])

promedio_publicaciones_4anios_edad=df.groupby(intervalos_edad, observed=False)['producciones_ult_4_anios'].mean()
print('El promedio de publicaciones en los ultimos 4 años por edad es de:')
print(promedio_publicaciones_4anios_edad)
print('-----------------------------------------------------') 

# Promedio de publicaciones por edad y por sexo 

promedio_publicaciones_4anios_edad_sexo=df.groupby([intervalos_edad, 'sexo'], observed=False)['producciones_ult_4_anios'].mean()
print('El promedio de publicaciones en los ultimos 4 años por edad y sexo es de:')
print(promedio_publicaciones_4anios_edad_sexo)
print('-----------------------------------------------------')

# Grafico de distribucion de producciones por edad
filtered_df = df[(df['edad'] >= 18) & (df['edad'] <= 70)]
plt.figure(figsize=(10,6))
sns.histplot(filtered_df['producciones_ult_4_anios'], kde=True, bins=100, element='step', alpha=0.4)
plt.title('Distribución de producciones por rango etario')
plt.xlabel('Edades')
plt.ylabel('Frecuencia')
plt.xlim(18, 50) 
plt.ylim(0, 2000)   
plt.show()


# Cantidad de personas en el área cientifica clasificadas por tipo de personal
# Creamos una nueva columna para asignar valores tipo string a los valores numéricos de referencia para el tipo de personal

df['Tipo de Personal']=df['tipo_personal_id'].map({-1: 'Sin Datos', 1:'Becario', 2:'Otro personal de la Institución', 3:'Investigador', 4:'Docente'})
personas_por_tipo_personal=df['Tipo de Personal'].value_counts()
print('La cantidad de personas por tipo de personal en el área cientifica en el 2019 es de:')
print(personas_por_tipo_personal)
print('-----------------------------------------------------')

# Distribución de tipo de personal por sexo 
personal_por_sexo=df.groupby('sexo')['Tipo de Personal'].value_counts()
print('La distribución del tipo de personal por sexo es:')
print(personal_por_sexo)
print('-----------------------------------------------------')

# Promedio de producciones cientificas en los ultimos 4 años segun el tipo de personal

promedio_publicaciones_4anios_personal=df.groupby('Tipo de Personal', observed=False)['producciones_ult_4_anios'].mean()
print('El promedio de publicaciones en los ultimos 4 años por tipo de personal es de:')
print(promedio_publicaciones_4anios_personal)
print('-----------------------------------------------------')

#Producciones científicas en los ultimos 4 años por tipo de personal 
plt.figure(figsize=(10,6))
sns.countplot(data=df, x='Tipo de Personal', order=df['Tipo de Personal'].value_counts().index, palette='pastel', hue='sexo', legend=True)
plt.title('Producciones Científicas por Grupo de Personal')
plt.xlabel('Grupo')
plt.ylabel('Número de Producciones')
plt.xticks(rotation=0)
plt.show()


# Promedio de publicaciones científicas según el tipo de personal y rango de edades
promedio_publicaciones_4anios_edad_personal=df.groupby([intervalos_edad, 'Tipo de Personal'], observed=False)['producciones_ult_4_anios'].mean()
print('El promedio de publicaciones en los ultimos 4 años por edad y tipo de personal es de:')
print(promedio_publicaciones_4anios_edad_personal)
print('-----------------------------------------------------')

# Clase de cargo docente 

