import numpy as np
import random
import turtle

class SnakeGame(object):
  def __init__(self, boardSize, ticksPerSecond):
    self.drawsize = 660
    self.go = False
    self.boardSizeInt = boardSize
    boardSize = [boardSize, boardSize]
    self.boardSize = [boardSize, boardSize]
    self.board = [[0 for i in range(boardSize[0])] for t in range(boardSize[1])]
    self.board[boardSize[0] / 2 - 1][boardSize[1] / 2 - 1] = 1
    lvValid = False
    while lvValid == False:
      self.lvPos = np.random.randint(0, boardSize[0] - 1, 2)
      if self.lvPos[0] != boardSize[0] / 2 - 1 and self.lvPos[1] != boardSize[0] / 2 - 1:
        lvValid = True
    self.board[self.lvPos[0]][self.lvPos[1]] = 2
    self.vel = [0, 1]
    self.pos = [[boardSize[0] / 2 - 1, boardSize[1] / 2 - 1]]
    self.ticksPerSecond = ticksPerSecond



  def step(self, vel):
    if vel != [0, 0]:
      self.vel = vel

    #Check if you hit a wall
    if (((self.pos[0][0] == 0 and self.vel[0] == -1) or (self.pos[0][0] == self.boardSizeInt - 1 and self.vel[0] == 1)) or ((self.pos[0][1] == 0 and self.vel[1] == -1) or (self.pos[0][1] == self.boardSizeInt - 1 and self.vel[1] == 1))):
      self.go = True
      return

    #Move the snake
    oldPos = self.pos[:]
    for part in range(len(oldPos)):
      if part == 0:
        if self.board[self.pos[part][0] + self.vel[0]][self.pos[part][1] + self.vel[1]] == 1:
          self.go = True

          return
        self.pos[part] = [self.pos[part][0] + self.vel[0], self.pos[part][1] + self.vel[1]]
      else:
        self.pos[part] = oldPos[part - 1]
        
    #Add a part to snake if snake is on lvPos
    if self.pos[0] == [self.lvPos[0], self.lvPos[1]]:
        if len(self.pos) > 1:
          lastPos = [self.pos[-1][0] - self.pos[-2][0], self.pos[-1][1] - self.pos[-1][1]]
        else:
          lastPos = [self.vel[0] * -1, self.vel[1] * -1]
        self.pos.append([self.pos[-1][0] + lastPos[0], self.pos[-1][1] + lastPos[1]])
        lvValid = False
        while lvValid == False:
            self.lvPos = np.random.randint(0, self.boardSizeInt - 1, 2)
            lvValid = True
            for part in self.pos:
              if(self.lvPos[0] == part[0] and self.lvPos[1] == part[1]):
                lvValid = False

    #Write snake and lvPos to board
    self.board = [[0 for i in range(self.boardSizeInt)] for t in range(self.boardSizeInt)]
    for i in self.pos:
        if i[0] >= 0 or i[0] < self.boardSize[0] or i[1] >= 0 or i[1] < self.boardSize[1]:
          self.board[i[0]][i[1]] = 1

    self.board[self.lvPos[0]][self.lvPos[1]] = 2



  def draw(self, pen):
    sqareDiameter = self.drawsize / self.boardSizeInt
    pen.penup()
    for boardLine in range(len(self.board)):
      for boardColumn in range(len(self.board[boardLine])):
        pen.goto(sqareDiameter * boardColumn, self.drawsize - sqareDiameter * boardLine)

        pen.pendown()
        pen.begin_fill()
        for i in range(4):
          pen.forward(sqareDiameter)

          pen.left(90)

        pen.up()
        pen.end_fill() 



# game = SnakeGame(10, 1)

# for i in np.array(game.board).transpose():

#   print(i.transpose())

# while game.go == False:

#   key = raw_input()

#   if key == "d":

#     game.step([0, 1])

#   elif key == "u":

#     game.step([0, -1])

#   elif key == "l":

#     game.step([-1, 0])

#   elif key == "r":

#     game.step([1, 0])

#   for i in np.array(game.board).transpose():

#     print(i.transpose())

# print("Game over")

  

# draw = turtle.Turtle()

# draw.speed('fastest')

# draw.hideturtle()

# game.draw(draw)

# turtle.mainloop()
