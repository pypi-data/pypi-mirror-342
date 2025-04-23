from unittest import TestCase
import numpy as np
from shapely import MultiPoint, Point

from src.bounding_shape.bounding_shape import create_bounding_area, create_spaced_points

class TestBoundingArea(TestCase):
    def test_simple_triangle(self):
        # Creates points which form a single triangle

        points = MultiPoint([[0.0, 0.0], [1.0, 2.0], [2.0, 0.0]])

        area = create_bounding_area(points=points, buffer=0.1)
        self.assertTrue(area.contains(points))
        self.assertFalse(area.contains(Point(-1.0, -1.0)))
        
    
    def test_larger_shape(self):
        # Creates points which form a pentagon
        points = MultiPoint([[0.0, 0.0], [0.0, 2.0], [1.0, 3.0], [2.0, 2.0], [2.0, 0.0]])
        area = create_bounding_area(points=points, buffer=0.1, include_outlier_points=True)
        self.assertTrue(area.contains(points))
        self.assertFalse(area.contains(Point(-1.0, -1.0)))

    
    def test_larger_shape_exclude_outlying_point(self):
        x_coords = list(np.arange(0, 5, 1))
        y_coords = list(np.arange(0, 3, 1))
        
        x, y = np.meshgrid(x_coords, y_coords)
                                    
        close_points = list(zip(x.flatten(),y.flatten()))
        distant_point = (20, 20)
                
        points = MultiPoint(close_points + [distant_point])
        area = create_bounding_area(points=points, buffer=0.1, include_outlier_points=False)
        self.assertTrue(area.contains(MultiPoint(close_points)))
        self.assertFalse(area.contains(Point(-1.0, -1.0)))
        self.assertFalse(area.contains(Point(distant_point)))


class TestGrid(TestCase):
    def test_simple_triangle(self):
        # Creates points which form a single triangle

        points = MultiPoint([[0.0, 0.0], [0.0, 100.0], [100.0, 100.0], [100.0, 0.0]])

        spaced_points = create_spaced_points(points=points, buffer=0.1, grid_spacing=20)
        # Points spaced at 10, 30, 50, 70, 90
        self.assertEqual(len(spaced_points.geoms), 25)