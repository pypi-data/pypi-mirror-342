import sys
from pathlib import Path

# Автоматически добавляет корень проекта в PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))