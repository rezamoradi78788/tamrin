import  threading
import socket

host = '127.0.0.1'
port = 5000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

# Function to handle clients connections

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname}  left the chat room! '.encode('ascii'))
            nicknames.remove(nickname)
            break

# Main function to receive the clients connection

def receive():
    while True:
        print('Server is running and listening...')
        client, address =  server.accept()
        print(f'connection is established with {str(address)}')
        client.send('nickname'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        print(f'The nickname of this client is {nickname}')
        broadcast(f'{nickname} has connected to the chat room! '.encode('ascii'))
        client.send('you are now connected!'.encode('ascii'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

        

receive()