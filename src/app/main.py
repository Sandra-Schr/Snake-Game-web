import pygame
import random
import copy
import time
import asyncio



#######################
#### BLOCK ############
#######################

class block(object):

  def __init__(self,x,y):
    self.x = x
    self.y = y

  @classmethod
  def copyMe(cls,_block):
    return copy.copy(_block)

  def copyMee(self):
    return copy.copy(self)

  def reset(self):
    self.x = 0
    self.y = 0
  
  def __eq__(self, other):
    return (self.x, self.y) == (other.x, other.y)

  

#######################
### GAME CONTROLLER ###
#######################

class GameController():

  def __init__(self):
    self.initialize()
    
  
  def initialize(self):
    # Initializing surface
    self.window_x = 1000
    self.window_y = 800

    # defining colors
    self.black = pygame.Color(0, 0, 0)
    self.white = pygame.Color(255, 255, 255)
    self.red = pygame.Color(255, 0, 0)
    self.green = pygame.Color(0, 255, 0)
    self.blue = pygame.Color(0, 0, 255)

    # initial score
    self.score: int = 0

     ### Initialize pygame modules ####
    pygame.init()

   # Font
    self.myFont_S = pygame.font.Font("/home/sandra/SnakeGame/ARCADECLASSIC.TTF", size=40)
    self.myFont_L = pygame.font.Font("/home/sandra/SnakeGame/ARCADECLASSIC.TTF", size=70)
    
    # Initialise game window
    self.game_window = pygame.display.set_mode((self.window_x, self.window_y))

    # FPS (frames per second) controller --> aktuell nur eine Zeit
    self.fps = pygame.time.Clock()

    # setting default snake direction towards
    # right
    self.direction = 'RIGHT'
    self.change_to = self.direction

    # Set display caption
    pygame.display.set_caption('Snake Game')

      

    snakeLength = 6
    self.head = block(100,50)
    self.mySnake = snake(copy.copy(self.head),snakeLength) # ToDo: Check if copy for snakes' head is necessary!

    # Snake 2 --> Mutlti-Player
    #self.mySnake2 = snake(400,300,3)
    
    # Generate random position for the apple
    self.myAppleBlock = self.generateRandomPosOnBoard()

    # initialize mines list of blocks
    self.myMines: list[block] = []
    
    # Generate random mine positions on game screen
    for countMines in range(30):
      self.myMines.append(self.generateRandomPosOnBoard())

    #dupValue = self.compareListDuplicates(self.myAppleBlock,self.myMines)
    #while dupValue == True:
      #self.myAppleBlock = self.generateRandomPosOnBoard()
      
      
   

  def processInput(self):
    # handling key events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
          self.change_to = 'UP'
        elif event.key == pygame.K_DOWN:
          self.change_to = 'DOWN'
        elif event.key == pygame.K_LEFT:
          self.change_to = 'LEFT'
        elif event.key == pygame.K_RIGHT:
          self.change_to = 'RIGHT'
        
    
  def update(self):
    
    self.mySnake.movement(self.change_to)
    
    snake_ate = self.mySnake.growingSnake(self.myAppleBlock) # needs snake_ate= ... for return value -> return value will be saved in snake_ate
    if snake_ate == True:
      self.myAppleBlock = self.generateRandomPosOnBoard()
      self.score += 10


    # ToDo: Collision dection mines
    #listValue = self.compareListDuplicates(self.myMines, self.mySnake.body)
    #listValue = False
    listValue = self.compareListDuplicates(self.mySnake.body, self.myMines)
    if listValue == True:
      self.game_over()
    listValue = self.compareListDuplicates(self.mySnake.body, self.myAppleBlock)
    if listValue == True:
      self.game_over()

    # collision detection (with head and snakes' body)
    # count von 0 bis 4!
    for count in range(len(self.mySnake.body)-1): 
      if self.mySnake.body[0] == self.mySnake.body[count+1]:
        self.game_over()  
    

    # collision detection (with game window)
    if self.mySnake.body[0].x < 0 or self.mySnake.body[0].x > self.window_x-10:
      self.game_over()
    if self.mySnake.body[0].y < 0 or self.mySnake.body[0].y > self.window_y-10:
      self.game_over()

    
  def compareListDuplicates(self, list1, list2):
  
      if not isinstance(list1, list):
        list1 = [block(list1.x, list1.y)]
      if not isinstance(list2, list):
        list2 = [block(list2.x, list2.y)]
                
      if any(x in list1 for x in list2):
        return True # duplicates found
      else:
        return False # no duplicates found     
     
    
  def game_over(self):

    # creating a text surface on which text 
    # will be drawn
    game_over_surface = self.myFont_L.render('Your Score is ' + str(self.score), True, self.blue)
    
    # create a rectangular object for the text 
    # surface object
    game_over_rect = game_over_surface.get_rect()
    
    # setting position of the text
    game_over_rect.midtop = (self.window_x/2, self.window_y/4)
    
    # blit will draw the text on screen
    self.game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    
    # after 2 seconds we will quit the program
    time.sleep(2)
    
    # deactivating pygame libraryself.game_window.fill(self.black)
    pygame.quit()
    
    # quit the program
    quit()


  def render(self):
    self.game_window.fill(self.black)

    # draw the snake 1
    for curBlock in self.mySnake.body:
      pygame.draw.rect(self.game_window, self.green, pygame.Rect(curBlock.x, curBlock.y, 10, 10))
 
    # draw the snake 2 --> Multi-Player test
    #for pos in self.mySnake2.body:
    #  pygame.draw.rect(self.game_window, self.green, pygame.Rect(pos[0], pos[1], 10, 10))

    # draw the apple  
    pygame.draw.rect(self.game_window, self.white, pygame.Rect(self.myAppleBlock.x, self.myAppleBlock.y, 10, 10))

    # draw the mines
    for curMine in self.myMines:
      pygame.draw.rect(self.game_window, self.red, pygame.Rect(curMine.x, curMine.y, 10, 10))

    # displaying score continuously
    #self.show_score(1, self.white, 'comic sans', 20)
    self.show_score()

    # Refresh game screen
    pygame.display.update()

    # Frame Per Second /Refresh Rate
    self.fps.tick(self.mySnake.speed)


### Game Loop ###
  async def run(self):
    while True:
      self.processInput()
      self.update()
      self.render()
      await asyncio.sleep(0)  # let other tasks run
  
  def generateRandomPosOnBoard(self) -> block: #return type: block
   randomNumbers = random.randrange(1, (self.window_x//10)) * 10, random.randrange(1, (self.window_y//10)) * 10
      
          
   # ToDo: Check if following positions already existing on game board:
   # (1) apple with snake
   # (2) mine(s) with snake
   # (3) apple with mine
   # (4) mine with mine
   
   return block(randomNumbers[0],randomNumbers[1]) 

   '''
      try:
        self.myMines.index(self.mySnake.body[0])
        self.game_over()
      except:
        pass # no collision with mine
    
  '''
    
  # displaying Score function
  def show_score(self):
      
    # create the display surface object 
    # score_surface
    score_surface = self.myFont_S.render('Score ' + str(self.score), True, self.white) # Wieso hier weißer Hintergrund, wenn score als Variable übergeben?!
    
    # create a rectangular object for the text
    # surface object
    score_rect = score_surface.get_rect()
    
    # displaying text
    self.game_window.blit(score_surface, score_rect)
    





#######################
####### SNAKE #########
#######################

class snake(object):
  def __init__(self, myBlock: block, length):
    
    self.body: list[block] = []
    for count in range(length):
      self.body.append(block(myBlock.x-10*count,myBlock.y))
      
    #self.body = [[100, 50], [90, 50], [80, 50], [70, 50]]
       
    self.speed = 10
    self.length = length

  
  def movement (self,moveTo):
    # Moving the snake
    
    # newBlock = self.body[0]    # I need a copy, not a reference
    newBlock = block.copyMe(self.body[0]) # copy by class method
    
    #newBlock2 = self.body[0].copyMee() # copy by instance method
    
    # newBlock = block(self.body[0])  # is this possible?
   
    if moveTo == 'UP':
      self.direction = 'UP'
      newBlock.y -=10
      #newBlock[1]-=10
    if moveTo == 'DOWN':
      self.direction = 'DOWN'
      newBlock.y +=10
      #newBlock[1]+=10
    if moveTo == 'LEFT':
      self.direction = 'LEFT'
      newBlock.x -=10
      #newBlock[0]-=10
    if moveTo == 'RIGHT':
      self.direction = 'RIGHT'
      newBlock.x +=10
      #newBlock[0]+=10
       
    self.body.insert(0,newBlock)   
    self.body.pop()
     

  def growingSnake(self,fruit) -> bool:
    snakeHead = block.copyMe(self.body[0])
    eatApple: bool = False
    
    if snakeHead.x == fruit.x and snakeHead.y == fruit.y:
      if (self.body[-2].x - self.body[-1].x) > 0:
          self.body.append(block(self.body[-1].x-10,self.body[-1].y))
      if (self.body[-2].x - self.body[-1].x) < 0:
          self.body.append(block(self.body[-1].x+10,self.body[-1].y))
      if (self.body[-2].y - self.body[-1].y) > 0:
          self.body.append(block(self.body[-1].x,self.body[-1].y-10))
      if (self.body[-2].y - self.body[-1].y) < 0:
          self.body.append(block(self.body[-1].x,self.body[-1].y+10))

      eatApple = True

    return eatApple #return value for update fuction in GC




myGameController = GameController()
asyncio.run(myGameController.run())

'''
  print(myGameController.number)
  myGameController2 = GameController()
  print(myGameController.number)
  print(myGameController2.number)
  print(GameController.number)
'''
