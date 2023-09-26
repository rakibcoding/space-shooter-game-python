from pygame import mixer
import pygame
import random
import math
pygame.font.init()
pygame.mixer.init()

# check pygame version
# print(pygame.__version__)

# Create the screen
screen = pygame.display.set_mode((800, 600))
is_running = True


# Title and Icon
pygame.display.set_caption('Space Invasion')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
background = pygame.image.load('background.jpg')

# Add Music
mixer.music.load('background_music.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# Player variables
img_player = pygame.image.load('rocket.png')
player_x = 362
player_y = 500
player_x_change = 0

# Enemy variables
img_enemy = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
number_of_enemies = 8

for e in range(number_of_enemies):
    img_enemy.append(pygame.image.load('enemy.png'))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 200))
    enemy_x_change.append(0.5)
    enemy_y_change.append(50)

# Bullet variables
img_bullet = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 500
bullet_x_change = 0
bullet_y_change = 2
visible_bullet = False


# Score
score = 0
my_font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

# End of game text
end_font = pygame.font.Font('freesansbold.ttf', 40)


def final_text():
    my_final_font = end_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(my_final_font, (300, 200))


# show score function 
def show_score(x, y):
    text = my_font.render(f'Score : {score}', True, (255, 255, 255))
    screen.blit(text, (x, y))


# Player function
def player(x, y):
    screen.blit(img_player, (x, y))


# Enemy function
def enemy(x, y, en):
    screen.blit(img_enemy[en], (x, y))


# Shoot Bullet function
def shoot_bullet(x, y):
    global visible_bullet
    visible_bullet = True
    screen.blit(img_bullet, (x + 16, y + 10))


# Detect Collision Function
def there_is_a_collision(x_1, y_1, x_2, y_2):
    distance = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))
    if distance < 27:
        return True
    else:
        return False


# Game loop
while is_running:
    # Background Image
    screen.blit(background, (0, 0))

    # Event iteration
    for event in pygame.event.get():
        # Closing Event
        if event.type == pygame.QUIT:
            is_running = False
        # Press arrow key event
        if event.type == pygame.KEYDOWN:
            # print('A key has been pressed')
            if event.key == pygame.K_LEFT:
                # print('Left arrow key pressed')
                player_x_change = - 0.5
            if event.key == pygame.K_RIGHT:
                player_x_change = 0.5
                # print('Right arrow key pressed')

            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound('shot.mp3')
                bullet_sound.play()
                # if visible_bullet == False:
                if not visible_bullet:
                    bullet_x = player_x
                    shoot_bullet(bullet_x, bullet_y)

        # Release key event
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # print('The key was released')
                player_x_change = 0

    # Modify player location
    player_x += player_x_change

    # Keep player inside screen
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # Modify enemy location
    for enm in range(number_of_enemies):
        # End of Game
        if enemy_y[enm] > 500:
            for k in range(number_of_enemies):
                enemy_y[k] = 1000
            final_text()
            break
        enemy_x[enm] += enemy_x_change[enm]

        # Keep enemy inside screen
        if enemy_x[enm] <= 0:
            enemy_x_change[enm] = 0.5
            enemy_y[enm] += enemy_y_change[enm]
        elif enemy_x[enm] >= 736:
            enemy_x_change[enm] = -0.5
            enemy_y[enm] += enemy_y_change[enm]

        # Collision
        collision = there_is_a_collision(
            enemy_x[enm], enemy_y[enm], bullet_x, bullet_y)
        if collision:
            collision_sound = mixer.Sound('punch.mp3')
            collision_sound.play()
            bullet_y = 500
            visible_bullet = False
            score += 1
            # print(score)
            enemy_x[enm] = random.randint(0, 736)
            enemy_y[enm] = random.randint(50, 200)

        enemy(enemy_x[enm], enemy_y[enm], enm)

    # Bullet Movement
    if bullet_y <= -64:
        bullet_y = 500
        visible_bullet = False
    if visible_bullet:
        shoot_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    player(player_x, player_y)

    # Show score
    show_score(text_x, text_y)

    # Update
    pygame.display.update()
