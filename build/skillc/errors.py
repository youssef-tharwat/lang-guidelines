# Copyright (c) 2026 Youssef Khalil
# SPDX-License-Identifier: MIT
"""The error every build failure derives from, so the CLI reports them uniformly."""


class BuildError(Exception):
    """A skill cannot be built from its inputs."""
