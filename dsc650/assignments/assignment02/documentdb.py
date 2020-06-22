from tinydb import TinyDB
from pathlib import Path
import json
import os
from dsc650.assignments.assignment02.util import RESULTS_DIR


KV_DATA_DIR = RESULTS_DIR.joinpath('kvdb')


def _load_json(json_path):
    with open(json_path) as f:
        return json.load(f)


class DocumentDB(object):
    def __init__(self, db_path):
        people_json = KV_DATA_DIR.joinpath('people.json')
        visited_json = KV_DATA_DIR.joinpath('visited.json')
        sites_json = KV_DATA_DIR.joinpath('sites.json')
        measurements_json = KV_DATA_DIR.joinpath('measurements.json')

        self._db_path = Path(db_path)
        self._db = None
        self._person_lookup = _load_json(people_json)
        self._visit_lookup = _load_json(visited_json)
        self._site_lookup = _load_json(sites_json)
        self._measurements_lookup = _load_json(measurements_json)
        self._load_db()

    def _get_site(self, site_id):
        return self._site_lookup[str(site_id)]

    def _get_measurements(self, person_id):
        measurements = []

        for values in self._measurements_lookup.values():
            measurements.extend([value for value in values if str(value['person_id']) == str(person_id)])

        return measurements

    def _get_visit(self, visit_id):
        visit = self._visit_lookup.get(str(visit_id))
        site_id = str(visit['site_id'])
        site = self._site_lookup[site_id]
        visit['site'] = site

        return visit

    def _load_db(self):
        self._db = TinyDB(self._db_path)
        persons = self._person_lookup.items()
        for person_id, record in persons:
            measurements = self._get_measurements(person_id)
            visit_ids = set([measurement['visit_id'] for measurement in measurements])
            visits = []
            for visit_id in visit_ids:
                visit = self._get_visit(visit_id)
                visit['measurements'] = [
                    measurement for measurement in measurements
                    if visit_id == measurement['visit_id']
                ]
                visits.append(visit)

            record['visits'] = visits
            self._db.insert(record)


def main():
    db_path = RESULTS_DIR.joinpath('patient-info.json')
    if db_path.exists():
        os.remove(db_path)

    DocumentDB(db_path)
    with open(db_path) as f:
        data = json.load(f)

    with open(db_path, 'w') as f:
        json.dump(data, f, indent=2)


if __name__ == '__main__':
    main()
