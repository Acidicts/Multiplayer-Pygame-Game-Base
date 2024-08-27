import socket
import threading
import pickle

# Server configuration
HOST = '127.0.0.1'
PORT = 5555

# Server setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# List to store connected clients and their respective players
clients = []
players = []

class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

def handle_client(client, addr):
    print(f"New connection from {addr}")
    player = Player(50, 50, (255, 0, 0))  # Starting position and color
    players.append(player)
    clients.append(client)

    while True:
        try:
            data = client.recv(1024)
            if not data:
                print(f"Connection from {addr} closed")
                clients.remove(client)
                players.remove(player)
                client.close()
                break

            received_data = pickle.loads(data)
            player.x, player.y = received_data['x'], received_data['y']

            players_data = pickle.dumps(players)
            for c in clients:
                c.sendall(players_data)
        except Exception as e:
            print(f"Error handling client {addr}: {str(e)}")
            break

def main():
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client, addr))
        client_thread.start()

if __name__ == "__main__":
    main()