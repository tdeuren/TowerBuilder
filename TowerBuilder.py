"""This is the game TowerBuilder.
There is a moving block at the top of the screen. If arrow key down is pressed, the block falls down.
You get one point if the block falls on the previous block (except the first block). If the block falls perfectly on the previous one, you get 10 points.
The game stops if the block doesn't fall on the previous block.
The highest score is kept and changes if a new highscore is reached.

Pygame was used for the graphics."""
import pygame
import random


# Standard settings
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)


# Classes
class Block(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('imgs/TowerBuilderblok.png').convert()
        self.rect = self.image.get_rect()
        self.rect.x = 30
        self.rect.y = 30
        self.change_y = 0
        self.change = 1
        self.change_x = 4
        self.change_y2 = 0
    def changespeed(self):
        self.change_y = 4
    def stopmove(self):
        self.change = 0
    def stop(self):
        self.change_y = 0
    def down(self):
        self.change_y = 35
    def moredown(self):
        self.change_y2 = 15
    def givey(self):
        return self.rect.y
    def givex(self):
        return self.rect.x
    def update(self):
        if self.change == 1:
            if self.rect.x <= 30:
                self.change_x = 4
            if self.rect.x >= 420:
                self.change_x = -4
            self.rect.x += self.change_x
            self.rect.y = -3/2420*self.rect.x*self.rect.x+75/121*self.rect.x+1515/121
        self.rect.y += self.change_y + self.change_y2
        if self.change_y > 10:
            self.change_y = 0
        if self.change_y2 > 10:
            self.change_y2 =0

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([500, 10])
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 690
        self.change_y = 0
        self.change_y2 = 0
    def down(self):
        self.change_y = 35
    def moredown(self):
        self.change_y2 = 15
    def update(self):
        self.rect.y += self.change_y + self.change_y2
        self.change_y, self.change_y2 = 0, 0


# Game mechanics
    # Initialiazing
def init(xdisplay, ydisplay, name):
    pygame.init()
    display = pygame.display.set_mode([xdisplay, ydisplay])
    pygame.display.set_caption(name)
    return display

    # User moves
def usermoves(done, done2, block1, state, display):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
            done2 = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                block1.stopmove()
                block1.changespeed()
            elif event.key == pygame.K_SPACE:
                if state == 1:
                    state = 0
                else:
                    state = 1
            elif event.key == pygame.K_r:
                done = False
                done2 = False
                play(display)
    return done, done2, block1, state

    # Background
def backgroundchange(ybackground, backgrounddown, numberbackgrounds, display, background, background2):
    if ybackground%700 == 0 and backgrounddown is True:
        numberbackgrounds += 1
    if backgrounddown is True:
        ybackground += 35
        backgrounddown = False
    for i in range(1, numberbackgrounds):
        display.blit(background, [0, ybackground - i*700])
    display.blit(background2, [0, ybackground])
    return ybackground, backgrounddown, numberbackgrounds

    # If block hits ground
def hitground(hit, block1, tohit, allblocks, ground, block2):
    if hit == 0:
        hits = pygame.sprite.spritecollide(block1, tohit, False)
        if len(hits) > 0:
            block1.stop()
            block2 = block1
            block1 = Block()
            allblocks.add(block1)
            tohit.remove(ground)
            tohit.add(block2)
            hit += 1
    return hit, block1, tohit, allblocks, block2

    # When block goes down
def blockdown(hit, block1, tohit, block2, allblocks, backgrounddown, done):
    if hit > 0:
        hits = pygame.sprite.spritecollide(block1, tohit, False)
        if len(hits) > 0:
            block1.stop()
            tohit.remove(block2)
            if block1.givex() == block2.givex():
                hit += 10
                for i in allblocks:
                    i.moredown()
            block2 = block1
            tohit.add(block2)
            if len(allblocks) > 8:
                for i in allblocks:
                    i.down()
                    backgrounddown = True
            block1 = Block()
            allblocks.add(block1)
            hit += 1
        else:
            if block1.givey() > 720:
                done = False
    return hit, block1, tohit, block2, allblocks, backgrounddown, done

    # Write text
def write(font, text, color, display, place):
    txt = font.render(text, True, color)
    display.blit(txt, place)

    # Read highscore
def readhigh(name):
    with open(name, 'r') as file:
        z = file.read()
        try:
            highscore = int(z)
        except:
            highscore = 0
    return highscore

    # Improve highscore
def improvehigh(name, newhighscore, highscore, score):
    with open(name, 'w') as file:
        if score > highscore:
            file.write(str(score))
            newhighscore = True
        else:
            file.write(str(highscore))
    return newhighscore

# Game loop
def play(display):
    # Names
    background = pygame.image.load('imgs/TowerBuilderachtergrond.png').convert()
    background2 = pygame.image.load('imgs/TowerBuilderachtergrond2.png').convert()
    font = pygame.font.Font("C:/Windows/Fonts/FORTE.TTF", 20)
    font2 = pygame.font.Font("C:/Windows/Fonts/STENCIL.TTF", 40)
    allblocks = pygame.sprite.Group()
    block1 = Block()
    block2 = None
    allblocks.add(block1)
    tohit = pygame.sprite.Group()
    ground = Ground()
    tohit.add(ground)
    allblocks.add(ground)
    backgrounddown = False
    ybackground = 0
    numberbackgrounds = 2
    newhighscore = False
    hit = 0
    clock = pygame.time.Clock()
    time = 0
    done = True
    done2 = True
    state = 1
    # Game
    while done:
        # User moves
        done, done2, block1, state = usermoves(done, done2, block1, state, display)

        # When game plays
        if state == 1:
            
            time += 1

            # Background
            ybackground, backgrounddown, numberbackgrounds = backgroundchange(ybackground, backgrounddown, numberbackgrounds, display, background, background2)

            # Main game mechanics
            hit, block1, tohit, allblocks, block2 = hitground(hit, block1, tohit, allblocks, ground, block2)
            hit, block1, tohit, block2, allblocks, backgrounddown, done = blockdown(hit, block1, tohit, block2, allblocks, backgrounddown, done)

            # Display
            write(font, 'Score: ' + str(hit), green, display,[200, 10])
            allblocks.update()
            allblocks.draw(display)

            # Time between loops
            clock.tick(60)

        # When pause
        else:

            # Display
            display.fill(black)
            write(font2, 'Pause', white, display, [100, 200])
            write(font2, 'Score=' + str(hit), green, display, [10, 350])
            write(font, 'Press r to restart', white, display, [10, 10])

        # Flip display
        pygame.display.flip()
        
    # Highscore
    highscore = readhigh('HighscoreTowerBuilder.txt')
    newhighscore = improvehigh('HighscoreTowerBuilder.txt', newhighscore, highscore, hit)
                
    # End display
    while done2:
        # User moves
        done, done2, block1, state = usermoves(done, done2, block1, state, display)

        # Display
        display.fill(black)
        write(font2, 'Score=' + str(hit), green, display, [10, 300])
        write(font, 'Highscore = ' + str(highscore), white, display, [150, 10])
        write(font, 'Press r to restart', white, display, [10, 50])
        if newhighscore is True:
            write(font, 'New Highscore', green, display, [150, 30])

        # Flip display
        pygame.display.flip()


# Main loop
def main():
    display = init(500, 700, 'Tower Builder')
    play(display)
    pygame.quit()


# Start game
if __name__ == '__main__':
    main()
