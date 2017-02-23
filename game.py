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
        self.show_instructions = True

    def load_sounds(self):
        if not pg.mixer or not pg.mixer.get_init():
            print "load sounds failed 1"
            self.sound_supported = False
            return False
        try:
            self.sound_pop = pg.mixer.Sound(path.join('sounds','pop.ogg'))
            self.music_background = pg.mixer.music.load(path.join('sounds','carnivalrides.ogg'))
            self.sound_supported = True
        except pg.error as er:
            print "load_sounds crashed: %s" % er
            self.sound_supported = False

        return self.sound_supported

    def play_music(self):
        if self.sound_supported:
            pg.mixer.music.play(-1)

    def stop_music(self):
        if self.sound_supported:
            pg.mixer.music.stop()

    def play_bubble_pop(self):
        if self.sound_supported:
            self.sound_pop.play()

    def new_game(self):
        self.rocks = []
        self.balloons = []
        self.game_over = False
        self.show_instructions = False
        self.person = Person(self.screen, (self.screen_width / 3, self.screen_height - 65), self.initial_angle)
        self.score = 0
        self.new_balloon_count = 2
        self.generate_balloons(self.new_balloon_count)        

    def write_text(self, text, x, y, color):
        label = self.font.render(text, 0, color)
        self.screen.blit(label, (x, y))

    def write_instructions(self):
        x = 80
        indent = 20
        y = 100
        lf = 30
        color = Color("green")
        self.write_text("Instructions:", x-indent, y, color)
        y+=lf
        self.write_text("Left/right arrow keys to move", x, y, color)
        y+=lf
        self.write_text("Space to shoot, press longer for further", x, y, color)
        y+=lf
        self.write_text("Up/down keys to change angle", x, y, color)
        y+=lf
        self.write_text("Press enter when ready", x-indent, y, color)
        

    def update_text(self):
        if self.show_instructions:
            self.write_instructions()
        else:
            self.write_text("Angle %s" % self.person.angle, 50, 80, self.white)
            self.write_text("Score: %s" % self.score, 50, 120, self.white)
            if self.game_over:
                self.write_text("Game Over - Press enter to play again", 100, 200, self.red)

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
        self.font = pg.font.SysFont(None, 30)
        clock = pg.time.Clock()        
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height)) 
        pg.display.set_caption("Balloon Pop") 
        self.load_sounds()

        # self.new_game()

        new_rock_velocity = 0
        release_slingshot = False
        release_slingshot_completed = False
        is_playing = False

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

                    if e.key == K_RETURN:
                        if self.show_instructions or self.game_over:
                            is_playing = True
                            self.new_game()

                    if e.key == K_SPACE and is_playing:
                        new_rock_velocity = 0
                        self.person.aim()

                if e.type == KEYUP:
                    if e.key == K_SPACE and is_playing:
                        release_slingshot = True

            # draw background first
            self.screen.blit(self.background, (0,0))

            if is_playing:
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
                            is_playing = False

                if is_playing:
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
                                self.play_bubble_pop()
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