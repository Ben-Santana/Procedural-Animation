from typing import Tuple
import pygame
from node import Node
from section import Section

class Leg(Section):
    def __init__(self, nodes: list[Node], node_spacing: float, attatchedNode: Node):
        super().__init__(nodes, node_spacing)
        self.attachedNode: Node = attatchedNode
        self.targetPosition: list[Node] = []

    
    def setExampleLeg(self):
        legShape = [6, 6, 6, 6, 6]
        for i in range(len(legShape)):
            if i == 0:
                self.nodes.append(Node(10, 10, legShape[i], None))
            else:
                self.nodes.append(Node(10, 10, legShape[i], self.nodes[i-1]))
        self.lateralPoints = self.getLateralSetPointList()

    def update(self):
        super().update()
        self.setAnchorNodePosition(self.attachedNode.x, self.attachedNode.y)

    def moveLegEndTo(self, target: Tuple[int, int]):
        if self.kinematicsHandler.tooFar(self.nodes, target):
            self.extendTowards(target, 0.7)
        else:
            self.nodes = self.kinematicsHandler.fabrik(self.nodes, target)
    
    
    def moveTowards(self, target: Tuple[int, int], percentage: float):
        xDistance = target[0] - self.nodes[-1].x
        yDistance = target[1] - self.nodes[-1].y
        deltaX = xDistance * percentage
        deltaY = yDistance * percentage
        newX = self.nodes[-1].x + deltaX
        newY = self.nodes[-1].y + deltaY
        self.moveLegEndTo([newX, newY])