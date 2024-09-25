import mysql.connector
from mysql.connector import Error
from decouple import config


class Producto:
    #Construyo la clase
    def __init__(self, nombre, codigo,  precio, cantidad_stock, talle):        
        #Defino los atributos                       
        self.__nombre = nombre                                                                       
        self.__codigo=self.validar_codigo(codigo)                                                     #Con doble guion bajo los atributos son privados para protegerlos
        self.__precio = self.validar_precio(precio)
        self.__precio_venta = self.__precio                                                           # Inicializo el precio de venta igual al precio base luego de ser validado
        self.__cantidad_stock = self.validar_cantidad_stock(cantidad_stock)
        self.__talle= talle
    #Con property defino las propiedades para que puedan ser utilizadas por subclases. Las vuelvo accesibles y tratables. 
    @property                                                                                         
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
        self.__actualizar_precio_venta()                   # Actualizamos el precio de venta cada vez que cambiamos el precio base
    
    @property
    def precio_venta(self):
        return self.__precio_venta

    def establecer_incremento(self):
        try:
            incremento = float(input('Ingrese el porcentaje de incremento (por ejemplo, 30 para 30%): '))
            if incremento < 0:
                raise ValueError('El porcentaje de incremento no puede ser negativo.')
            self.__actualizar_precio_venta(incremento)
        except ValueError as e:
            print(f'Error: {e}')

    def __actualizar_precio_venta(self, incremento=0):
        #Actualiza el precio de venta según el porcentaje proporcionado
        self.__precio_venta = self.precio * (1 + incremento / 100)
        print(f"Precio base: {self.precio}")
        print(f"Precio de venta: {self.precio_venta}")

    def establecer_incremento(self):
        try:
            incremento = float(input('Ingrese el porcentaje de incremento (por ejemplo, 30 para 30%): '))
            if incremento < 0:
                raise ValueError('El porcentaje de incremento no puede ser negativo.')
            
            # Actualizamos el precio de venta
            self.__actualizar_precio_venta(incremento)

        except ValueError as e:
            print(f'Error: {e}')

    

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
        data = super().to_dict()                   #Guarda en una variable llamada data la info to dict de la super clase. Llevan parentesis porque son methods
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
            return None   
    def crear_producto(self, producto):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT codigo FROM producto WHERE codigo = %s', (producto.codigo,))
                    if cursor.fetchone():
                        print(f'Error: ya existe producto con COD: {producto.codigo}')
                        return

                    producto_query = 'INSERT INTO producto (codigo, nombre, precio, cantidad_stock, talle) VALUES (%s, %s, %s, %s, %s)'
                    cursor.execute(producto_query, (producto.codigo, producto.nombre, producto.precio, producto.cantidad_stock, producto.talle))

                    if isinstance(producto, Calzado):
                        detalle_query = 'INSERT INTO calzado (codigo, tipo_calzado, color) VALUES (%s, %s, %s)' 
                        cursor.execute(detalle_query, (producto.codigo, producto.tipo_calzado, producto.color))
                    
                    elif isinstance(producto, Bikini):
                        detalle_query = 'INSERT INTO bikini (codigo, tipo_bikini, estampa) VALUES (%s, %s, %s)'
                        cursor.execute(detalle_query, (producto.codigo, producto.tipo_bikini, producto.estampa))

                    connection.commit()
                    print(f'Producto {producto.nombre} COD: {producto.codigo} creado exitosamente <3')
        except Exception as error:
            print(f'Error al crear el producto: {error}')
        finally:
            if connection:
                connection.close()

    def leer_producto(self, codigo):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute('SELECT * FROM producto WHERE codigo = %s', (codigo,))
                    producto_data = cursor.fetchone()

                    if producto_data:
                        detalle = self._obtener_detalle_producto(cursor, codigo)           # Para obtener los detalles del producto utilizo un método auxiliar
                        producto_data.update(detalle)                                      # Luego de leer los detalles, actualizo la info del producto

                        if 'tipo_calzado' in detalle:
                            producto = Calzado(**producto_data)                            # ** se usa para desempaquetar el diccionario en argumentos de palabra clave
                        elif 'tipo_bikini' in detalle:                                     # es decir, accede a la info por ejemplo talle=38, color=negro, etc. 
                            producto = Bikini(**producto_data)
                        else:
                            producto = Producto(**producto_data)

                        print(f'Producto encontrado: {producto}')
                        print('Datos de venta:')
                        print(f'Precio: {producto.precio}')
                        print(f'Talle: {producto.talle}')
                        print(f'Cantidad en stock: {producto.cantidad_stock}')
                    else:
                        print(f'No se encontró producto con COD: {codigo}')
        except Exception as e:
            print(f'Error al leer el producto: {e}')
        finally:
            if connection and connection.is_connected():
                connection.close()

    def _obtener_detalle_producto(self, cursor, codigo):                                                #Método auxiliar para obtener los detalles desde la DB
        detalle = {}                                                                                    #Diccionario vacio para almacenar los detalles
        for tabla, campos in [('calzado', ['tipo_calzado', 'color']), ('bikini', ['tipo_bikini', 'estampa'])]:     #La tupla indica la tabla y los camposa  los que accede
            for campo in campos:
                cursor.execute(f'SELECT {campo} FROM {tabla} WHERE codigo = %s', (codigo,))
                resultado = cursor.fetchone()
                if resultado:
                    detalle[campo] = resultado[campo]                                                   #Si el resultado no es vacío, se agrega el campo y su valor  al diccionario 
        return detalle

    def leer_productos_por_nombre(self, nombre):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute('SELECT * FROM producto WHERE nombre = %s', (nombre,))
                    productos_data = cursor.fetchall()

                    if productos_data:
                        for producto_data in productos_data:
                            detalle = self._obtener_detalle_producto(cursor, producto_data['codigo'])
                            producto_data.update(detalle)

                            if 'tipo_calzado' in detalle:
                                producto = Calzado(**producto_data)
                            elif 'tipo_bikini' in detalle:
                                producto = Bikini(**producto_data)
                            else:
                                producto = Producto(**producto_data)

                            print(f'Producto encontrado: {producto}')
                            print(f'Datos de venta:')
                            print(f'Precio: {producto.precio}')
                            print(f'Talle: {producto.talle}')
                            print(f'Cantidad en stock: {producto.cantidad_stock}')
                    else:
                        print(f'No se encontraron productos con nombre: {nombre}')
        except Exception as e:
            print(f'Error al leer productos por nombre: {e}')
        finally:
            if connection and connection.is_connected():
                connection.close()

    def actualizar_producto(self, codigo, nuevo_precio):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    # Verifica si el producto existe
                    cursor.execute('SELECT * FROM producto WHERE codigo = %s', (codigo,))
                    producto = cursor.fetchone()

                    if producto:
                        # Actualiza el precio si encuentra un producto con el cursor
                        cursor.execute('UPDATE producto SET precio = %s WHERE codigo = %s', (nuevo_precio, codigo))
                        connection.commit()
                        print(f'El precio del producto con COD: {codigo} se actualizó exitosamente a ${nuevo_precio}.')
                    else:
                        print(f'No se encontró producto con COD: {codigo}.')
        except Exception as e:
            print(f'Error al actualizar el producto: {e}')
        finally:
            if connection and connection.is_connected():
                connection.close()

    def mostrar_productos(self):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute('SELECT * FROM producto')
                    productos_data = cursor.fetchall()
                
                    productos=[]
                    if productos_data:
                        for producto_data in productos_data:
                            detalle = self._obtener_detalle_producto(cursor, producto_data['codigo'])
                            producto_data.update(detalle)

                            if 'tipo_calzado' in detalle:
                                producto = Calzado(**producto_data)
                            elif 'tipo_bikini' in detalle:
                                producto = Bikini(**producto_data)
                            else:
                                producto = Producto(**producto_data)

                            productos.append(producto)
                        return productos 
                    else:
                        print('No se encontraron productos en la base de datos.')
        except Exception as e:
            print(f'Error al mostrar productos: {e}')
        finally:
            if connection and connection.is_connected():
                connection.close()

    def agregar_stock(self, codigo, cantidad_a_agregar):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT cantidad_stock FROM producto WHERE codigo = %s', (codigo,))
                    producto = cursor.fetchone()

                    if producto:
                        nuevo_stock = int(producto[0]) + cantidad_a_agregar  # Suma el nuevo stock al existente
                        cursor.execute('UPDATE producto SET cantidad_stock = %s WHERE codigo = %s', (nuevo_stock, codigo))
                        connection.commit()
                        print(f'Se agregó {cantidad_a_agregar} unidades al producto con COD: {codigo}. Nuevo stock: {nuevo_stock}.')
                    else:
                        print(f'No se encontró producto con COD: {codigo}.')
        except Exception as e:
            print(f'Error al agregar stock: {e}')
        finally:
            if connection and connection.is_connected():
                connection.close()


    def eliminar_producto(self, codigo):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM producto WHERE codigo = %s', (codigo,))
                    producto = cursor.fetchone()

                    if producto:
                        # Hay que eliminar primero el producto de las tablas hijas para que no de error debido a la relacion entre ellas con la foreign key
                        cursor.execute('DELETE FROM calzado WHERE codigo = %s', (codigo,))
                    
                        cursor.execute('DELETE FROM bikini WHERE codigo = %s', (codigo,))
                        
                        # Despues elimina de la tabla producto
                        cursor.execute('DELETE FROM producto WHERE codigo = %s', (codigo,))
                        connection.commit()
                        print(f'Producto con COD: {codigo} eliminado exitosamente <3')

                    else:
                        print('No existe producto con COD:{codigo} :( ')
        
        except Exception as e:
            print(f'Error al eliminar el producto: {e}')
        finally:
            if connection and connection.is_connected():
                connection.close()
