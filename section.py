from typing import Tuple
from constants import BLUE, GREEN, RED
from inverseKinematicsHandler import InverseKinematicsHandler
from kinematicsHandler import KinematicsHandler
from node import Node
import pygame
from scipy.interpolate import CubicSpline
import numpy as np

class Section:
    def __init__(self, nodes: list[Node], node_spacing: float):
        """
        Holds a list of nodes within set distance. First node is anchor node. Also has capability to draw parametric boundary as well to fill in section on pygame screen.
        """
        self.nodes: list[Node] = nodes
        self.kinematicsHandler = InverseKinematicsHandler(3, node_spacing)
        self.lateralPoints = self.getLateralSetPointList()
        self.curvePoints = self.getParametricCurvePoints()
        self.colors = [BLUE, RED, GREEN]
        self.currentColorIndex = 0
        pass

# --- Update --- #

    def update(self):
        self.applyDistanceConstraint()
        # self.kinematicsHandler.applyAngleConstraint(self.nodes, angle_margin=np.pi / 16)
        self.updateLateralPointSetPositions()
        self.updateCurvePoints()

    def updateLateralPointSetPositions(self):
        self.lateralPoints = self.getLateralSetPointList()

    def updateCurvePoints(self):
        self.curvePoints = self.getParametricCurvePoints()

    def applyDistanceConstraint(self):
        self.kinematicsHandler.applyForwardsDistanceConstraint(self.nodes)

# --- Set --- #:

    def switchColor(self):
        if self.currentColorIndex >= len(self.colors) - 1:
            self.currentColorIndex = 0
        else:
            self.currentColorIndex += 1

    def setAnchorNodePosition(self, x, y):
        self.nodes[0].x = x
        self.nodes[0].y = y

    def extendTowards(self, target: Tuple[int, int]):
        for i in range(len(self.nodes) - 1):
            newPosition = self.nodes[i].getRelativePoint(target[0], target[1], self.kinematicsHandler.node_spacing)
            self.nodes[i + 1].x = newPosition[0]
            self.nodes[i + 1].y = newPosition[1]
# --- Get --- #

    def getCurrentColor(self):
        return self.colors[self.currentColorIndex]
  
    def getLateralSetPointList(self):
        points = []

        # For anchor node
        if len(self.nodes) > 1:
            anchorLateralPoints = []
            for point in self.nodes[0].getAnchorLateralPoints(self.nodes[1].x, self.nodes[1].y):
                anchorLateralPoints.append(point)
            points.append(anchorLateralPoints)

        # For other nodes
        for i in range(len(self.nodes)):
            if i > 0:
                targetX = self.nodes[i-1].x
                targetY = self.nodes[i-1].y

                lateralPoints = []
                for point in self.nodes[i].getLateralPoints(targetX, targetY):
                    lateralPoints.append(point)
                points.append(lateralPoints)

        return points

    def getParametricCurvePoints(self):
        # Return empty if no lateral points
        if len(self.lateralPoints) <= 0:
            return []

        points = []
        numOfSets = len(self.lateralPoints)

        # Add overlapping point for smooth edge at start point
        points.append(self.lateralPoints[0][3])

        # Add points
        for i in range(numOfSets):
            points.append(self.lateralPoints[i][0])
        for i in range(numOfSets):
            points.append(self.lateralPoints[numOfSets - i - 1][1])

        # Add anchor points
        points.append(self.lateralPoints[0][4])
        points.append(self.lateralPoints[0][2])
        points.append(self.lateralPoints[0][3])
        points.append(self.lateralPoints[0][0])

        # Add overlapping point for smooth edge at start point
        points.append(self.lateralPoints[1][0])

        
        # Generate t values for the given points
        num_points = len(points)
        t_points = np.linspace(0, 1, num_points)  # Assign t in [0, 1] for the given points

        # Ignore overlapping points put in to smooth out starting edge
        start_t = t_points[1]
        end_t = t_points[len(t_points) - 2]
        
        # Separate x and y coordinates
        x_points, y_points = zip(*points)

        # Create cubic splines for x(t) and y(t)
        x_spline = CubicSpline(t_points, x_points)
        y_spline = CubicSpline(t_points, y_points)  

        # Generate parameterized values for t
        t_values = np.linspace(0, 1, 500)  # Smooth curve with 1000 points
        curve_points = []
        for t in t_values:
            if t > start_t and t < end_t:
                curve_points.append([x_spline(t), y_spline(t)])

        return curve_points
    
    def getTotalLength(self):
        return self.node_spacing * (len(self.nodes)-1)
# --- Display --- #

    def display(self, screen: pygame.Surface):
        self.displayCurvePoints(screen)
        self.displayFilledInParametricCurve(screen)

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
            pygame.draw.line(screen, pygame.color.Color(255, 255, 255), (x1, y1), (x2, y2), 5)
            
    def displayFilledInParametricCurve(self, screen: pygame.Surface):

        # Ensure valid coordinates
        filled_curve_points = []
        for point in self.curvePoints:
            if len(point) > 0:
                x, y = point
                x = float(x)
                y = float(y)
                filled_curve_points.append((x, y))

        # Draw the filled polygon
        pygame.draw.polygon(screen, self.getCurrentColor(), filled_curve_points)

    def displayLateralPoints(self, screen: pygame.Surface):
        for lateralPointSet in self.lateralPoints:
            for point in lateralPointSet:
                pygame.draw.circle(screen, pygame.color.Color(150, 140, 130), (point[0], point[1]), 5, 3)
            # Right point
            pygame.draw.circle(screen, pygame.color.Color(255, 0, 0), (lateralPointSet[0][0], lateralPointSet[0][1]), 5, 3)
            # Left point
            pygame.draw.circle(screen, pygame.color.Color(0, 0, 255), (lateralPointSet[1][0], lateralPointSet[1][1]), 5, 3)

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

    def displayNodes(self, screen: pygame.Surface):
        """
        Display nodes onto inputed pygame surface
        """
        for node in self.nodes:
            node.display(screen)
    
