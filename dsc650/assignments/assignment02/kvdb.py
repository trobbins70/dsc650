from dsc650.assignments.assignment02.util import RESULTS_DIR
from pathlib import Path

kvdb_dir = RESULTS_DIR.joinpath('kvdb')
# Create the db_dir if it doesn't exist
kvdb_dir.mkdir(parents=True, exist_ok=True)
person_json = kvdb_dir.joinpath('people.json')
visit_json = kvdb_dir.joinpath('visited.json')
site_json = kvdb_dir.joinpath('sites.json')
measurements_json = kvdb_dir.joinpath('measurements.json')

from pathlib import Path
import json
class KVDB(object):
    def __init__(self, db_path):
        self._db_path = Path(db_path)
        self._db = {}
        self._load_db()
    def _load_db(self):
        if self._db_path.exists():
            with open(self._db_path) as f:
                self._db = json.load(f)
    def get_value(self, key):
        return self._db.get(key)
    def set_value(self, key, value):
        self._db[key] = value
    def save(self):
        with open(self._db_path) as f:
            json.dump(self._db, f, indent=2)