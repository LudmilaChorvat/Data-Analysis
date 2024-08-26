
import mysql.connector
from mysql.connector import Error
from decouple import config



class Producto:
    def __init__(self, nombre, codigo,  precio, cantidad_stock, talle):                               #Construyo la clase
        self.__nombre = nombre                                                                        #Defino los atributos
        self.__codigo=self.validar_codigo(codigo)                                                     #Con doble guion bajo los atributos son privados para protegerlos
        self.__precio = self.validar_precio(precio)
        self.__precio_venta = self.__precio                                                           # Inicializamos el precio de venta igual al precio base
        self.__cantidad_stock = self.validar_cantidad_stock(cantidad_stock)
        self.__talle= talle

    @property                                                                                         #Con property defino las propiedades para que puedan ser utilizadas por subclases. Las vuelvo accesibles y tratables. 
    def nombre(self):                                                                                 # Puedo aplicar tratamientos a la info que yo deseo devolver.
        return self.__nombre                                                                          # Por ejemplo, podría devolver el precio de venta y no el precio de costo 
    
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
        
    
    @precio.setter   #Sirve para modificar datos resguardados, por ejemplo el COD 
    def precio(self, nuevo_precio):
        self.__precio = self.validar_precio(nuevo_precio)  #Creo un nuevo metodo que afecte a el atributo. Ej: Validad_precio
        self.__actualizar_precio_venta()  # Actualizamos el precio de venta cada vez que cambiamos el precio base
    
    # @property
    # def precio_venta(self):
    #     return self.__precio_venta

    # def establecer_incremento(self):
    #     try:
    #         incremento = float(input("Ingrese el porcentaje de incremento (por ejemplo, 10 para 10%): "))
    #         if incremento < 0:
    #             raise ValueError("El porcentaje de incremento no puede ser negativo.")
    #         self.__actualizar_precio_venta(incremento)
    #     except ValueError as e:
    #         print(f"Error: {e}")

    # def __actualizar_precio_venta(self, porcentaje=0):
    #     '''Actualiza el precio de venta según el porcentaje proporcionado'''
    #     self.__precio_venta = self.__precio * (1 + porcentaje / 100)
        # print(f"Precio base: {producto.precio}")
        # print(f"Precio de venta inicial: {producto.precio_venta}")

        # producto.establecer_incremento()  # Solicita al usuario el porcentaje de incremento
        # print(f"Nuevo precio de venta: {producto.precio_venta}")



    @cantidad_stock.setter
    def cantidad_stock(self, nuevo_stock):
        self.__cantidad_stock=self.validar_cantidad_stock(nuevo_stock)

    def validar_codigo(self, codigo):
        try:
            codigo_str = str(codigo)
            if len(str(codigo_str)) not in [5, 6] or codigo_str[3] != '-':
                raise ValueError("El código debe tener el formato XXX-XX")
            return codigo_str
        except ValueError as e:
            raise ValueError(f"Error de validación: {e}")
        
    def validar_precio(self, precio):
        try:
            precio = float(precio)
            if precio <= 0:
                raise ValueError("El precio debe ser un valor positivo")
            return round(precio, 2)
        except ValueError as e:
            raise ValueError(f"Error de validación: {e}")
    
    def validar_cantidad_stock(self, cantidad_stock):
        try:
            cantidad_stock = int(cantidad_stock)
            if cantidad_stock < 0:
                raise ValueError("La cantidad en stock no puede ser un número negativo")
            return cantidad_stock
        except ValueError as e:
            raise ValueError(f"Error de validación: {e}. La cantidad en stock debe ser un número entero no negativo.")

    def to_dict(self): #Retorna todos los atributos como un diccionario
        return {
            "nombre": self.nombre,
            "codigo":self.codigo,
            "precio": self.precio,
            "cantidad_stock": self.cantidad_stock,
            "talle": self.talle,
        }

    def __str__(self):  #Cuando imprime da una cadema de texto con el nombre del articulo y su codigo
        return f"{self.nombre} - COD:{self.codigo}"

class Calzado(Producto):      
    def __init__(self, nombre, codigo, precio, cantidad_stock, talle, color, tipo_calzado):
        super().__init__(nombre, codigo, precio, cantidad_stock, talle)  #Super (clase superior) se usa para heredar atributos de la clase Productos 
        self.__tipo_calzado = tipo_calzado
        self.__color= color

    @property
    def tipo_calzado(self):
        return self.__tipo_calzado
    
    @property
    def color(self):
        return self.__color

    def to_dict(self):
        data = super().to_dict()             #Guarda en una variable llamada data la info to dict de la super clase. Llevan parentesisi porque son metods
        data['tipo_calzado'] = self.tipo_calzado   #Agrego las variables que tambien queiro que guarde en el dict
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

class Gestion_productos:                                                                               #En esta clase se crea el CRUD
    def __init__(self):                                                                                #Setea las variables a usar desde el archivo .env. Se usa así para proteger los datos
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
                return connection                                                                      #Establezco la coneccion a la DB y la devuelve para que pueda interactuar con ella. 

        except Error as e:
            print(f'Error al conectar a la base de datos:{e}')
            return None                                                                                  #Establece coneccion con la base de datos

    def crear_producto(self, producto):
        try:
            connection = self.connect()
            if connection:
             with connection.cursor() as cursor:
                # Verifico si el código del producto existe
                cursor.execute('SELECT codigo FROM producto WHERE codigo = %s', (producto.codigo,))
                if cursor.fetchone():  # Si el cursor encuentra una coincidencia, el codigo ya existe
                    print(f'Error: ya existe producto con COD: {producto.codigo}')
                    return  # Interrumpo la ejecución del código si da error

                # Preparar las consultas para insertar los campos en la tabla general de Producto
                producto_query = 'INSERT INTO producto (codigo, nombre, precio, cantidad_stock, talle) VALUES (%s, %s, %s, %s, %s)'

                # Ejecutar la consulta común e inserto los campos 
                cursor.execute(producto_query, (producto.codigo, producto.nombre, producto.precio, producto.cantidad_stock, producto.talle))

                # Consultas segun el tipo de producto
                if isinstance(producto, Calzado):
                    detalle_query = 'INSERT INTO calzado (codigo, tipo_calzado, color) VALUES (%s, %s, %s)' 
                    cursor.execute(detalle_query, (producto.codigo, producto.tipo_calzado, producto.color))
                
                elif isinstance(producto, Bikini):
                    detalle_query = 'INSERT INTO Bikini (codigo, tipo_bikini, estampa) VALUES (%s, %s, %s)'
                    cursor.execute(detalle_query, (producto.codigo, producto.tipo_bikini, producto.estampa))

                # Confirmo los cambios, conecto a la DB
                connection.commit()
                print('================================== !!!!!==================================')
                print(f'Producto {producto.nombre} COD: {producto.codigo} creado exitosamente <3')
                print('================================== !!!!!==================================')
        except Exception as error:
            print(f'Error al crear el producto: {error}')
        finally:
        # Asegurarse de cerrar la conexión si o si siempre que la establezco al principio. 
            if connection:
             connection.close()


    def leer_producto(self, codigo):
        try:
            connection = self.connect()  # Conecta a la base de datos
            if connection:
             with connection.cursor(dictionary=True) as cursor:
                # Lee la información básica del producto
                cursor.execute('SELECT * FROM producto WHERE codigo = %s', (codigo,))
                producto_data = cursor.fetchone()

                if producto_data:
                    # Consulta detalles 
                    talle = self._get_field(cursor, 'talle', codigo) #El cursor consulta la columna 'tipo_bikini' donde hay coincidencia de código 
                    precio = self._get_field(cursor, 'precio', codigo)
                    
                    # Consultar tipo específico del producto
                    tipo_calzado = self._get_field(cursor, 'tipo_calzado', codigo, 'calzado') #Hago lo mismo pero en la tabla especificada
                    color = self._get_field(cursor, 'color', codigo, 'calzado')
                    
                    if tipo_calzado and color:
                        # Configurar datos para Calzado
                        producto_data.update({
                            'tipo_calzado': tipo_calzado,
                            'color': color,
                            'talle': talle,
                            'precio': precio
                        })
                        producto = Calzado(**producto_data)
                    
                    else:
                        tipo_bikini = self._get_field(cursor, 'tipo_bikini', codigo, 'bikini') 
                        estampa = self._get_field(cursor, 'estampa', codigo, 'bikini')

                        if tipo_bikini and estampa:
                            # Configurar datos para Bikini
                            producto_data.update({
                                'tipo_bikini': tipo_bikini,
                                'estampa': estampa,
                                'talle': talle,
                                'precio': precio
                            })
                            producto = Bikini(**producto_data)
                        
                        else:
                            # Configurar datos para Producto genérico
                            producto_data.update({
                                'talle': talle,
                                'precio': precio
                            })
                            producto = Producto(**producto_data)

                    # Imprimir detalles del producto encontrado
                    print(f'Producto encontrado. {producto}')
                    print('Datos de venta:')
                    print(f'{precio} {talle}')
                    print('----------<3------------')

                else:
                    print(f'No se encontró producto con COD: {codigo} :()')

        except Exception as e:
            print(f'Error al leer el producto: {e}')        
        finally:
         if connection and connection.is_connected():
            connection.close()

    def _get_field(self, cursor, field, codigo, table=None):  #Consulta y devuelve el valor de un campo específico para un código dado. Si se proporciona `table`, consulta en la tabla específica.
        query = f'SELECT {field} FROM producto WHERE codigo=%s'
        if table: #Si se le proporciona un nombre de tabla la consulta tiene la siguiente forma:
            query = f'SELECT {field} FROM {table} WHERE codigo=%s'
        
        cursor.execute(query, (codigo,))
        result = cursor.fetchone()
        return result[field] if result else None

    def leer_productos_por_nombre(self, nombre):    
        try:
            connection = self.connect()  # Conecta a la base de datos
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    # Lee todos los productos con el mismo nombre
                    cursor.execute('SELECT * FROM producto WHERE nombre = %s', (nombre,))
                    productos_data = cursor.fetchall()  # Obtiene todos los productos con el mismo nombre

                    if productos_data:
                        for producto_data in productos_data:
                            # Consulta detalles adicionales
                            codigo = producto_data['codigo'] #A partir de acá vuelvo a manejarme con los codigos asi uso el mismo script 
                            talle = self._get_field(cursor, 'talle', codigo)
                            precio = self._get_field(cursor, 'precio', codigo)
                            cantidad_stock = self._get_field(cursor, 'cantidad_stock', codigo)

                            # Consultar tipo específico del producto
                            tipo_calzado = self._get_field(cursor, 'tipo_calzado', codigo, 'calzado')
                            color = self._get_field(cursor, 'color', codigo, 'calzado')

                            if tipo_calzado and color:
                                # Configurar datos para Calzado
                                producto_data.update({
                                    'tipo_calzado': tipo_calzado,
                                    'color': color,
                                    'talle': talle,
                                    'precio': precio,
                                    'cantidad_stock':cantidad_stock
                                })
                                producto = Calzado(**producto_data)

                            else:
                                tipo_bikini = self._get_field(cursor, 'tipo_bikini', codigo, 'bikini')
                                estampa = self._get_field(cursor, 'estampa', codigo, 'bikini')

                                if tipo_bikini and estampa:
                                    # Configurar datos para Bikini
                                    producto_data.update({
                                        'tipo_bikini': tipo_bikini,
                                        'estampa': estampa,
                                        'talle': talle,
                                        'precio': precio,
                                        'cantidad_stock':cantidad_stock
                                    })
                                    producto = Bikini(**producto_data)

                                else:
                                    # Configurar datos para Producto genérico
                                    producto_data.update({
                                        'talle': talle,
                                        'precio': precio
                                    })
                                    producto = Producto(**producto_data)

                            # Imprimir detalles del producto encontrado
                            print(f'Producto encontrado: {producto}')
                            print('Datos de venta:')
                            print(f'Precio: {precio}')
                            print(f'Talle: {talle}')
                            print(f'Cantidad en stock: {cantidad_stock}')
                            print('----------<3------------')

                    else:
                        print(f'No se encontraron productos con nombre: {nombre} :()')

        except Exception as e:
            print(f'Error al leer los productos: {e}')
        
        finally:
            if connection and connection.is_connected():
                connection.close()

    def _get_field(self, cursor, field, codigo, table=None):
        # Consulta y devuelve el valor de un campo específico para un código dado
        query = f'SELECT {field} FROM producto WHERE codigo=%s'
        if table:  # Si se le proporciona un nombre de tabla
            query = f'SELECT {field} FROM {table} WHERE codigo=%s'
        
        cursor.execute(query, (codigo,))
        result = cursor.fetchone()
        return result[field] if result else None
    

    def actualizar_producto(self, codigo, nuevo_precio):
        try:
            connection=self.connect()
            if connection:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM producto WHERE codigo=%s',(codigo,))
                    if not cursor.fetchone():
                        print(f'No se econtró producto con COD:{codigo}. El producto no existe o el código es incorrecto')
                        return
                    cursor.execute('UPDATE producto SET precio=%s WHERE codigo=%s',(nuevo_precio, codigo))
                    if cursor.rowcount > 0:                                                                         #Rowcont es una funcion que se aplica al cursor para que cuente el numero de columnas  
                        connection.commit() 
                        print ('================================== !!!!!==================================')          
                        print(f'El precio del producto con COD: {codigo} se actualizó correctamente <3')  
                        print ('================================== !!!!!==================================')      
                    else: 
                        print ('================================== !!!!!==================================')      
                        print(f'No se econtró producto con COD:{codigo}') 
                        print ('================================== !!!!!==================================')                                                                       #Aplico los cambios a la DB

        except Exception as e:
            print(f'Error al actualizar producto: {e}')
        finally:
            if connection.is_connected():                #Si le llevó a cabo laconeccion a la base de datos hay que terminarla luego de cada actualización. 
                connection.close()                       #Estos () tienen en cuenta estados o actividades a realizar sobre la coneccion. Si tiene alguna especificacion entre () tiene que estar en DDL como por ejemplo para cursor.execute(.....)

    def eliminar_producto(self, codigo):
        try:
            connection=self.connect()
            if connection:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM producto WHERE codigo=%s',(codigo,))
                    if not cursor.fetchone():
                        print(f'No se econtró producto con COD:{codigo}. El producto no existe o el código es incorrecto')
                        return
                    
                    cursor.execute('DELETE FROM calzado WHERE codigo=%s', (codigo,))
                    cursor.execute('DELETE FROM bikini WHERE codigo=%s', (codigo,))
                    cursor.execute('DELETE FROM producto WHERE codigo=%s', (codigo,))
                    if cursor.rowcount >0: #Si es mayor a cero quiere decir que encontró un producto con ese codigo para borrar entonces recien ahi mando la accion a la DB
                        connection.commit()
                        print ('================================== !!!!!==================================')      
                        print(f'Producto con COD: {codigo} eliminado ')  
                        print ('================================== !!!!!==================================')            
                    else:
                        print(f'No se encontró producto con COD:{codigo}')
 
        except Exception as e:
            print ('================================== !!!!!==================================')      
            print(f'Error al eliminar el producto: {e}')
            print ('================================== !!!!!==================================')      
        finally:
            if connection.is_connected():
                connection.close()
               
    def mostrar_productos(self):
        try:
            connection=self.connect()                                                                                     
            if connection:
                with connection.cursor(dictionary=True) as cursor:                                                        
                    cursor.execute('SELECT * FROM producto') #Con esto leo todos los codigos
                    productos_data=cursor.fetchall()

                    productos=[] #Productos ahora es un diccionario
                    for producto_data in productos_data: #Para cada conjunto de datos de 1 producto entre todos los productos
                        codigo=producto_data['codigo']  #Creo la variable codigo donde se guarda la info del codigo de cada producto extraido de su forma de diccionario
 
                        cursor.execute('SELECT talle FROM producto WHERE codigo=%s', (codigo, ))   
                        talle=cursor.fetchone()
                        cursor.execute('SELECT precio FROM producto WHERE codigo=%s', (codigo, ))   
                        precio=cursor.fetchone() 
                        #Tengo que diferenciar ahora si es calzado o bikini  
                        cursor.execute('SELECT tipo_calzado FROM calzado WHERE codigo=%s', (codigo, ))
                        tipo_calzado=cursor.fetchone()
                        cursor.execute('SELECT color FROM calzado WHERE codigo=%s', (codigo, ))
                        color=cursor.fetchone()
                        
                        if tipo_calzado and color:
                            producto_data['tipo_calzado']=tipo_calzado['tipo_calzado'] 
                            producto_data['color']=color['color']
                            producto_data['talle']=talle['talle'] 
                            producto_data['precio']=precio['precio']                                                     # ** se usa para pasar todos los atributos de la subclase teniendo en cuenta que tiene formato de diccionario
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

                        productos.append(producto)

        except Exception as e:
            print ('================================== !!!!!==================================')      
            print(f'Error al mostrar los productos: {e}')
            print ('================================== !!!!!==================================')      
        else: 
            return productos
        finally:
            if connection.is_connected():
                connection.close()