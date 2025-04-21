"""
Configuration file for pytest
"""

import pytest
import os
import sys

# Add the parent directory to the path so pytest can find the src package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 