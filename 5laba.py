# импортируем модули для работы с сокетами и аргументами командной строки
from socket import *
import threading
import sys

# Запуск
# python 5labseti_res.py 192.168.56.1 6789 HelloWorld.html

# python 5labseti_res.py 192.168.56.1 6789 D:/JS_CSS_HTML/WEBSite/My%20WEBSite/index.html
# http://192.168.56.1:6789/D:/JS_CSS_HTML/WEBSite/My%20WEBSite/index.html

# Функция для обработки запроса от клиента


def handle_request(connectionSocket):
    try:
        # Получаем сообщение от клиента
        message = connectionSocket.recv(1024)

        # Извлекаем имя файла из сообщения
        filename = message.split()[1][1:]

        with open(filename, 'rb') as f:
            outputdata = f.read()

        # Создаем заголовок ответа
        header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: " + \
            str(len(outputdata)) + "\r\n\r\n"

        # Отправляем заголовок ответа на клиент
        connectionSocket.send(header.encode())

        # Отправляем тело ответа (содержимое файла) на клиент
        connectionSocket.send(outputdata)

        # Закрываем соединение с клиентом
        connectionSocket.close()

    # Если произошла ошибка ввода-вывода при открытии файла
    except IOError:
        # Создаем сообщение об ошибке 404 (страница не найдена)
        not_found_msg = "HTTP/1.1 404 Not Found\r\n\r\n"

        # Отправляем сообщение об ошибке на клиент
        connectionSocket.send(not_found_msg.encode())

        # Закрываем соединение с клиентом
        connectionSocket.close()


if len(sys.argv) != 4:
    print("Usage: python server.py <server_host> <server_port> <html_file>")
    sys.exit(1)

# Получаем значения аргументов командной строки
server_host = sys.argv[1]
server_port = int(sys.argv[2])
html_file = sys.argv[3]

# Создаем сокет для сервера
serverSocket = socket(AF_INET, SOCK_STREAM)

# Привязываем сокет к заданному хосту и порту
serverSocket.bind((server_host, server_port))

# Начинаем прослушивание входящих соединений
serverSocket.listen()


print('Готов к обслуживанию...')

# Бесконечный цикл для прослушивания входящих соединений
while True:
    # Принимаем входящее соединение и сохраняем сокет и адрес клиента
    connectionSocket, addr = serverSocket.accept()

    # Создаем новый поток для обработки запроса клиента
    client_thread = threading.Thread(
        target=handle_request, args=(connectionSocket,))

    # Запускаем поток
    client_thread.start()
