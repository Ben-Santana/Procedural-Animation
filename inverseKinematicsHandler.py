
from typing import Tuple

from kinematicsHandler import KinematicsHandler
from node import Node

class InverseKinematicsHandler(KinematicsHandler):

    def __init__(self, errorMargin: float, node_spacing: float):
        super().__init__(node_spacing)
        self.errorMargin = errorMargin
    
    def backwardReach(self, nodes: list[Node], start: Tuple[int, int]) -> list[Node]:
        updatedNodes = nodes
        nodes[0].x, nodes[0].y = start
        self.applyForwardsNodeSpacing(nodes)
        return updatedNodes

    def forwardReach(self, nodes: list[Node], target: Tuple[int, int]) -> list[Node]:
        updatedNodes = nodes
        nodes[-1].x, nodes[-1].y = target
        self.applyBackwardsNodeSpacing(nodes)
        return updatedNodes

    def fabrik(self, nodes: list[Node], target: Tuple[int, int]) -> list[Node]:
        updatedNodes: list[Node] = nodes
        start: Tuple[int, int] = [nodes[0].x, nodes[0].y]
        while self.calculateError(updatedNodes, target) > self.errorMargin:
            updatedNodes = self.forwardReach(updatedNodes, target)
            updatedNodes = self.backwardReach(updatedNodes, start)
        return updatedNodes

    def calculateError(self, nodes: list[Node], target: Tuple[int, int]) -> float:
        error = nodes[-1].coordinateDistance(target[0], target[1])
        print(error)
        return error
    
    def tooFar(self, nodes: list[Node], target: Tuple[int, int]) -> bool:
        return self.node_spacing * (len(nodes) - 1) < nodes[0].coordinateDistance(target[0], target[1])