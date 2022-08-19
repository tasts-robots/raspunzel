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

"""
Sync Bazel workspace to the Raspberry Pi.
"""

import subprocess

from .bazel import Workspace


def run(*args, **kwargs):
    print("run: " + args[0])
    subprocess.check_call(*args, shell=True, **kwargs)


def sync(workspace: Workspace, destination: str) -> None:
    """
    Synchronize Bazel workspace with remote host.

    Args:
        workspace: Bazel workspace information.
        destination: Destination in rsync+ssh format ``[user@]host:path``.
    """
    if ":" not in destination:
        raise ValueError(
            f"Destination '{destination}' is not in host:path format"
        )
    bazel_bin = workspace.bazel_bin.rstrip("/")
    destination = destination.rstrip("/")
    run(f"rsync -Lrtu --delete {bazel_bin}/ {destination}/")
    run(f"scp {workspace.root}/WORKSPACE {destination}/WORKSPACE")
