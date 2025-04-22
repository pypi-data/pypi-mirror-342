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

from unittest.mock import MagicMock
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
from virtual_landmark import Connections, get_extended_pose_landmarks_style

class DummyVirtualLandmark:
    def __init__(self):
        self._connections = {("NECK", "MIDDLE_HIP"), ("LEFT_SHOULDER", "NECK")}
        self._virtual_landmark = {
            "NECK": 33,
            "MIDDLE_HIP": 34,
            "LEFT_SHOULDER": 11,
        }

    def __getitem__(self, key):
        # Access by name or index
        if isinstance(key, str):
            return self._virtual_landmark[key]
        # Simulate custom landmark with slight x variation
        lm = landmark_pb2.NormalizedLandmark()
        lm.x = 0.5 + 0.1 * (key % 3 - 1)  # values: 0.4, 0.5, 0.6
        lm.y = 0.5
        lm.z = 0.5
        return lm

    def __len__(self):
        return 35  # 33 built-in + 2 custom

    def __contains__(self, item):
        return isinstance(item, int) and 0 <= item < 35

    def __iter__(self):
        return iter(range(35))

    def as_landmark_list(self):
        return MagicMock()

    @property
    def virtual_landmark(self):
        return self._virtual_landmark


def test_connections_class_properties():
    dummy = DummyVirtualLandmark()
    conn = Connections(dummy)

    assert isinstance(conn.CUSTOM_CONNECTION, list)
    assert (33, 34) in conn.CUSTOM_CONNECTION or (34, 33) in conn.CUSTOM_CONNECTION
    assert isinstance(conn.POSE_CONNECTIONS, list)
    assert isinstance(conn.ALL_CONNECTIONS, list)
    assert all(len(pair) == 2 for pair in conn.ALL_CONNECTIONS)


def test_get_extended_pose_landmarks_style():
    dummy = DummyVirtualLandmark()
    style = get_extended_pose_landmarks_style(dummy)

    assert isinstance(style, dict)
    assert 33 in style and 34 in style
    assert all(hasattr(v, 'color') for v in style.values())