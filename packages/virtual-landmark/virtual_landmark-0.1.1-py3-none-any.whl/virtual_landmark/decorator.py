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

def landmark(name: str, connection: list[str] = None):
    """
    Decorator to register a method as a virtual landmark generator with optional connections.

    This decorator marks a method as responsible for calculating a virtual landmark
    with a unique name. When the containing class is instantiated, all decorated methods
    are automatically executed, and their return values are added to the final landmark list.

    Additionally, you can specify virtual connections to other named landmarks using
    the `connection` parameter. These connections define topological relationships between
    virtual landmarks (e.g., connecting "NECK" to "LEFT_SHOULDER"), and are stored as
    unique, undirected pairs.

    The generated landmark becomes accessible as a dynamic attribute with enum-like behavior:
        - `instance.NAME` → a dynamic object with `.value` (the landmark index)
        - `instance[instance.NAME.value]` → the corresponding NormalizedLandmark
        - The landmark is also included in `CUSTOM_CONNECTIONS` if connected

    Args:
        name (str): Unique name/key to associate with the custom landmark. Must be a valid identifier.
        connection (list[str], optional): Names of other landmarks to which this one should connect.
            Defaults to an empty list if not provided.

    Returns:
        Callable: The original method, wrapped with metadata used during class initialization.

    Example:
        @landmark(\"NECK\", connection=[\"LEFT_SHOULDER\", \"RIGHT_SHOULDER\"])
        def calc_neck(self):
            return self._middle(
                self._landmarks[self._plm.LEFT_SHOULDER.value],
                self._landmarks[self._plm.RIGHT_SHOULDER.value]
            )
    """
    if not isinstance(name, str) or not name.isidentifier():
        raise ValueError("Landmark name must be a valid identifier string.")

    connection_names = []
    if connection:
        for c in connection:
            if isinstance(c, str):
                connection_names.append(c)
            elif hasattr(c, "name"):  # PoseLandmark enum or similar
                connection_names.append(c.name)
            else:
                raise ValueError(f"Invalid connection value: {c!r}")

    def wrapper(fn):
        fn._is_custom_landmark = True
        fn._landmark_name = name
        fn._landmark_connections = connection_names
        return fn

    return wrapper