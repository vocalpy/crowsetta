import nox


@nox.session
def tests(session):
    """
    Run the unit and regular tests.
    """
    session.install(".[test]")
    session.run("pytest", *session.posargs)


@nox.session
def coverage(session):
    """
    Run the unit and regular tests, and save coverage report
    """
    session.install(".[test]", "pytest-cov")
    session.run(
        "pytest", "--cov=./", "--cov-report=xml", *session.posargs
    )
