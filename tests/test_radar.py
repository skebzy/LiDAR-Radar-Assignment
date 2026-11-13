"""Tests for the radar project.

Run using:
    python -m unittest discover -s tests -v
"""

import math
import unittest

from radar import (
    DEFAULT_OBSTACLES,
    Obstacle,
    Sensor,
    degrees_to_radians,
    locate_obstacle,
    radians_to_degrees,
    scan,
)


class AngleConversionTests(unittest.TestCase):
    # checking the degree and radian conversions

    def test_degrees_to_radians(self):
        self.assertAlmostEqual(degrees_to_radians(120), 2 * math.pi / 3)

    def test_radians_to_degrees(self):
        self.assertAlmostEqual(radians_to_degrees(3 * math.pi / 4), 135)

    def test_round_trip(self):
        angle = 73.25
        self.assertAlmostEqual(radians_to_degrees(degrees_to_radians(angle)), angle)


class SensorGeometryTests(unittest.TestCase):
    def setUp(self):
        self.sensor = Sensor(30, 120)

    # checking the circular measurements

    def test_arc_length(self):
        self.assertAlmostEqual(self.sensor.arc_length, 20 * math.pi)

    def test_sector_area(self):
        self.assertAlmostEqual(self.sensor.sector_area, 300 * math.pi)

    def test_perimeter(self):
        self.assertAlmostEqual(self.sensor.perimeter, 60 + 20 * math.pi)

    def test_triangle_and_segment_add_to_sector(self):
        self.assertAlmostEqual(
            self.sensor.triangle_area + self.sensor.segment_area,
            self.sensor.sector_area,
        )

    # checking if invalid sensor values are rejected

    def test_rejects_non_positive_range(self):
        with self.assertRaises(ValueError):
            Sensor(0, 120)

    def test_rejects_invalid_fov(self):
        for fov in (0, -10, 361):
            with self.subTest(fov=fov):
                with self.assertRaises(ValueError):
                    Sensor(30, fov)


class DetectionTests(unittest.TestCase):
    def setUp(self):
        self.sensor = Sensor(30, 120)

    # checking which obstacles should be detected

    def test_expected_detected_obstacles(self):
        results = scan(self.sensor, DEFAULT_OBSTACLES)
        detected = {item.obstacle.name for item in results if item.detected}
        self.assertEqual(detected, {"Pedestrian", "Car ahead", "Cone", "Dog"})

    def test_truck_is_too_far(self):
        truck = locate_obstacle(Obstacle("Truck", 40, 5), self.sensor)
        self.assertFalse(truck.detected)
        self.assertEqual(truck.reason, "too far")

    def test_cyclist_is_outside_angle(self):
        cyclist = locate_obstacle(Obstacle("Cyclist", 5, -15), self.sensor)
        self.assertFalse(cyclist.detected)
        self.assertEqual(cyclist.reason, "outside angle")

    def test_negative_x_axis_is_180_degrees(self):
        bus = locate_obstacle(Obstacle("Bus", -20, 0), self.sensor)
        self.assertAlmostEqual(abs(bus.angle_deg), 180)
        self.assertEqual(bus.reason, "outside angle")

    # checking the edge cases too

    def test_exact_range_boundary_is_included(self):
        boundary = locate_obstacle(Obstacle("Boundary", 30, 0), self.sensor)
        self.assertTrue(boundary.detected)

    def test_exact_angle_boundary_is_included(self):
        angle = math.radians(60)
        point = Obstacle("Edge", 30 * math.cos(angle), 30 * math.sin(angle))
        result = locate_obstacle(point, self.sensor)
        self.assertTrue(result.detected)

    def test_pole_needs_more_range(self):
        pole = locate_obstacle(Obstacle("Pole", 28, 12), self.sensor)
        self.assertAlmostEqual(pole.distance_m, math.sqrt(928))
        self.assertEqual(pole.reason, "too far")

    def test_extension_point_is_detected(self):
        result = locate_obstacle(Obstacle("Custom", 15, 25), self.sensor)
        self.assertTrue(result.detected)


if __name__ == "__main__":
    unittest.main()
