# About

This was meant to be a property-based testing solution for CCLAW's json form web app. It also aimed to do some simple internal consistency checks on the examples.

The original plan had been to come up with a generator and property-based tests in `Hypothesis`, and then wire up the hypothesis infra to Playwright, and have Playwright automatedly step through the form. The better approach would have been to do the bulk of the testing at the level of data instead of automatedly stepping through the web form, but the architecture of the web app back then didn't really allow for that.

# Current status 

I have finished the Hypothesis data generator, but have not wired it up to Playwright. And while I've stubbed out some of internal consistency checks, I haven't implemented most of them.

 The generator is quite nice, though more work would be needed to wire this up to other things (e.g., with our current setup, wiring it to Playwright to automate clicking through the form based on the generated inputs). The next step would be to do that wiring to Playwright and extracting data from the resulting outcomes tab so that properties can be tested regarding the inputs and outputs.

* The data generator samples a base user profile, and includes edge-case-dates that are based on the dates in the base user profile when generating dates in the json schema

* The json schema is also massaged before we generate data from it so that
    * we don't bother generating form data we don't need for the claim type path we've chosen / sampled

    * we don't generate vacuously empty dicts of the sort we do not want (this is implemented via the requiredProperties field in json schema)

* At the same time, it also doesn't always generate data for certain form fields that aren't required —- in this way, we ensure that, if `max_examples` is set to a high enough number, the cases where the user leaves out certain fields will also be generated and tested

# How to run

Right now there isn't much point in doing this, because it hasn't yet been wired up to things like Playwright 

`poetry run python -m jsonform_test_cclaw.main`

# Roadmap

We will probably have a mix of Playwright-only and Hypothesis-driving-Playwright tests

# To figure out

* may want to implement this as a `pytest` *plugin* (https://docs.pytest.org/en/7.1.x/how-to/writing_plugins.html) instead of calling pytest -- not sure right now


# resources

https://github.com/pyodide/pytest-pyodide/blob/2a9b65d9afe5126861e7f6badeee7a464934210c/pytest_pyodide/fixture.py#L30 may be helpful for figuring out how to combine hypothesis with things like playwright and selenium
