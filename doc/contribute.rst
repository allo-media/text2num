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
If you are going to submit some patches, you should fork the project on GitHub and clone
your own fork in your workspace.

Finally, install the sources in-place::

    python setup.py develop

You do that once. Then, any change you make to the code is immediately visible when you import the modules.

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

If you wish to contribute code or documentation to the project, you should first open an issue
on https://github.com/allo-media/text2num/issues to describe what you intend to do, and
why:

* if it's a bug fix, link to the related issues or describe precisely, with examples, what the faulty behavior is;
* if it's a new feature, describe the use case, with examples, and why it matters;
* if it's new or updated documentation, describe precisely which parts you are going to edit, to avoid edition conflicts;
* if it's support for a new language, announce it clearly in order to avoid duplicate effort and to get help from other people interested in that language.

Once you get positive feedback on your issue, you can fork the project on GitHub and start working on the code.

All PR should be made from a dedicated branch, not from *master*, please.
Please check your files are in proper Unicode encoded as UTF-8, and that the line endings follow the Unix convention (LF).
