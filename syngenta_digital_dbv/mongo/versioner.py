import json

from pymongo import MongoClient

from syngenta_digital_dbv.common.config import Config
from syngenta_digital_dbv.common.directory_scanner import DirectoryScanner


class MongoVersioner:

    def __init__(self, **kwargs):
        self.config = Config(**kwargs)
        self.version_scanner = DirectoryScanner(directory=kwargs['versions_directory'], extension='.json')
        self.seed_scanner = DirectoryScanner(directory=kwargs.get('seed_directory'), extension='.json')
        self.app_client = None
        self.versioner_collection = None

    def version(self):
        config = self.config.get_config()
        self.__connect(**config)
        files = self.version_scanner.get_files()
        mongo_applied = self.__get_applied_versions()
        applied = [doc['_id'] for doc in mongo_applied]
        new_versions = self.version_scanner.sort_files(list(set(files) - set(applied)))
        self.__apply_versions(new_versions)
        self.__seed_data()

    def __connect(self, **config):
        self.app_client = MongoClient(config['endpoint'], username=config['user'], password=config['password'])
        db = self.app_client['__versions']
        self.versioner_collection = db['files_completed']

    def __get_applied_versions(self):
        results = self.versioner_collection.find()
        return list(results)

    def __apply_versions(self, new_versions):
        for version in new_versions:
            print(f'APPLYING {version}')
            try:
                with open(version, 'r', encoding='utf-8') as file:
                    changes = json.load(file)
                    for change in changes:
                        db = self.app_client[change['database']]
                        collection = db[change['collection']]
                        query = getattr(collection, change['operation'])
                        query(change['query'], **change.get('params', {}))
                        print(f'RAN QUERY: {change}')
                    file.close()
                self.__remember_version(version)
            except Exception as error:
                print(f'ERROR WITH {version}', error)
        print(f'APPLIED {len(new_versions)} NEW VERSION(S)')

    def __remember_version(self, version):
        self.versioner_collection.insert_one({'_id': version})

    def __seed_data(self):
        if self.config.seed:
            print('SEEDING DATA')
            files = self.seed_scanner.get_files()
            for version in files:
                print(f'SEEDING: {version}')
                with open(version, 'r', encoding='utf-8') as file:
                    seed_data = json.load(file)
                    for seed in seed_data:
                        db = self.app_client[seed['database']]
                        collection = db[seed['collection']]
                        collection.insert_many(seed['docs'])
                    file.close()
