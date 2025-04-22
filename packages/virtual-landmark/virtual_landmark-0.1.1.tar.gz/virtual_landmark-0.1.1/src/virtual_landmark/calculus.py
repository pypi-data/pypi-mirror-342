# Copyright 2024 cvpose
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
from mediapipe.framework.formats.landmark_pb2 import NormalizedLandmark
from typing import Tuple


def middle(p1: NormalizedLandmark, p2: NormalizedLandmark) -> Tuple[float, float, float]:
    """
    Calculates the geometric midpoint between two landmarks.

    Useful for estimating centerlines or body balance points.

    Args:
        p1 (NormalizedLandmark): First landmark.
        p2 (NormalizedLandmark): Second landmark.

    Returns:
        Tuple[float, float, float]: The midpoint (x, y, z).
    """
    a = np.array([p1.x, p1.y, p1.z])
    b = np.array([p2.x, p2.y, p2.z])
    return tuple((a + b) / 2)


def projection(p1: NormalizedLandmark, p2: NormalizedLandmark, target: NormalizedLandmark) -> Tuple[float, float, float]:
    """
    Projects a point onto the line defined by two other landmarks.

    Args:
        p1 (NormalizedLandmark): First point on the line.
        p2 (NormalizedLandmark): Second point on the line.
        target (NormalizedLandmark): The point to be projected.

    Returns:
        Tuple[float, float, float]: Coordinates of the projected point.
    """
    a = np.array([p1.x, p1.y, p1.z])
    b = np.array([p2.x, p2.y, p2.z])
    p = np.array([target.x, target.y, target.z])
    ab = b - a
    ap = p - a
    t = np.dot(ap, ab) / np.dot(ab, ab)
    return tuple(a + t * ab)


def centroid(*points: NormalizedLandmark) -> Tuple[float, float, float]:
    """
    Calculates the centroid (geometric center) of multiple landmarks.

    Args:
        *points (NormalizedLandmark): Any number of landmarks.

    Returns:
        Tuple[float, float, float]: Coordinates of the centroid.
    """
    coords = np.array([[p.x, p.y, p.z] for p in points])
    return tuple(np.mean(coords, axis=0))


def mirror(p: NormalizedLandmark, axis_point: NormalizedLandmark) -> Tuple[float, float, float]:
    """
    Reflects a landmark across a vertical axis defined by another point.

    Useful for symmetry-based mirroring (e.g., left-right body alignment).

    Args:
        p (NormalizedLandmark): The point to reflect.
        axis_point (NormalizedLandmark): Reference axis for the X reflection.

    Returns:
        Tuple[float, float, float]: Reflected point.
    """
    dx = axis_point.x - p.x
    return (axis_point.x + dx, p.y, p.z)


def weighted_average(p1: NormalizedLandmark, p2: NormalizedLandmark, w1=0.5, w2=0.5) -> Tuple[float, float, float]:
    """
    Computes a weighted average between two landmarks.

    Args:
        p1 (NormalizedLandmark): First point.
        p2 (NormalizedLandmark): Second point.
        w1 (float): Weight for p1.
        w2 (float): Weight for p2.

    Returns:
        Tuple[float, float, float]: Weighted average position.
    """
    total = w1 + w2
    a = np.array([p1.x, p1.y, p1.z]) * (w1 / total)
    b = np.array([p2.x, p2.y, p2.z]) * (w2 / total)
    return tuple(a + b)


def extend(p1: NormalizedLandmark, p2: NormalizedLandmark, factor=1.0) -> Tuple[float, float, float]:
    """
    Extends the vector from p1 to p2 beyond p2 by a given factor.

    Args:
        p1 (NormalizedLandmark): Start point of the vector.
        p2 (NormalizedLandmark): End point of the vector.
        factor (float): How much to extend beyond p2 (default = 1.0 for full vector length).

    Returns:
        Tuple[float, float, float]: New extended point.
    """
    v = np.array([p2.x, p2.y, p2.z]) - np.array([p1.x, p1.y, p1.z])
    return tuple(np.array([p2.x, p2.y, p2.z]) + v * factor)


def normalize(p1: NormalizedLandmark, p2: NormalizedLandmark) -> np.ndarray:
    """
    Returns the unit direction vector from p1 to p2.

    Args:
        p1 (NormalizedLandmark): Start point.
        p2 (NormalizedLandmark): End point.

    Returns:
        np.ndarray: Unit vector (x, y, z).
    """
    v = np.array([p2.x - p1.x, p2.y - p1.y, p2.z - p1.z])
    norm = np.linalg.norm(v)
    return v / norm if norm != 0 else v


def interpolate(p1: NormalizedLandmark, p2: NormalizedLandmark, alpha=0.5) -> Tuple[float, float, float]:
    """
    Interpolates between two landmarks with a blending factor.

    Args:
        p1 (NormalizedLandmark): Start landmark.
        p2 (NormalizedLandmark): End landmark.
        alpha (float): Interpolation factor (0.0 = p1, 1.0 = p2).

    Returns:
        Tuple[float, float, float]: Interpolated point.
    """
    a = np.array([p1.x, p1.y, p1.z])
    b = np.array([p2.x, p2.y, p2.z])
    return tuple((1 - alpha) * a + alpha * b)


def bisector(p1: NormalizedLandmark, pivot: NormalizedLandmark, p2: NormalizedLandmark) -> Tuple[float, float, float]:
    """
    Calculates the angle bisector vector between two limbs at a pivot joint.

    Useful for understanding direction flow in elbows, knees, etc.

    Args:
        p1 (NormalizedLandmark): First point forming the angle.
        pivot (NormalizedLandmark): Center of the angle.
        p2 (NormalizedLandmark): Second point forming the angle.

    Returns:
        Tuple[float, float, float]: Unit bisector vector.
    """
    v1 = normalize(pivot, p1)
    v2 = normalize(pivot, p2)
    bisect = v1 + v2
    norm = np.linalg.norm(bisect)
    return tuple(bisect / norm if norm != 0 else bisect)


def rotate(p: NormalizedLandmark, axis_p1: NormalizedLandmark, axis_p2: NormalizedLandmark, angle: float) -> Tuple[float, float, float]:
    """
    Rotates a landmark around a 3D axis defined by two other landmarks.

    Uses Rodrigues’ rotation formula for 3D rotation.

    Args:
        p (NormalizedLandmark): Point to rotate.
        axis_p1 (NormalizedLandmark): Axis start.
        axis_p2 (NormalizedLandmark): Axis end.
        angle (float): Rotation angle in radians.

    Returns:
        Tuple[float, float, float]: Rotated point (x, y, z).
    """
    point = np.array([p.x, p.y, p.z])
    a = np.array([axis_p1.x, axis_p1.y, axis_p1.z])
    b = np.array([axis_p2.x, axis_p2.y, axis_p2.z])
    k = b - a
    k = k / np.linalg.norm(k)
    v = point - a
    cos_theta = np.cos(angle)
    sin_theta = np.sin(angle)
    v_rot = (v * cos_theta +
             np.cross(k, v) * sin_theta +
             k * (np.dot(k, v)) * (1 - cos_theta))
    return tuple(v_rot + a)