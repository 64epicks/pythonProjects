import numpy as np
import random
from abc import ABC, abstractmethod

class SnakeGame(object):
  def __init__(self, boardSize, ticksPerSecond):
    self.boardSize = boardSize
    self.board = [[0 for i in range(boardSize[0])] for t in range(boardSize[1])]
    self.board[boardSize[0] / 2 - 1][boardSize[1] / 2 - 1] = 1
    lvValid = False
    while lvValid == False:
      self.lvPos = np.random.randint(0, boardSize[0] - 1, 2)
      if self.lvPos[0] != boardSize[0] / 2 - 1 and self.lvPos[1] != boardSize[0] / 2 - 1:
        lvValid = True
    self.vel = [0, 1]
    self.pos = [[boardSize[0] / 2 - 1, boardSize[1] / 2 - 1]]
    self.ticksPerSecond = ticksPerSecond

  def step(self, vel):
    if vel != [0, 0]:
      self.vel = vel
    #Check if you hit a wall
    if ((self.pos[0][0] == 0 and self.vel[0] == -1) or (self.pos[0][0] == len(self.pos) - 1 and self.vel[0] == 1)) or ((self.pos[0][1] == 0 and self.vel[1] == -1) or (self.pos[0][1] == len(self.pos) - 1 and self.vel[1] == 1)):
      return
    #Move the snake
    oldPos = self.pos
    for part in range(len(oldPos)):
      if part == 0:
        if self.pos[self.pos[part][0] + self.vel[0]][self.pos[part][1] + self.vel[1]] == 1:
          self.go = True
          break
        self.pos[part] = [self.pos[part][0] + self.vel[0], self.pos[part][1] + self.vel[1]]
      else:
        self.pos[part] = oldPos[part - 1]
    
    #Add a part to snake if snake is on lvPos
    if self.pos[lvPos[0]][lvPos[1]] == 1:
        lastPos = [self.pos[-1][0] - self.pos[-2][0], self.pos[-1][1] - self.pos[-1][1]]
        self.pos.append([self.pos[-1][0] + lastPos[0], self.pos[-1][1] + lastPos[1]])

        lvValid = False
        while lvValid == False:
            self.lvPos = np.random.randint(0, self.boardSize[0] - 1, 2)
            # FIX THIS IF STATEMENT
            if self.lvPos[0] != boardSize[0] / 2 - 1 and self.lvPos[1] != boardSize[0] / 2 - 1:
                lvValid = True

    #Write snake and lvPos to board
    self.board = [[0 for i in range(self.boardSize[0])] for t in range(self.boardSize[1])]
    for i in self.pos:
        if i[0] >= 0 or i[0] < self.boardSize[0] or i[1] >= 0 or i[1] < self.boardSize[1]
            self.board[i[0]][i[1]] = 1
