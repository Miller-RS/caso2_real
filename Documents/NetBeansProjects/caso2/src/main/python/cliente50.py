import socket
from multiprocessing import Pool, Barrier


HOST = "192.168.1.7"
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

        print("data que llega del servidor: ", decoded_data)

        self.cliente_recibe(decoded_data)

        print('Respuesta del servidor:', data.decode('utf-8'))

    def enviar_mensaje(self, mensaje):
        try:
            # Enviar datos al servidor
            self.cliente_socket.sendall(mensaje.encode('utf-8'))

            # Esperar la respuesta del servidor
            # respuesta = self.cliente_socket.recv(1024)
            # print('Respuesta del servidor:', respuesta.decode('utf-8'))

        except ConnectionResetError:
            print('Se perdió la conexión con el servidor.')

        finally:
            self.cliente_socket.close()

    def cerrar_conexion(self):
        # Cerrar la conexión del cliente
        self.cliente_socket.close()

    def cliente_recibe(self, data):
        # spliteamos
        # txt = "enviar 7x^1+8x^2 5 10 10000"
        x = data.split(" ")

        print("data spliteada", x[1], x[2], x[3], x[4])
        x[2] = float(x[2])
        x[3] = float(x[3])
        x[4] = int(x[4])
        print("Valores spliteados: ", "min: ",
              x[2], "max: ", x[3], "numero de rectangulos: ", x[4])
        # self.procesar(x[1],x[2],x[3],x[4])
        self.calcular_integral_paralelo(x[1], x[2], x[3], x[4])

    def calcular(self, funcion, x, ancho):  # 7x^1+8x^2
        # Reemplazar la notación de potencia en la expresión
        funcion = funcion.replace('x^', '*x**')  # 7*x**1+8*x**2
        # Reemplazar el valor de x en la expresión
        funcion = funcion.replace('x', str(x))
        # Evaluar la expresión y obtener el resultado
        funcion_x = eval(funcion)
        area = ancho*funcion_x
        # Señalar que este proceso ha terminado su ejecución
        return area

    # Función para calcular la suma de áreas de los rectángulos en paralelo
    def calcular_integral_paralelo(self, funcion, a, b, num_rectangulos):
        pool = Pool()
        ancho = (b-a)/num_rectangulos
        print("Este es el valor del ancho: ", ancho)
        # calculamos x de la izquierda
        xs = [a + ancho*x for x in range(num_rectangulos)]
        print("Valores de X: ", xs)
        print(len(xs))
        results = [pool.apply_async(
            self.calcular, args=(funcion, x, ancho)) for x in xs]

        # barrier = Barrier(num_rectangulos)  # Crear una barrera con el número de procesos

        areas = [result.get() for result in results]
        print("numero de areaas: ", areas)
        # print("X final: ", xs[-1])
        print("estas son las areas de cada proceso: ", areas)
        total_area = sum(areas)
        print("area total: ", total_area)
        print(total_area)
        self.enviar_mensaje("rpta " + str(total_area))


if __name__ == '__main__':

    # Ejemplo de uso
    # Crear instancia del cliente con la IP y el puerto del servidor
    cliente = Client50(HOST, PORT)
    cliente.conectar()  # Conectar al servidor
