import numpy as np
from node import Node


class KinematicsHandler:
    def __init__(self, node_spacing: float):
        self.node_spacing = node_spacing

    def applyForwardsDistanceConstraint(self, nodes: list[Node]):
        """
        Checks to see any nodes are too far apart with respect to set node_spacing. If they are, normalize starting from first node
        """
        for i in range(len(nodes)):
            # Check if beyond node_spacing
            distance = nodes[i].nodeDistance(nodes[i-1])
            if i > 0 and distance > self.node_spacing:
                nodes[i].normalize(nodes[i-1].x, nodes[i-1].y, distance - self.node_spacing)

    def applyBackwardsDistanceConstraint(self, nodes: list[Node]):
        """
        Checks to see any nodes are too far apart with respect to set node_spacing. If they are, normalize starting from first node
        """
        for i in range(len(nodes) - 1):
            # Start from end
            i = len(nodes) - i - 2

            # Check if beyond node_spacing
            distance = nodes[i].nodeDistance(nodes[i+1])
            if i > 0 and distance > self.node_spacing:
                nodes[i].normalize(nodes[i+1].x, nodes[i+1].y, distance - self.node_spacing)

    def applyForwardsNodeSpacing(self, nodes: list[Node]):
        for i in range(len(nodes)):
            if i > 0:
                distance = nodes[i].nodeDistance(nodes[i-1])
                nodes[i].normalize(nodes[i-1].x, nodes[i-1].y, distance - self.node_spacing)

    def applyBackwardsNodeSpacing(self, nodes: list[Node]):
        for i in range(len(nodes) - 1):
            # Start from end
            i = len(nodes) - i - 2
            if i > 0:
                distance = nodes[i].nodeDistance(nodes[i+1])
                nodes[i].normalize(nodes[i+1].x, nodes[i+1].y, distance - self.node_spacing)
    
    def applyAngleConstraint(self, nodes: list[Node], angle_margin: float):
        """
        Constrains the curvature of the section by limiting the angle formed by each triplet of nodes.
        :param nodes: List of Node objects in the section.
        :param angle_margin: Maximum allowed curvature angle (in radians).
        """
        if len(nodes) < 3:
            return  # Not enough nodes to calculate curvature

        for i in range(1, len(nodes) - 1):
            # Get the coordinates of the three points
            prev_node = nodes[i - 1]
            curr_node = nodes[i]
            next_node = nodes[i + 1]

            # Calculate vectors
            v1 = np.array([curr_node.x - prev_node.x, curr_node.y - prev_node.y])
            v2 = np.array([next_node.x - curr_node.x, next_node.y - curr_node.y])

            # Normalize vectors to calculate angle
            norm_v1 = np.linalg.norm(v1)
            norm_v2 = np.linalg.norm(v2)
            if norm_v1 == 0 or norm_v2 == 0:
                continue  # Skip if nodes are coincident

            unit_v1 = v1 / norm_v1
            unit_v2 = v2 / norm_v2

            # Calculate the angle between vectors
            dot_product = np.dot(unit_v1, unit_v2)
            angle = np.arccos(np.clip(dot_product, -1.0, 1.0))  # Clip for numerical stability

            # Check if the angle exceeds the margin
            if angle > angle_margin:
                # Calculate the clamped angle
                clamped_angle = angle_margin

                # Adjust the position of the next node to satisfy the clamped angle
                bisector = (unit_v1 + unit_v2) / np.linalg.norm(unit_v1 + unit_v2)
                distance = curr_node.nodeDistance(next_node)
                next_node.x = curr_node.x + distance * bisector[0]
                next_node.y = curr_node.y + distance * bisector[1]