========
DBCursor
========

Read :Oracle:`Oracle documentation <programmer_reference/index.html>`
for better understanding.

:OracleAPIC:`More info... <dbc.html>`

DBCursor Methods
----------------

.. function:: close()

   Discards the cursor. If the cursor is created within a transaction
   then you *must* be sure to close the cursor before commiting the
   transaction.
   :OracleAPIC:`More info... <dbcclose.html>`

.. function:: count(flags=0)

   Returns a count of the number of duplicate data items for the key
   referenced by the cursor.
   :OracleAPIC:`More info... <dbccount.html>`

.. function:: delete(flags=0)

   Deletes the key/data pair currently referenced by the cursor.
   :OracleAPIC:`More info... <dbcdel.html>`

.. function:: dup(flags=0)

   Create a new cursor.
   :OracleAPIC:`More info... <dbcdup.html>`

.. function:: set_priority(priority)

   Set the cache priority for pages referenced by the DBC handle.
   :OracleAPIC:`More info... <dbcset_priority.html>`

.. function:: get_priority()

   Returns the cache priority for pages referenced by the DBC handle.
   :OracleAPIC:`More info... <dbcget_priority.html>`

.. function:: put(key, data, flags=0, dlen=-1, doff=-1)

   Stores the key/data pair into the database. Partial data records can
   be written using dlen and doff.
   :OracleAPIC:`More info... <dbcput.html>`

.. function:: get(flags, dlen=-1, doff=-1)

   See get(key, data, flags, dlen=-1, doff=-1) below.

.. function:: get(key, flags, dlen=-1, doff=-1)

   See get(key, data, flags, dlen=-1, doff=-1) below.

.. function:: get(key, data, flags, dlen=-1, doff=-1)

   Retrieves key/data pairs from the database using the cursor. All the
   specific functionalities of the get method are actually provided by
   the various methods below, which are the preferred way to fetch data
   using the cursor. These generic interfaces are only provided as an
   inconvenience. Partial data records are returned if dlen and doff
   are used in this method and in many of the specific methods below.
   :OracleAPIC:`More info... <dbcget.html>`

.. function:: pget(flags, dlen=-1, doff=-1)

   See pget(key, data, flags, dlen=-1, doff=-1) below.

.. function:: pget(key, flags, dlen=-1, doff=-1)

   See pget(key, data, flags, dlen=-1, doff=-1) below.

.. function:: pget(key, data, flags, dlen=-1, doff=-1)

   Similar to the already described get(). This method is available only
   on secondary databases. It will return the primary key, given the
   secondary one, and associated data
   :OracleAPIC:`More info... <dbcget.html>`

DBCursor Get Methods
--------------------

These DBCursor methods are all wrappers around the get() function in the
C API.

.. function:: current(flags=0, dlen=-1, doff=-1)

   Returns the key/data pair currently referenced by the cursor.
   :OracleAPIC:`More info... <dbcget.html#dbcget_DB_CURRENT>`

.. function:: get_current_size()

   Returns length of the data for the current entry referenced by the
   cursor.

.. function:: first(flags=0, dlen=-1, doff=-1)

   Position the cursor to the first key/data pair and return it.
   :OracleAPIC:`More info... <dbcget.html#dbcget_DB_FIRST>`

.. function:: last(flags=0, dlen=-1, doff=-1)

   Position the cursor to the last key/data pair and return it.
   :OracleAPIC:`More info... <dbcget.html#dbcget_DB_LAST>`

.. function:: next(flags=0, dlen=-1, doff=-1)

   Position the cursor to the next key/data pair and return it.
   :OracleAPIC:`More info... <dbcget.html#dbcget_DB_NEXT>`

.. function:: prev(flags=0, dlen=-1, doff=-1)

   Position the cursor to the previous key/data pair and return it.
   :OracleAPIC:`More info... <dbcget.html#dbcget_DB_PREV>`

.. function:: consume(flags=0, dlen=-1, doff=-1)

   For a database with the Queue access method, returns the record
   number and data from the first available record and deletes it from
   the queue.

   *NOTE:* This method is deprecated in Berkeley DB version 3.2 in favor
   of the new consume method in the DB class.

.. function:: get_both(key, data, flags=0)

   Like set() but positions the cursor to the record matching both key
   and data. (An alias for this is set_both, which makes more sense to
   me...)
   :OracleAPIC:`More info... <dbcget.html#dbcget_DB_GET_BOTH>`

.. function:: get_recno()

   Return the record number associated with the cursor. The database
   must use the BTree access method and have been created with the
   DB_RECNUM flag.
   :OracleAPIC:`More info... <dbcget.html#dbcget_DB_GET_RECNO>`

.. function:: join_item(flags=0)

   For cursors returned from the DB.join method, returns the combined
   key value from the joined cursors.
   :OracleAPIC:`More info... <dbcget.html#dbcget_DB_JOIN_ITEM>`

.. function:: next_dup(flags=0, dlen=-1, doff=-1)

   If the next key/data pair of the database is a duplicate record for
   the current key/data pair, the cursor is moved to the next key/data
   pair of the database, and that pair is returned.
   :OracleAPIC:`More info... <dbcget.html#dbcget_DB_NEXT_DUP>`

.. function:: next_nodup(flags=0, dlen=-1, doff=-1)

   The cursor is moved to the next non-duplicate key/data pair of the
   database, and that pair is returned.
   :OracleAPIC:`More info... <dbcget.html#dbcget_DB_NEXT_NODUP>`

.. function:: prev_dup(flags=0, dlen=-1, doff=-1)

   If the previous key/data pair of the database is a duplicate data
   record for the current key/data pair, the cursor is moved to the
   previous key/data pair of the database, and that pair is returned. 
   :OracleAPIC:`More info... <dbcget.html#dbcget_DB_PREV_DUP>`

.. function:: prev_nodup(flags=0, dlen=-1, doff=-1)

   The cursor is moved to the previous non-duplicate key/data pair of
   the database, and that pair is returned.
   :OracleAPIC:`More info... <dbcget.html#dbcget_DB_PREV_NODUP>`

.. function:: set(key, flags=0, dlen=-1, doff=-1)

   Move the cursor to the specified key in the database and return the
   key/data pair found there.
   :OracleAPIC:`More info... <dbcget.html#dbcget_DB_SET>`

.. function:: set_range(key, flags=0, dlen=-1, doff=-1)

   Identical to set() except that in the case of the BTree access
   method, the returned key/data pair is the smallest key greater than
   or equal to the specified key (as determined by the comparison
   function), permitting partial key matches and range searches.
   :OracleAPIC:`More info... <dbcget.html#dbcget_DB_SET_RANGE>`

.. function:: set_recno(recno, flags=0, dlen=-1, doff=-1)

   Move the cursor to the specific numbered record of the database, and
   return the associated key/data pair. The underlying database must be
   of type Btree and it must have been created with the DB_RECNUM flag.
   :OracleAPIC:`More info... <dbcget.html#dbcget_DB_SET_RECNO>`

.. function:: set_both(key, data, flags=0)

   See get_both(). The only difference in behaviour can be disabled
   using set_get_returns_none(2).
   :OracleAPIC:`More info... <dbcget.html#dbcget_DB_GET_BOTH>`

