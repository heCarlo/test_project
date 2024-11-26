import os
import sys
import pytest

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

pytest.main(['--cov=app', '--maxfail=1', '--disable-warnings', '--tb=short'])