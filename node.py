import numpy as np
import pygame
from typing import Tuple

Coordinate = Tuple[float, float]

class Node:
    def __init__(self, x: int, y: int, size: int):
        self.x = x
        self.y = y
        self.size = size

    def nodeDistance(self, otherNode: 'Node') -> float:
        return ((self.x - otherNode.x) ** 2 + (self.y - otherNode.y) ** 2) ** 0.5
    
    def coordinateDistance(self, x: int, y: int) -> float:
        return ((self.x - x) ** 2 + (self.y - y) ** 2) ** 0.5
    
    def normalize(self, targetX: int, targetY: int, travelDistance: float):
        """
        Takes in a target x and y position and a distance float value and moves node that distance towards given node
        """
        if self.coordinateDistance(targetX, targetY) < travelDistance:
            self.x = targetX
            self.y = targetY
        else:
            slope = (targetY - self.y) / (targetX - self.x)
            theta = np.arctan(slope)
            coef = 1
            if targetX < self.x:
                coef = -1
            self.x = self.x + travelDistance * np.cos(theta) * coef
            self.y = self.y + travelDistance * np.sin(theta) * coef

    def display(self, screen: pygame.Surface):
        pygame.draw.circle(screen, pygame.color.Color(255, 255, 255), (self.x, self.y), self.size, 3)
    
    def getLateralPoints(self, targetX: int, targetY: int) -> Tuple[Coordinate, Coordinate, Coordinate]:
        """
        Takes in target coordinate and returns left and right positions relative to node assuming the node is facing the target coordinate.
        """
        slope = 1
        if not (targetX - self.x) == 0:
            slope = (targetY - self.y) / (targetX - self.x)
        theta = np.arctan(slope)

        coef = -1
        if targetX > self.x:
            coef = 1

        # Right
        x1 = self.x + np.cos(theta + np.pi / 2) * coef * self.size
        y1 = self.y + np.sin(theta + np.pi / 2) * coef * self.size

        # Left
        x2 = self.x + np.cos(theta - np.pi / 2) * coef * self.size
        y2 = self.y + np.sin(theta - np.pi / 2) * coef * self.size

        # For anchor
        x3 = self.x + np.cos(theta) * coef * self.size
        y3 = self.y + np.sin(theta) * coef * self.size
        # 
        x4 = self.x + np.cos(theta + np.pi/4) * coef * self.size
        y4 = self.y + np.sin(theta + np.pi/4) * coef * self.size
        # 
        x5 = self.x + np.cos(theta - np.pi/4) * coef * self.size
        y5 = self.y + np.sin(theta - np.pi/4) * coef * self.size
        # Eyes
        x6 = self.x + np.cos(theta - np.pi / 2) * coef * self.size * 1/2
        y6 = self.y + np.sin(theta - np.pi / 2) * coef * self.size * 1/2
        x7 = self.x + np.cos(theta + np.pi / 2) * coef * self.size * 1/2
        y7 = self.y + np.sin(theta + np.pi / 2) * coef * self.size * 1/2
        

        return [ [x1, y1], [x2, y2], [x3, y3], [x4, y4], [x5, y5], [x6, y6], [x7, y7] ]

        
        