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

import abc
import numpy as np
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2

from .virtual_pose_landmark import VirtualPoseLandmark


class AbstractLandmark(abc.ABC):
    """
    Abstract class that encapsulates MediaPipe pose landmarks and allows
    adding virtual (custom) landmarks while maintaining compatibility with 
    MediaPipe's landmark list structure.

    This class supports iteration, indexing, and conversion to MediaPipe's
    `NormalizedLandmarkList`. It is designed to be extended by subclasses
    that compute and register additional landmarks dynamically.

    Attributes:
        landmark_list (NormalizedLandmarkList): Combined list of original and added landmarks.
    """

    def __init__(self, landmarks):
        """
        Initializes the class with a copy of the original MediaPipe landmarks.

        Args:
            landmarks (List[NormalizedLandmark]): List of landmarks from MediaPipe's pose estimation.
        """
        self._landmark_list = landmark_pb2.NormalizedLandmarkList()
        self._landmark_list.landmark.extend(landmarks)

        self._virtual_landmark = VirtualPoseLandmark()

        self._connections = set()

    def _add_landmark(self, name: str, point):
        """
        Adds a new virtual landmark to the landmark list.

        Args:
            point (Union[tuple, list, np.ndarray]): A normalized 3D point (x, y, z), 
                where each value is typically between 0 and 1.

        Returns:
            int: Index of the newly added landmark in the full landmark list.

        Raises:
            ValueError: If the input point is not a 3D coordinate.
        """
        if not isinstance(point, (list, tuple, np.ndarray)) or len(point) < 3:
            raise ValueError("point must be a 3D tuple/list/np.ndarray")

        lm = landmark_pb2.NormalizedLandmark()
        lm.x, lm.y, lm.z = float(point[0]), float(point[1]), float(point[2])
        lm.visibility = 1.0
        self._landmark_list.landmark.append(lm)

        idx = len(self._landmark_list.landmark) - 1

        self._virtual_landmark[name] = idx

        return idx

    def _add_connection(self, name: str, targets: list):
        """
        Adds connections between a landmark and a list of other landmarks.

        Args:
            name (str): The base landmark name.
            targets (List[Union[str, Enum]]): List of target landmark names or enums.
        """
        for target in targets:
            a = name
            b = target.name if hasattr(target, "name") else target
            self._connections.add(tuple(sorted((a, b))))

    def as_landmark_list(self):
        """
        Returns the complete landmark list in the MediaPipe format.

        Returns:
            NormalizedLandmarkList: Combined list of original and custom landmarks.
        """
        return self._landmark_list

    def __getitem__(self, idx):
        """
        Access a landmark by index.

        Args:
            idx (int): Index of the landmark.

        Returns:
            NormalizedLandmark: Landmark at the given index.
        """
        return self._landmark_list.landmark[idx]

    def __len__(self):
        """
        Returns the total number of landmarks.

        Returns:
            int: Count of all landmarks (original + custom).
        """
        return len(self._landmark_list.landmark)

    def __iter__(self):
        """
        Iterates over the complete landmark list.

        Returns:
            Iterator[NormalizedLandmark]: An iterator over all landmarks.
        """
        return iter(self._landmark_list.landmark)
    
    def __contains__(self, index: int) -> bool:
        """
        Checks whether a landmark index is within the bounds of the list.

        Args:
            index (int): Index to check.

        Returns:
            bool: True if the index exists, False otherwise.
        """
        return 0 <= index < len(self)

    def __repr__(self):
        """
        Returns a string representation showing number of landmarks and connections.

        Returns:
            str: Descriptive string of the VirtualLandmark object.
        """
        return (
            f"<VirtualLandmark landmarks={len(self)} "
            f"custom={len(self._virtual_landmark) - 33} "
            f"connections={len(self._connections)}>"
        )
