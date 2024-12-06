from typing import Tuple
from node import Node
import pygame
from scipy.interpolate import CubicSpline
import numpy as np

class Line:
    def __init__(self, nodes: list[Node], node_spacing: float):
        """
        Holds a list of nodes. First node is anchor node
        """
        self.nodes = nodes
        self.node_spacing = node_spacing
        self.lateralPoints = self.getLateralSetPointList()
        self.curvePoints = self.getParametricCurvePoints()
        pass

    def updateNodePositions(self):
        """
        Checks to see any nodes are too far apart with respect to set node_spacing. If they are, normalize starting from first node
        """
        for i in range(len(self.nodes)):
            # Check if beyond node_spacing
            distance = self.nodes[i].nodeDistance(self.nodes[i-1])
            if i > 0 and distance > self.node_spacing:
                self.nodes[i].normalize(self.nodes[i-1].x, self.nodes[i-1].y, distance - self.node_spacing)
    
    def updateLateralPointSetPositions(self):
        self.lateralPoints = self.getLateralSetPointList()

    def displayNodes(self, screen: pygame.Surface):
        """
        Display nodes onto inputed pygame surface
        """
        for node in self.nodes:
            node.display(screen)
    
    def setAnchorNodePosition(self, x, y):
        self.nodes[0].x = x
        self.nodes[0].y = y

    def displayLinesBetweenNodes(self, screen: pygame.Surface):
        """
        Draws lines between the nodes on the inputted pygame surface.
        """
        for i in range(1, len(self.nodes)):
            pygame.draw.line(
                screen,  # Surface to draw on
                (255, 255, 255),  # Color of the line (white)
                (self.nodes[i-1].x, self.nodes[i-1].y),  # Start point
                (self.nodes[i].x, self.nodes[i].y),  # End point
                5  # Line thickness
            )

    def followMouse(self, mousePos):
        distance = self.nodes[0].coordinateDistance(mousePos[0], mousePos[1])
        self.nodes[0].normalize(mousePos[0], mousePos[1], distance / 30)

    def setExampleLine(self):
        bodyShape = [18, 17, 17, 20, 21, 20, 20, 18, 18, 16,
                     16, 16, 14, 14, 14, 12, 12, 12, 8, 4]
        for i in range(20):
            self.nodes.append(Node(10, 10, bodyShape[i]))
        self.lateralPoints = self.getLateralSetPointList()
    
    def getLateralSetPointList(self):
        points = []

        # For anchor node
        if len(self.nodes) > 0:
            mousePos = pygame.mouse.get_pos()
            anchorLateralPoints = []
            for point in self.nodes[0].getLateralPoints(mousePos[0], mousePos[1]):
                anchorLateralPoints.append(point)
            points.append(anchorLateralPoints)

        # For other nodes
        for i in range(len(self.nodes)):
            if i > 0:
                targetX = self.nodes[i-1].x
                targetY = self.nodes[i-1].y
                rightPoint = self.nodes[i].getLateralPoints(targetX, targetY)[0]
                leftPoint = self.nodes[i].getLateralPoints(targetX, targetY)[1]
                points.append([rightPoint, leftPoint])
        return points
    
    def displayLateralPoints(self, screen: pygame.Surface):
        for lateralPointSet in self.lateralPoints:
            # Right point
            pygame.draw.circle(screen, pygame.color.Color(255, 0, 0), (lateralPointSet[0][0], lateralPointSet[0][1]), 5, 3)
            # Left point
            pygame.draw.circle(screen, pygame.color.Color(0, 0, 255), (lateralPointSet[1][0], lateralPointSet[1][1]), 5, 3)

    def getParametricCurvePoints(self):
        # Return empty if no lateral points
        if len(self.lateralPoints) <= 0:
            return []

        points = []
        numOfSets = len(self.lateralPoints)
        for i in range(numOfSets):
            points.append(self.lateralPoints[i][0])
        for i in range(numOfSets):
            points.append(self.lateralPoints[numOfSets - i - 1][1])
        points.append(self.lateralPoints[0][4])
        points.append(self.lateralPoints[0][2])
        points.append(self.lateralPoints[0][3])
        points.append(self.lateralPoints[0][0])

        
        # Generate t values for the given points
        num_points = len(points)
        t_points = np.linspace(0, 1, num_points)  # Assign t in [0, 1] for the given points
        
        # Separate x and y coordinates
        x_points, y_points = zip(*points)

        # Create cubic splines for x(t) and y(t)
        x_spline = CubicSpline(t_points, x_points)
        y_spline = CubicSpline(t_points, y_points)  

        # Generate parameterized values for t
        t_values = np.linspace(0, 1, 500)  # Smooth curve with 500 points
        curve_points = []
        for t in t_values:
            curve_points.append([x_spline(t), y_spline(t)])

        return curve_points
    
    def updateCurvePoints(self):
        self.curvePoints = self.getParametricCurvePoints()
    
    def displayCurvePoints(self, screen: pygame.Surface):
        # Draw the parametric curve
        for i in range(1, len(self.curvePoints)):
            # Get consecutive points
            x1, y1 = self.curvePoints[i - 1]
            x2, y2 = self.curvePoints[i]

            # Convert to native Python floats
            x1, y1, x2, y2 = float(x1), float(y1), float(x2), float(y2)

             # Ensure all coordinates are valid
            if not (isinstance(x1, (int, float)) and isinstance(y1, (int, float)) and
                    isinstance(x2, (int, float)) and isinstance(y2, (int, float))):
                print(f"Invalid points: x1={x1}, y1={y1}, x2={x2}, y2={y2}")
                continue

            # Draw line segment
            pygame.draw.line(screen, pygame.color.Color(255, 255, 255), (x1, y1), (x2, y2), 2)
            
    def displayFilledInParametricCurve(self, screen: pygame.Surface):
        # Ensure valid coordinates
        filled_curve_points = []
        for point in self.curvePoints:
            if len(point) > 0:
                x, y = point
                x = float(x)
                y = float(y)
                filled_curve_points.append((x, y))
        print(filled_curve_points)

        # Draw the filled polygon
        pygame.draw.polygon(screen, pygame.color.Color(180, 180, 255), filled_curve_points)
    
    def displayEyes(self, screen: pygame.Surface):
        print(self.lateralPoints[0])
        if len(self.lateralPoints) > 0 and len(self.lateralPoints[0]) > 5:
            eyeOne = self.lateralPoints[0][5]
            eyeTwo = self.lateralPoints[0][6]
            pygame.draw.circle(screen, pygame.color.Color(255, 255, 255), (eyeOne[0], eyeOne[1]), 3)
            pygame.draw.circle(screen, pygame.color.Color(255, 255, 255), (eyeTwo[0], eyeTwo[1]), 3)



            


            