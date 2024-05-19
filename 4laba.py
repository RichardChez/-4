from socket import *
import base64  # для кодирования изображения перед его отправкой
import socket  # для создания сетевых соединений
import ssl  # для обеспечения защищенного соединения по протоколу SSL/TLS
# для создания объекта, который содержит сообщение и изображение
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Выбираем почтовый сервер
mailserver = "smtp.gmail.com"
port = 587

# Создаем сокет clientSocket и устанавливаем TCP-соединение
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((mailserver, port))

# Обмен данными между клиентом и сервером с использованием сокета
recv = clientSocket.recv(1024)
print(recv)
if recv[:3] != '220':
    print('код 220 от сервера не получен.')

# Отправляем команду HELO чтобы установить начальное соединение.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('код 250 от сервера не получен.')

# Отправляем команду STARTTLS (для запуска защищенного соединения по протоколу TLS) и выводим ответ сервера.
starttlsCommand = 'STARTTLS\r\n'
clientSocket.send(starttlsCommand.encode())
recv2 = clientSocket.recv(1024).decode()
print(recv2)
if recv2[:3] != '220':
    print('код 220 от сервера не получен.')

# Создаем обычный сокет (устанавливаем SSL-соединение)
clientSocket = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_TLS)

# Отправляем команду HELO после установки SSL-соединения и выводим ответ сервера.
heloCommandSSL = 'HELO Alice\r\n'
clientSocket.send(heloCommandSSL.encode())
recv3 = clientSocket.recv(1024).decode()
print(recv3)
if recv3[:3] != '250':
    print('код 250 от сервера не получен.')

# Отправляем команду AUTH LOGIN и выводим ответ сервера.
authCommand = 'AUTH LOGIN\r\n'
clientSocket.send(authCommand.encode())
recv4 = clientSocket.recv(1024).decode()
print(recv4)
if recv4[:3] != '334':
    print('код 334 от сервера не получен.')

# Отправляем логин и пароль в закодированном виде
login = "ulyagolova@gmail.com"
password = "fjiq dvmo nlmk itvz"
clientSocket.send(base64.b64encode(login.encode()) + b'\r\n')
recv5 = clientSocket.recv(1024).decode()
print(recv5)
if recv5[:3] != '334':
    print('код 334 от сервера не получен.')

clientSocket.send(base64.b64encode(password.encode()) + b'\r\n')
recv6 = clientSocket.recv(1024).decode()
print(recv6)
if recv6[:3] != '235':
    print('код 235 от сервера не получен.')

# Отправляем команду MAIL FROM и выводим ответ сервера.
mailFromCommand = 'MAIL FROM: <ulyagolova@gmail.com>\r\n'
clientSocket.send(mailFromCommand.encode())
recv7 = clientSocket.recv(1024).decode()
print(recv7)
if recv7[:3] != '250':
    print('код 250 от сервера не получен.')

# Отправляем команду RCPT TO и выводим ответ сервера.
rcptToCommand = 'RCPT TO: <ulyagolova@mail.ru>\r\n'
clientSocket.send(rcptToCommand.encode())
recv8 = clientSocket.recv(1024).decode()
print(recv8)
if recv8[:3] != '250':
    print('код 250 от сервера не получен.')

# Отправляем команду DATA и выводим ответ сервера (указание начала передачи текста письма.).
dataCommand = 'DATA\r\n'
clientSocket.send(dataCommand.encode())
recv9 = clientSocket.recv(1024).decode()
print(recv9)
if recv9[:3] != '354':
    print('код 354 от сервера не получен.')

# Создание объекта MIMEMultipart для хранения сообщения
msg = MIMEMultipart()

# Создание объекта MIMEText для текстового сообщения
text = MIMEText("Я люблю компьютерные сети!")

# Добавление текстового сообщения в объект MIMEMultipart
msg.attach(text)

# Открытие изображения в бинарном режиме для чтения
with open("image.jpg", "rb") as f:
    image = MIMEImage(f.read())  # Создание объекта MIMEImage для изображения

# Добавление изображения в объект MIMEMultipart
msg.attach(image)

# Отправка объекта MIMEMultipart как строки на сервер
clientSocket.send(msg.as_string().encode())

endmsg = "\r\n.\r\n"  # Строка, обозначающая конец сообщения

# Сообщение завершается одинарной точкой.
clientSocket.send(endmsg.encode())
recv10 = clientSocket.recv(1024).decode()
print(recv10)
if recv10[:3] != '250':
    print('код 250 от сервера не получен.')

# Отправляем команду QUIT, получаем ответ сервера
quitCommand = 'QUIT\r\n'
clientSocket.send(quitCommand.encode())
recv11 = clientSocket.recv(1024).decode()
print(recv11)
if recv11[:3] != '221':
    print('код 221 от сервера не получен.')

# Закрываем соединение.
clientSocket.close()
