import unittest
import numpy as np
import pygame
from node import Node
from legNode import LegNode
from leg import Leg
from section import Section
from kinematicsHandler import KinematicsHandler
from inverseKinematicsHandler import InverseKinematicsHandler
from body import Body


class TestNode(unittest.TestCase):
    def test_node_distance(self):
        node1 = Node(0, 0, 5, None)
        node2 = Node(3, 4, 5, None)
        self.assertAlmostEqual(node1.nodeDistance(node2), 5.0)

    def test_coordinate_distance(self):
        node = Node(0, 0, 5, None)
        self.assertAlmostEqual(node.coordinateDistance(3, 4), 5.0)

    def test_normalize(self):
        node = Node(0, 0, 5, None)
        node.normalize(6, 8, 5)
        self.assertAlmostEqual(node.x, 3.0)
        self.assertAlmostEqual(node.y, 4.0)


class TestLeg(unittest.TestCase):
    def test_leg_set_example(self):
        leg = Leg([], 10, Node(0, 0, 5, None))
        leg.setExampleLeg()
        self.assertEqual(len(leg.nodes), 5)

    def test_leg_move_end_to(self):
        leg = Leg([Node(0, 0, 5, None)], 10, Node(0, 0, 5, None))
        leg.moveLegEndTo([10, 0])
        self.assertAlmostEqual(leg.nodes[-1].x, 10)


class TestLegNode(unittest.TestCase):
    def test_target_positions(self):
        leg_node = LegNode(0, 0, 5, Node(10, 0, 5, None), 100, [], [(10, np.pi / 4)])
        target = leg_node.getTargetPosition((10, 0), 0)
        self.assertEqual(len(target), 2)

    def test_move_legs_towards_target(self):
        leg = Leg([], 10, Node(0, 0, 5, None))
        leg.setExampleLeg()
        leg_node = LegNode(0, 0, 5, Node(10, 0, 5, None), 100, [leg], [(10, np.pi / 4)])
        leg_node.moveLegsTowardsTarget(0.5)
        self.assertTrue(len(leg.nodes) > 0)


class TestSection(unittest.TestCase):
    def test_set_anchor_position(self):
        section = Section([Node(0, 0, 5, None)], 10)
        section.setAnchorNodePosition(10, 10)
        self.assertEqual(section.nodes[0].x, 10)

    def test_get_total_length(self):
        section = Section([Node(0, 0, 5, None), Node(10, 0, 5, None)], 10)
        self.assertEqual(section.getTotalLength(), 10)

    def test_apply_distance_constraint(self):
        section = Section([Node(0, 0, 5, None), Node(15, 0, 5, None)], 10)
        section.applyDistanceConstraint()
        self.assertAlmostEqual(section.nodes[1].x, 10)


class TestKinematicsHandler(unittest.TestCase):
    def test_distance_constraints(self):
        handler = KinematicsHandler(10)
        nodes = [Node(0, 0, 5, None), Node(15, 0, 5, None)]
        handler.applyForwardsDistanceConstraint(nodes)
        self.assertAlmostEqual(nodes[1].x, 10)


class TestInverseKinematicsHandler(unittest.TestCase):
    def test_fabrik(self):
        handler = InverseKinematicsHandler(1, 10)
        nodes = [Node(0, 0, 5, None), Node(15, 0, 5, None)]
        target = (10, 0)
        handler.fabrik(nodes, target)
        self.assertAlmostEqual(nodes[-1].x, 10)


class TestBody(unittest.TestCase):
    def test_body_update_leg_nodes(self):
        body = Body([], 10)
        body.setExampleBody()
        body.updateLegNodes()
        for node in body.nodes:
            if isinstance(node, LegNode):
                self.assertTrue(len(node.legs) > 0)

    def test_body_display_legs(self):
        body = Body([], 10)
        body.setExampleBody()
        screen = pygame.Surface((500, 500))
        body.display(screen)  # Visual test, ensure no exceptions


if __name__ == "__main__":
    unittest.main()
