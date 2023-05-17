import socket
import multiprocessing
from functools import partial

HOST = "192.168.1.4"
PORT = 4444

class Client50:
    # sum[40] = [0 for i in range(40)]
  
    def __init__(self, ip, puerto):
        self.ip = ip
        self.puerto = puerto
        self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def conectar(self):
        try:
            # Conectar al servidor
            self.cliente_socket.connect((self.ip, self.puerto))
            print('Conexión establecida con el servidor.')

        except ConnectionRefusedError:
            print('No se pudo establecer la conexión con el servidor.')

        data = self.cliente_socket.recv(1024)
        decoded_data = data.decode('utf-8') 

        self.cliente_recibe(decoded_data)

        print('Respuesta del servidor:', data.decode('utf-8'))

    def enviar_mensaje(self, mensaje):
        try:
            # Enviar datos al servidor
            self.cliente_socket.sendall(mensaje.encode('utf-8'))

            # Esperar la respuesta del servidor
            respuesta = self.cliente_socket.recv(1024)
            print('Respuesta del servidor:', respuesta.decode('utf-8'))

        except ConnectionResetError:
            print('Se perdió la conexión con el servidor.')

    def cerrar_conexion(self):
        # Cerrar la conexión del cliente
        self.cliente_socket.close()

    def cliente_recibe(self,data):
      # spliteamos
      # txt = "enviar 7x^1+8x^2 5 10 10000"
      x = data.split(" ")

      print("data spliteada",x[1],x[2],x[3],x[4])
      x[2] = float(x[2])
      x[3] = float(x[3])
      x[4] = int(x[4])
      print("Valores spliteados: ",x[2],x[3],x[4])
      # self.procesar(x[1],x[2],x[3],x[4])
      self.calcular_integral_paralelo(x[1],x[2],x[3],x[4])

    def evaluar_funcion(self, funcion,x):#7x^1+8x^2
      # Reemplazar la notación de potencia en la expresión
      funcion = funcion.replace('x^', '*x**')#7*x**1+8*x**2
      #Reemplazar el valor de x en la expresión
      funcion = funcion.replace('x', str(x))
      # Evaluar la expresión y obtener el resultado
      resultado = eval(funcion)
      return resultado
      #return funcion

    # def evaluar_funcion(self,expresion):
    #   return self.cambio_funcion(expresion)

    def calcular_area(self, base, altura):
      return base * altura

    # Función para calcular la suma de áreas de los rectángulos en paralelo
    def calcular_integral_paralelo(self,expresion,a, b, num_rectangulos):
        # Calcular el ancho de cada rectángulo
        ancho = (b - a) / num_rectangulos
        print("bandera 1")
        # Crear la piscina de procesos
        with multiprocessing.Pool() as pool:
            print("bandera 2")
            # Calcular las alturas de los rectángulos en paralelo
            evaluar_funcion_parcial = partial(self.evaluar_funcion, expresion=expresion)#7x^1+8x^2

            alturas = pool.map(evaluar_funcion_parcial, [a + i * ancho for i in range(num_rectangulos)])

        print("bandera 3")
        # Calcular las áreas de los rectángulos en paralelo
        areas = pool.starmap(self.calcular_area, [(ancho, altura) for altura in alturas])

        # Calcular la suma total de las áreas de los rectángulos
        suma_areas = sum(areas)

        print(suma_areas)
        return suma_areas

# Ejemplo de uso
cliente = Client50(HOST, PORT)  # Crear instancia del cliente con la IP y el puerto del servidor
cliente.conectar()  # Conectar al servidor




