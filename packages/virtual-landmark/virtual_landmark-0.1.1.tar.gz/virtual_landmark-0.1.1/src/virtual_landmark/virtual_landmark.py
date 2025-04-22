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

from .abstract_landmark import AbstractLandmark


class VirtualLandmark(AbstractLandmark):
    """
    Concrete class that automatically detects and registers virtual landmarks
    defined using the @landmark decorator. Each method returns a 3D point and
    may declare connections to other landmarks.

    It extends AbstractLandmark and supports:
    - Dynamic landmark creation
    - Automatic connection registration
    """

    def __init__(self, landmarks):
        super().__init__(landmarks)
        self._process_virtual_landmarks()

    def _process_virtual_landmarks(self):
        """
        Scans the class for methods decorated with @landmark, executes them to
        get the 3D points, and registers them using _add_landmark and _add_connection.
        """
        for attr_name in dir(self):
            method = getattr(self, attr_name)
            if callable(method) and getattr(method, "_is_custom_landmark", False):
                name = method._landmark_name
                connections = method._landmark_connections

                point = method()
                self._add_landmark(name, point)
                self._add_connection(name, connections)
                
    @property
    def virtual_landmark(self):
        return self._virtual_landmark