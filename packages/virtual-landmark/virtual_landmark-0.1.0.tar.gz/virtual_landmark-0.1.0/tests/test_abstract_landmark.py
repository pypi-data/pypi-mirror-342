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

import pytest
from mediapipe.framework.formats.landmark_pb2 import NormalizedLandmark
from virtual_landmark.abstract_landmark import AbstractLandmark

class DummyLandmark(AbstractLandmark):
    def add_virtual(self, name, point, connections=None):
        idx = self._add_landmark(name, point)
        if connections:
            self._add_connection(name, connections)
        return idx

@pytest.fixture
def sample_landmarks():
    landmarks = []
    for i in range(3):
        lm = NormalizedLandmark(x=i, y=i, z=i, visibility=1.0)
        landmarks.append(lm)
    return landmarks

def test_initialization(sample_landmarks):
    obj = DummyLandmark(sample_landmarks)
    assert len(obj) == 3
    assert isinstance(obj.as_landmark_list().landmark[0], NormalizedLandmark)

def test_add_landmark_success(sample_landmarks):
    obj = DummyLandmark(sample_landmarks)
    idx = obj.add_virtual("NECK", (0.5, 0.5, 0.5))
    assert idx == 3
    assert len(obj) == 4
    assert obj[idx].x == 0.5

def test_add_landmark_invalid_type(sample_landmarks):
    obj = DummyLandmark(sample_landmarks)
    with pytest.raises(ValueError):
        obj.add_virtual("BAD", 123)
    with pytest.raises(ValueError):
        obj.add_virtual("BAD", [1.0])

def test_add_connection_with_string(sample_landmarks):
    obj = DummyLandmark(sample_landmarks)
    obj.add_virtual("NECK", (0.5, 0.5, 0.5), ["CHEST", "NOSE"])
    assert ("CHEST", "NECK") in obj._connections

def test_add_connection_with_enum(sample_landmarks):
    class EnumMock:
        def __init__(self, name): self.name = name
    obj = DummyLandmark(sample_landmarks)
    obj.add_virtual("CHEST", (0.1, 0.2, 0.3), [EnumMock("LEFT"), "RIGHT"])
    assert ("CHEST", "RIGHT") in obj._connections

def test_index_access_and_iteration(sample_landmarks):
    obj = DummyLandmark(sample_landmarks)
    assert obj[1].x == 1
    assert 2 in obj
    assert 100 not in obj
    for i, lm in enumerate(obj):
        assert lm.x == i

def test_repr(sample_landmarks):
    obj = DummyLandmark(sample_landmarks)
    obj.add_virtual("NECK", (0.1, 0.1, 0.1))
    rep = repr(obj)
    assert "landmarks=4" in rep
    assert "custom=1" in rep