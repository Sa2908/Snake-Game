import os
import pygame
import random
pygame.init()
pygame.mixer.init()


white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
SCREENWIDTH = 900
SCREENHEIGHT = 600
FPS = 32 
bgimg = pygame.image.load('back.jpg')
pygame.transform.scale(bgimg, (SCREENWIDTH, SCREENHEIGHT))
snake_x = 45
snake_y = 55
snake_size = 10
velocity_x = 0
velocity_y = 0
init_velocity = 5
food_x = random.randint(20, SCREENWIDTH/2)
food_y = random.randint(20, SCREENHEIGHT/2)
clock = pygame.time.Clock()
score = 0

gameWindow = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("SnakesWithSanket")

pygame.display.update()

exit_game = False
game_over = False


def plot_snake(gameWindow, color, snake_list, snake_size):
    for x,y in snake_list:
        pygame.draw.rect(gameWindow, color, (x, y, snake_size, snake_size))



font = pygame.font.SysFont(None, 55)
def screen_score(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

snake_list = []
snake_length = 1

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(white)
        screen_score("Welcome to Snakes", black, 250, 250)
        screen_score("Press Space To Play", black, 230, 300)
        gameWindow.blit(bgimg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameLoop()
        pygame.display.update()
        clock.tick(32)


def gameLoop():
    if(not os.path.exists("highScore.txt")):
        with open("highScore.txt", "w") as f:
            f.write("0")

    with open("highScore.txt", "r") as f:
        highScore = f.read()

    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snake_list = []
    snake_length = 1

    food_x = random.randint(20, SCREENWIDTH / 2)
    food_y = random.randint(20, SCREENHEIGHT / 2)
    score = 0
    init_velocity = 5
    snake_size = 10
    FPS = 32
    proximity = 6


    while not exit_game:
        if game_over:
            with open("highScore.txt", "w") as f:
                f.write(str(highScore))

            gameWindow.fill(white)
            screen_score("Game Over! Press Enter To Continue", red, 100, 250)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        welcome()
        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x =  init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x =  -init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y =  - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_q:
                        score += 10
                    if event.key == pygame.K_i:
                        proximity += 1

            snake_x += velocity_x
            snake_y += velocity_y
            if abs(snake_x - food_x)<proximity and abs(snake_y - food_y)<proximity:
                score += 1
                # print(score * 10)
                snake_length += 5
                pygame.mixer.music.load('die.wav')
                pygame.mixer.music.play()

                if score>int(highScore):
                    highScore = score

                food_x = random.randint(20, SCREENWIDTH / 2)
                food_y = random.randint(20, SCREENHEIGHT / 2)
            gameWindow.fill(white)
            screen_score(f"Score : {score} High Score : {highScore}", red, 5, 5)
            pygame.draw.rect(gameWindow, red, (food_x, food_y, snake_size, snake_size))


            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)
            plot_snake(gameWindow, black, snake_list, snake_size)

            if len(snake_list)>snake_length:
                del snake_list[0]
            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load('hit.wav')
                pygame.mixer.music.play()

            if snake_x<0 or snake_x>SCREENWIDTH or snake_y<0 or snake_y>SCREENHEIGHT:
                game_over = True
                pygame.mixer.music.load('hit.wav')
                pygame.mixer.music.play()

        clock.tick(FPS)
        pygame.display.update()


    pygame.quit()
    quit()

welcome()