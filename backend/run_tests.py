#!/usr/bin/env python3
"""
Entry-point for running tests with correct PYTHONPATH and coverage.
테스트 실행 및 커버리지 측정을 위한 엔트리포인트 (日: テスト実行・カバレッジ測定用エントリーポイント)
"""
import os
import sys
import subprocess

# 1. Set PYTHONPATH to project root
root = os.path.dirname(os.path.abspath(__file__))
os.environ["PYTHONPATH"] = root

# 2. Build pytest command with coverage
cmd = [
    sys.executable, "-m", "pytest",
    "--cov=backend",
    "--cov-report=term-missing",
    "--cov-report=xml",
    "--cov-report=html"
] + sys.argv[1:]

# 3. Run tests
ret = subprocess.call(cmd)
sys.exit(ret)
