Contribute to `text2num`
========================

Submit bug reports, questions or feature requests
-------------------------------------------------

Bug reports, questions and feature requests should be submitted on https://github.com/allo-media/text2num/issues.

When you submit a bug report:

- Precisely describe what was the expected behavior and what you actually got;
- indicate your python version;
- set the **Bug** label on your issue.


When you submit a feature request:

- Precisely describe what you'd like, with many illustrative examples;
- expose the rationale behind your request;
- set the **Enhancement** label on your issue.

When you submit a question:

- set the **Question** label on your issue.

Install from sources
--------------------

First, create and activate a virtual environment with the tool of you preference.

Then clone https://github.com/allo-media/text2num in your workspace.
If you are going to submit some patches, you should fork the project on Github and clone
your own fork in your workspace.

Finally, install the sources in-place::

    python setup.py develop

You do that once. Then, any change you make to the code is immediatly visible when you import the modules.

Run the tests
-------------

To run the tests, simply do::

    python setup.py test

The tests are automatically discovered and run from the ``text_to_num/tests`` directory.

We also use mypy::

    pip install mypy
    mypy text_to_num

Submit changes
--------------

If you wish to submit changes, fork the projec on github, and clone your own fork locally.

All PR should be made from a dedicated branch, not from *master*, please.
