"""Helpers to read settings from setup.cfg or pyproject.toml
"""
import configparser
import logging
import os
import toml
import json

logger = logging.getLogger(__name__)


def config(repository_root_path):

    parser = configparser.ConfigParser()
    parser.read(
        [
            os.path.join(repository_root_path, 'setup.cfg'),
        ]
    )
    conf_dict = {key: value for key, value in parser.items()}
    if 'software_release' not in conf_dict:
        conf_dict['software_release'] = {}
    toml_conf_path = os.path.join(repository_root_path, "pyproject.toml")
    if os.path.isfile(toml_conf_path):
        # Overwrite with any settings from pyproject.toml
        with open(toml_conf_path, 'r') as pyproject_toml:
            try:
                pyproject_toml = toml.load(pyproject_toml)
                software_release_settings = (
                    pyproject_toml.get("tool", {}).get('software-release', {}).items()
                )
                for key, value in software_release_settings:
                    conf_dict['software_release'][key] = str(value)
            except toml.TomlDecodeError as error:
                logger.debug("Could not decode pyproject.toml: " + json.dumps({
                    'error': error,
                    'pyproject.toml': toml_conf_path,
                }))
    # parser['semantic_release']['setup_py'] = os.path.join(current_dir, 'setup.py')
    # parser['semantic_release']['changelog_rst'] = os.path.join(current_dir, 'CHANGELOG.rst')
    # parser['semantic_release']['readme_rst'] = os.path.join(current_dir, 'README.rst')
    # parser['semantic_release']['readme_md'] = os.path.join(current_dir, 'README.md')
    return conf_dict
