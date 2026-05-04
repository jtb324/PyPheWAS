import nox
import os

# Define the python versions to test
# Note: 3.14 and 3.15 are future versions and may not be available on all systems.
PYTHON_VERSIONS = ["3.11", "3.12", "3.13", "3.14"]


@nox.session(python=PYTHON_VERSIONS)
def tests(session):
    """Run integration tests using PDM (--prod) and Pytest."""
    # Install pdm in the session
    session.install("pdm")
    # Force PDM to use Nox's python interpreter
    session.env["PDM_IGNORE_SAVED_PYTHON"] = "1"

    # Install production dependencies and the package itself using pdm --prod
    # PDM_USE_VENV=1: ensure pdm installs into the current nox virtualenv
    session.run("pdm", "install", "--prod", external=True)

    # # Diagnostics
    # session.run("pdm", "list", env={"PDM_USE_VENV": "1"})
    # session.run("pip", "list")

    # Install pytest separately to run the tests
    session.run("pdm", "add", "pytest")

    # Run integration tests
    session.run("pdm", "run", "pytest", "tests/integration_tests.py", external=True)
