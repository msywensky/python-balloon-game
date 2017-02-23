import pygame as pg
import sys
from os import path
from person import Person
from movingitems import Rock, Balloon
from pygame.locals import Color, KEYUP, KEYDOWN, K_ESCAPE, \
    K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE, K_RETURN

class Game(object):
    
    def __init__(self):
        self.screen_width = 640
        self.screen_height = 480
        self.initial_angle = 30
        self.frames_per_second = 30
        self.wind = 0
        self.white = Color("white")
        self.red = Color("red")
        self.background = pg.image.load(path.join('images','bg_cropped.png'))


    def new_game(self):
        self.rocks = []
        self.balloons = []
        self.game_over = False
        self.person = Person(self.screen, (self.screen_width / 3, self.screen_height - 65), self.initial_angle)
        self.score = 0
        self.new_balloon_count = 2
        self.generate_balloons(self.new_balloon_count)        

    def update_text(self):
        label = self.font.render("Angle: %s" % self.person.angle, 0, self.white)
        self.screen.blit(label, (50, 80))

        label = self.font.render("Score: %s" % self.score, 0, self.white)
        self.screen.blit(label, (50, 120))

        if self.game_over:
            label = self.font.render("Game Over - Press enter to play again", 0, self.red)
            self.screen.blit(label, (100,200))

    def generate_balloons(self,num):
        for i in range(num):
            self.balloons.append(Balloon(self.screen, 300, 600, self.screen_height - 50, self.screen_height - 20))

    def add_rock(self, velocity):
        rock_x = self.person.x + 32
        rock_y = self.person.y + 3
        self.rocks.append(Rock( self.screen, (rock_x, rock_y), self.person.angle, velocity))


    def run_game(self): 
        # Initialize and set up screen. 
        pg.init() 
        self.font = pg.font.SysFont(None, 40)
        clock = pg.time.Clock()        
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height)) 
        pg.display.set_caption("Balloon Pop") 

        self.new_game()

        new_rock_velocity = 0
        release_slingshot = False
        release_slingshot_completed = False

        # Start main loop. 
        while True: 
            clock.tick(self.frames_per_second)
            keys = pg.key.get_pressed()

            # Start event loop. 
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    sys.exit()

                if e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        sys.exit()

                    if e.key == K_SPACE:
                        new_rock_velocity = 0
                        self.person.aim()

                    if e.key == K_RETURN:
                        print "return pressed"
                        if self.game_over:
                            self.new_game()
                        print "gameOver %s Balloons len: %s.  Score: %s" % (self.game_over, len(self.balloons), self.score)

                if e.type == KEYUP:
                    if e.key == K_SPACE:
                        release_slingshot = True

            if release_slingshot:
                release_slingshot_completed = self.person.fire()
                if release_slingshot_completed:
                    release_slingshot = False
                    self.add_rock(new_rock_velocity)
                    new_rock_velocity = 0

            # holding keys down is outside of event loop
            if keys[K_LEFT]:          
                self.person.move_left(4)

            if keys[K_RIGHT]:
                self.person.move_right(4)

            if keys[K_UP]:
                self.person.increase_angle(2)

            if keys[K_DOWN]:
                self.person.decrease_angle(2)

            if keys[K_SPACE]:
                new_rock_velocity += 3

            
            for balloon in self.balloons:
                if not self.game_over:
                    balloon.update(self.wind)

                    # Game ends when balloon reaches top of screen
                    if balloon.is_offscreen():
                        self.game_over = True

            self.screen.blit(self.background, (0,0))

            if not self.game_over:
                for rock in self.rocks:
                    rock.update(self.wind)
                    if rock.x > self.screen_width or rock.y > self.screen_height:
                        self.rocks.remove(rock)
                    else:
                        temp_balloon = rock.hit_balloon(self.balloons)
                        if temp_balloon == None:
                            rock.draw()
                        else:
                            self.rocks.remove(rock)
                            self.balloons.remove(temp_balloon)
                            self.score += 1
                            if len(self.balloons) == 0:
                                self.new_balloon_count += 1
                                self.generate_balloons(self.new_balloon_count)

                for balloon in self.balloons:
                    balloon.draw()

                self.person.draw()

            # Refresh screen. 
            self.update_text()
            pg.display.flip() 

game = Game()            
game.run_game()