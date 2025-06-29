#!/usr/bin/env python3
"""
Entry-point for running tests with proper PYTHONPATH:...
"""
import os
import sys
import subprocess

# 1 Set PYTHONPATH to the backend folder
root = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(root, "backend")
os.environ["PYTHONPATH"] = backend_dir

# 2" Delegate to pytest
args = [sys.executable, "-m", "pytest"] + sys.argv[1:]
sys.exit(subprocess.call(args))
