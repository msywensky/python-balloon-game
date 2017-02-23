# python-balloon-game
Simple game using PyGame

I wrote a balloon popping game as a simple exercise to learn Python and PyGame to help my son with his school project.

This was written using 2.7.12 on a mac.  I tried to keep it cross platform but did not try it in any other OS.

To run from source:
* install homebrew (if you do not have it):https://brew.sh/ 
* install Python 2.7.x.  Yes, OSX comes with Python but there are issues with it and PyGame: $ brew python
* install PyGame dependencies.  This was a pain to get right on Sierra. They could probably go all on one line, but I split them out.
* * Mercurial: $ brew install mercurial
* * sdl libraries: $ brew install sdl sdl_image 
* * $ brew install sdl_mixer --with-libvorbis
* * $ brew install sdl_ttf portmidi
* install PyGame: pip install hg+http://bitbucket.org/pygame/pygame

Attributions:
background: https://www.seeedstudio.com/gameduino-a-game-adapter-for-microcontrollers-p-860.html
person: http://opengameart.org/content/boy-with-a-slingshot - Software Atelier Kamber (http://shop.software-atelier.ch)
balloon: Ripped from Kirby Mass Attack, Nintendo DS - http://drshnaps.com
background music: http://opengameart.org/content/carnival-rides
pop sound: http://opengameart.org/content/bubbles-pop

