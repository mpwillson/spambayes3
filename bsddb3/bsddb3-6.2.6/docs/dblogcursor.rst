===========
DBLogCursor
===========

Read :Oracle:`Oracle documentation <programmer_reference/index.html>`
for better understanding.

:OracleAPIC:`More info... <logc.html>`

DBLogCursor Methods
-------------------

.. function:: close()

   Discards the log cursor.
   :OracleAPIC:`More info... <logcclose.html>`

DBLogCursor Get Methods
-----------------------

These DBLogCursor methods are all wrappers around the get() function in
the C API.

These functions returns a tuple. The first element is a LSN tuple,
and the second element is a string/bytes with the log data.

If the following methods don't have log data to return, they return
None.

.. function:: current()

   Return the log record to which the log currently refers.
   :OracleAPIC:`More info... <logcget.html#get_DB_CURRENT>`

.. function:: first()

   The first record from any of the log files found in the log
   directory is returned.

   This method will return None if the log is empty. 

   :OracleAPIC:`More info... <logcget.html#get_DB_FIRST>`

.. function:: last()

   The last record in the log is returned.

   This method will return None if the log is empty. 

   :OracleAPIC:`More info... <logcget.html#get_DB_LAST>`

.. function:: next()

   The current log position is advanced to the next record in the log,
   and that record is returned. If the cursor position was not set
   previously, it will return the first record in the log.

   This method will return None if the log is empty. 

   :OracleAPIC:`More info... <logcget.html#get_DB_NEXT>`

.. function:: prev()

   The current log position is advanced to the previous record in the
   log, and that record is returned. If the cursor position was not set
   previously, it will return the last record in the log.
   
   This method will return None if the log is empty. 

   :OracleAPIC:`More info... <logcget.html#get_DB_PREV>`

.. function:: set(lsn)

   Retrieve the record specified by the lsn parameter.

   :OracleAPIC:`More info... <logcget.html#get_DB_SET>`

