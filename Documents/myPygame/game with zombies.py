import pygame
import json

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Haunted Mansion")

# Load room images
rooms = {
    "Grand Entrance": pygame.transform.scale(pygame.image.load("images/Grand Entrance.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    "Main Hallway": pygame.transform.scale(pygame.image.load("images/Main Hallway.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    "Dining Room": pygame.transform.scale(pygame.image.load("images/Dining Room.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    "Kitchen": pygame.transform.scale(pygame.image.load("images/Kitchen.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    "Pantry": pygame.transform.scale(pygame.image.load("images/Pantry.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    "Library": pygame.transform.scale(pygame.image.load("images/Library.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    "Study": pygame.transform.scale(pygame.image.load("images/Study.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    "Guest Bedroom": pygame.transform.scale(pygame.image.load("images/Guest Bedroom.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    "Master Bedroom": pygame.transform.scale(pygame.image.load("images/Master Bedroom.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    "Bathroom": pygame.transform.scale(pygame.image.load("images/Bathroom.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    "Ballroom": pygame.transform.scale(pygame.image.load("images/Ballroom.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    "Gallery": pygame.transform.scale(pygame.image.load("images/Gallery.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    "Servants' Quarters": pygame.transform.scale(pygame.image.load("images/Servants Quarters.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    "Wine Cellar": pygame.transform.scale(pygame.image.load("images/Wine Cellar.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    "Basement Storage": pygame.transform.scale(pygame.image.load("images/Basement Storage.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    "Attic": pygame.transform.scale(pygame.image.load("images/Attic.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    "Secret Passage": pygame.transform.scale(pygame.image.load("images/Secret Passage.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    "Torture Chamber": pygame.transform.scale(pygame.image.load("images/Torture Chamber.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    "Garden Courtyard": pygame.transform.scale(pygame.image.load("images/Garden Courtyard.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    "Exit Gate": pygame.transform.scale(pygame.image.load("images/Exit Gate.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
}

room_exits = {
    "Grand Entrance": {"south": "Library", "east": "Main Hallway"},
    "Main Hallway": {"west": "Grand Entrance", "east": "Dining Room", "south": "Study"},
    "Dining Room": {"west": "Main Hallway", "east": "Kitchen", "south": "Guest Bedroom"},
    "Kitchen": {"west": "Dining Room", "east": "Pantry", "south": "Master Bedroom"},
    "Pantry": {"west": "Kitchen", "south": "Bathroom"},

    "Library": {"north": "Grand Entrance", "south": "Ballroom", "east": "Study"},
    "Study": {"north": "Main Hallway", "south": "Gallery", "west": "Library", "east": "Guest Bedroom"},
    "Guest Bedroom": {"north": "Dining Room", "south": "Servants' Quarters", "west": "Study", "east": "Master Bedroom"},
    "Master Bedroom": {"north": "Kitchen", "south": "Wine Cellar", "west": "Guest Bedroom", "east": "Bathroom"},
    "Bathroom": {"north": "Pantry", "south": "Basement Storage", "west": "Master Bedroom"},

    "Ballroom": {"north": "Library", "south": "Attic", "east": "Gallery"},
    "Gallery": {"north": "Study", "south": "Secret Passage", "west": "Ballroom", "east": "Servants' Quarters"},
    "Servants' Quarters": {"north": "Guest Bedroom", "south": "Torture Chamber", "west": "Gallery", "east": "Wine Cellar"},
    "Wine Cellar": {"north": "Master Bedroom", "south": "Garden Courtyard", "west": "Servants' Quarters", "east": "Basement Storage"},
    "Basement Storage": {"north": "Bathroom", "south": "Exit Gate", "west": "Wine Cellar"},

    "Attic": {"north": "Ballroom", "east": "Secret Passage"},
    "Secret Passage": {"north": "Gallery", "west": "Attic", "east": "Torture Chamber"},
    "Torture Chamber": {"north": "Servants' Quarters", "west": "Secret Passage", "east": "Garden Courtyard"},
    "Garden Courtyard": {"north": "Wine Cellar", "west": "Torture Chamber", "east": "Exit Gate"},
    "Exit Gate": {"north": "Basement Storage", "west": "Garden Courtyard"}
}

# Player setup
player = pygame.Rect(400, 300, 40, 40)
player_speed = 1
player_health = 5
font = pygame.font.SysFont(None, 36)

# Doors setup
doors = {}
def create_doors():
    for room, exits in room_exits.items():
        doors[room] = []
        if "north" in exits:
            doors[room].append(("north", pygame.Rect(370, 30, 60, 20)))
        if "south" in exits:
            doors[room].append(("south", pygame.Rect(370, 550, 60, 20)))
        if "west" in exits:
            doors[room].append(("west", pygame.Rect(30, 270, 20, 60)))
        if "east" in exits:
            doors[room].append(("east", pygame.Rect(750, 270, 20, 60)))
create_doors()

# Define room boundaries
wall_thickness = 30
room_bounds = [
    pygame.Rect(0, 0, SCREEN_WIDTH, wall_thickness),
    pygame.Rect(0, SCREEN_HEIGHT - wall_thickness, SCREEN_WIDTH, wall_thickness),
    pygame.Rect(0, 0, wall_thickness, SCREEN_HEIGHT),
    pygame.Rect(SCREEN_WIDTH - wall_thickness, 0, wall_thickness, SCREEN_HEIGHT)
]

# Enemy setup
class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)

    def chase_player(self, player_rect):
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        distance = max(1, (dx**2 + dy**2) ** 0.5)
        speed = player_speed * 0.5
        move_x = speed * dx / distance
        move_y = speed * dy / distance
        self.rect.x += int(move_x)
        self.rect.y += int(move_y)

    def knockback_player(self, player_rect):
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        distance = max(1, (dx**2 + dy**2) ** 0.5)
        knockback = 70
        offset_x = int(knockback * dx / distance)
        offset_y = int(knockback * dy / distance)
        player_rect.x += offset_x
        player_rect.y += offset_y

enemy_rooms = ["Main Hallway", "Ballroom", "Torture Chamber", "Servants' Quarters", "Basement Storage", "Kitchen"]
enemies = {}

for room in enemy_rooms:
    enemies[room] = [
        Enemy(SCREEN_WIDTH // 2 - 30, SCREEN_HEIGHT // 2 - 30),
        Enemy(SCREEN_WIDTH // 2 + 30, SCREEN_HEIGHT // 2 + 30)
    ]

current_room = "Grand Entrance"
running = True

damage_cooldowns = {}  # store cooldowns per enemy

while running:
    screen.blit(rooms[current_room], (0, 0))
    pygame.draw.ellipse(screen, (255, 0, 0), player)

    for direction, door in doors[current_room]:
        pygame.draw.rect(screen, (0, 255, 0), door)

    if current_room in enemies:
        for i, enemy in enumerate(enemies[current_room]):
            enemy.chase_player(player)
            pygame.draw.circle(screen, (0, 200, 0), enemy.rect.center, 15)

            cooldown_key = (current_room, i)
            if cooldown_key not in damage_cooldowns:
                damage_cooldowns[cooldown_key] = 0

            if player.colliderect(enemy.rect) and damage_cooldowns[cooldown_key] == 0:
                player_health -= 1
                enemy.knockback_player(player)
                damage_cooldowns[cooldown_key] = 30
                if player_health <= 0:
                    print("Game Over")
                    running = False

            if damage_cooldowns[cooldown_key] > 0:
                damage_cooldowns[cooldown_key] -= 1

    for wall in room_bounds:
        pygame.draw.rect(screen, (0, 0, 255), wall, 2)

    health_text = font.render(f"Health: {player_health}", True, (255, 255, 255))
    screen.blit(health_text, (10, 10))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    new_x, new_y = player.x, player.y

    if keys[pygame.K_a]:
        new_x -= player_speed
    if keys[pygame.K_d]:
        new_x += player_speed
    if keys[pygame.K_w]:
        new_y -= player_speed
    if keys[pygame.K_s]:
        new_y += player_speed

    temp_rect = pygame.Rect(new_x, new_y, player.width, player.height)
    for wall in room_bounds:
        if temp_rect.colliderect(wall):
            break
    else:
        player.x, player.y = new_x, new_y

    for direction, door in doors[current_room]:
        if player.colliderect(door) and keys[pygame.K_o]:
            next_room = room_exits[current_room][direction]
            current_room = next_room
            if direction == "north":
                player.x, player.y = 400, 500
            elif direction == "south":
                player.x, player.y = 400, 100
            elif direction == "west":
                player.x, player.y = 700, 300
            elif direction == "east":
                player.x, player.y = 100, 300
            break

pygame.quit()