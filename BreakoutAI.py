import pygame
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from random import randint
import pandas as pd
import math
import warnings
import time
import numpy as np
warnings.filterwarnings('ignore', category=UserWarning)
df = pd.read_csv("./training.csv")


X = df[["ballX","velocityX", "velocityY", "angle"]]
y = df["paddleX"]

x_train = X.iloc[:len(X)//2]
y_train = y.iloc[:len(y)//2]
x_test = X.iloc[len(X)//2:]
y_true = y.iloc[len(y)//2:]

mlr = LinearRegression()
mlr.fit(X, y)
# mlr my beloved <3

ballXTrain = 0
velocityTrain=0
angle=0

pygame.init()

WHITE = (255,255,255)
DARKBLUE = (36,90,190)
LIGHTBLUE = (0,176,240)
RED = (255,0,0)
ORANGE = (255,100,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)

score = 0
lives = 5


class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()
    def moveLeft(self, pixels):
        self.rect.x -= pixels
        if self.rect.x < 0:
          self.rect.x = 0
    def moveRight(self, pixels):
        self.rect.x += pixels
        if self.rect.x > 700:
          self.rect.x = 700


class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        if randint(0,1) == 0:
            self.velocity = [-6,6]
        else:
            self.velocity = [6,6]
        #yes i use print statements for debugging
            # what is wrong with you ??????????????? (i do the same thing)
        #print(f"Initial velocity: {self.velocity}", flush=True)
        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
          
    def bounce(self):
        self.velocity[1] = -self.velocity[1]



class Brick(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Breakout Game")

all_sprites_list = pygame.sprite.Group()

#Paddle
paddle = Paddle(LIGHTBLUE, 100, 10)
paddle.rect.x = 350
paddle.rect.y = 560

#Ball
ball = Ball(WHITE,10,10)
ball.rect.x = 400
ball.rect.y = 300


all_bricks = pygame.sprite.Group()
for i in range(8):
    brick = Brick(RED,92,30)
    brick.rect.x = 5 + i* 100
    brick.rect.y = 60
    all_sprites_list.add(brick)
    all_bricks.add(brick)
for i in range(8):
    brick = Brick(ORANGE,92,30)
    brick.rect.x = 5 + i* 100
    brick.rect.y = 100
    all_sprites_list.add(brick)
    all_bricks.add(brick)
for i in range(8):
    brick = Brick(YELLOW,92,30)
    brick.rect.x = 5 + i* 100
    brick.rect.y = 140
    all_sprites_list.add(brick)
    all_bricks.add(brick)
for i in range(8):
    brick = Brick(WHITE,92,30)
    brick.rect.x = 5 + i* 100
    brick.rect.y = 180
    all_sprites_list.add(brick)
    all_bricks.add(brick)



all_sprites_list.add(paddle)
all_sprites_list.add(ball)

carryOn = True
clock = pygame.time.Clock()

#Main Program Loop 
while carryOn:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
              carryOn = False
    
    PADDLE_SPEED = 10 

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.moveLeft(PADDLE_SPEED)
    if keys[pygame.K_RIGHT]:
        paddle.moveRight(PADDLE_SPEED)

    all_sprites_list.update()
    

    #change this variable to get it less often
        # nuh
    if ball.rect.y > 440 and ball.rect.y < 450 and ball.velocity[1] > 0:

        ballXTrain = ball.rect.x
        velocityTrain = ball.velocity[0]
        magnitude = (ball.velocity[0]**2 + ball.velocity[1]**2)**0.5
        angle = math.degrees(math.atan2(ball.velocity[1], ball.velocity[0]))
        # print(f"Ball angle: {angle:.2f}°", flush=True)

        # code of instant pain and suffering
        yhat = mlr.predict([[ball.rect.x, ball.velocity[0], ball.velocity[1], angle]])
        if yhat[0] < 0:
            paddle.rect.x = 0
        if yhat[0] > 700:
            paddle.rect.x = 700
        else:
            paddle.rect.x = yhat[0]

        # model.predict(nyaa)
        # model.predict(nyaa)
        # model.predict(nyaa)
        # model.predict(nyaa)
        # model.predict(nyaa)
    if ball.rect.x>=790:
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x<=0:
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.y>590:
        # ball.velocity[1] = -ball.velocity[1]
        ball.rect.x=400
        ball.rect.y=300
        time.sleep(1)
        lives -= 1
        if lives == 0:
            font = pygame.font.Font(None, 74)
            text = font.render("GAME OVER", 1, WHITE)
            screen.blit(text, (250,300))
            pygame.display.flip()
            carryOn=False

    if ball.rect.y<40:
        ball.velocity[1] = -ball.velocity[1]

    if pygame.sprite.collide_rect(ball, paddle):
        ball.rect.bottom = paddle.rect.top
        ball.bounce()
        train_data = {"ballX": [ballXTrain], "velocityX": [ball.velocity[0]], "velocityY": [ball.velocity[1]], "angle": [angle], "paddleX": [paddle.rect.x]}
        train_df = pd.DataFrame(train_data)
        train_df.to_csv("training.csv", mode='a', header=False, index=False)
        
    
    brick_collision_list = pygame.sprite.spritecollide(ball,all_bricks,False)
    for brick in brick_collision_list:
      ball.bounce()
      score += 1
      brick.kill()
      # NOOOOOOOOOO DONT KILL HIM WHAT DID BRICK DO TO YOUUUUUU
      if len(all_bricks)==0:
            font = pygame.font.Font(None, 74)
            text = font.render("LEVEL COMPLETE", 1, WHITE)
            screen.blit(text, (200,300))
            pygame.display.flip()
            pygame.time.wait(3000)
            carryOn=False


    screen.fill(DARKBLUE)
    pygame.draw.line(screen, WHITE, [0, 38], [800, 38], 2)

    font = pygame.font.Font(None, 34)
    text = font.render("Score: " + str(score), 1, WHITE)
    screen.blit(text, (20,10))
    text = font.render("Lives: " + str(lives), 1, WHITE)
    screen.blit(text, (650,10))

    all_sprites_list.draw(screen)
    pygame.display.flip()
    clock.tick(60)


pygame.quit()

y_pred = mlr.predict(x_test)

mae = mean_absolute_error(y_true, y_pred)
r2 = r2_score(y_true, y_pred)

print("Mean Absolute Error: ", round(mae,3))
print("R2 Score: ", round(r2,3))