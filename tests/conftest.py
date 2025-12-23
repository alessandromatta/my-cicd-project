import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

#the reason for this is that running python -m pytest tests/ -v resulted in some errors
