import json
from pathlib import Path
from typing import Dict, Any

class FileCache:
    def __init__(self, cache_file: Path):
        self.cache_file = cache_file
        self.cache: Dict[str, Dict[str, Any]] = self._load_cache()

    def _load_cache(self) -> Dict[str, Dict[str, Any]]:
        if self.cache_file.exists():
            with self.cache_file.open('r') as f:
                return json.load(f)
        return {}

    def _save_cache(self):
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        with self.cache_file.open('w') as f:
            json.dump(self.cache, f, indent=2)

    def get(self, theme: str, key: str) -> Any:
        return self.cache.get(theme, {}).get(key)

    def set(self, theme: str, key: str, value: Any):
        if theme not in self.cache:
            self.cache[theme] = {}
        self.cache[theme][key] = value
        self._save_cache()
