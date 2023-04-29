from pathlib import Path
from dataclasses import dataclass

@dataclass
class PathConstants: 
    constant_file_path: Path = Path(__file__)
    project_base_path: Path = constant_file_path.parents[2]
    database_path: Path = project_base_path.joinpath("data/database.sqlite")
    configs_path: Path = project_base_path.joinpath("configs")
