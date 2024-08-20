
import mysql.connector
from mysql.connector import Error
from decouple import config

import json

class Producto:
    def __init__(self, nombre, codigo,  precio, cantidad_stock, talle):     #Construyo la clase
        self.__nombre = nombre                                              #Defino los atributos
        self.__codigo=self.validar_codigo(codigo)                           #Con doble guion bajo los atributos son privados para protegerlos
        self.__precio = self.validar_precio(precio)
        self.__cantidad_stock = self.validar_cantidad_stock(cantidad_stock)
        self.__talle= talle

    @property                                                               #Con property defino las propiedades para que puedan ser utilizadas por subclases. Las vuelvo accesibles y tratables. 
    def nombre(self):                                                       # Puedo aplicar tratamientos a la ingo que to deseo devolver.
        return self.__nombre                                                # Por ejemplo, podría devolver el precio de venta y no el precio de costo 
    
    @property
    def codigo(self):
        return self.__codigo
    
    @property
    def precio(self):
        return self.__precio
    
    @property
    def cantidad_stock(self):
        return self.__cantidad_stock
    
    @property
    def talle(self):
        return self.__talle
    
    @codigo.setter
    def codigo(self, nuevo_codigo):
        self.__codigo=self.validar_codigo(nuevo_codigo)
    
    @precio.setter                                                            #Sirve para modificar datos resguardados, por ejemplo el COD 
    def precio(self, nuevo_precio):
        self.__precio = self.validar_precio(nuevo_precio)                     #Creo un nuevo metodo que afecte a el atributo. Ej: Validad_precio
   
    @cantidad_stock.setter
    def cantidad_stock(self, nuevo_stock):
        self.__cantidad_stock=self.validar_cantidad_stock(nuevo_stock)

    def validar_codigo(self, codigo):
        try:
            codigo=str(codigo)
            if len(str(codigo)) > 6:
                raise ValueError("El codigo debe tener el siguiente formato XXX-XX (COD-talle)")
            if len(str(codigo)) < 0:
                raise ValueError("El codigo no puede ser un número negativo")
            return codigo
        except ValueError:
            raise ValueError("El codigo debe ser un numero válido")
        
    def validar_precio(self, precio):
        try:
            precio_art= float(precio)
            if precio_art <= 0:
                raise ValueError("El precio debe ser un valor positivo")
            return round(precio_art,2)
        except ValueError:
            raise ValueError("El precio debe ser un valor numérico.")
    
    def validar_cantidad_stock(self, cantidad_stock):
        try:
            cantidad_stock= int(cantidad_stock)
            if cantidad_stock < 0:
                raise ValueError("La cantidad en stock no puede ser un número negativo")
            return cantidad_stock
        except ValueError:
            raise ValueError("La cantidad en stock debe ser un número válido.")

    def to_dict(self):                                      #Retorna todos los atributos como un diccionario
        return {
            "nombre": self.nombre,
            "codigo":self.codigo,
            "precio": self.precio,
            "cantidad_stock": self.cantidad_stock,
            "talle": self.talle,
        }

    def __str__(self):                                      #Cuando imprime da una cadema de texto con el nombre del articulo y su codigo
        return f"{self.nombre} - COD:{self.codigo}"

class Calzado(Producto):      
    def __init__(self, nombre, codigo, precio, cantidad_stock, talle, color, tipo_calzado):
        super().__init__(nombre, codigo, precio, cantidad_stock, talle)                 #Super (clase superior) se usa para heredar atributos de la clase Productos 
        self.__tipo_calzado = tipo_calzado
        self.__color= color

    @property
    def tipo_calzado(self):
        return self.__tipo_calzado
    
    @property
    def color(self):
        return self.__color

    def to_dict(self):
        data = super().to_dict()                    #Guarda en una variable llamada data la info to dict de la super clase. Llevan parentesisi porque son metods
        data['tipo_calzado'] = self.tipo_calzado            #Agrego las variables que tambien queiro que guarde en el dict
        data['color']= self.color
        return data

    def __str__(self):
        return f"{super().__str__()} - Tipo de calzado: {self.tipo_calzado} y color: {self.color}"

class Bikini(Producto):
    def __init__(self,nombre, codigo, precio, cantidad_stock, talle, estampa, tipo_bikini ):
        super().__init__(nombre, codigo, precio, cantidad_stock, talle)
        self.__tipo_bikini = tipo_bikini
        self.__estampa=estampa

    @property
    def tipo_bikini(self):
        return self.__tipo_bikini
    
    @property
    def estampa(self):
        return self.__estampa

    def to_dict(self):
        data = super().to_dict()
        data['tipo_bikini'] = self.tipo_bikini
        data['estampa']=self.estampa
        return data

    def __str__(self):
        return f"{super().__str__()} - Tipo de Bikini: {self.tipo_bikini} - Color: {self.estampa}"

class Gestion_productos:                                                    #En esta clase se crea el CRUD
    def __init__(self):                                                     #Setea las variables a usar desde el archivo .env. Se usa así para proteger los datos
        self.host = config('DB_host')
        self.database=config('DB_name')
        self.user=config('DB_user')
        self.password=config('DB_password')
        self.port=config('DB_port')

    def connect(self):
        try:
            connection=mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port,
            )
            if connection.is_connected():
                return connection                                         #Establezco la coneccion a la DB y la devuelve para que pueda interactuar con ella. 

        except Error as e:
            print(f'Error al conectar a la base de datos:{e}')
            return None                                                        #Establece coneccion con la base de datos
###
    def leer_datos(self):
        try:
            with open(self.archivo, 'r') as file:                          #abrimos el archivo en forma de lectura como file
                datos = json.load(file)                                    #el load toma el archivo json y disponibiliza para leerlo y modificarlo en py
        except FileNotFoundError:                                          #Si no se encuentra el archivo retorna un diccionario vacío
            return {}
        except Exception as error:
            raise Exception(f'Error al leer datos del archivo: {error}')   #Me dice el error ocurrido
        else:
            return datos

    def guardar_datos(self, datos):
        try:
            with open(self.archivo, 'w') as file:
                json.dump(datos, file, indent=4)                       # dump lo que hace es transofrmar el archivo py a json para poder guardarlo. Con ident digo cuantos espacios separa cada cosa 
        except IOError as error:
            print(f'Error al intentar guardar los datos en {self.archivo}: {error}')
        except Exception as error:
            print(f'Error inesperado: {error}')
###
    def crear_producto(self, producto):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:                                                 #Me permite hacer consultas
                #Verificar si el código del producto existe
                    cursor.execute('select codigo FROM producto WHERE codigo = %s',(producto.codigo,))
                    if cursor.fetchone():                                                               #Si el cursos encuentra una conincidencia:
                        print(f'Error: ya existe producto con COD: {producto.codigo} ')
                        return                                                                          #Interurmpo la ejecucion de l codigo si da error
                 
                #Insertar producto dependiendo del tipo (nombre que usé en el main para referirme a los objetos de la clase Producto)
                    if isinstance(producto,Calzado):                                                     #Chequea si es Calzado
                        query= '''
                        INSERT INTO producto (codigo, nombre, precio, cantidad_stock, talle)
                        VALUES (%s, %s, %s, %s, %s)
                        '''
                        cursor.execute(query, (producto.codigo, producto.nombre, producto.precio, producto.cantidad_stock, producto.talle))

                        query= '''
                        INSERT INTO calzado (codigo, tipo_calzado, color)
                        VALUES (%s, %s, %s)
                        '''
                        cursor.execute (query, (producto.codigo, producto.tipo_calzado, producto.color))

                    elif isinstance(producto, Bikini):
                        query= '''
                        INSERT INTO producto (codigo, nombre, precio, cantidad_stock, talle)
                        VALUES (%s, %s, %s, %s, %s)
                        '''
                        cursor.execute(query, (producto.codigo, producto.nombre, producto.precio, producto.cantidad_stock, producto.talle))

                        query= '''
                        INSERT INTO Bikini (codigo, tipo_bikini, estampa)
                        VALUES (%s, %s, %s)                                      
                        '''
                        cursor.execute (query, (producto.codigo, producto.tipo_bikini, producto.estampa))           #Ver la forma de modificar esto para no repetir codigo. 
                
                    connection.commit()                                                                             #hace la coneccion con la base de datos. MUY IMPORTANTE
                    print (f'producto {producto.nombre} COD: {producto.codigo} creado exitosamente <3 ')
        except Exception as error:
            print(f'Error al crear el producto: {error}')


    def leer_producto(self, codigo):
        try:
            connection=self.connect()                                                             #Con esto me conecto a la DB con el metodo que definó anteriormente para eso
            if connection:
                with connection.cursor(dictionary=True) as cursor:                                 #Con esto creo un cursor que escanee la info
                    cursor.execute('SELECT * FROM producto WHERE codigo = %s',(codigo,))      #Con esto leo todos los codigos
                    producto_data=cursor.fetchone()                                                #En esta variable guardo la info que recopila el fetchone al tomar un codigo
                    
                    if producto_data:
                        cursor.execute('SELECT talle FROM producto WHERE codigo=%s', (codigo, ))   
                        talle=cursor.fetchone()
                        cursor.execute('SELECT precio FROM producto WHERE codigo=%s', (codigo, ))   
                        precio=cursor.fetchone()                                                           #Tengo que diferenciar ahora si es calzado o bikini  
                        cursor.execute('SELECT tipo_calzado FROM calzado WHERE codigo=%s', (codigo, ))
                        tipo_calzado=cursor.fetchone()
                        cursor.execute('SELECT color FROM calzado WHERE codigo=%s', (codigo, ))
                        color=cursor.fetchone()
                        
                        if tipo_calzado and color:
                            producto_data['tipo_calzado']=tipo_calzado['tipo_calzado'] 
                            producto_data['color']=color['color']
                            producto_data['talle']=talle['talle'] 
                            producto_data['precio']=precio['precio']          # ** se usa para pasar todos los atributos de la subclase teniendo en cuenta que tiene formato de diccionario
                            producto=Calzado(**producto_data)                                       
                        else:
                            cursor.execute('SELECT talle FROM producto WHERE codigo=%s', (codigo, ))   
                            talle=cursor.fetchone()
                            cursor.execute('SELECT precio FROM producto WHERE codigo=%s', (codigo, ))   
                            precio=cursor.fetchone()
                            cursor.execute('SELECT tipo_bikini FROM bikini WHERE codigo=%s', (codigo, ))
                            tipo_bikini=cursor.fetchone()
                            cursor.execute('SELECT estampa FROM bikini WHERE codigo=%s', (codigo, ))
                            estampa=cursor.fetchone()
                            
                            if tipo_bikini and estampa:
                                producto_data['tipo_bikini']=tipo_bikini['tipo_bikini']
                                producto_data['estampa']=estampa['estampa']
                                producto_data['talle']=talle['talle'] 
                                producto_data['precio']=precio['precio']
                                producto=Bikini(**producto_data) 
                            else:
                                producto=Producto(**producto_data)
                        print(f'Producto encontrado. {producto}')
                        print('Datos de venta:')
                        print(f'{precio} {talle}')
                        print('----------<3------------')
                   
                    else: 
                        print(f'No se encontró producto con COD: {codigo} :()')
                                                                           
        except Error as e:
            print(f'Error al leer el producto: {e}')        
        finally:
            if connection.is_connected():
                connection.close()

    def actualizar_producto(self, codigo, nuevo_precio):
        try:
            datos = self.leer_datos()
            if str(codigo) in datos:
                 datos[str(codigo)]['precio'] = nuevo_precio
                 self.guardar_datos(datos)
                 print(f'Precio actializado para el producto con código:{codigo}')
            else:
                print(f'No se encontró producto con código:{codigo}')
        except Exception as e:
            print(f'Error al actualizar producto: {e}')

    def eliminar_producto(self, codigo):
        try:
            datos = self.leer_datos()
            if str(codigo) in datos.keys():
                 del datos[str(codigo)]
                 self.guardar_datos(datos)
                 print(f'Producto con COD:{codigo} eliminado correctamente')
            else:
                print(f'No se encontró producto con COD:{codigo}')
        except Exception as e:
            print(f'Error al eliminar el producto: {e}')
    def mostrar_productos(self):
        try:
            datos = self.leer_datos()
            if datos:
                print('=============== Listado de Stock Disponible ==============')
                for codigo, producto_data in datos.items():
                    print(f"COD: {codigo}")
                    print(f"  Nombre: {producto_data['nombre']}")
                    print(f"  Precio: {producto_data['precio']}")
                    print(f"  Cantidad Total: {producto_data['cantidad_stock']}")
                    print(f" Talle: {producto_data['talle']}")
                    print(f" Tipo: {producto_data['tipo']}")
                    print(f" Color: {producto_data['color']}")
                    print(f" Estampa: {producto_data['estampa']}")
                    
                print('=========================<3===============================')
            else:
                print('No hay Stock disponible .')
        except Exception as e:
            print(f'Error : {e}')