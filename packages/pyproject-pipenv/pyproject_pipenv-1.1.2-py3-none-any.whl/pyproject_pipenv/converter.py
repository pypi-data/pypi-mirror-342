# tomlkit over toml because it preserves format/comments
from pathlib import Path

import tomlkit

from .models import Diff, DiffDeps, DiffVersion


class Converter:
    def __init__(self, pipfile_path: Path, pyproject_path: Path):
        self.pipfile_path = pipfile_path
        self.pyproject_path = pyproject_path
        self.pipfile_content = None
        self.pyproject_content = None
        self.load()

    def load(self):
        with open(self.pipfile_path, 'r') as f:
            self.pipfile_content = tomlkit.parse(f.read())
        with open(self.pyproject_path, 'r') as f:
            self.pyproject_content = tomlkit.parse(f.read())

    def pipfile_version(self):
        return self.pipfile_content.get('requires', {}).get('python_version')

    def pipfile_list_dependencies(self):
        packages = []
        for name, version_dict in self.pipfile_content.get('packages', {}).items():
            if isinstance(version_dict, dict):
                version = version_dict['version']
            else:
                version = version_dict
            if version == '*':
                version = ''
            elif version[0].isdigit():
                # manually edited Pipfile can have version without operator and it is valid
                version = f'=={version}'
            packages.append(f'{name}{version}')
        return packages

    def pyproject_version(self):
        return self.pyproject_content['project'].get('requires-python')

    def pyproject_list_dependencies(self):
        return self.pyproject_content['project']['dependencies']

    def diff(self) -> Diff:
        return Diff(
            deps=self.diff_dependencies(),
            # TODO: drop version as it DOES NOT MAKE SENSE - Pipfile requires exact version, not a range, and it's optional
            # version=self.diff_version(),
        )

    def diff_dependencies(self):
        pp = set(self.pyproject_list_dependencies())
        pf = set(self.pipfile_list_dependencies())
        extra = pp - pf
        missing = pf - pp
        if not extra and not missing:
            return None
        return DiffDeps(extra=extra, missing=missing)

    def diff_version(self):
        pp = self.pyproject_version()
        pf = self.pipfile_version()
        if pp == pf:
            return None
        return DiffVersion(pipfile=pf, pyproject=pp)

    def sync(self):
        self.pyproject_content['project']['dependencies'] = self.pipfile_list_dependencies()
        if self.pipfile_version():
            self.pyproject_content['project']['requires-python'] = self.pipfile_version()
        else:
            try:
                del self.pyproject_content['project']['requires-python']
            except KeyError:
                """all good if not there"""
        with open(self.pyproject_path, 'w') as f:
            f.write(tomlkit.dumps(self.pyproject_content))
