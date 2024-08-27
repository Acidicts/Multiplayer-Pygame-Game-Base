import pygame
import socket
import pickle
import threading

# Client configuration
HOST = '127.0.0.1'
PORT = 5555

# Pygame initialization
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Multiplayer")

# Client setup
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

# List to store other players' data
other_players = []

def receive():
    while True:
        try:
            data = client.recv(4096)  # Increased buffer size
            if not data:
                break
            other_players_data = pickle.loads(data)
            other_players.clear()
            other_players.extend(other_players_data)
        except Exception as e:
            print(f"Error receiving data: {str(e)}")
            break

def main():
    clock = pygame.time.Clock()
    running = True

    threading.Thread(target=receive).start()

    local_player = Player(400, 300, (0, 0, 255))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        move_data = {'x': local_player.x, 'y': local_player.y}

        if keys[pygame.K_a]:
            move_data['x'] -= 5
        elif keys[pygame.K_d]:
            move_data['x'] += 5
        if keys[pygame.K_w]:
            move_data['y'] -= 5
        elif keys[pygame.K_s]:
            move_data['y'] += 5

        local_player.x, local_player.y = move_data['x'], move_data['y']
        client.sendall(pickle.dumps(move_data))

        screen.fill(WHITE)
        pygame.draw.rect(screen, local_player.color, (local_player.x, local_player.y, 50, 50))
        for player in other_players:
            pygame.draw.rect(screen, player.color, (player.x, player.y, 50, 50))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()