# This file contains utility functions for geometric calculations involving circles and lines

# Imports
import numpy as np
import math

def compute_tangents_circle(circle_center: np.array, circle_radius: float, point: np.array, extension_length: float = 1000) -> list:
    """
    Compute the tangent points from a given point to a circle and extend the tangent lines.
    
    Args:
    -----
        circle_center (np.array): The center of the circle as a numpy array [x, y].
        circle_radius (float): The radius of the circle.
        point (np.array): The point from which tangents are drawn as a numpy array [x, y].
        extension_length (float, optional): The length to which the tangent lines are extended. Default is 100.
    
    Returns:
    --------
        list: A list containing the tangent points and extended tangent lines. 
              Format: [tangent_point_1, tangent_point_2, extended_tangent_line_1, extended_tangent_line_2]
    
    Raises:
    -------
        ValueError: If the point is inside the circle, making tangents impossible.
    """
    
    # Extract x and y coordinates of the point and the circle center
    point_x, point_y = point
    circle_center_x, circle_center_y = circle_center
    
    # Compute the difference in x and y coordinates between the point and the circle center
    diff_x, diff_y = point_x - circle_center_x, point_y - circle_center_y
    
    # Calculate the distance from the point to the circle center using the Pythagorean theorem
    distance = np.hypot(diff_x, diff_y)
    
    # Check if the point is inside or on the circle, making tangents impossible
    if distance <= circle_radius:
        raise ValueError("No tangents possible: point is inside or on the circle.")
    
    # Compute the angle from the point to the circle center using arctan2
    angle_to_center = np.arctan2(diff_y, diff_x)
    
    # Compute the angle offset for the tangents using the inverse cosine
    angle_offset = np.arccos(circle_radius / distance)
    
    # Calculate the angles for the two tangent points
    angles = [angle_to_center - angle_offset, angle_to_center + angle_offset]
    
    # Calculate the tangent points using polar to Cartesian conversion
    tangent_points = [
        (circle_center_x + circle_radius * np.cos(a), circle_center_y + circle_radius * np.sin(a))
        for a in angles
    ]
    
    # Calculate the extended tangent lines
    extended_tangent_lines = []
    for tangent_point in tangent_points:
        # Calculate the direction vector from the point to the tangent point
        direction = np.array(tangent_point) - point
        # Normalize the direction vector to get a unit vector
        direction = direction / np.linalg.norm(direction)
        # Calculate the end point of the extended line
        end_point = point + direction * extension_length
        # Add the line (starting from the original point) to the list
        extended_tangent_lines.append((tuple(point), tuple(end_point)))
    
    # Return the tangent points and extended tangent lines
    return tangent_points + extended_tangent_lines

def does_line_intersect_circle(point1: np.array, point2: np.array, circle_center: np.array, circle_radius: float) -> bool:
    """
    Determine if a straight line from point1 to point2 intersects a circle.

    Args:
    -----
        point1 (np.array): The first point of the line segment as a numpy array [x1, y1].
        point2 (np.array): The second point of the line segment as a numpy array [x2, y2].
        circle_center (np.array): The center of the circle as a numpy array [cx, cy].
        circle_radius (float): The radius of the circle.

    Returns:
    --------
        bool: True if the line segment intersects the circle, False otherwise.
    """
    
    # Extract the coordinates of the points and circle center
    point1_x, point1_y = point1
    point2_x, point2_y = point2
    circle_center_x, circle_center_y = circle_center

    # Calculate the differences in x and y coordinates of the line segment
    diff_x, diff_y = point2_x - point1_x, point2_y - point1_y

    # Calculate the coefficients of the line equation ax + by + c = 0
    a = diff_y
    b = -diff_x
    c = diff_x * point1_y - diff_y * point1_x

    # Calculate the perpendicular distance from the center of the circle to the line
    distance = abs(a * circle_center_x + b * circle_center_y + c) / np.sqrt(a**2 + b**2)

    # Check if the distance is greater than the radius (no intersection possible)
    if distance > circle_radius:
        return False

    # Further check if the closest point on the line segment to the circle's center lies within the segment
    dot = (circle_center_x - point1_x) * diff_x + (circle_center_y - point1_y) * diff_y
    len_sq = diff_x**2 + diff_y**2
    param = dot / len_sq

    # Determine the closest point on the segment
    if param < 0:
        closest_x, closest_y = point1_x, point1_y
    elif param > 1:
        closest_x, closest_y = point2_x, point2_y
    else:
        closest_x = point1_x + param * diff_x
        closest_y = point1_y + param * diff_y

    # Calculate the distance from the closest point to the circle's center
    closest_distance = np.hypot(closest_x - circle_center_x, closest_y - circle_center_y)

    # Return True if the closest distance is less than the radius (intersection occurs)
    return closest_distance < circle_radius

def shortest_path_with_circle(circle_center: np.array, circle_radius: float, point1: np.array, point2: np.array):
    """
    Find the shortest path between two points that avoids intersecting a circle.

    Args:
    -----
    circle_center (np.array): The center of the circle as a numpy array [x, y].
    circle_radius (float): The radius of the circle.
    point1 (np.array): The starting point as a numpy array [x, y].
    point2 (np.array): The ending point as a numpy array [x, y].

    Returns:
    --------
    tuple: (shortest_distance, path_points)
        shortest_distance (float): The length of the shortest path.
        path_points (list): List of points along the shortest path.
    """
    
    # Check if the direct path intersects the circle
    if not does_line_intersect_circle(point1, point2, circle_center, circle_radius):
        # If no intersection, return the direct distance and path
        return np.linalg.norm(point2 - point1), [point1, point2]
    
    # Compute tangent points for both points
    tangents1 = compute_tangents_circle(circle_center, circle_radius, point1)
    tangents2 = compute_tangents_circle(circle_center, circle_radius, point2)
    
    # Extract tangent points
    t1a, t1b = np.array(tangents1[0]), np.array(tangents1[1])
    t2a, t2b = np.array(tangents2[0]), np.array(tangents2[1])
    
    # Calculate distances and paths for all possible combinations of tangent points
    paths = [
        (np.linalg.norm(t1a - point1) + np.linalg.norm(t2a - point2) + arc_length(circle_center, circle_radius, t1a, t2a),
         [point1, t1a, t2a, point2]),
        (np.linalg.norm(t1b - point1) + np.linalg.norm(t2b - point2) + arc_length(circle_center, circle_radius, t1b, t2b),
         [point1, t1b, t2b, point2]),
        (np.linalg.norm(t1a - point1) + np.linalg.norm(t2b - point2) + arc_length(circle_center, circle_radius, t1a, t2b),
         [point1, t1a, t2b, point2]),
        (np.linalg.norm(t1b - point1) + np.linalg.norm(t2a - point2) + arc_length(circle_center, circle_radius, t1b, t2a),
         [point1, t1b, t2a, point2])
    ]
    
    # Return the shortest path and its points
    return min(paths, key=lambda x: x[0])

def arc_length(center: np.array, radius: float, point1: np.array, point2: np.array) -> float:
    """
    Calculate the length of the shorter arc between two points on a circle.

    Args:
    -----
    center (np.array): The center of the circle as a numpy array [x, y].
    radius (float): The radius of the circle.
    point1 (np.array): First point on the circle circumference as a numpy array [x1, y1].
    point2 (np.array): Second point on the circle circumference as a numpy array [x2, y2].

    Returns:
    --------
    float: Length of the shorter arc between point1 and point2.
    """
    # Calculate vectors from center to points
    v1 = point1 - center
    v2 = point2 - center
    
    # Calculate the dot product of the vectors
    dot_product = np.dot(v1, v2)
    
    # Calculate the angle between the vectors, ensuring the result is within [-1, 1]
    angle = np.arccos(np.clip(dot_product / (radius ** 2), -1.0, 1.0))
    
    # Return the length of the shorter arc
    return radius * min(angle, 2*np.pi - angle)

def calculate_angle(point: np.array, source: np.array) -> float:
    """
    Calculate the angle of a line with respect to point p1.

    Parameters
    ----------
    point : 
        The target point.
    p1 : 
        The reference point.

    Returns
    -------
    angle : float
        The angle in radians.
    """
    vector = (point[0] - source[0], point[1] - source[1])
    angle = math.atan2(vector[1], vector[0])
    
    # Normalize angle to [0, 2*pi]
    if angle < 0:
        angle += 2 * math.pi

    return angle
