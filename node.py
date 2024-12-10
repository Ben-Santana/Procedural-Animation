import numpy as np
import pygame
from typing import Tuple

Coordinate = Tuple[float, float]

class Node:
    def __init__(self, x: int, y: int, size: int, prevNode: 'Node'):
        self.x = x
        self.y = y
        self.size = size
        self.prevNode = prevNode
        

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
            slope = 1
            if not (targetX - self.x) == 0:
                slope = (targetY - self.y) / (targetX - self.x)
            theta = np.arctan(slope)
            coef = 1
            if targetX < self.x:
                coef = -1
            self.x = self.x + travelDistance * np.cos(theta) * coef
            self.y = self.y + travelDistance * np.sin(theta) * coef

    def display(self, screen: pygame.Surface):
        pygame.draw.circle(screen, pygame.color.Color(255, 255, 255), (self.x, self.y), self.size, 3)

    def getRelativePoint(self, targetX: int, targetY: int, distance: float, deltaTheta: float = 0):
        """
        Calculate a relative point at a given distance and angle (deltaTheta) from the current node,
        based on the target's position.
        """
        if targetX == self.x:  # Vertically aligned
            if targetY > self.y:
                theta = np.pi / 2  # Upwards
            elif targetY < self.y:
                theta = -np.pi / 2  # Downwards
            else:
                print("Error: Target and current node are at the same position.")
                return [self.x, self.y]
        else:
            # General case: calculate angle using arctan2 for correct quadrant handling
            theta = np.arctan2(targetY - self.y, targetX - self.x)

        # Compute the new point based on the angle and distance
        x1 = self.x + np.cos(theta + deltaTheta) * distance
        y1 = self.y + np.sin(theta + deltaTheta) * distance

        return [x1, y1]


    def getPointOnRadius(self, targetX: int, targetY: int, deltaTheta: float = 0) -> Coordinate:
        return self.getRelativePoint(targetX, targetY, self.size, deltaTheta)
    
    def getEyesPosition(self, targetX, targetY) -> Tuple[Coordinate, Coordinate]:\
        return self.getRelativePoint(targetX, targetY, self.size/2, -np.pi/2), self.getRelativePoint(targetX, targetY, self.size/2, np.pi/2)
    
    def getLateralPoints(self, targetX: int, targetY: int) -> Tuple[7]:
        """
        Takes in target coordinate and returns left and right positions relative to node assuming the node is facing the target coordinate.
        """

        rightPoint = self.getPointOnRadius(targetX, targetY, np.pi / 2)
        leftPoint = self.getPointOnRadius(targetX, targetY, -np.pi / 2)
        frontPoint = self.getPointOnRadius(targetX, targetY, 0)
        backPoint = self.getPointOnRadius(targetX, targetY, -np.pi)
        rightLeaningPoint = self.getPointOnRadius(targetX, targetY, np.pi / 4)
        leftLeaningPoint = self.getPointOnRadius(targetX, targetY, -np.pi / 4)
        rightBackLeaningPoint = self.getPointOnRadius(targetX, targetY, np.pi * 3 / 4)
        leftBackLeaningPoint = self.getPointOnRadius(targetX, targetY, -np.pi * 3 / 4)
        eyesPoints = self.getEyesPosition(targetX, targetY)

        return [ rightPoint, leftPoint, 
                frontPoint, 
                rightLeaningPoint, leftLeaningPoint, 
                eyesPoints[0], eyesPoints[1],
                rightBackLeaningPoint, leftBackLeaningPoint,
                backPoint]
    
    def getAnchorLateralPoints(self, targetX, targetY):
        lateralPoints = self.getLateralPoints(targetX, targetY)
        #Switch left and right
        lateralPoints[1], lateralPoints[0] = lateralPoints[0], lateralPoints[1]
        # #Switch front and back
        lateralPoints[2], lateralPoints[9] = lateralPoints[9], lateralPoints[2]
        # #Switch left and right leaning
        lateralPoints[3], lateralPoints[8] = lateralPoints[8], lateralPoints[3]
        lateralPoints[4], lateralPoints[7] = lateralPoints[7], lateralPoints[4]
        return lateralPoints

        
        