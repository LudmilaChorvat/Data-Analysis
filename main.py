import os
import platform

from Afrodita_GP2 import (
    Calzado,
    Bikini,
    Gestion_productos,
)

def limpiar_pantalla():
    ''' Limpiar la pantalla según el sistema operativo'''
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear') # Para Linux/Unix/MacOs

def mostrar_menu():
    print("========== Menú de Gestión de Productos AFRODITA <3 ==========")
    print('1. Agregar Calzado')
    print('2. Agregar Bikini')
    print('3. Buscar producto por código')
    print('4. Buscar producto por nombre')
    print('5. Actualizar producto')
    print('6. Eliminar producto por código')
    print('7. Mostrar todos los productos')
    print('8. Agregar más stock')  
    print('9. Salir')
    print('==========================<3===========================')

def agregar_producto(gestion, opcion):
    try:
        codigo = input('Ingrese codigo del producto. El codigo debe tener el siguiente formato XXX-XX (COD-talle): ')
        nombre = input('Ingrese nombre del producto: ')
        
        while True:
            try:
                precio = float(input('Ingrese precio de costo del producto: '))
                if precio <= 0:
                    raise ValueError("El precio debe ser mayor que cero.")
                break
            except ValueError as e:
                print(f'Error: {e}. Por favor, ingrese un precio válido.')
        
        talle = input('Ingrese talle del producto: ')
        
        while True:
            try:
                cantidad_stock = int(input('Ingrese cantidad de stock del producto: '))
                if cantidad_stock < 0:
                    raise ValueError("La cantidad de stock no puede ser negativa.")
                break
            except ValueError as e:
                print(f'Error: {e}. Por favor, ingrese una cantidad válida.')
        
        if opcion == '1':
            tipo_calzado = input('Ingrese tipo de calzado (sandalia/bota/zapatilla): ')
            color = input('Ingrese color del producto: ')
            producto = Calzado(nombre, codigo, precio, cantidad_stock, talle, color, tipo_calzado)
            producto.establecer_incremento()  #establecer el incremento
        elif opcion == '2':
            tipo_bikini = input('Ingrese tipo de bikini (entera/2 partes/3 partes): ')
            estampa = input('Ingrese color del producto: ')
            producto = Bikini(nombre, codigo, precio, cantidad_stock, talle, estampa, tipo_bikini)
            producto.establecer_incremento()  

        gestion.crear_producto(producto)
        input('Producto agregado exitosamente. Presione enter para continuar...')

    except ValueError as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f'Error inesperado: {e}')


def buscar_producto_por_COD(gestion):
    codigo = input('Ingrese el COD del producto a buscar: ')
    gestion.leer_producto(codigo)
    input('Presione enter para continuar...')

def buscar_productos_por_nombre(gestion):
    nombre = input('Ingrese el nombre del producto a buscar: ')
    gestion.leer_productos_por_nombre(nombre)
    input('Presione enter para continuar...')

def actualizar_precio_producto(gestion):
    codigo = input('Ingrese el COD del producto para actualizar el precio de venta: ')
    precio =float(input('Ingrese el precio del producto:'))
    gestion.actualizar_producto(codigo, precio)
    input('Presione enter para continuar...')

def eliminar_producto_por_COD(gestion):
    codigo = input('Ingrese el COD del producto a eliminar: ')
    gestion.eliminar_producto(codigo)
    input('Presione enter para continuar...')

def mostrar_todos_los_productos(gestion):
    try:
        productos=gestion.mostrar_productos()
        if productos:
            for producto in productos:
                if isinstance(producto,Calzado):
                    print('________________________________________________________________')
                    print(f'COD:{producto.codigo}, nombre:{producto.nombre}, talle: {producto.talle}, precio:$ {producto.precio}, stock disponible: {producto.cantidad_stock} unidades, tipo: {producto.tipo_calzado}')
                elif isinstance(producto,Bikini):
                    print('________________________________________________________________')
                    print(f'COD:{producto.codigo}, nombre: {producto.nombre}, talle:{producto.talle}, precio:$ {producto.precio}, stock disponible: {producto.cantidad_stock} unidades')
        else:
            print('No hay productos disponibles')
    except Exception as e:
        print(f'Error al mostrar los productos{e}')

    print('================================<3====================================')
    input('Presione enter para continuar...')

def agregar_mas_stock(gestion):
    codigo = input('Ingrese el COD del producto para agregar más stock: ')
    
    while True:
        try:
            nuevo_stock = int(input('Ingrese la cantidad de stock a agregar: '))
            if nuevo_stock <= 0:
                raise ValueError("La cantidad debe ser mayor que cero.")
            break
        except ValueError as e:
            print(f'Error: {e}. Por favor, ingrese una cantidad válida.')
    print('================================<3====================================')
    gestion.agregar_stock(codigo, nuevo_stock)
    input('Stock agregado exitosamente. Presione enter para continuar...')


if __name__ == "__main__":
    gestion = Gestion_productos()              #El metodo se ejecuta internamente, ya no requeire del archivo json

    while True:
        mostrar_menu()
        opcion = input('Seleccione una opción: ')

        if opcion == '1' or opcion == '2':
            agregar_producto(gestion, opcion)
        elif opcion == '8':  
            agregar_mas_stock(gestion)
        elif opcion == '3':
            buscar_producto_por_COD(gestion)

        elif opcion == '5':
            actualizar_precio_producto(gestion)

        elif opcion == '6':
            eliminar_producto_por_COD(gestion)

        elif opcion == '7':
            mostrar_todos_los_productos(gestion)

        elif opcion == '9':
            print('Saliendo del programa...')
            break
        else:
            print('Opción no válida. Por favor, seleccione una opción válida (1-8)')

        
