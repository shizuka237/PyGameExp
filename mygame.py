import pygame, random, sys
from pygame.locals import *
# variables and constraints of the code 
WIDTH_OF_WINDOW = 800
HEIGHT_OF_WINDOW = 800
COLOR_OF_TEXT = (255, 255, 255)
COLOR_OF_BACKGROUND = (0, 0, 0)
FRAME_PER_SECOND = 40
MIN_SIZE_BAD = 10 
MAX_SIZE_BAD= 40
MIN_SPEED_BAD = 1
MAX_SPEED_BAD = 8
ADD_NEW_BAD = 6
MOVE_RATE_PLAYER = 5

def end():
      pygame.quit()
      sys.exit()
	  
	  
#This function is to pause the game until the player presses a key. 
#This infinite loop breaks down when KEYDOWN or QUIT event is encountered
def playerPresskey():
     while True:
              for ev in pygame.event.get():
               if ev.type == QUIT:
                  end()
               if ev.type == KEYDOWN:
                 if ev.key == K_ESCAPE: # pressing escape quits
                     end()
                 return

def playerCollidedwithBad(pRect, bad):
     for b in bad:
         if pRect.colliderect(b['rect']):
              return True
     return False
	 
#This function draws the text on the window	 
def draw(text, font, area, x, y):
     objecttext = font.render(text, 1, COLOR_OF_TEXT)
     recttext = objecttext.get_rect()
     recttext.topleft = (x, y)
     area.blit(objecttext, recttext)

# set up the pygame, the window and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowArea = pygame.display.set_mode((WIDTH_OF_WINDOW, HEIGHT_OF_WINDOW))
pygame.display.set_caption('STAR WARS : RogueNation')
pygame.mouse.set_visible(False)

 
font = pygame.font.SysFont(None, 48)

soundGame = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')

# set up images
pImage = pygame.image.load('player.png')
pRect = pImage.get_rect()
bad_Image = pygame.image.load('baddie.png')

# show the "Start" screen
draw('Python game', font, windowArea, (WIDTH_OF_WINDOW / 3), (HEIGHT_OF_WINDOW / 4))
draw('Enter to start', font, windowArea, (WIDTH_OF_WINDOW / 3) - 30, (HEIGHT_OF_WINDOW / 4) + 50)
draw('This game can be played in two ways', font, windowArea, (WIDTH_OF_WINDOW /3 ) - 30, (HEIGHT_OF_WINDOW / 4) + 100)
draw('with keyboard or with mouse', font, windowArea, (WIDTH_OF_WINDOW / 3) - 30, (HEIGHT_OF_WINDOW / 4) + 150)
draw('w : to move Up ', font, windowArea, (WIDTH_OF_WINDOW / 3) - 30, (HEIGHT_OF_WINDOW / 4) + 200)
draw('a : to move left ', font, windowArea, (WIDTH_OF_WINDOW / 3) - 30, (HEIGHT_OF_WINDOW / 4) + 250)
draw('s : to move Down ', font, windowArea, (WIDTH_OF_WINDOW / 3) - 30, (HEIGHT_OF_WINDOW / 4) + 300)
draw('d : to move Right ', font, windowArea, (WIDTH_OF_WINDOW / 3) - 30, (HEIGHT_OF_WINDOW / 4) + 350)
draw('z and x : cheat codes ', font, windowArea, (WIDTH_OF_WINDOW / 3) - 30, (HEIGHT_OF_WINDOW / 4) + 400)

pygame.display.update()
playerPresskey()

#This while loop will iterate when the player starts a new game.
#When the player loses and the game resets, the program will loop back.

countScore = 0
while True:
      
      bad = []
      count = 0
      pRect.topleft = (WIDTH_OF_WINDOW / 2, HEIGHT_OF_WINDOW - 50)
      left = right = up = down = False
      rev = slow = False
      badAddscore = 0
      pygame.mixer.music.play(-1, 0.0)
	  
      #The loop exits when the player either loses the game or quits the program.
      while True:
         count += 1 
 
         for ev in pygame.event.get():
              if ev.type == QUIT:
                  end()
		      #For the purpose of playing game with the help of keyboard
			  #'w' is used for up, 'a' is used for left
			  #'d' is used for right, 's' is used for down
			  # 'z' is used for moving in reverse direction which penalises count
			  # 'x' is used for slow movement in forward direction which again penalises count
              if ev.type == KEYDOWN:
                  if ev.key == ord('z'):
                      rev = True
                  if ev.key == ord('x'):
                      slow = True
                  if ev.key == K_LEFT or ev.key == ord('a'):
                      right = False
                      left = True
                  if ev.key == K_RIGHT or ev.key == ord('d'):
                      left = False
                      right = True
                  if ev.key == K_UP or ev.key == ord('w'):
                      down = False
                      up = True
                  if ev.key == K_DOWN or ev.key == ord('s'):
                     up = False
                     down = True
              
			  #It checks whether player has released a key 
	          #Releasing 'z' will deactivate the reverse movement
              if ev.type == KEYUP:
                 if ev.key == ord('z'):
                     rev = False
                     count = 0
                 if ev.key == ord('x'):
                     slow = False
                     count = 0
                 if ev.key == K_ESCAPE:
                         end()

                 if ev.key == K_LEFT or ev.key == ord('a'):
                     left = False
                 if ev.key == K_RIGHT or ev.key == ord('d'):
                     right = False
                 if ev.key == K_UP or ev.key == ord('w'):
                     up = False
                 if ev.key == K_DOWN or ev.key == ord('s'):
                     down = False

              if ev.type == MOUSEMOTION:
                 
                 pRect.move_ip(ev.pos[0] - pRect.centerx, ev.pos[1] - pRect.centery)

         
		 #Increment badAddscore which happens when 'rev' and 'slow ' are not enabled.
         if not rev and not slow:
             badAddscore += 1
         if badAddscore == ADD_NEW_BAD:
             badAddscore = 0
             bad_size = random.randint(MIN_SIZE_BAD, MAX_SIZE_BAD)
             new_bad = {'rect': pygame.Rect(random.randint(0, WIDTH_OF_WINDOW-bad_size), 0 - bad_size, bad_size, bad_size),
                         'speed': random.randint(MIN_SPEED_BAD, MAX_SPEED_BAD),
                         'area':pygame.transform.scale(bad_Image, (bad_size, bad_size)),
                         }

             bad.append(new_bad)

         # Let the player rectangle moved to left until it reaches 
		 #leftmost edge of the game window.Similarly for other cases.
         if left and pRect.left > 0:
             pRect.move_ip(-1 * MOVE_RATE_PLAYER, 0)
         if right and pRect.right < WIDTH_OF_WINDOW:
             pRect.move_ip(MOVE_RATE_PLAYER, 0)
         if up and pRect.top > 0:
             pRect.move_ip(0, -1 * MOVE_RATE_PLAYER)
         if down and pRect.bottom < HEIGHT_OF_WINDOW:
             pRect.move_ip(0, MOVE_RATE_PLAYER)

         # Move the mouse cursor to match the player.
         pygame.mouse.set_pos(pRect.centerx, pRect.centery)

            # Move the bad element down if 'rev' and 'slow' are not enabled .
         for b in bad:
             if not rev and not slow:
                 b['rect'].move_ip(0, b['speed'])
             elif rev:
                 b['rect'].move_ip(0, -5)
             elif slow:
                 b['rect'].move_ip(0, 1)

         # Delete bad element that have fallen past the bottom.
         for b in bad[:]:
             if b['rect'].top > HEIGHT_OF_WINDOW:
                 bad.remove(b)

         
         windowArea.fill(COLOR_OF_BACKGROUND)

         
         draw('Score: %s' % (count), font, windowArea, 10, 0)
         draw('Top count: %s' % (countScore), font, windowArea, 10, 40)

         # Draws the player's character image at windowArea at player rectangle.
         windowArea.blit(pImage, pRect)

         
         for b in bad:
             windowArea.blit(b['area'], b['rect'])

         pygame.display.update()

         # Collision detection.
         if playerCollidedwithBad(pRect, bad):
             if count > countScore:
                 countScore = count # set new top count
             break
         mainClock.tick(FRAME_PER_SECOND)

     # Stop the game and show the "Game Over" screen.
      pygame.mixer.music.stop()
      soundGame.play()

      draw('GAME OVER', font, windowArea, (WIDTH_OF_WINDOW / 3), (HEIGHT_OF_WINDOW / 3))
      draw('Press a key to play again.', font, windowArea, (WIDTH_OF_WINDOW / 3) - 80, (HEIGHT_OF_WINDOW / 3) + 50)
      pygame.display.update()
      playerPresskey()

      soundGame.stop()
     

