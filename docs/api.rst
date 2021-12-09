API Documentation
=================


High-level API
--------------

The high level API exposes functions that works on plain unicode strings.

If you need to process other source or have implemented your own tokenizer, you'd better
use the lower level parser classes below.


.. autofunction:: text_to_num.text2num

.. autofunction:: text_to_num.alpha2digit


Parsers
-------

The high-level API is build upon these parsers implemented as classes.

Those classes passively consume word tokens and thus can be easly integrated into your own
tokenizer/framework.

.. automodule:: text_to_num.parsers
   :members:
   :undoc-members:


Misc.
-----

.. autofunction:: text_to_num.transforms.look_ahead