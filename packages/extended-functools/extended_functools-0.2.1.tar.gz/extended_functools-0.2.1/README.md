# extended-functools

Additional tools for functional programming in Python.

This project intends to offer a variety of general-purpose tools, starting with
a timeout decorator, while keeping transient third-party dependencies to a
minimum.

| Type         | Badges |
|--------------|---|
| PyPI         | ![Python versions](https://img.shields.io/pypi/pyversions/extended-functools?logo=python) ![PyPI - Implementation](https://img.shields.io/pypi/implementation/extended-functools) ![Wheel](https://img.shields.io/pypi/wheel/extended-functools?logo=pypi) ![Downloads](https://img.shields.io/pypi/dm/extended-functools?logo=pypi) [![Version](https://img.shields.io/pypi/v/extended-functools)](https://pypi.org/project/extended-functools/) |
| Tests        | [![codecov](https://codecov.io/gh/Diapolo10/extended-functools/branch/main/graph/badge.svg?token=N3JOBzERqP)](https://codecov.io/gh/Diapolo10/extended-functools)  ![Unit tests](https://github.com/diapolo10/extended-functools/actions/workflows/unit_tests.yml/badge.svg) ![Ruff](https://github.com/diapolo10/extended-functools/workflows/Ruff/badge.svg) ![Deploy to PyPI](https://github.com/diapolo10/extended-functools/actions/workflows/pypi_deploy.yml/badge.svg) |
| Activity     | ![GitHub contributors](https://img.shields.io/github/contributors/diapolo10/extended-functools) ![Last commit](https://img.shields.io/github/last-commit/diapolo10/extended-functools?logo=github) ![GitHub all releases](https://img.shields.io/github/downloads/diapolo10/extended-functools/total?logo=github) ![GitHub issues](https://img.shields.io/github/issues/diapolo10/extended-functools) ![GitHub closed issues](https://img.shields.io/github/issues-closed/diapolo10/extended-functools) ![GitHub pull requests](https://img.shields.io/github/issues-pr/diapolo10/extended-functools) ![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/diapolo10/extended-functools) |
| QA           | [![CodeFactor](https://www.codefactor.io/repository/github/diapolo10/extended-functools/badge?logo=codefactor)](https://www.codefactor.io/repository/github/diapolo10/extended-functools) [![Rating](https://img.shields.io/librariesio/sourcerank/pypi/extended-functools)](https://libraries.io/github/Diapolo10/extended-functools/sourcerank) |
| Other        | [![License](https://img.shields.io/github/license/diapolo10/extended-functools)](https://opensource.org/licenses/MIT) [![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FDiapolo10%2Fextended-functools.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FDiapolo10%2Fextended-functools?ref=badge_shield) [![Known Vulnerabilities](https://snyk.io/test/github/diapolo10/extended-functools/badge.svg)](https://snyk.io/test/github/diapolo10/extended-functools) ![Repository size](https://img.shields.io/github/repo-size/diapolo10/extended-functools?logo=github) ![Code size](https://img.shields.io/github/languages/code-size/diapolo10/extended-functools?logo=github) ![Files](https://tokei.rs/b1/github/diapolo10/extended-functools?category=files) ![Lines of code](https://tokei.rs/b1/github/diapolo10/extended-functools) ![Blanks](https://tokei.rs/b1/github/diapolo10/extended-functools?category=blanks) ![Comments](https://tokei.rs/b1/github/diapolo10/extended-functools?category=comments) ![Code](https://tokei.rs/b1/github/diapolo10/extended-functools?category=code) |

## Installing

You can install the project from PyPI:

```pwsh
# For general use
pip install extended-functools

# For uv (and other package managers)
uv add extended-functools
```

## Development

You can use whatever package manager you prefer, but the core team behind the
project uses `uv`, and the CI scripts and Tox assume as much. This guide will
assume you'll use `uv`. If you need more information on `uv`, consider reading
through [this guide][UV tutorial].

It may also be a good idea to use VS Code as an IDE; the project includes a
list of recommended extensions to install, which the IDE should tell you about
on opening the project. Feel free to use something else if you want, though.

### Setting up the development environment

You can install the project and its development dependencies by running
`uv install` in the project directory after cloning it.
After that, you should run

```pwsh
uv run pre-commit install
```

to install the pre-commit hooks, which are used to ensure commits are correctly
formatted and meet the project's baseline quality standards. If the hooks need
to be updated, you may run

```pwsh
uv run pre-commit autoupdate
```

to update them to the latest versions.

### Contributing

This project follows semantic versioning, and uses a relaxed variant of the Git
Flow workflow style, with feature branches playing a key role.

- Direct commits to `main` are forbidden
- The history of `main` is to remain linear through the use of fast-forward
  merges and rebasing
- Commits must be signed
- Messy PR histories are encouraged to be cleaned up before merging the PR.

More detailed information can be found in [`CONTRIBUTING.md`][CONTRIBUTING].

Issues reports, feature requests, and PRs are all welcome.

[UV tutorial]: https://docs.astral.sh/uv/getting-started/
[CONTRIBUTING]: ./CONTRIBUTING.md
