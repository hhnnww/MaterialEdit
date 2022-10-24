from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class MyImg:
    img_path: Path
    ratio: float


@dataclass
class ComList:
    img_list: List[MyImg]
    ratio: float
    diff_ratio: float
