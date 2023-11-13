`poetry run python -m jsonform_test_cclaw.main`


We will probably have a mix of Playwright-only and Hypothesis-driving-Playwright tests

# To figure out

* may want to implement this as a `pytest` *plugin* (https://docs.pytest.org/en/7.1.x/how-to/writing_plugins.html) instead of calling pytest -- not sure right now


# resources

https://github.com/pyodide/pytest-pyodide/blob/2a9b65d9afe5126861e7f6badeee7a464934210c/pytest_pyodide/fixture.py#L30 may be helpful for figuring out how to combine hypothesis with things like playwright and selenium