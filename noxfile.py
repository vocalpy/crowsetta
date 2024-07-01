import os
import pathlib
import shutil
import sys

import nox

DIR = pathlib.Path(__file__).parent.resolve()
VENV_DIR = pathlib.Path('./.venv').resolve()


nox.options.sessions = ['test', 'coverage']


@nox.session
def build(session: nox.Session) -> None:
    """
    Build an SDist and wheel with ``flit``.
    """

    dist_dir = DIR.joinpath("dist")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)

    session.install(".[dev]")
    session.run("flit", "build")


@nox.session(python="3.10")
def dev(session: nox.Session) -> None:
    """
    Sets up a python development environment for the project.

    This session will:
    - Create a python virtualenv for the session
    - Install the `virtualenv` cli tool into this environment
    - Use `virtualenv` to create a global project virtual environment
    - Invoke the python interpreter from the global project environment to install
      the project and all it's development dependencies.
    """

    session.install("virtualenv")
    # VENV_DIR here is a pathlib.Path location of the project virtualenv
    # e.g. .venv
    session.run("virtualenv", os.fsdecode(VENV_DIR), silent=True)

    if sys.platform.startswith("linux") or sys.platform == "darwin":
        python = os.fsdecode(VENV_DIR.joinpath("bin/python"))
    elif sys.platform.startswith("win"):
        python = os.fsdecode(VENV_DIR.joinpath("Scripts/python.exe"))

    # Use the venv's interpreter to install the project along with
    # all it's dev dependencies, this ensures it's installed in the right way
    session.run(python, "-m", "pip", "install", "-e", ".[dev,test,doc]", external=True)


@nox.session(python="3.10")
def lint(session):
    """
    Run the linter.
    """
    session.install(".[dev]")
    # run isort first since black disagrees with it
    session.run("isort", "./src")
    session.run("black", "./src", "--line-length=120")
    session.run("flake8", "./src", "--max-line-length", "120", "--exclude", "./src/crowsetta/_vendor")


TEST_PYTHONS = [
    "3.10",
    "3.11",
    "3.12",
]


@nox.session(python=TEST_PYTHONS)
def test(session) -> None:
    """
    Run the unit and regular tests.
    """
    session.install(".[test]")
    session.run("pytest", "-n", "auto", *session.posargs)


@nox.session
def coverage(session) -> None:
    """
    Run the unit and regular tests, and save coverage report
    """
    session.install(".[test]", "pytest-cov")
    session.run(
        "pytest", "-n", "auto", "--cov=./", "--cov-report=xml", *session.posargs
    )


@nox.session
def doc(session: nox.Session) -> None:
    """
    Build the docs. 

    To run ``sphinx-autobuild``,  do:

    .. code-block::console

       nox -s doc -- autobuild
    
    Otherwise the docs will be built once using
    """
    session.install(".[doc]")
    if session.posargs:
        if "autobuild" in session.posargs:
            print("Building docs at http://127.0.0.1:8000 with sphinx-autobuild -- use Ctrl-C to quit")
            session.run("sphinx-autobuild", "doc", "doc/_build/html")
        else:
            print("Unsupported argument to docs")
    else:
        session.run("sphinx-build", "-nW", "--keep-going", "-b", "html", "doc/", "doc/_build/html")
