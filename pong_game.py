import pygame
import random
import sys

pygame.init()

#global variables
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
icon = pygame.image.load('ping-pong.png')
pygame.display.set_icon(icon)
font_32 = pygame.font.Font('freesansbold.ttf', 32)
font_24 = pygame.font.Font('freesansbold.ttf', 24)
clock = pygame.time.Clock()
FPS = 120


#main menu
def play():

    class Button():
        
        def __init__(self, color, x, y, width, height, text = ''):
            self.color = color
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.text = text

        def draw(self, screen):
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            
            if self.text != '':
                text = font_24.render(self.text, True, (0, 0, 0))
                screen.blit(text, ((self.x + (self.width/2 - text.get_width()/2), (self.y + (self.height/2 - text.get_height()/2)))))

        def is_over(self, pos):
            if pos[0] > self.x and pos[0] < self.x + self.width:
                if pos[1] > self.y and pos[1] < self.y + self.height:
                    return True
            
            return False
    
    
    
    pvp = Button((255, 255, 255), (WIDTH/2 - 150), (HEIGHT/3 - 50), 250, 100, 'Player vs Player')
    computer = Button((255, 255, 255), (WIDTH/2 - 150), (HEIGHT*2/3 - 50), 250, 100, 'Computer vs Player')

    def redraw():
        screen.fill((0, 0, 0))
        pvp.draw(screen)
        computer.draw(screen)

    while True:
        clock.tick(FPS)
        redraw()
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pvp.is_over(pos):
                    player_vs_player()
                if computer.is_over(pos):
                    computer_vs_player()
            if event.type == pygame.MOUSEMOTION:
                if pvp.is_over(pos):
                    pvp.color = (200, 200, 200)
                else:
                    pvp.color = (255, 255, 255)
                if computer.is_over(pos):
                    computer.color = (200, 200, 200)
                else: 
                    computer.color = (255, 255, 255)
            if event.type == pygame.K_DOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


#game code for player vs player
def player_vs_player():

    class Player():

        def __init__(self, x, y, width, height, speed):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.speed = speed

        def draw(self):
            pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))

    
    class Ball():

        def __init__(self, x, y, width, height, dx, dy, color):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.dx = dx
            self.dy = dy
            self.color = color

        def draw(self):
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        def move(self):
            self.x += self.dx
            self.y += self.dy


    player1 = Player(0, 260, 10, 70, 0)
    player2 = Player(790, 260, 10, 70, 0)
    ball = Ball((WIDTH/2 - 5), (HEIGHT/2 -5), 10, 10, random.choice([-5, 5]), 0, (255, 255, 255))
    score_value1 = 0
    score_value2 = 0
    

    running = True
    while running:
        clock.tick(FPS)
        screen.fill((0, 0, 0))

        #set font of score
        score1 = font_24.render("score: " + str(score_value1), True, (255, 255, 255))
        score2 = font_24.render("score: " + str(score_value2), True, (255, 255, 255))
        winner1 = font_32.render("Player 1 wins!", True, (255, 255, 255))
        winner2 = font_32.render("Player 2 wins!", True, (255, 255, 255))
        screen.blit(score1, ((WIDTH / 4 - score1.get_width() / 2), 10))
        screen.blit(score2, ((WIDTH * 3 / 4 - score2.get_width() / 2), 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_w:
                    player1.speed = -3
                if event.key == pygame.K_s:
                    player1.speed = 3
                if event.key == pygame.K_UP:
                    player2.speed = -3
                if event.key == pygame.K_DOWN:
                    player2.speed = 3
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player1.speed = 0
                if event.key == pygame.K_s:
                    player1.speed = 0
                if event.key == pygame.K_UP:
                    player2.speed = 0
                if event.key == pygame.K_DOWN:
                    player2.speed = 0

        player1.draw()
        player2.draw()
        ball.draw()
        player1.y += player1.speed
        player2.y += player2.speed
        ball.move()
        #boundaries
        if player1.y < 0:
            player1.y = 0
        if player2.y < 0:
            player2.y = 0
        if player1.y > HEIGHT - 70:
            player1.y = HEIGHT - 70
        if player2.y > HEIGHT - 70:
            player2.y = HEIGHT - 70
        #collision
        if player1.x + player1.width == ball.x and player1.y - ball.height < ball.y and player1.y + player1.height + ball.height > ball.y:
            ball.dx *= -1
            ball.dy = random.randrange(-5, 5)
        if player2.x == ball.x and player2.y - ball.height < ball.y and player2.y + player2.height + ball.height > ball.y:
            ball.dx *= -1
            ball.dy = random.randrange(-5, 5)
        if ball.y < 0:
            ball.dy *= -1
        elif ball.y > HEIGHT - ball.height:
            ball.dy *= -1
        #scoring
        if ball.x < 0:
            ball.x = WIDTH/2 - 5
            ball.y = HEIGHT/2 -5
            ball.dx = random.choice([-5, 5])
            ball.dy = 0
            score_value2 += 1
        if ball.x > WIDTH - ball.width:
            ball.x = WIDTH/2 - 5
            ball.y = HEIGHT/2 - 5
            ball.dx = random.choice([-5, 5])
            ball.dy = 0
            score_value1 +=1
        if score_value1 == 5:
            ball.x = WIDTH/2 - ball.width/2
            ball.y = HEIGHT/2 - ball.height/2
            ball.dx = 0
            ball.dy = 0
            ball.color = (0, 0, 0)
            screen.blit(winner1, ((WIDTH/2 - winner1.get_width()/2), (HEIGHT/2 - winner1.get_height() - 20)))
        if score_value2 == 5:
            ball.x = WIDTH/2 - ball.width/2
            ball.y = HEIGHT/2 - ball.height/2
            ball.dx = 0
            ball.dy = 0
            ball.color = (0, 0, 0)
            screen.blit(winner2, ((WIDTH/2 - winner2.get_width()/2), (HEIGHT/2 - winner2.get_height() - 20)))

        pygame.display.update()


#game for computer against the player
def computer_vs_player():

    class Player():

        def __init__(self, x, y, width, height, speed):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.speed = speed

        def draw(self):
            pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))

    
    class Ball():

        def __init__(self, x, y, width, height, dx, dy, color):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.dx = dx
            self.dy = dy
            self.color = color

        def draw(self):
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        def move(self):
            self.x += self.dx
            self.y += self.dy

    def get_final_ball_y():
        y = ball.y + (ball.dy * ((ball.x - player1.width)/abs(ball.dx)))

        if y < 0:
            return abs(y)
        elif y > HEIGHT:
            return 2*HEIGHT - y
        else:
            return y


    player1 = Player(0, 260, 10, 70, 0)
    player2 = Player(790, 260, 10, 70, 0)
    ball = Ball((WIDTH/2 - 5), (HEIGHT/2 -5), 10, 10, random.choice([-5, 5]), 0, (255, 255, 255))
    score_value1 = 0
    score_value2 = 0
    

    running = True
    while running:
        clock.tick(FPS)
        screen.fill((0, 0, 0))

        #set font of score
        score1 = font_24.render("score: " + str(score_value1), True, (255, 255, 255))
        score2 = font_24.render("score: " + str(score_value2), True, (255, 255, 255))
        winner1 = font_32.render("Computer wins!", True, (255, 255, 255))
        winner2 = font_32.render("Player 2 wins!", True, (255, 255, 255))
        screen.blit(score1, ((WIDTH / 4 - score1.get_width() / 2), 10))
        screen.blit(score2, ((WIDTH * 3 / 4 - score2.get_width() / 2), 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_UP:
                    player2.speed = -3
                if event.key == pygame.K_DOWN:
                    player2.speed = 3
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player2.speed = 0
                if event.key == pygame.K_DOWN:
                    player2.speed = 0

        player1.draw()
        player2.draw()
        ball.draw()
        player1.y += player1.speed
        player2.y += player2.speed
        ball.move()
        
        #boundaries
        if player1.y < 0:
            player1.y = 0
        if player2.y < 0:
            player2.y = 0
        if player1.y > HEIGHT - 70:
            player1.y = HEIGHT - 70
        if player2.y > HEIGHT - 70:
            player2.y = HEIGHT - 70
        #collision
        if player1.x + player1.width == ball.x and player1.y - ball.height < ball.y and player1.y + player1.height + ball.height > ball.y:
            ball.dx *= -1
            ball.dy = random.randrange(-5, 5)
        if player2.x == ball.x and player2.y - ball.height < ball.y and player2.y + player2.height + ball.height > ball.y:
            ball.dx *= -1
            ball.dy = random.randrange(-5, 5)
        if ball.y < 0:
            ball.dy *= -1
        elif ball.y > HEIGHT - ball.height:
            ball.dy *= -1
        #scoring
        if ball.x < 0:
            ball.x = WIDTH/2 - 5
            ball.y = HEIGHT/2 -5
            ball.dx = random.choice([-5, 5])
            ball.dy = 0
            score_value2 += 1
        if ball.x > WIDTH - ball.width:
            ball.x = WIDTH/2 - 5
            ball.y = HEIGHT/2 - 5
            ball.dx = random.choice([-5, 5])
            ball.dy = 0
            score_value1 +=1
        #winning
        if score_value1 == 5:
            ball.x = WIDTH/2 - ball.width/2
            ball.y = HEIGHT/2 - ball.height/2
            ball.dx = 0.00000000000000000000001
            ball.dy = 0.00000000000000000000001
            ball.color = (0, 0, 0)
            screen.blit(winner1, ((WIDTH/2 - winner1.get_width()/2), (HEIGHT/2 - winner1.get_height() - 20)))
        if score_value2 == 5:
            ball.x = WIDTH/2 - ball.width/2
            ball.y = HEIGHT/2 - ball.height/2
            ball.dx = 0.00000000000000000000001
            ball.dy = 0.0000000000000000000001
            ball.color = (0, 0, 0)
            screen.blit(winner2, ((WIDTH/2 - winner2.get_width()/2), (HEIGHT/2 - winner2.get_height() - 20)))
        #move computer player
        if ball.dx <= 0:
            if get_final_ball_y() + ball.height/2 < player1.y + player1.height/2:
                player1.speed = -3
            elif get_final_ball_y() + ball.height/2 > player1.y + player1.height/2:
                player1.speed = 3
            else:
                player1.speed = 0
        if ball.dx > 0:
            if player1.y + player1.height/2 > HEIGHT/2:
                player1.speed = -3
            elif player1.y + player1.height/2 < HEIGHT/2:
                player1.speed = 3
            else:
                player1.speed = 0

        pygame.display.update()

play()
