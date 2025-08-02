import os
import sys

# Add the parent directory to the Python path so tests can import the application modules
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
