==========
DBSequence
==========

Read :Oracle:`Oracle documentation <programmer_reference/index.html>`
for better understanding.

Sequences provide an arbitrary number of persistent objects that return
an increasing or decreasing sequence of integers. Opening a sequence
handle associates it with a record in a database. The handle can
maintain a cache of values from the database so that a database update
is not needed as the application allocates a value.

:OracleAPIC:`More info... <seq.html>`

DBSequence Methods
------------------

.. function:: DBSequence(db, flags=0)

   Constructor.
   :OracleAPIC:`More info... <seqcreate.html>`

.. function:: open(key, txn=None, flags=0)

   Opens the sequence represented by the key.
   :OracleAPIC:`More info... <seqopen.html>`

.. function:: close(flags=0)

   Close a DBSequence handle.
   :OracleAPIC:`More info... <seqclose.html>`

.. function:: initial_value(value)

   Set the initial value for a sequence. This call is only effective
   when the sequence is being created.
   :OracleAPIC:`More info... <seqinitial_value.html>`

.. function:: get(delta=1, txn=None, flags=0)

   Returns the next available element in the sequence and changes the
   sequence value by delta.
   :OracleAPIC:`More info... <seqget.html>`

.. function:: get_dbp()

   Returns the DB object associated to the DBSequence.
   :OracleAPIC:`More info... <seqget_dbp.html>`

.. function:: get_key()

   Returns the key for the sequence.
   :OracleAPIC:`More info... <seqget_key.html>`

.. function:: remove(txn=None, flags=0)

   Removes the sequence from the database. This method should not be
   called if there are other open handles on this sequence.
   :OracleAPIC:`More info... <seqremove.html>`

.. function:: get_cachesize()

   Returns the current cache size.
   :OracleAPIC:`More info... <seqget_cachesize.html>`

.. function:: set_cachesize(size)

   Configure the number of elements cached by a sequence handle.
   :OracleAPIC:`More info... <seqset_cachesize.html>`

.. function:: get_flags()

   Returns the current flags.
   :OracleAPIC:`More info... <seqget_flags.html>`

.. function:: set_flags(flags)

   Configure a sequence.
   :OracleAPIC:`More info... <seqset_flags.html>`

.. function:: stat(flags=0)

   Returns a dictionary of sequence statistics with the following keys:

     +------------+----------------------------------------------+
     | wait       | The number of times a thread of control was  |
     |            | forced to wait on the handle mutex.          |
     +------------+----------------------------------------------+         
     | nowait     | The number of times that a thread            |
     |            | of control was able to obtain handle mutex   |
     |            | without waiting.                             |
     +------------+----------------------------------------------+           
     | current    | The current value of the sequence            |
     |            | in the database.                             |
     +------------+----------------------------------------------+            
     | value      | The current cached value of the sequence.    |
     +------------+----------------------------------------------+
     | last_value | The last cached value of the sequence.       |
     +------------+----------------------------------------------+
     | min        | The minimum permitted value of the sequence. |
     +------------+----------------------------------------------+
     | max        | The maximum permitted value of the sequence. |
     +------------+----------------------------------------------+
     | cache_size | The number of values that will be cached in  |
     |            | this handle.                                 |
     +------------+----------------------------------------------+               
     | flags      | The flags value for the sequence.            |               
     +------------+----------------------------------------------+

   :OracleAPIC:`More info... <seqstat.html>`

.. function:: stat_print(flags=0)

   Prints diagnostic information.
   :OracleAPIC:`More info... <seqstat_print.html>`

.. function:: get_range()

   Returns a tuple representing the range of values in the sequence.
   :OracleAPIC:`More info... <seqget_range.html>`

.. function:: set_range((min,max))

   Configure a sequence range.
   :OracleAPIC:`More info... <seqset_range.html>`

