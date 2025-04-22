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
from virtual_landmark import landmark


def test_landmark_decorator_assigns_attributes():
    @landmark("TEST_POINT", connection=["A", "B"])
    def dummy_method():
        return (0.0, 0.0, 0.0)

    assert dummy_method._is_custom_landmark is True
    assert dummy_method._landmark_name == "TEST_POINT"
    assert dummy_method._landmark_connections == ["A", "B"]


def test_landmark_decorator_accepts_enum_like_objects():
    class FakeEnum:
        def __init__(self, name):
            self.name = name

    left = FakeEnum("LEFT_EAR")
    right = FakeEnum("RIGHT_EAR")

    @landmark("HEAD_CENTER", connection=[left, right])
    def calc():
        return (0.5, 0.5, 0.5)

    assert calc._landmark_connections == ["LEFT_EAR", "RIGHT_EAR"]


def test_landmark_decorator_rejects_invalid_name_type():
    with pytest.raises(ValueError, match="valid identifier string"):
        landmark(123)


def test_landmark_decorator_rejects_invalid_name_string():
    with pytest.raises(ValueError, match="valid identifier string"):
        landmark("123ABC")

        
def test_decorator_skips_connection_block_when_none():
    @landmark("SKIP_CONNECTION")
    def f():
        return (0.0, 0.0, 0.0)

    assert f._landmark_connections == []


def test_decorator_accepts_all_strings_in_connection():
    @landmark("STRINGS_ONLY", connection=["A", "B", "C"])
    def f():
        return (0.0, 0.0, 0.0)

    assert f._landmark_connections == ["A", "B", "C"]


def test_decorator_accepts_enum_like_objects_in_connection():
    class FakeEnum:
        def __init__(self, name):
            self.name = name

    @landmark("ENUM_LIKE", connection=[FakeEnum("LEFT"), FakeEnum("RIGHT")])
    def f():
        return (0.0, 0.0, 0.0)

    assert f._landmark_connections == ["LEFT", "RIGHT"]


def test_decorator_accepts_mixed_string_and_enum_like():
    class FakeEnum:
        def __init__(self, name):
            self.name = name

    @landmark("MIXED", connection=["CENTER", FakeEnum("EDGE")])
    def f():
        return (0.0, 0.0, 0.0)

    assert f._landmark_connections == ["CENTER", "EDGE"]


def test_decorator_raises_on_invalid_connection_type():
    with pytest.raises(ValueError, match="Invalid connection value"):
        @landmark("BAD_CONNECTION", connection=[123])
        def f():
            return (0.0, 0.0, 0.0)