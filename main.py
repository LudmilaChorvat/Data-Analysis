import os
import platform

from Afrodita_GP import (
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
    print('4. Actualizar producto')
    print('5. Eliminarar producto por codigo')
    print('6. Mostrar todos los productos')
    print('7. Salir')
    print('==========================<3===========================')

def agregar_producto(gestion, tipo_producto):
    try:
        codigo = (input('Ingrese codigo del producto. El codigo debe tener el siguiente formato XXX-XX (COD-talle) '))
        nombre = input('Ingrese nombre del producto: ')
        precio = (input('Ingrese precio del producto: '))
        talle = int(input('Ingrese talle del producto: '))
        cantidad_stock=int(input('Ingrese cantidad de stock del producto: '))

       

        if tipo_producto == '1':
            tipo_calzado = input('Ingrese tipo de calzado (sandalia/bota/zapatilla): ')
            color = input('Ingrese color del producto: ')
            producto = Calzado(nombre, codigo, precio, cantidad_stock, talle, color, tipo_calzado) #tengo que pasarle todos los atributos para que pueda ser ejecutada la clase y quede guardada en la instancia producto
        elif tipo_producto == '2':
            tipo_bikini = input('Ingrese tipo de cbikini (entera/2 partes/ 3 partes): ')
            estampa = (input('Ingrese color del producto: '))
            producto = Bikini(nombre, codigo, precio, cantidad_stock, talle, estampa, tipo_bikini)
        else:
            print('Opción inválida')
            return

        gestion.crear_producto(producto)
        input('Presione enter para continuar...')

    except ValueError as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f'Error inesperado: {e}')

def buscar_producto_por_COD(gestion):
    codigo = input('Ingrese el COD del producto a buscar: ')
    gestion.leer_producto(codigo)
    input('Presione enter para continuar...')

def actualizar_precio_producto(gestion):
    codigo = input('Ingrese el COD del producto para actualizar el precio de venta: ')
    precio =(input('Ingrese el precio del producto'))
    gestion.actualizar_producto(codigo, precio)
    input('Presione enter para continuar...')

def eliminar_producto_por_COD(gestion):
    codigo = input('Ingrese el COD del producto a eliminar: ')
    gestion.eliminar_producto(codigo)
    input('Presione enter para continuar...')

def mostrar_todos_los_productos(gestion):
    gestion.mostrar_productos()
    print('================================<3====================================')
    input('Presione enter para continuar...')

if __name__ == "__main__":
    gestion = Gestion_productos()              #El metodo se ejecuta internamente, ya no requeire del archivo json

    while True:
        mostrar_menu()
        opcion = input('Seleccione una opción: ')

        if opcion == '1' or opcion == '2':
            agregar_producto(gestion, opcion)
        
        elif opcion == '3':
            buscar_producto_por_COD(gestion)

        elif opcion == '4':
            actualizar_precio_producto(gestion)

        elif opcion == '5':
            eliminar_producto_por_COD(gestion)

        elif opcion == '6':
            mostrar_todos_los_productos(gestion)

        elif opcion == '7':
            print('Saliendo del programa...')
            break
        else:
            print('Opción no válida. Por favor, seleccione una opción válida (1-7)')

        
