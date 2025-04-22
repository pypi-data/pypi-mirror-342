# Copyright 2024 cvpose
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
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

from virtual_landmark.calculus import (
    middle, projection, centroid, mirror,
    weighted_average, extend, normalize,
    interpolate, bisector, rotate
)

def lm(x, y, z):
    return NormalizedLandmark(x=x, y=y, z=z, visibility=1.0)

def test_middle():
    assert middle(lm(0, 0, 0), lm(2, 2, 2)) == (1.0, 1.0, 1.0)

def test_projection():
    result = projection(lm(0, 0, 0), lm(1, 0, 0), lm(0.5, 1, 0))
    assert np.allclose(result, (0.5, 0, 0))

def test_centroid():
    result = centroid(lm(0, 0, 0), lm(2, 2, 2), lm(1, 1, 1))
    assert result == (1.0, 1.0, 1.0)

def test_mirror():
    result = mirror(lm(0.2, 0.5, 0.5), lm(0.5, 0.5, 0.5))
    assert result == (0.7999999970197678, 0.5, 0.5)

def test_weighted_average():
    result = weighted_average(lm(0, 0, 0), lm(2, 2, 2), 1, 3)
    assert result == (1.5, 1.5, 1.5)

def test_extend():
    result = extend(lm(0, 0, 0), lm(1, 0, 0), 2)
    assert result == (3.0, 0.0, 0.0)

def test_normalize_nonzero():
    result = normalize(lm(0, 0, 0), lm(1, 0, 0))
    assert np.allclose(result, [1, 0, 0])

def test_normalize_zero_vector():
    result = normalize(lm(0, 0, 0), lm(0, 0, 0))
    assert np.allclose(result, [0, 0, 0])

def test_interpolate_halfway():
    result = interpolate(lm(0, 0, 0), lm(2, 2, 2))
    assert result == (1.0, 1.0, 1.0)

def test_interpolate_custom_alpha():
    result = interpolate(lm(0, 0, 0), lm(10, 10, 10), alpha=0.2)
    assert result == (2.0, 2.0, 2.0)

def test_bisector():
    result = bisector(lm(0, 1, 0), lm(0, 0, 0), lm(1, 0, 0))
    expected = normalize(lm(0, 0, 0), lm(1, 1, 0))
    assert np.allclose(result, expected)

def test_bisector_zero_vector():
    result = bisector(lm(0, 0, 0), lm(0, 0, 0), lm(0, 0, 0))
    assert np.allclose(result, [0, 0, 0])

def test_rotate_identity():
    result = rotate(lm(1, 0, 0), lm(0, 0, 0), lm(0, 0, 1), angle=0)
    assert np.allclose(result, [1, 0, 0])

def test_rotate_quarter_turn():
    result = rotate(lm(1, 0, 0), lm(0, 0, 0), lm(0, 0, 1), angle=np.pi / 2)
    assert np.allclose(result, [0, 1, 0], atol=1e-6)