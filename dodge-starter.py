import pygame
import random
import math

pygame.init()

sc = pygame.display.set_mode((400, 600))
clock = pygame.time.Clock()

# Player (circle)
player_x = 200
player_y = 550
player_radius = 20
player_speed = 5
player_health = 3

score = 0
font = pygame.font.SysFont(None, 36)


# Circle-rectangle collision function
def circle_rect_collision(circle_x, circle_y, radius, rect):
    closest_x = max(rect.left, min(circle_x, rect.right))
    closest_y = max(rect.top, min(circle_y, rect.bottom))

    distance_x = circle_x - closest_x
    distance_y = circle_y - closest_y

    return (distance_x ** 2 + distance_y ** 2) <= radius ** 2


# Enemy Class
class Enemy:
    def __init__(self):
        self.x = random.randint(0, 360)
        self.y = random.randint(-600, 0)
        self.size = 25
        self.speed = random.randint(2, 8)

    def move(self):
        self.y += self.speed

    def reset(self):
        self.x = random.randint(0, 360)
        self.y = 0
        self.speed = random.randint(1, 9)

    def draw(self, su):
        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(su, (255, 0, 0), rect)
        return rect


# Create enemies
enemies = []

for i in range(7):
    enemies.append(Enemy())

running = True

while running:
    sc.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_x -= player_speed

    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Keep player inside screen
    if player_x - player_radius < 0:
        player_x = player_radius
    if player_x + player_radius > 400:
        player_x = 400 - player_radius

    # Enemy updates
    for enemy in enemies:
        enemy.move()

        if enemy.y > 600:
            enemy.reset()
            score += 1

        enemy_rect = enemy.draw(sc)

        if circle_rect_collision(player_x, player_y,
            player_radius, enemy_rect):
            player_health -= 1
            enemy.reset()
        
        if player_health == 0:
            running = False

    # Draw player
    pygame.draw.circle(
        sc, (0, 255, 0), (player_x, player_y),
        player_radius)

    # Draw score
    text = font.render("Score: " + str(score),
        True, (255, 255, 255))

    health = font.render("Health: " + str(player_health),
                         True, (255, 255, 255))

    sc.blit(text, (10, 10))
    sc.blit(health, (10, 50))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
