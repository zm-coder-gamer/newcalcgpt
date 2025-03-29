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

current_room = "Grand Entrance"
running = True

while running:
    screen.blit(rooms[current_room], (0, 0))
    pygame.draw.ellipse(screen, (255, 0, 0), player)
    for direction, door in doors[current_room]:
        pygame.draw.rect(screen, (0, 255, 0), door)
    for wall in room_bounds:
        pygame.draw.rect(screen, (0, 0, 255), wall, 2)
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

    # Room Transition
    for direction, door in doors[current_room]:
        if player.colliderect(door) and keys[pygame.K_o]:
            next_room = room_exits[current_room][direction]
            current_room = next_room

            # Seamless entry
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
