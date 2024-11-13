# #######################################
# ## Trabajo con datos de ventas.csv
# #######################################

'''
Ejemplo 1: Filtrado por marca y calcular:
    - Precio Promedio
    - Desviación Estándar
    - Precio Máximo
    - Precio Mínimo
    - Cantidad Total Vendida
    - Ingresos Totales
    - Frecuencia de Ventas
'''
import csv
from collections import defaultdict
import statistics

def analisis_estadistico_ventas(archivo_csv):
    marca_datos=defaultdict (list)                                        #Utilizo defaultdict para acumular los datos por marca 
    try:
        with open(archivo_csv, mode='r', encoding='utf-8') as file: #Abre el archivo csv en modo lectura
            csv_reader=csv.DictReader(file, delimiter=';')          #Creo el objeto que va a leer el archivo csv 
            for row_num, row in enumerate(csv_reader, start=1):     #Itera sobre cada fila del archivo. Enumerate usa el objeto lector.
                try:
                    marca=row['Marca']
                    precio_venta=float(row['precio de venta'])
                    cantidad_vendida=1                              #Asumimos que cada fila corresponde a un producto vendido 
                    
                    #HASTA ACÁ LOGRAMOS QUE EL CODIGO INTERPRETE EL ARCHIVO Y SAQUE LA INFO QUE NOS INTERESA, AHORA TENEMOS QUE DARLE FORMA:
                    marca_datos[marca].append({
                        'precio_venta': precio_venta,
                        'cantidad_vendida': cantidad_vendida,
                        'ingresos': precio_venta * cantidad_vendida
                    })
                except ValueError as e: 
                    print(f'Error de conversion de datos en la fila {row_num}:{e}')
                except KeyError as e: 
                    print(f'Dato faltante en la fila: {row_num}:{e}')
                except Exception as e: 
                    print(f'Error inesperado en la fila: {row_num}:{e}')
        resultados={}                                                                 #creo un diccionario vacío para alamacernar los resultados por marca
        for marca, datos in marca_datos.items():
            precios=[d['precio_venta'] for d in datos]
            cantidades=[d['cantidad_vendida'] for d in datos]
            ingresos = [d['ingresos'] for d in datos]
            
            if len(precios)>1:
                precio_promedio=statistics.mean(precios)
                desviacion_estandar=statistics.stdev(precios)
            else: 
                precio_promedio=precios[0] if precios else 0
                desviacion_estandar= 0 
            
            precio_maximo = max(precios) if precios else 0
            precio_minimo = min(precios) if precios else 0
            cantidad_total_vendida = sum(cantidades)
            ingresos_totales = sum(ingresos)
            frecuencia_ventas = len(datos)                                            #Cantidad de transacciones por marca

            # Almacenar resultados por marca en el diccionario
            resultados[marca] = {
                'Precio Promedio': precio_promedio,
                'Desviación Estándar': desviacion_estandar,
                'Precio Máximo': precio_maximo,
                'Precio Mínimo': precio_minimo,
                'Cantidad Total Vendida': cantidad_total_vendida,
                'Ingresos Totales': ingresos_totales,
                'Frecuencia de Ventas': frecuencia_ventas
            }

    except FileNotFoundError:
        print(f"Archivo no encontrado: {archivo_csv}")
    except csv.Error as e:
        print(f"Error al procesar el archivo CSV: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    else:
        return resultados

# Ejemplo de uso:
if __name__ == "__main__":
    archivo_csv = 'c:/Users/Ludmila/Documents/Análisis de datos/ventas.csv'
    resultados = analisis_estadistico_ventas(archivo_csv)
    
    # Imprimir resultados
    for marca, datos in resultados.items():
        print(f'Marca: {marca}')
        for metrica, valor in datos.items():
            print(f'  {metrica}: {valor:.2f}')
        print() 


                

