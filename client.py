import socket
import errno # specific error codes
import sys
import time

HEADERSIZE = 10
IP = "25.79.128.177"
PORT = 1234

my_username = input("Username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False) # receive wont be blocking

username = my_username.encode("utf-8")
username_header = f"{len(username):<{HEADERSIZE}}".encode("utf-8")
client_socket.send(username_header + username)


# BURASI SICAKLIK DEĞERLERİNİN SUNUCUYA GÖNDERİLDİĞİ KISIM... SONSUZ DÖNGÜDE (SÜRESİ SANİYEDE 1 VS OLABİLİR.) SÜREKLİ OLARAK SUNUCUYA SICAKLIK GÖNDERİMİ GERÇEKLEŞECEK...
while True:
    time.sleep(1)
    message = "25+Sera Info\n Dilemma \n\n\n\n************\nHumudity:23232\nKonum:12321-N, 123123-E"+"\nSera Adı:  "+my_username

    if message:
        message = message.encode("utf-8")
        message_header = f"{len(message) :< {HEADERSIZE}}".encode("utf-8")
        client_socket.send(message_header + message)

    try:
        while True:
            # receive things
            username_header = client_socket.recv(HEADERSIZE)
            if not len(username_header):
                print("Connection Closed by the Server")
                sys.exit()

            username_length = int(username_header.decode("utf-8").strip())
            # username = client_socket.recv(username_length.decode("utf-8"))
            username = client_socket.recv(username_length)


            message_header = client_socket.recv(HEADERSIZE)
            message_length = int(message_header.decode("utf-8").strip())
            # message = client_socket.recv(message_length.decode("utf-8"))
            message = client_socket.recv(message_length)


            print(f"{username} > {message}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            sys.exit()
        continue

    except Exception as e:
        print('General error', str(e))
        sys.exit()
