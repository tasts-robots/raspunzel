#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Stéphane Caron
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

from .find import find_file


def get_workspace_name(workspace_file: str) -> str:
    """
    Read workspace name from WORKSPACE file.

    Args:
        workspace_file: Path to WORKSPACE file.

    Returns:
        Workspace name, if found.

    Raises:
        ValueError: if workspace name could not be found.
    """
    for line in open(workspace_file, encoding="utf-8").readlines():
        if line.startswith('workspace(name = "'):
            return line.split('"')[1]

    raise ValueError(
        "Could not find name in WORKSPACE. "
        "Note that we don't parse Starlark beyond "
        '``workspace(name = "something")``.'
    )


class Workspace:

    """
    Bazel workspace information.
    """

    def __init__(self):
        workspace_file = find_file("WORKSPACE", required=True)
        self.bazel_bin = find_file("bazel-bin", required=True)
        self.workspace_name = get_workspace_name(workspace_file)
        self.workspace_file = workspace_file
