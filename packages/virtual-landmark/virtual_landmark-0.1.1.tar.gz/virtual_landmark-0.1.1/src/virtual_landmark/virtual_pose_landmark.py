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

import mediapipe as mp

PoseLandmark = mp.solutions.pose.PoseLandmark


class VirtualPoseLandmark(dict):
    """
    A dynamic simulation of an enum that contains both MediaPipe's built-in pose landmarks
    and user-defined virtual landmarks.

    Provides access to landmarks via both string names and integer indices. New landmarks
    can be registered at runtime while preserving bi-directional mapping.

    Features:
    - Name-to-index access: `vpl["NECK"]` → 33
    - Attribute access: `vpl.NECK` → 33
    - Index-to-name access: `vpl[33]` → "NECK"
    - Dynamic insertion of custom landmark names and indices.

    Example:
        >>> vpl = VirtualPoseLandmark()
        >>> vpl["LEFT_EAR"]
        7
        >>> vpl[7]
        'LEFT_EAR'
        >>> vpl.add("NECK", 33)
        >>> vpl.NECK
        33
    """

    def __init__(self):
        super().__init__()
        self._reverse = {}  # Maps index → name
        self._load_builtin_landmarks()

        # Provide attribute-style access for all landmarks
        for name in self:
            setattr(self, name, self[name])

    def _load_builtin_landmarks(self):
        """
        Loads all MediaPipe built-in pose landmarks into the internal map.

        These landmarks are taken from `mp.solutions.pose.PoseLandmark` and include
        standard names like "NOSE", "LEFT_EAR", "RIGHT_SHOULDER", etc.
        """
        for landmark in PoseLandmark:
            self[landmark.name] = landmark.value
            self._reverse[landmark.value] = landmark.name

    def add(self, name: str, index: int):
        """
        Adds a new virtual landmark to the mapping.

        Useful for dynamically generated or computed landmarks such as virtual joints
        (e.g., "NECK", "THORAX", "CENTER_MASS").

        Args:
            name (str): Name of the new landmark (must be a valid Python identifier).
            index (int): Numerical index to assign.

        Raises:
            ValueError: If name or index already exists, or name is invalid.
        """
        if not isinstance(name, str) or not name.isidentifier():
            raise ValueError("Custom landmark name must be a valid identifier string.")
        if name in self:
            raise ValueError(f"Landmark '{name}' is already defined.")
        if index in self._reverse:
            raise ValueError(
                f"Index {index} is already used by landmark '{self._reverse[index]}'."
            )

        self[name] = index
        self._reverse[index] = name
        setattr(self, name, index)

    def __getattr__(self, name):
        """
        Enables attribute-style access (e.g., vpl.LEFT_HIP).
        """

        if name in self:
            return self[name]

        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{name}'"
        )

    def __getitem__(self, key):
        """
        Supports both name-based and index-based access:
        - `vpl["NOSE"]` → 0
        - `vpl[0]` → "NOSE"
        """
        if isinstance(key, int):
            return self._reverse[key]

        return super().__getitem__(key)

    def __contains__(self, item):
        """
        Checks for existence by either name or index.
        """
        if isinstance(item, int):
            return item in self._reverse

        return super().__contains__(item)

    def __repr__(self):
        """
        Returns a compact summary of the landmark mapping.
        """
        return f"<VirtualPoseLandmark {dict(self)}>"
