# -*- coding: utf-8 -*-
from __future__ import unicode_literals
try:
    # Python 3+
    from urllib.parse import urlencode
except ImportError:
    # Python 2+
    from urllib import urlencode

import os
import json
import requests
from django.conf import settings


class RepositoryNotFoundException(Exception):
    """
    If requested repository is not found at cdnjs.com
    """
    pass


class FileNotFoundException(Exception):
    """
    If requested file is not found at cdnjs.com repository
    """
    pass


class InvalidFileException(Exception):
    """
    Internal library exceptions type
    """
    pass


class CDNJsObject(object):
    """
    CDNJs object
    """
    def __init__(self, name, version, default=None, files=None, keywords=None):
        """
        Init object
        :param name:
        :param version:
        :param str default:
        :param dict files:
        :param list keywords:
        """
        self.name = name
        self.version = version
        self.default = default.split('/')[-1]
        self.files = files or {}
        self.keywords = keywords or []

    def __str__(self):
        """
        :return str:
        """
        return '<{}/{}>'.format(self.name, self.version)

    def __unicode__(self):
        """
        :return unicode:
        """
        return str(self)

    def __getitem__(self, item):
        """
        Returns file
        :param item:
        :return:
        """
        for name, obj in self.files.items():
            if item in name:
                return obj['cdn' if getattr(settings, 'FORCE_CDN') else 'uri']

        raise FileNotFoundException(
            'File {} was not found at {}'.format(item, self.name))

    def __setitem__(self, key, value):
        """
        Adds file
        :param key:
        :param value:
        :return:
        """
        if 'uri' not in value or 'cdn' not in value:
            raise InvalidFileException(
                'File {} that is trying to add is invalid'.format(key))

        self.files[key] = value

    def __contains__(self, item):
        """
        Contains file
        :param item:
        :return:
        """
        for f in self.files.keys():
            if item in f:
                return True

    @property
    def dict(self):
        return {
            'default': self.default,
            'files': self.files
        }

    @property
    def is_valid(self):
        """
        Is valid
        :return:
        """
        return len(self.files.keys()) > 0

    def matches(self, name, version=None):
        """
        Is matched to name with version
        :param name:
        :param version:
        :return:
        """
        if not any([name in x for x in self.keywords]) \
                and name not in self.name:
            return False

        if version is not None and self.version != version:
            return False

        return True

    def download(self):
        """
        Downloads cdn repository to local storage
        :return:
        """
        # Create storage path
        storage_path = os.path.join(
            settings.CDN_STATIC_ROOT,
            self.name,
            self.version)

        if not os.path.exists(storage_path):
            os.makedirs(storage_path)

        # Load files
        for name, path_data in self.files.items():
            subdir = CDNJs.get_dir(path_data['cdn'], self.version)
            dir_path = os.path.join(storage_path, subdir)
            file_path = os.path.join(dir_path, name)
            file_uri = '{root}{name}/{version}/{subdir}{file}'.format(
                root=settings.CDN_STATIC_URL,
                name=self.name,
                version=self.version,
                subdir=subdir + '/' if subdir else '',
                file=name
            )

            if not os.path.exists(file_path):
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)

                with open(file_path, 'w') as f:
                    for c in requests.get(path_data['cdn']):
                        f.write(c)
                    f.close()

            self[name] = {
                'cdn': path_data['cdn'],
                'uri': file_uri
            }


class CDNJs(object):
    """
    CDNJs.com parser
    """
    API_URL = 'https://api.cdnjs.com/libraries{query}'
    FILE_CDN = 'https://cdnjs.cloudflare.com/ajax/libs/{name}/{version}/{file}'

    @staticmethod
    def get_dir(cdn, version):
        """
        Returns subdirectory
        :param cdn:
        :return:
        """
        filename = cdn.split('/')[-1]
        return cdn.split(version)[-1].replace(filename, '').strip('/')

    def find(self, name, version=None):
        """
        Lads CDNJSObject
        :param name:
        :param version:
        :return CDNJsObject:
        """
        # Load base info
        realname = self._find_hit(name)

        # Check hits
        if realname is None:
            raise RepositoryNotFoundException(
                'Repository {} was not found'.format(name))

        # Load version files
        return self._load_version(realname, version)

    def _find_hit(self, name):
        """
        Tries to find hits for selected repository
        :param str name:
        :return dict:
        """
        query = {
            'search': name
        }

        response = json.loads(
            requests.get(
                self.API_URL.format(query='?' + urlencode(query))
            ).text
        )['results'][0]

        return response['name']

    def _load_version(self, name, version=None):
        """
        Loads files for selected version
        :param name:
        :param version:
        :return CDNJsObject:
        """
        # Result files
        files = []

        # Load info about version
        response = json.loads(
            requests.get(
                self.API_URL.format(query='/{}'.format(name))
            ).text
        )

        # Version to be saved
        version = version or response['version']

        # Create initial cdnjs object
        obj = CDNJsObject(
            name=response['name'],
            version=version,
            default=response['filename'],
            keywords=response['keywords'])

        # Get version assets
        for assets in response['assets']:
            if assets['version'] == version:
                obj.files = self._parse_assets(response['name'], assets)

        if not obj.is_valid:
            return None

        return obj

    def _parse_assets(self, repository, assets):
        """
        Returns files
        :param repository:
        :param assets:
        :return:
        """
        result = {}

        for filename in assets['files']:
            result[self._file_name(filename)] = {
                'cdn': self._file_cdn(repository, assets['version'], filename),
                'uri': None
            }

        return result

    def _file_cdn(self, repository, version, fname):
        """
        Returns file cdn
        :param version:
        :param fname:
        :return:
        """
        return self.FILE_CDN.format(
            name=repository,
            version=version,
            file=fname
        )

    def _file_name(self, fname):
        """
        Returns clean filename
        :param fname:
        :return:
        """
        return fname.split('/')[-1]


class CDNStorage(object):
    """
    CDN Storage
    """
    DB_PATH = os.path.join(settings.CDN_STATIC_ROOT, 'cache.json')

    def __init__(self):
        self.database = list(self._load_db())
        self.storage = CDNJs()

    def get(self, repository, filename):
        """
        Returns CDN or URI
        :param repository:
        :param filename:
        :return:
        """
        name, ver = self.parse_name(repository)

        # Find repo
        repo = None
        for r in self.database:
            if r.matches(name, ver):
                repo = r
                break

        # If not local copy exists load it
        if repo is None:
            repo = self.storage.find(name, ver)
        if repo is None:
            raise RepositoryNotFoundException(
                'Repository {} was not found'.find(repository))
        else:
            self.database.append(repo)

        # If we need local URI
        if not getattr(settings, 'FORCE_CDN'):
            repo.download()

        # Update database
        self._save_db()

        # Find file
        return repo[filename or repo.default]

    def _load_db(self):
        """
        Loads cdns from db
        :return CDNJsObject:
        """
        if not os.path.exists(self.DB_PATH):
            return

        with open(self.DB_PATH, 'r') as f:
            # Read db
            try:
                content = json.loads(f.read())
                # Parse objects
                for name, info in content.items():
                    for ver, data in info['releases'].items():
                        yield CDNJsObject(
                            name=name,
                            version=ver,
                            default=data['default'],
                            files=data['files'],
                            keywords=info['keywords']
                        )
            finally:
                f.close()

    def _save_db(self):
        """
        Saving cdns to db
        :return:
        """
        with open(self.DB_PATH, 'w') as f:
            data = {}

            for cdn in self.database:
                if cdn.name not in data:
                    data[cdn.name] = {
                        'releases': {},
                        'keywords': cdn.keywords
                    }

                if cdn.version not in data[cdn.name]['releases']:
                    data[cdn.name]['releases'][cdn.version] = cdn.dict

            f.write(json.dumps(data, indent=2))

    @staticmethod
    def parse_name(repository_name):
        """
        Parses repository name and version
        :param repository_name:
        :return tuple(str, str):
        """
        pair = repository_name.split('/')
        return pair[0], pair[1] if len(pair) > 1 else None
