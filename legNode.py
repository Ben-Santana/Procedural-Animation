from typing import Tuple
import numpy as np
import numpy
import pygame
from leg import Leg
from node import Node


class LegNode(Node):
    def __init__(self, x: int, y: int, size: int, prevNode: Node,
                 updateDistance: float,
                 legs: list[Leg] = [], 
                 targets: list[Tuple[float, float]] = [],
                 ):
        
        super().__init__(x, y, size, prevNode)
        self.legs: list[Leg] = legs
        # Targets are stored as polar coordinates relative to the leg node
        self.targets: list[Tuple[float, float]] = targets
        self.currentTargets: list[Tuple[float, float]] = self.getAllTargetPositions()
        self.updateDistance: float = updateDistance

    def updateTargetPosition(self, forward: Tuple[int, int], legIndex: int):
        newTarget: Tuple[float, float] = self.getRelativePoint(forward[0], forward[1], self.targets[legIndex][0], self.targets[legIndex][1])
        self.currentTargets[legIndex] = newTarget

    def getTargetPosition(self, forward: Tuple[int, int], legIndex: int):
        newTarget: Tuple[float, float] = self.getRelativePoint(forward[0], forward[1], self.targets[legIndex][0], self.targets[legIndex][1])
        return newTarget
    
    def getAllTargetPositions(self):
        newTargets: list[Tuple[float, float]] = []
        for legIndex in range(len(self.legs)):
            cartesian_target = self.getTargetPosition([self.prevNode.x, self.prevNode.y], legIndex)
            newTargets.append(cartesian_target)
            print(f"Leg {legIndex} target (polar to Cartesian): {cartesian_target}")
        return newTargets

    
    def display(self, screen: pygame.Surface):
        super().display(screen)
        for leg in self.legs:
            for node in leg.nodes:
                node.display(screen)
    
    def moveLegsTowardsTarget(self, percentage=0.3):
        for legIndex in range(len(self.legs)):
            self.legs[legIndex].moveTowards(self.currentTargets[legIndex], percentage)
            

    def update(self, forward: Tuple[int, int]):

        for i in range(len(self.legs)):

            self.legs[i].update()
            xDiff = self.currentTargets[i][0] - self.polar_to_cartesian(self.targets[i])[0]
            yDiff = self.currentTargets[i][1] - self.polar_to_cartesian(self.targets[i])[1]
            distance = numpy.sqrt(numpy.square(xDiff) + numpy.square(yDiff))
            if distance > self.updateDistance:
                self.updateTargetPosition(forward, i)
        self.moveLegsTowardsTarget()

    def displayLegs(self, screen: pygame.Surface):
        for leg in self.legs:
            leg.display(screen)
        

    def displayTargetPoints(self, screen: pygame.Surface):
        """
        Displays all current target points and original target points onto the given pygame surface.
        :param screen: The pygame surface to draw on.
        """
        font = pygame.font.Font(None, 24)  # Font for text labels

        for i, leg in enumerate(self.legs):
            # Display original target points (polar coordinates as text)
            original_target = self.targets[i]
            # target_text = f"Target {i + 1}: Dist={original_target[0]:.2f}, Theta={original_target[1]:.2f} rad"
            # target_label = font.render(target_text, True, pygame.color.Color('white'))
            # screen.blit(target_label, (self.x + 10, self.y + i * 20))

            # Convert original polar target to Cartesian coordinates for visualization
            polar_x, polar_y = self.getRelativePoint(self.prevNode.x, self.prevNode.y,
                                                     original_target[0], original_target[1])

            # Draw original target point (as a small red circle)
            pygame.draw.circle(screen, pygame.color.Color('red'), (int(polar_x), int(polar_y)), 5)

            # Draw current target point (as a small blue circle)
            current_target = self.currentTargets[i]
            pygame.draw.circle(screen, pygame.color.Color('blue'), 
                               (int(current_target[0]), int(current_target[1])), 5)

            # Optionally, draw connecting lines for better visualization
            pygame.draw.line(screen, pygame.color.Color('yellow'), 
                             (self.x, self.y), (polar_x, polar_y), 2)  # Line to original target
            pygame.draw.line(screen, pygame.color.Color('green'), 
                             (self.x, self.y), (current_target[0], current_target[1]), 2)  # Line to current target

    def polar_to_cartesian(self, target: Tuple[float, float]) -> Tuple[float, float]:
            """
            Converts this LegNode's target from polar coordinates (r, theta) to Cartesian coordinates on the screen.
            
            :param target: A tuple (r, theta) where:
                - r is the distance from the leg node to the target point.
                - theta is the angle (in radians) relative to the leg node's front direction.
            :return: A tuple (x, y) representing the target's Cartesian coordinates on the screen.
            """
            # Extract polar coordinates
            r, theta = target

            # Current position of the LegNode
            node_x, node_y = self.x, self.y

            # Reference position: the position of the prevNode
            ref_x, ref_y = self.prevNode.x, self.prevNode.y

            # Calculate the reference angle (orientation of the node's front)
            ref_angle = np.arctan2(ref_y - node_y, ref_x - node_x)

            # Convert polar to Cartesian
            x = node_x + r * np.cos(ref_angle + theta)
            y = node_y + r * np.sin(ref_angle + theta)

            return x, y