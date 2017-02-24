import pygame as pg
import sys
from os import path
from person import Person
from movingitems import Rock, Balloon
from pygame.locals import Color, KEYUP, KEYDOWN, K_ESCAPE, K_s,\
    K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE, K_RETURN

class Game(object):
    """Primary class of the application.  
    """

    def __init__(self):
        """Constructor class.  This is executed when an instance of the class is created
        """
        self.screen_width = 800
        self.screen_height = 480
        self.initial_angle = 30
        self.frames_per_second = 60
        self.wind = 0
        self.white = Color("white")
        self.red = Color("red")
        self.green = Color("green")
        self.background = pg.image.load(path.join('images','bg_cropped.png'))
        self.show_instructions = True
        self.sound_on = True
        self.game_over = False

    def load_sounds(self):
        """Method that loads the background and sound files.
        The sound_supported property is also initialized.  
        """
        if not pg.mixer or not pg.mixer.get_init():
            print "load mixer failed"
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
        """Starts playing the background music
        """
        if self.sound_supported and self.sound_on and not (self.game_over or self.show_instructions):
            pg.mixer.music.play(-1)

    def stop_music(self):
        """Stops the background music
        """
        if self.sound_supported:
            pg.mixer.music.stop()

    def play_pop_sound(self):
        """Plays the sound of a balloon being popped
        """
        if self.sound_supported and self.sound_on:
            self.sound_pop.play()

    def toggle_sound(self):
        """Turns all sounds and music in the app on or off
        Toggles the sound_on property
        """
        if self.sound_on:
            self.sound_on = False
            self.stop_music()
        else:
            self.sound_on = True
            self.play_music()

    def new_game(self):
        """Starts a new game.  
        Balloons and Rocks from the previous game are discarded.
        A new Person object is created.
        Score is reset.
        New balllons for level 1 are created
        """
        self.rocks = []
        self.balloons = []
        self.game_over = False
        self.show_instructions = False
        self.person = Person(self.screen, (self.screen_width / 3, self.screen_height - 65), self.initial_angle)
        self.score = 0
        self.new_balloon_count = 2
        self.generate_balloons(self.new_balloon_count) 
        self.play_music()       

    def write_text(self, text, x, y, color):
        """Convenience method for writing text to the screen
        """
        label = self.font.render(text, 0, color)
        self.screen.blit(label, (x, y))

    def write_instructions(self):
        """Write the instructions to the screen
        """
        x = 80
        indent = 20
        y = 100
        lf = 30
        
        self.write_text("Instructions:", x-indent, y, self.green)
        y+=lf
        self.write_text("Left/right arrow keys to move", x, y, self.green)
        y+=lf
        self.write_text("Space to shoot, press longer for further", x, y, self.green)
        y+=lf
        self.write_text("Up/down keys to change angle", x, y, self.green)
        y+=lf
        self.write_text("Press S to toggle sound", x, y, self.green)
        y+=lf
        self.write_text("Press enter when ready", x-indent, y, self.green)
        

    def update_text(self):
        """Updates all text on the screen.  
        This is called once at the bottom of the program loop.
        """
        if self.show_instructions:
            self.write_instructions()
        else:
            self.write_text("Angle %s" % self.person.angle, 50, 80, self.white)
            self.write_text("Score: %s" % self.score, 50, 120, self.white)
            if self.game_over:
                self.write_text("Game Over - Press enter to play again", 100, 200, self.red)
        if not self.sound_on:
            self.write_text("sound off", self.screen_width / 2 - 4, 50 , Color("blue"))

    def generate_balloons(self,num):
        """Generates a new set of balloons.
        This is called at the beginning of a new game, and when all previous balloons have been popped
        """
        xLow = self.screen_width / 2
        xHigh = self.screen_width - 20
        yLow = self.screen_height - 100
        yHigh = self.screen_height - 50
        for i in range(num):
            self.balloons.append(Balloon(self.screen, xLow, xHigh, yLow, yHigh))

    def add_rock(self, velocity):
        """Throw a rock
        """
        rock_x = self.person.x + 32
        rock_y = self.person.y + 3
        self.rocks.append(Rock( self.screen, (rock_x, rock_y), self.person.angle, velocity))


    def run_game(self): 
        """The method that contains the main event loop
        """

        # Initialize and set up screen. 
        pg.init() 
        self.font = pg.font.SysFont(None, 30)
        clock = pg.time.Clock()        
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height)) 
        pg.display.set_caption("Balloon Pop") 
        self.load_sounds()

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

                # Window was closed, clean up
                if e.type == pg.QUIT:
                    sys.exit()

                if e.type == KEYDOWN:

                    # Esc key was pressed, quit the app
                    if e.key == K_ESCAPE:
                        sys.exit()

                    # Enter key was pressed, start a new game if not in a game
                    if e.key == K_RETURN:
                        if self.show_instructions or self.game_over:
                            is_playing = True
                            self.new_game()

                    # Space bar pressed down, start the slingshot sequence
                    if e.key == K_SPACE and is_playing:
                        new_rock_velocity = 0
                        self.person.aim()

                    # s key was pressed, toggle the sound
                    if e.key == K_s:
                        self.toggle_sound()

                if e.type == KEYUP:
                    # Space bar was released
                    # Complete the throwing sequence
                    if e.key == K_SPACE and is_playing:
                        release_slingshot = True

            # draw background first
            # this will overwrite everything that was previously on the screen
            # all other items and text will need to be redrawn after this
            self.screen.blit(self.background, (0,0))

            if is_playing:
                # Begin the slingshot release sequence
                if release_slingshot:

                    # There are multiple images to release the rock
                    release_slingshot_completed = self.person.fire()
                    if release_slingshot_completed:
                        release_slingshot = False
                        # Release the rock to begin it's journey
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
                    # longer the space bar is held, the faster the rock will be thrown
                    new_rock_velocity += 1.5

                # Loop through the list of balloons
                for balloon in self.balloons:
                    if not self.game_over:
                        # Update the balloon's coordinates
                        balloon.update(self.wind)

                        # Game ends when balloon reaches top of screen
                        if balloon.is_offscreen():
                            self.game_over = True
                            is_playing = False
                            self.stop_music()

                if is_playing:
                    # Loop through the list of thrown rocks on the screen
                    for rock in self.rocks:
                        # Update the rock's coordinates
                        rock.update(self.wind)

                        # remove rocks that fall off the bottom or sides of the screen
                        # rocks that go straight up (less than 0) are not removed, since they will come down
                        if rock.x > self.screen_width or rock.y > self.screen_height:
                            self.rocks.remove(rock)
                        else:
                            # Get the balloon that was hit (hopefully) or get None
                            temp_balloon = rock.hit_balloon(self.balloons)
                            if temp_balloon == None:
                                # Rock is still on the screen and did not hit a balloon
                                # Add it to the screen
                                rock.draw()
                            else:
                                # Rock hit a balloon
                                # Remove the rock from the Rocks list
                                self.rocks.remove(rock)

                                # Remove the popped balloon from the Balloons list
                                self.balloons.remove(temp_balloon)

                                # Play the pop sound and increase the score
                                self.play_pop_sound()
                                self.score += 1

                                # Level ends when there are no balloons left to display
                                if len(self.balloons) == 0:
                                    # Generate a new set of balloons
                                    # One more balloon than the last level
                                    self.new_balloon_count += 1
                                    self.generate_balloons(self.new_balloon_count)

                    # Add the balloons to the screen
                    for balloon in self.balloons:
                        balloon.draw()

                    # Add the person to the screen
                    self.person.draw()

            # Add all text to the screen
            self.update_text()

            # Redraw the screen to reflect all changes
            pg.display.flip() 

game = Game()            
game.run_game()