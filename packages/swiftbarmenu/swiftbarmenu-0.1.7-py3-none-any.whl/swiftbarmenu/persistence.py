from __future__ import annotations

import os
import pickle
from pathlib import Path
from typing import Any


class Persistence:
    def __init__(self, file_name: str = "data"):
        """Initialize Persistence with a file name.

        Args:
            file_name: Name of the data file to save/load
        """

        self.file_path = Path(
            os.getenv('SWIFTBAR_PLUGIN_DATA_PATH', '.'),
            f'{file_name}.pkl'
        )

    def save(self, data: dict[str, Any]) -> None:
        """Save data to a file using pickle.

        Args:
            data: Dictionary containing the data to save
        """
        with self.file_path.open('wb') as file:
            pickle.dump(data, file)

    def load(self) -> dict[str, Any]:
        """Load data from a file using pickle.

        Returns:
            Dictionary containing the loaded data
        """
        if not self.file_path.exists():
            return {}

        with self.file_path.open('rb') as file:
            return pickle.load(file)

    def clear(self) -> None:
        """Remove the data file if it exists."""
        if self.file_path.exists():
            self.file_path.unlink()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return (
            f"Persistence("
            f"file_name='{self.file_path.stem}', "
            f"path='{self.file_path}'"
            f")"
        )
