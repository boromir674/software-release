Software Release Toolkit
========================

Automate Releasing of Software, while following Semantic Versioning.

.. start-badges

| |build| |coverage| |maintainability| |bettercodehub| |tech-debt|
| |release_version| |wheel| |supported_versions| |gh-lic| |commits_since_specific_tag_on_master| |commits_since_latest_github_release|


|
| **Source Code:** https://github.com/boromir674/software-release
| **Pypi Package:** https://pypi.org/project/software_release/
|

Let's assume you are developing a software and you 'store' and 'track' your `source files` in a repository using `git` and `github`.
Let's also assume that the time has come to 'release' (publish) a new `version` of your software.

Finally, let's hope that you have been or are willing to operate a `command line interface` (cli)` :)
Just a `console` (aka terminal) :)

Then the **Software Release Toolkit** can be your ally in helping you automate the `release process`!

The `Toolkit` features the `software_release` python module, available also in `pypi` (ie install with `pip install software-release`),
which provides the `release-software` cli, upon installation.

The capabilities of `software_release` are all about automating various "tasks" that are part of the `release process`.
Most of the **automation** is currently supplied through an `Interactive Console Wizard`.


Features
========

1. **software_release** `python package`

   a. Command Line Interface (cli) to automate the Release Process
   b. **Release Wizard**: Interactive Console Wizard

    The `Wizard` guides the user step-by-step through the 'Release Process'


2. **Test Suite** using `Pytest`
3. **Parallel Execution** of Unit Tests, on multiple cpu's
4. **Automation**, using `tox`

   a. **Code Coverage** measuring
   b. **Build Command**, using the `build` python package
   c. **Pypi Deploy Command**, supporting upload to both `pypi.org` and `test.pypi.org` servers
   d. **Type Check Command**, using `mypy`
5. **CI Pipeline**, running on `Github Actions`

   a. **Job Matrix**, spanning different `platform`'s and `python version`'s

      1. Platforms: `ubuntu-latest`, `macos-latest`
      2. Python Interpreters: `3.8`
   b. **Parallel Job** execution, generated from the `matrix`, that runs the `Test Suite`


Prerequisites
=============

You need to have `Python` installed.

Quickstart
==========

Installing `software_release` inside a `virtual environment`_ using `pip`_ is the approved way.

Open a console and run:

.. code-block:: sh

    virtualenv env --python=python3.8
    source env/bin/activate

    pip install software_release


Then navigate (do a `cd`) into a folder where your 'ready-for-releasing' project (git repository) is.

.. code-block:: shell

    git checkout master
    git pull
    git checkout release
    git rebase master
    git push -f

    release-software

This will run the `Release Wizard` which will automatically step through the tasks
required for 'releasing' a new software version!

Note: It is required that your git HEAD is pointing to a branch named "release" and
that there is a "release" on the 'remote' as well.


License
=======

|gh-lic|

* `GNU Affero General Public License v3.0`_


License
=======

* Free software: GNU Affero General Public License v3.0


.. MACROS/ALIASES

.. start-badges

.. Test Workflow Status on Github Actions for specific branch <branch>

.. |build| image:: https://img.shields.io/github/workflow/status/boromir674/software-release/Test%20Python%20Package/master?label=build&logo=github-actions&logoColor=%233392FF
    :alt: GitHub Workflow Status (branch)
    :target: https://github.com/boromir674/software-release/actions/workflows/test.yaml?query=branch%3Amaster


.. above url to workflow runs, filtered by the specified branch

.. |coverage| image:: https://codecov.io/gh/boromir674/software-release/branch/master/graph/badge.svg?token=TNP2MG13F5
      :target: https://codecov.io/gh/boromir674/software-release
      :alt: Test Coverage

.. |release_version| image:: https://img.shields.io/pypi/v/software_release
    :alt: Production Version
    :target: https://pypi.org/project/software_release/

.. |wheel| image:: https://img.shields.io/pypi/wheel/software-release?color=green&label=wheel
    :alt: PyPI - Wheel
    :target: https://pypi.org/project/software_release

.. |supported_versions| image:: https://img.shields.io/pypi/pyversions/software-release?color=blue&label=python&logo=python&logoColor=%23ccccff
    :alt: Supported Python versions
    :target: https://pypi.org/project/software_release

.. |commits_since_specific_tag_on_master| image:: https://img.shields.io/github/commits-since/boromir674/software-release/v0.1.0/master?color=blue&logo=github
    :alt: GitHub commits since tagged version (branch)
    :target: https://github.com/boromir674/software-release/compare/v0.1.0..master

.. |commits_since_latest_github_release| image:: https://img.shields.io/github/commits-since/boromir674/software-release/latest?color=blue&logo=semver&sort=semver
    :alt: GitHub commits since latest release (by SemVer)

.. Github License (eg AGPL, MIT)
.. |gh-lic| image:: https://img.shields.io/github/license/boromir674/software-release
    :alt: GitHub
    :target: https://github.com/boromir674/software-release/blob/master/LICENSE

.. CODE QUALITY, MAINTAINABILITY, TECH DEBT

.. |maintainability| image:: https://api.codeclimate.com/v1/badges/3c088c81951f15d717f1/maintainability
   :target: https://codeclimate.com/github/boromir674/software-release/maintainability
   :alt: Maintainability

.. if tech debt < 5% then maintainability = A

.. |tech-debt| image:: https://img.shields.io/codeclimate/tech-debt/boromir674/software-release
    :target: https://codeclimate.com/github/boromir674/software-release/maintainability
    :alt: Code Climate technical debt

.. GOOD SOFTWARE PATTERNS

.. |bettercodehub| image:: https://bettercodehub.com/edge/badge/boromir674/software-release?branch=master
    :target: https://bettercodehub.com/
    :alt: Better Code Hub


.. LINKS

.. _GNU Affero General Public License v3.0: https://github.com/boromir674/software-release/blob/master/LICENSE

.. _virtual environment: https://virtualenv.pypa.io/en/stable/

.. _pip: https://pip.pypa.io/en/stable/
