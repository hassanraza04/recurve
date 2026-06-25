"""Pytest bootstrap.

The orchestration package lives under pipeline/orchestration so it can be loaded
as a top-level `recurve_orchestration` module (matching how `dagster dev` runs
it). Put that directory on sys.path for the tests.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "pipeline" / "orchestration"))
