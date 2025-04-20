#!/usr/bin/env python3
"""Test the main module."""

import unittest

from mcpnacos_config.main import just_get_version


class TestMain(unittest.TestCase):
    """Test cases for the main module."""

    def test_version(self):
        """Test that just_get_version returns a version string."""
        self.assertIsInstance(just_get_version(), str)


if __name__ == "__main__":
    unittest.main() 