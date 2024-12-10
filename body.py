from constants import BLUE, GREEN, RED
from leg import Leg
from legNode import LegNode
from node import Node
import pygame
from scipy.interpolate import CubicSpline
import numpy as np
from section import Section

class Body(Section):
    def __init__(self, nodes: list[Node], node_spacing: float):
        """
        Holds a list of nodes. First node is anchor node
        """
        super().__init__(nodes, node_spacing)
        pass

    def displayEyes(self, screen: pygame.Surface):
        if len(self.lateralPoints) > 0 and len(self.lateralPoints[0]) > 5:
            eyeOne = self.lateralPoints[0][5]
            eyeTwo = self.lateralPoints[0][6]
            pygame.draw.circle(screen, pygame.color.Color(255, 255, 255), (eyeOne[0], eyeOne[1]), 3)
            pygame.draw.circle(screen, pygame.color.Color(255, 255, 255), (eyeTwo[0], eyeTwo[1]), 3)

    def setExampleBody(self):
        bodyShape = [23, 25, 16, 23, 35, 35, 25, 10, 6, 4, 4, 4]
        for i in range(len(bodyShape)):
            if i == 1 or i == 5:
                # Create first leg
                exampleLeg1 = Leg([], 20, Node(0, 0, 0, None))
                exampleLeg1.setExampleLeg()
                
                # Create second leg
                exampleLeg2 = Leg([], 20, Node(0, 0, 0, None))
                exampleLeg2.setExampleLeg()
                
                # Create LegNode with two legs and their targets
                self.nodes.append(LegNode(
                    10, 10, bodyShape[i], self.nodes[i-1], 150,
                    [exampleLeg1, exampleLeg2],  # Two legs
                    [[100, np.pi/6], [100, -np.pi/6]]  # Targets for both legs
                ))

                # Attach each leg to the LegNode
                self.nodes[i].legs[0].attachedNode = self.nodes[i]
                self.nodes[i].legs[1].attachedNode = self.nodes[i]
            
            else:
                if i == 0:
                    self.nodes.append(Node(10, 10, bodyShape[i], None))
                else:
                    self.nodes.append(Node(10, 10, bodyShape[i], self.nodes[i-1]))

        # Update lateral points for all nodes
        self.lateralPoints = self.getLateralSetPointList()
        for node in self.nodes:
            if isinstance(node, LegNode):
                for leg in node.legs:
                    leg.lateralPoints = leg.getLateralSetPointList()

        

    def followMouse(self, mousePos):
        distance = self.nodes[0].coordinateDistance(mousePos[0], mousePos[1])
        self.nodes[0].normalize(mousePos[0], mousePos[1], distance / 30)

    def display(self, screen):
        for node in self.nodes:
            if isinstance(node, LegNode):
                node.displayLegs(screen)
        super().display(screen)
        self.displayEyes(screen)

    def update(self, followMouse: bool):
        super().update()
        # self.kinematicsHandler.applyAngleConstraint(self.nodes, angle_margin=np.pi / 16)

        if followMouse:
            self.followMouse(pygame.mouse.get_pos())

        self.kinematicsHandler.applyForwardsDistanceConstraint(self.nodes)

        self.updateLegNodes()

    def updateLegNodes(self):
        # For anchor node:
        if isinstance(self.nodes[0], LegNode):
                self.nodes[0].update(self.nodes[0].getAnchorLateralPoints(self.nodes[1].x, self.nodes[1].y)[2])

        for i in range(len(self.nodes)-2):
            # Skip first node (anchor node)
            i += 1

            if isinstance(self.nodes[i], LegNode):
                self.nodes[i].update(self.nodes[i].getLateralPoints(self.nodes[i-1].x, self.nodes[i-1].y)[2])
            
    def displayLegNodeTargetPoints(self, screen: pygame.Surface):
        """
        Displays target points for all LegNodes in the Body on the given pygame surface.
        :param screen: The pygame surface to draw on.
        """
        for node in self.nodes:
            if isinstance(node, LegNode):
                node.displayTargetPoints(screen)

    def displayNodes(self, screen):
        super().displayNodes(screen)
        self.displayLegNodeTargetPoints(screen)
