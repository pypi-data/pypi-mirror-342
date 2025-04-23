"""
Sync files from an upstream CPython release.
"""

import json
import pathlib
import re
import subprocess

import packaging.version
from requests_toolbelt import sessions

from jaraco.ui.main import main

gh_content = sessions.BaseUrlSession(
    'https://raw.githubusercontent.com/python/cpython/'
)
gh_api = sessions.BaseUrlSession('https://api.github.com/repos/python/cpython/')


def load_file_map():
    text = pathlib.Path('file map.json').read_text(encoding='utf-8')
    clean = re.sub('^#.*', '', text, re.MULTILINE)
    return json.loads(clean)


class Version(packaging.version.Version):
    @property
    def is_stable(self):
        """
        Include release candidates in stable.
        """
        return not self.is_prerelease or self.is_rc

    @property
    def is_rc(self):
        return self.pre[1:] == ['rc']


def by_tag(tag):
    return Version(tag['name'])


def is_stable(tag):
    return not by_tag(tag).is_stable


@main
def run(pre: bool = False):
    tags = gh_api.get('tags').json()
    filtered = tags if pre else filter(is_stable, tags)
    tag = max(filtered, key=by_tag)
    version = tag['name']
    for src, dst in load_file_map().items():
        resp = gh_content.get(f'{version}/{src}')
        resp.raise_for_status()
        with open(dst, 'wb') as out:
            out.write(resp.content)
    cmd = [
        'git',
        'commit',
        '-a',
        '-m',
        f'cpython-{version} rev={tag["commit"]["sha"][:12]}',
    ]
    subprocess.run(cmd)
