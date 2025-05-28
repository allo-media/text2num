API Documentation
=================


High-level API
--------------

The high level API exposes functions that works on plain unicode strings.

If you need to process other sources or have implemented your own tokenizer, you'd better
use the other API below.


.. autofunction:: text_to_num.text2num

.. autofunction:: text_to_num.alpha2digit


Custom Token Processing
-----------------------

.. autoclass:: text_to_num.Occurence
   :members:

.. autoclass:: text_to_num.Token
   :members:

.. autofunction:: text_to_num.find_numbers
