=====
DBEnv
=====

Read :Oracle:`Oracle documentation <programmer_reference/index.html>`
for better understanding.

:OracleAPIC:`More info... <env.html>`

DBEnv Attributes
----------------

.. function:: DBEnv(flags=0)

   database home directory (read-only)

DBEnv Methods
-------------

.. function:: DBEnv(flags=0)

   Constructor.
   :OracleAPIC:`More info... <envcreate.html>`

.. function:: set_rpc_server(host, cl_timeout=0, sv_timeout=0)

   Establishes a connection for this dbenv to a RPC server.
   This function is not available if linked to Berkeley DB 4.8 or up.
   :OracleAPIC:`More info... <envset_rpc_server.html>`

.. function:: close(flags=0)

   Close the database environment, freeing resources.
   :OracleAPIC:`More info... <envclose.html>`

.. function:: open(homedir, flags=0, mode=0660)

   Prepare the database environment for use.
   :OracleAPIC:`More info... <envopen.html>`

.. function:: log_cursor()

   Returns a created log cursor.
   :OracleAPIC:`More info... <logcursor.html>`

.. function:: memp_stat(flags=0)

   Returns the memory pool (that is, the buffer cache) subsystem
   statistics.

   The returning value is a tuple. The first element is a dictionary
   with the general stats. The second element is another dictionary,
   keyed by filename, and the values are the stats for each file.
   
   The first dictionary contains these data:

    +-------------------+---------------------------------------------+
    | gbytes            | Gigabytes of cache (total cache size is     |
    |                   | st_gbytes + st_bytes).                      |
    +-------------------+---------------------------------------------+
    | bytes             | Bytes of cache (total cache size is         |
    |                   | st_gbytes + st_bytes).                      |
    +-------------------+---------------------------------------------+
    | ncache            | Number of caches.                           |
    +-------------------+---------------------------------------------+
    | max_ncache        | Maximum number of caches, as configured     |
    |                   | with the DB_ENV->set_cache_max() method.    |
    +-------------------+---------------------------------------------+
    | regsize           | Individual cache size, in bytes.            |
    +-------------------+---------------------------------------------+
    | mmapsize          | Maximum memory-mapped file size.            |
    +-------------------+---------------------------------------------+
    | maxopenfd         | Maximum open file descriptors.              |
    +-------------------+---------------------------------------------+
    | maxwrite          | Maximum sequential buffer writes.           |
    +-------------------+---------------------------------------------+
    | maxwrite_sleep    | Microseconds to pause after writing maximum |
    |                   | sequential buffers.                         |
    +-------------------+---------------------------------------------+
    | map               | Requested pages mapped into the process'    |
    |                   | address space (there is no available        |
    |                   | information about whether or not this       |
    |                   | request caused disk I/O, although examining |
    |                   | the application page fault rate may be      |
    |                   | helpful).                                   |
    +-------------------+---------------------------------------------+
    | cache_hit         | Requested pages found in the cache.         |
    +-------------------+---------------------------------------------+
    | cache_miss        | Requested pages not found in the cache.     |
    +-------------------+---------------------------------------------+
    | page_create       | Pages created in the cache.                 |
    +-------------------+---------------------------------------------+
    | page_in           | Pages read into the cache.                  |
    +-------------------+---------------------------------------------+
    | page_out          | Pages written from the cache to the backing |
    |                   | file.                                       |
    +-------------------+---------------------------------------------+
    | ro_evict          | Clean pages forced from the cache.          |
    +-------------------+---------------------------------------------+
    | rw_evict          | Dirty pages forced from the cache.          |
    +-------------------+---------------------------------------------+
    | page_trickle      | Dirty pages written using the               |
    |                   | DB_ENV->memp_trickle() method.              |
    +-------------------+---------------------------------------------+
    | pages             | Pages in the cache.                         |
    +-------------------+---------------------------------------------+
    | page_clean        | Clean pages currently in the cache.         |
    +-------------------+---------------------------------------------+
    | page_dirty        | Dirty pages currently in the cache.         |
    +-------------------+---------------------------------------------+
    | hash_buckets      | Number of hash buckets in buffer hash       |
    |                   | table.                                      |
    +-------------------+---------------------------------------------+
    | hash_searches     | Total number of buffer hash table lookups.  |
    +-------------------+---------------------------------------------+
    | hash_longest      | Longest chain ever encountered in buffer    |
    |                   | hash table lookups.                         |
    +-------------------+---------------------------------------------+
    | hash_examined     | Total number of hash elements traversed     |
    |                   | during hash table lookups.                  |
    +-------------------+---------------------------------------------+
    | hash_nowait       | Number of times that a thread of control    |
    |                   | was able to obtain a hash bucket lock       |
    |                   | without waiting.                            |
    +-------------------+---------------------------------------------+
    | hash_wait         | Number of times that a thread of control    |
    |                   | was forced to wait before obtaining a hash  |
    |                   | bucket lock.                                |
    +-------------------+---------------------------------------------+
    | hash_max_nowait   | The number of times a thread of control was |
    |                   | able to obtain the hash bucket lock without |
    |                   | waiting on the bucket which had the maximum |
    |                   | number of times that a thread of control    |
    |                   | needed to wait.                             |
    +-------------------+---------------------------------------------+
    | hash_max_wait     | Maximum number of times any hash bucket     |
    |                   | lock was waited for by a thread of control. |
    +-------------------+---------------------------------------------+
    | region_wait       | Number of times that a thread of control    |
    |                   | was forced to wait before obtaining a cache |
    |                   | region mutex.                               |
    +-------------------+---------------------------------------------+
    | region_nowait     | Number of times that a thread of control    |
    |                   | was able to obtain a cache region mutex     |
    |                   | without waiting.                            |
    +-------------------+---------------------------------------------+
    | mvcc_frozen       | Number of buffers frozen.                   |
    +-------------------+---------------------------------------------+
    | mvcc_thawed       | Number of buffers thawed.                   |
    +-------------------+---------------------------------------------+
    | mvcc_freed        | Number of frozen buffers freed.             |
    +-------------------+---------------------------------------------+
    | alloc             | Number of page allocations.                 |
    +-------------------+---------------------------------------------+
    | alloc_buckets     | Number of hash buckets checked during       |
    |                   | allocation.                                 |
    +-------------------+---------------------------------------------+
    | alloc_max_buckets | Maximum number of hash buckets checked      |
    |                   | during an allocation.                       |
    +-------------------+---------------------------------------------+
    | alloc_pages       | Number of pages checked during allocation.  |
    +-------------------+---------------------------------------------+
    | alloc_max_pages   | Maximum number of pages checked during an   |
    |                   | allocation.                                 |
    +-------------------+---------------------------------------------+
    | io_wait           | Number of operations blocked waiting for    |
    |                   | I/O to complete.                            |
    +-------------------+---------------------------------------------+
    | sync_interrupted  | Number of mpool sync operations             |
    |                   | interrupted.                                |
    +-------------------+---------------------------------------------+

   The second dictionary contains these data:

    +-------------------+---------------------------------------------+
    | pagesize          | Page size in bytes.                         |
    +-------------------+---------------------------------------------+
    | cache_hit         | Requested pages found in the cache.         |
    +-------------------+---------------------------------------------+
    | cache_miss        | Requested pages not found in the cache.     |
    +-------------------+---------------------------------------------+
    | map               | Requested pages mapped into the process'    |
    |                   | address space.                              |
    +-------------------+---------------------------------------------+
    | page_create       | Pages created in the cache.                 |
    +-------------------+---------------------------------------------+
    | page_in           | Pages read into the cache.                  |
    +-------------------+---------------------------------------------+
    | page_out          | Pages written from the cache to the backing |
    |                   | file.                                       |
    +-------------------+---------------------------------------------+

   :OracleAPIC:`More info... <mempstat.html>`

.. function:: memp_stat_print(flags=0)

   Displays cache subsystem statistical information.
   :OracleAPIC:`More info... <mempstat_print.html>`

.. function:: memp_sync(lsn=None)

   Flushes modified pages in the cache to their backing files. If
   provided, lsn is a tuple: (file, offset).
   :OracleAPIC:`More info... <mempsync.html>`
  
.. function:: memp_trickle(percent)

   Ensures that a specified percent of the pages in the cache are clean,
   by writing dirty pages to their backing files.
   :OracleAPIC:`More info... <memptrickle.html>`
   
.. function:: remove(homedir, flags=0)

   Remove a database environment.
   :OracleAPIC:`More info... <envremove.html>`

.. function:: dbremove(file, database=None, txn=None, flags=0)

   Removes the database specified by the file and database parameters.
   If no database is specified, the underlying file represented by file
   is removed, incidentally removing all of the databases it contained.
   :OracleAPIC:`More info... <envdbremove.html>`

.. function:: dbrename(file, database=None, newname, txn=None, flags=0)

   Renames the database specified by the file and database parameters to
   newname. If no database is specified, the underlying file represented
   by file is renamed, incidentally renaming all of the databases it
   contained.
   :OracleAPIC:`More info... <envdbrename.html>`

.. function:: fileid_reset(file, flags=0)

   All databases contain an ID string used to identify the database in
   the database environment cache. If a physical database file is
   copied, and used in the same environment as another file with the
   same ID strings, corruption can occur. The DB_ENV->fileid_reset
   method creates new ID strings for all of the databases in the
   physical file.
   :OracleAPIC:`More info... <envfileid_reset.html>`

.. function:: get_thread_count()

   Returns the thread count as set by the DB_ENV->set_thread_count()
   method.
   :OracleAPIC:`More info... <envget_thread_count.html>`

.. function:: set_thread_count(count)

   Declare an approximate number of threads in the database environment.
   The DB_ENV->set_thread_count() method must be called prior to opening
   the database environment if the DB_ENV->failchk() method will be
   used. The DB_ENV->set_thread_count() method does not set the maximum
   number of threads but is used to determine memory sizing and the
   thread control block reclamation policy.
   :OracleAPIC:`More info... <envset_thread_count.html>`

.. function:: set_encrypt(passwd, flags=0)

   Set the password used by the Berkeley DB library to perform
   encryption and decryption.
   :OracleAPIC:`More info... <envset_encrypt.html>`

.. function:: get_encrypt_flags()

   Returns the encryption flags.
   :OracleAPIC:`More info... <envget_encrypt_flags.html>`

.. function:: get_intermediate_dir_mode()

   Returns the intermediate directory permissions.

   Intermediate directories are directories needed for recovery.
   Normally, Berkeley DB does not create these directories and will do
   so only if the DB_ENV->set_intermediate_dir_mode() method is called. 

   :OracleAPIC:`More info... <envget_intermediate_dir_mode.html>`

.. function:: set_intermediate_dir_mode(mode)

   By default, Berkeley DB does not create intermediate directories
   needed for recovery, that is, if the file /a/b/c/mydatabase is being
   recovered, and the directory path b/c does not exist, recovery will
   fail. This default behavior is because Berkeley DB does not know what
   permissions are appropriate for intermediate directory creation, and
   creating the directory might result in a security problem.

   The DB_ENV->set_intermediate_dir_mode() method causes Berkeley DB to
   create any intermediate directories needed during recovery, using the
   specified permissions.

   :OracleAPIC:`More info... <envset_intermediate_dir_mode.html>`

.. function:: get_timeout(flags)

   Returns a timeout value, in microseconds.
   :OracleAPIC:`More info... <envget_timeout.html>`

.. function:: set_timeout(timeout, flags)

   Sets timeout values for locks or transactions in the database
   environment.
   :OracleAPIC:`More info... <envset_timeout.html>`

.. function:: get_mp_max_openfd()

   Returns the maximum number of file descriptors the library will open
   concurrently when flushing dirty pages from the cache.
   :OracleAPIC:`More info... <mempget_mp_max_openfd.html>`

.. function:: set_mp_max_openfd(max_open_fd)

   Limits the number of file descriptors the library will open
   concurrently when flushing dirty pages from the cache. 
   :OracleAPIC:`More info... <mempset_mp_max_openfd.html>`

.. function:: get_mp_max_write()

   Returns a tuple with the current maximum number of sequential write
   operations and microseconds to pause that the library can schedule
   when flushing dirty pages from the cache.
   :OracleAPIC:`More info... <mempget_mp_max_write.html>`

.. function:: set_mp_max_write(maxwrite, maxwrite_sleep)

   Limits the number of sequential write operations scheduled by the
   library when flushing dirty pages from the cache. 
   :OracleAPIC:`More info... <mempset_mp_max_write.html>`

.. function:: set_shm_key(key)

   Specify a base segment ID for Berkeley DB environment shared memory
   regions created in system memory on VxWorks or systems supporting
   X/Open-style shared memory interfaces; for example, UNIX systems
   supporting shmget(2) and related System V IPC interfaces.
   :OracleAPIC:`More info... <envset_shm_key.html>`

.. function:: get_shm_key()

   Returns the base segment ID.
   :OracleAPIC:`More info... <envget_shm_key.html>`

.. function:: set_cache_max(gbytes, bytes)

   Sets the maximum cache size, in bytes. The specified size is rounded
   to the nearest multiple of the cache region size, which is the
   initial cache size divided by the number of regions specified to the
   DB_ENV->set_cachesize() method. If no value is specified, it defaults
   to the initial cache size.
   :OracleAPIC:`More info... <envset_cache_max.html>`

.. function:: get_cache_max()

   Returns the maximum size of the cache as set using the
   DB_ENV->set_cache_max() method.
   :OracleAPIC:`More info... <envget_cache_max.html>`

.. function:: set_cachesize(gbytes, bytes, ncache=0)

   Set the size of the shared memory buffer pool.
   :OracleAPIC:`More info... <envset_cachesize.html>`

.. function:: get_cachesize()

   Returns a tuple with the current size and composition of the cache.
   :OracleAPIC:`More info... <envget_cachesize.html>`

.. function:: set_data_dir(dir)

   Set the environment data directory. You can call this function
   multiple times, adding new directories.
   :OracleAPIC:`More info... <envset_data_dir.html>`

.. function:: get_data_dirs()

   Return a tuple with the directories.
   :OracleAPIC:`More info... <envget_data_dirs.html>`

.. function:: get_flags()

   Returns the configuration flags set for a DB_ENV handle.
   :OracleAPIC:`More info... <envget_flags.html>`

.. function:: set_flags(flags, onoff)

   Set additional flags for the DBEnv. The onoff parameter specifes if
   the flag is set or cleared.
   :OracleAPIC:`More info... <envset_flags.html>`

.. function:: set_tmp_dir(dir)

   Set the directory to be used for temporary files.
   :OracleAPIC:`More info... <envset_tmp_dir.html>`

.. function:: get_tmp_dir()

   Returns the database environment temporary file directory.
   :OracleAPIC:`More info... <envget_tmp_dir.html>`

.. function:: set_get_returns_none(flag)

   By default when DB.get or DBCursor.get, get_both, first, last, next
   or prev encounter a DB_NOTFOUND error they return None instead of
   raising DBNotFoundError. This behaviour emulates Python dictionaries
   and is convenient for looping.

   You can use this method to toggle that behaviour for all of the
   aformentioned methods or extend it to also apply to the DBCursor.set,
   set_both, set_range, and set_recno methods. Supported values of
   flag:

   - **0** all DB and DBCursor get and set methods will raise a
     DBNotFoundError rather than returning None.

   - **1** *Default in module version <4.2.4*  The DB.get and
     DBCursor.get, get_both, first, last, next and prev methods return
     None.

   - **2** *Default in module version >=4.2.4* Extends the behaviour of
     **1** to the DBCursor set, set_both, set_range and set_recno
     methods.

   The default of returning None makes it easy to do things like this
   without having to catch DBNotFoundError (KeyError)::

                    data = mydb.get(key)
                    if data:
                        doSomething(data)

   or this::

                    rec = cursor.first()
                    while rec:
                        print rec
                        rec = cursor.next()

   Making the cursor set methods return None is useful in order to do
   this::

                    rec = mydb.set()
                    while rec:
                        key, val = rec
                        doSomething(key, val)
                        rec = mydb.next()

   The downside to this it that it is inconsistent with the rest of the
   package and noticeably diverges from the Oracle Berkeley DB API. If
   you prefer to have the get and set methods raise an exception when a
   key is not found, use this method to tell them to do so.

   Calling this method on a DBEnv object will set the default for all
   DB's later created within that environment. Calling it on a DB
   object sets the behaviour for that DB only.

   The previous setting is returned.

.. function:: set_private(object)

   Link an object to the DBEnv object. This allows to pass around an
   arbitrary object. For instance, for callback context.

.. function:: get_private()

   Give the object linked to the DBEnv.

.. function:: get_open_flags()

   Returns the current open method flags. That is, this method returns
   the flags that were specified when DB_ENV->open() was called.
   :OracleAPIC:`More info... <envget_open_flags.html>`

.. function:: get_lg_filemode()

   Returns the log file mode.
   :OracleAPIC:`More info... <envget_lg_filemode.html>`

.. function:: set_lg_filemode(filemode)

   Set the absolute file mode for created log files.
   :OracleAPIC:`More info... <envset_lg_filemode.html>`

.. function:: get_lg_bsize()

   Returns the size of the log buffer, in bytes.
   :OracleAPIC:`More info... <envget_lg_bsize.html>`

.. function:: set_lg_bsize(size)

   Set the size of the in-memory log buffer, in bytes.
   :OracleAPIC:`More info... <envset_lg_bsize.html>`

.. function:: get_lg_dir()

   Returns the log directory, which is the location for logging files.
   :OracleAPIC:`More info... <envget_lg_dir.html>`

.. function:: set_lg_dir(dir)

   The path of a directory to be used as the location of logging files.
   Log files created by the Log Manager subsystem will be created in
   this directory.
   :OracleAPIC:`More info... <envset_lg_dir.html>`

.. function:: set_lg_max(size)

   Set the maximum size of a single file in the log, in bytes.
   :OracleAPIC:`More info... <envset_lg_max.html>`

.. function:: get_lg_max(size)

   Returns the maximum log file size.
   :OracleAPIC:`More info... <envset_lg_max.html>`

.. function:: get_lg_regionmax()

   Returns the size of the underlying logging subsystem region.
   :OracleAPIC:`More info... <envget_lg_regionmax.html>`

.. function:: set_lg_regionmax(size)

   Set the maximum size of a single region in the log, in bytes.
   :OracleAPIC:`More info... <envset_lg_regionmax.html>`

.. function:: get_lk_partitions()

   Returns the number of lock table partitions used in the Berkeley DB
   environment.
   :OracleAPIC:`More info... <envget_lk_partitions.html>`

.. function:: set_lk_partitions(partitions)

   Set the number of lock table partitions in the Berkeley DB
   environment.
   :OracleAPIC:`More info... <envset_lk_partitions.html>`

.. function:: get_lk_detect()

   Returns the deadlock detector configuration.
   :OracleAPIC:`More info... <envget_lk_detect.html>`

.. function:: set_lk_detect(mode)

   Set the automatic deadlock detection mode.
   :OracleAPIC:`More info... <envset_lk_detect.html>`

.. function:: set_lk_max(max)

   Set the maximum number of locks. (This method is deprecated.)
   :OracleAPIC:`More info... <envset_lk_max.html>`

.. function:: get_lk_max_locks()

   Returns the maximum number of potential locks.
   :OracleAPIC:`More info... <envget_lk_max_locks.html>`

.. function:: set_lk_max_locks(max)

   Set the maximum number of locks supported by the Berkeley DB lock
   subsystem.
   :OracleAPIC:`More info... <envset_lk_max_locks.html>`

.. function:: get_lk_max_lockers()

   Returns the maximum number of potential lockers.
   :OracleAPIC:`More info... <envget_lk_max_lockers.html>`

.. function:: set_lk_max_lockers(max)

   Set the maximum number of simultaneous locking entities supported by
   the Berkeley DB lock subsystem.
   :OracleAPIC:`More info... <envset_lk_max_lockers.html>`

.. function:: get_lk_max_objects()

   Returns the maximum number of locked objects.
   :OracleAPIC:`More info... <envget_lk_max_objects.html>`

.. function:: set_lk_max_objects(max)

   Set the maximum number of simultaneously locked objects supported by
   the Berkeley DB lock subsystem.
   :OracleAPIC:`More info... <envset_lk_max_lockers.html>`

.. function:: get_mp_mmapsize()

   Returns the the maximum file size, in bytes, for a file to be mapped
   into the process address space.
   :OracleAPIC:`More info... <envget_mp_mmapsize.html>`

.. function:: set_mp_mmapsize(size)

   Files that are opened read-only in the memory pool (and that satisfy
   a few other criteria) are, by default, mapped into the process
   address space instead of being copied into the local cache. This can
   result in better-than-usual performance, as available virtual memory
   is normally much larger than the local cache, and page faults are
   faster than page copying on many systems. However, in the presence
   of limited virtual memory it can cause resource starvation, and in
   the presence of large databases, it can result in immense process
   sizes.

   This method sets the maximum file size, in bytes, for a file to be
   mapped into the process address space. If no value is specified, it
   defaults to 10MB.
   :OracleAPIC:`More info... <envset_mp_mmapsize.html>`

.. function:: stat_print(flags=0)

   Displays the default subsystem statistical information.
   :OracleAPIC:`More info... <envstat.html>`

.. function:: log_file(lsn)

   Maps lsn to filenames, returning the name of the file
   containing the named record.
   :OracleAPIC:`More info... <logfile.html>`

.. function:: log_printf(string, txn=None)

   Appends an informational message to the Berkeley DB database
   environment log files.
   :OracleAPIC:`More info... <logprintf.html>`

.. function:: log_archive(flags=0)

   Returns a list of log or database file names. By default,
   log_archive returns the names of all of the log files that are no
   longer in use (e.g., no longer involved in active transactions), and
   that may safely be archived for catastrophic recovery and then
   removed from the system.
   :OracleAPIC:`More info... <logarchive.html>`

.. function:: log_flush()

   Force log records to disk. Useful if the environment, database or
   transactions are used as ACI, instead of ACID. For example, if the
   environment is opened as DB_TXN_NOSYNC.
   :OracleAPIC:`More info... <logflush.html>`

.. function:: log_get_config(which)

   Returns whether the specified which parameter is currently set or
   not. You can manage this value using the DB_ENV->log_set_config()
   method.
   :OracleAPIC:`More info... <envlog_get_config.html>`

.. function:: log_set_config(flags, onoff)

   Configures the Berkeley DB logging subsystem.
   :OracleAPIC:`More info... <envlog_set_config.html>`

.. function:: lock_detect(atype, flags=0)

   Run one iteration of the deadlock detector, returns the number of
   transactions aborted.
   :OracleAPIC:`More info... <lockdetect.html>`

.. function:: lock_get(locker, obj, lock_mode, flags=0)

   Acquires a lock and returns a handle to it as a DBLock object. The
   locker parameter is an integer representing the entity doing the
   locking, and obj is an object representing the item to be locked.
   :OracleAPIC:`More info... <lockget.html>`

.. function:: lock_id()

   Acquires a locker id, guaranteed to be unique across all threads and
   processes that have the DBEnv open.
   :OracleAPIC:`More info... <lockid.html>`

.. function:: lock_id_free(id)

   Frees a locker ID allocated by the "dbenv.lock_id()" method.
   :OracleAPIC:`More info... <lockid_free.html>`

.. function:: lock_put(lock)

   Release the lock.
   :OracleAPIC:`More info... <lockput.html>`

.. function:: lock_stat(flags=0)

   Returns a dictionary of locking subsystem statistics with the
   following keys:

    +----------------+---------------------------------------------+
    | id             | Last allocated lock ID.                     |
    +----------------+---------------------------------------------+
    | cur_maxid      | The current maximum unused locker ID.       |
    +----------------+---------------------------------------------+
    | nmodes         | Number of lock modes.                       |
    +----------------+---------------------------------------------+
    | maxlocks       | Maximum number of locks possible.           |
    +----------------+---------------------------------------------+
    | maxlockers     | Maximum number of lockers possible.         |
    +----------------+---------------------------------------------+
    | maxobjects     | Maximum number of objects possible.         |
    +----------------+---------------------------------------------+
    | nlocks         | Number of current locks.                    |
    +----------------+---------------------------------------------+
    | maxnlocks      | Maximum number of locks at once.            |
    +----------------+---------------------------------------------+
    | nlockers       | Number of current lockers.                  |
    +----------------+---------------------------------------------+
    | nobjects       | Number of current lock objects.             |
    +----------------+---------------------------------------------+
    | maxnobjects    | Maximum number of lock objects at once.     |
    +----------------+---------------------------------------------+
    | maxnlockers    | Maximum number of lockers at once.          |
    +----------------+---------------------------------------------+
    | nrequests      | Total number of locks requested.            |
    +----------------+---------------------------------------------+
    | nreleases      | Total number of locks released.             |
    +----------------+---------------------------------------------+
    | nupgrade       | Total number of locks upgraded.             |
    +----------------+---------------------------------------------+
    | ndowngrade     | Total number of locks downgraded.           |
    +----------------+---------------------------------------------+
    | lock_wait      | The number of lock requests not immediately |
    |                | available due to conflicts, for which the   |
    |                | thread of control waited.                   |
    +----------------+---------------------------------------------+
    | lock_nowait    | The number of lock requests not immediately | 
    |                | available due to conflicts, for which the   |
    |                | thread of control did not wait.             |
    +----------------+---------------------------------------------+
    | ndeadlocks     | Number of deadlocks.                        |
    +----------------+---------------------------------------------+
    | locktimeout    | Lock timeout value.                         |
    +----------------+---------------------------------------------+
    | nlocktimeouts  | The number of lock requests that have timed |
    |                | out.                                        |
    +----------------+---------------------------------------------+
    | txntimeout     | Transaction timeout value.                  |
    +----------------+---------------------------------------------+
    | ntxntimeouts   | The number of transactions that have timed  |
    |                | out. This value is also a component of      |
    |                | ndeadlocks, the total number of deadlocks   |
    |                | detected.                                   |
    +----------------+---------------------------------------------+
    | objs_wait      | The number of requests to allocate or       |
    |                | deallocate an object for which the thread   |
    |                | of control waited.                          |
    +----------------+---------------------------------------------+
    | objs_nowait    | The number of requests to allocate or       |
    |                | deallocate an object for which the thread   |
    |                | of control did not wait.                    |
    +----------------+---------------------------------------------+
    | lockers_wait   | The number of requests to allocate or       |
    |                | deallocate a locker for which the thread of |
    |                | control waited.                             |
    +----------------+---------------------------------------------+
    | lockers_nowait | The number of requests to allocate or       |
    |                | deallocate a locker for which the thread of |
    |                | control did not wait.                       |
    +----------------+---------------------------------------------+
    | locks_wait     | The number of requests to allocate or       |
    |                | deallocate a lock structure for which the   |
    |                | thread of control waited.                   |
    +----------------+---------------------------------------------+
    | locks_nowait   | The number of requests to allocate or       |
    |                | deallocate a lock structure for which the   |
    |                | thread of control did not wait.             |
    +----------------+---------------------------------------------+
    | hash_len       | Maximum length of a lock hash bucket.       |
    +----------------+---------------------------------------------+
    | regsize        | Size of the region.                         |
    +----------------+---------------------------------------------+
    | region_wait    | Number of times a thread of control was     |
    |                | forced to wait before obtaining the region  |
    |                | lock.                                       |
    +----------------+---------------------------------------------+
    | region_nowait  | Number of times a thread of control was     |
    |                | able to obtain the region lock  without     |
    |                | waiting.                                    |
    +----------------+---------------------------------------------+

   :OracleAPIC:`More info... <lockstat.html>`

.. function:: lock_stat_print(flags=0)

   Displays the locking subsystem statistical information.
   :OracleAPIC:`More info... <lockstat_print.html>`

.. function:: get_tx_max()

   Returns the number of active transactions.
   :OracleAPIC:`More info... <envget_tx_max.html>`

.. function:: set_tx_max(max)

   Set the maximum number of active transactions.
   :OracleAPIC:`More info... <envset_tx_max.html>`

.. function:: get_tx_timestamp()

   Returns the recovery timestamp.
   :OracleAPIC:`More info... <envget_tx_timestamp.html>`

.. function:: set_tx_timestamp(timestamp)

   Recover to the time specified by timestamp rather than to the most
   current possible date.
   :OracleAPIC:`More info... <envset_tx_timestamp.html>`

.. function:: txn_begin(parent=None, flags=0)

   Creates and begins a new transaction. A DBTxn object is returned.
   :OracleAPIC:`More info... <txnbegin.html>`

.. function:: txn_checkpoint(kbyte=0, min=0, flag=0)

   Flushes the underlying memory pool, writes a checkpoint record to the
   log and then flushes the log.
   :OracleAPIC:`More info... <txncheckpoint.html>`

.. function:: txn_stat(flags=0)

   Return a dictionary of transaction statistics with the following
   keys:

    +--------------+---------------------------------------------+
    | last_ckp     | The LSN of the last checkpoint.             |
    +--------------+---------------------------------------------+
    | time_ckp     | Time the last completed checkpoint finished |
    |              | (as the number of seconds since the Epoch,  |
    |              | returned by the IEEE/ANSI Std 1003.1 POSIX  |
    |              | time interface).                            |
    +--------------+---------------------------------------------+
    | last_txnid   | Last transaction ID allocated.              |
    +--------------+---------------------------------------------+
    | maxtxns      | Max number of active transactions possible. |
    +--------------+---------------------------------------------+
    | nactive      | Number of transactions currently active.    |
    +--------------+---------------------------------------------+
    | maxnactive   | Max number of active transactions at once.  |
    +--------------+---------------------------------------------+
    | nsnapshot    | The number of transactions on the snapshot  |
    |              | list. These are transactions which modified |
    |              | a database opened with DB_MULTIVERSION, and |
    |              | which have committed or aborted, but the    |
    |              | copies of pages they created are still in   |
    |              | the cache.                                  |
    +--------------+---------------------------------------------+
    | maxnsnapshot | The maximum number of transactions on the   |
    |              | snapshot list at any one time.              |
    +--------------+---------------------------------------------+
    | nbegins      | Number of transactions that have begun.     |
    +--------------+---------------------------------------------+
    | naborts      | Number of transactions that have aborted.   |
    +--------------+---------------------------------------------+
    | ncommits     | Number of transactions that have committed. |
    +--------------+---------------------------------------------+
    | nrestores    | Number of transactions that have been       |
    |              | restored.                                   |
    +--------------+---------------------------------------------+
    | regsize      | Size of the region.                         |
    +--------------+---------------------------------------------+
    | region_wait  | Number of times that a thread of control    |
    |              | was forced to wait before obtaining the     |
    |              | region lock.                                |
    +--------------+---------------------------------------------+
    | region_nowait| Number of times that a thread of control    |
    |              | was able to obtain the region lock without  |
    |              | waiting.                                    |
    +--------------+---------------------------------------------+

   :OracleAPIC:`More info... <txnstat.html>`

.. function:: txn_stat_print(flags=0)

   Displays the transaction subsystem statistical information.
   :OracleAPIC:`More info... <txnstat_print.html>`

.. function:: lsn_reset(file=None,flags=0)

   This method allows database files to be moved from one transactional
   database environment to another.
   :OracleAPIC:`More info... <envlsn_reset.html>`

.. function:: log_stat(flags=0)

   Returns a dictionary of logging subsystem statistics with the
   following keys:

    +-------------------+---------------------------------------------+
    | magic             | The magic number that identifies a file as  |
    |                   | a log file.                                 |
    +-------------------+---------------------------------------------+
    | version           | The version of the log file type.           |
    +-------------------+---------------------------------------------+
    | mode              | The mode of any created log files.          |
    +-------------------+---------------------------------------------+
    | lg_bsize          | The in-memory log record cache size.        |
    +-------------------+---------------------------------------------+
    | lg_size           | The log file size.                          |
    +-------------------+---------------------------------------------+
    | record            | The number of records written to this log.  |
    +-------------------+---------------------------------------------+
    | w_mbytes          | The number of megabytes written to this     |
    |                   | log.                                        |
    +-------------------+---------------------------------------------+
    | w_bytes           | The number of bytes over and above w_mbytes |
    |                   | written to this log.                        |
    +-------------------+---------------------------------------------+
    | wc_mbytes         | The number of megabytes written to this log |
    |                   | since the last checkpoint.                  |
    +-------------------+---------------------------------------------+
    | wc_bytes          | The number of bytes over and above          |
    |                   | wc_mbytes written to this log since the     |
    |                   | last checkpoint.                            |
    +-------------------+---------------------------------------------+
    | wcount            | The number of times the log has been        |
    |                   | written to disk.                            |
    +-------------------+---------------------------------------------+
    | wcount_fill       | The number of times the log has been        |
    |                   | written to disk because the in-memory log   |
    |                   | record cache filled up.                     |
    +-------------------+---------------------------------------------+
    | rcount            | The number of times the log has been read   |
    |                   | from disk.                                  |
    +-------------------+---------------------------------------------+
    | scount            | The number of times the log has been        |
    |                   | flushed to disk.                            |
    +-------------------+---------------------------------------------+
    | cur_file          | The current log file number.                |
    +-------------------+---------------------------------------------+
    | cur_offset        | The byte offset in the current log file.    |
    +-------------------+---------------------------------------------+
    | disk_file         | The log file number of the last record      |
    |                   | known to be on disk.                        |
    +-------------------+---------------------------------------------+
    | disk_offset       | The byte offset of the last record known to |
    |                   | be on disk.                                 |
    +-------------------+---------------------------------------------+
    | maxcommitperflush | The maximum number of commits contained in  |
    |                   | a single log flush.                         |
    +-------------------+---------------------------------------------+
    | mincommitperflush | The minimum number of commits contained in  |
    |                   | a single log flush that contained a commit. |
    +-------------------+---------------------------------------------+
    | regsize           | The size of the log region, in bytes.       |
    +-------------------+---------------------------------------------+
    | region_wait       | The number of times that a thread of        |
    |                   | control was forced to wait before obtaining |
    |                   | the log region mutex.                       |
    +-------------------+---------------------------------------------+
    | region_nowait     | The number of times that a thread of        |
    |                   | control was able to obtain the log region   |
    |                   | mutex without waiting.                      |
    +-------------------+---------------------------------------------+

   :OracleAPIC:`More info... <logstat.html>`

.. function:: log_stat_print(flags=0)

   Displays the logging subsystem statistical information.
   :OracleAPIC:`More info... <logstat_print.html>`

.. function:: txn_recover()

   Returns a list of tuples (GID, TXN) of transactions prepared but
   still unresolved. This is used while doing environment recovery in an
   application using distributed transactions.

   This method must be called only from a single thread at a time. It
   should be called after DBEnv recovery.
   :OracleAPIC:`More info... <txnrecover.html>`

.. function:: set_verbose(which, onoff)

   Turns specific additional informational and debugging messages in the
   Berkeley DB message output on and off. To see the additional
   messages, verbose messages must also be configured for the
   application.
   :OracleAPIC:`More info... <envset_verbose.html>`

.. function:: get_verbose(which)

   Returns whether the specified *which* parameter is currently set or
   not.
   :OracleAPIC:`More info... <envget_verbose.html>`

.. function:: set_event_notify(eventFunc)

   Configures a callback function which is called to notify the process
   of specific Berkeley DB events.
   :OracleAPIC:`More info... <envevent_notify.html>`

.. function:: mutex_stat(flags=0)

   Returns a dictionary of mutex subsystem statistics with the following
   keys:

    +-----------------+--------------------------------------------+
    | mutex_align     | The mutex alignment, in bytes.             |
    +-----------------+--------------------------------------------+
    | mutex_tas_spins | The number of times test-and-set mutexes   |
    |                 | will spin without blocking.                |
    +-----------------+--------------------------------------------+
    | mutex_cnt       | The total number of mutexes configured.    |
    +-----------------+--------------------------------------------+
    | mutex_free      | The number of mutexes currently available. |
    +-----------------+--------------------------------------------+
    | mutex_inuse     | The number of mutexes currently in use.    |
    +-----------------+--------------------------------------------+
    | mutex_inuse_max | The maximum number of mutexes ever in use. |
    +-----------------+--------------------------------------------+
    | regsize         | The size of the mutex region, in bytes.    |
    +-----------------+--------------------------------------------+
    | region_wait     | The number of times that a thread of       |
    |                 | control was forced to wait before          |
    |                 | obtaining the mutex region mutex.          |
    +-----------------+--------------------------------------------+
    | region_nowait   | The number of times that a thread of       |
    |                 | control was able to obtain the mutex       |
    |                 | region mutex without waiting.              |
    +-----------------+--------------------------------------------+

   :OracleAPIC:`More info... <mutexstat.html>`

.. function:: mutex_stat_print(flags=0)

   Displays the mutex subsystem statistical information.
   :OracleAPIC:`More info... <mutexstat_print.html>`

.. function:: mutex_set_max(value)

   Configure the total number of mutexes to allocate.
   :OracleAPIC:`More info... <mutexset_max.html>`

.. function:: mutex_get_max()

   Returns the total number of mutexes allocated.
   :OracleAPIC:`More info... <mutexget_max.html>`

.. function:: mutex_set_increment(value)

   Configure the number of additional mutexes to allocate.
   :OracleAPIC:`More info... <mutexset_increment.html>`

.. function:: mutex_get_increment()

   Returns the number of additional mutexes to allocate.
   :OracleAPIC:`More info... <mutexget_increment.html>`

.. function:: mutex_set_align(align)

   Set the mutex alignment, in bytes.
   :OracleAPIC:`More info... <mutexset_align.html>`

.. function:: mutex_get_align()

   Returns the mutex alignment, in bytes.
   :OracleAPIC:`More info... <mutexget_align.html>`

.. function:: mutex_set_tas_spins(tas_spins)

   Specify that test-and-set mutexes should spin tas_spins times without
   blocking. Check the default values in the Oracle webpage.
   :OracleAPIC:`More info... <mutexset_tas_spins.html>`

.. function:: mutex_get_tas_spins()

   Returns the test-and-set spin count.
   :OracleAPIC:`More info... <mutexget_tas_spins.html>`

DBEnv Replication Manager Methods
---------------------------------

This module automates many of the tasks needed to provide replication
abilities in a Berkeley DB system. The module is fairly limited, but
enough in many cases. Users more demanding must use the **full** Base
Replication API.

This module requires pthread support (in Unix), so you must compile
Berkeley DB with it if you want to be able to use the Replication
Manager.

.. function:: repmgr_start(nthreads, flags)

   Starts the replication manager.
   :OracleAPIC:`More info... <repmgrstart.html>`

.. function:: repmgr_site(host, port)

   Returns a DB_SITE handle that defines a site's host/port network
   address. You use the DB_SITE handle to configure and manage
   replication sites.
   :OracleAPIC:`More info... <repmgr_site.html>`

.. function:: repmgr_site_by_eid(eid)

   Returns a DB_SITE handle based on the site's Environment ID value.
   You use the DB_SITE handle to configure and manage replication sites.
   :OracleAPIC:`More info... <repmgr_site_by_eid.html>`

.. function:: repmgr_set_ack_policy(ack_policy)

   Specifies how master and client sites will handle acknowledgment of
   replication messages which are necessary for "permanent" records.
   :OracleAPIC:`More info... <repmgrset_ack_policy.html>`

.. function:: repmgr_get_ack_policy()

   Returns the replication manager's client acknowledgment policy.
   :OracleAPIC:`More info... <repmgrget_ack_policy.html>`

.. function:: repmgr_site_list()

   Returns a dictionary with the status of the sites currently known by
   the replication manager.
   
   The keys are the Environment ID assigned by the replication manager.
   This is the same value that is passed to the application's event
   notification function for the DB_EVENT_REP_NEWMASTER event. 

   The values are tuples containing the hostname, the TCP/IP port number
   and the link status.

   :OracleAPIC:`More info... <repmgrsite_list.html>`

.. function:: repmgr_stat(flags=0)

   Returns a dictionary with the replication manager statistics. Keys
   are:

   +-----------------+-------------------------------------------------+
   | perm_failed     | The number of times a message critical for      |
   |                 | maintaining database integrity (for example, a  |
   |                 | transaction commit), originating at this site,  |
   |                 | did not receive sufficient acknowledgement from |
   |                 | clients, according to the configured            |
   |                 | acknowledgement policy and acknowledgement      |
   |                 | timeout.                                        |
   +-----------------+-------------------------------------------------+
   | msgs_queued     | The number of outgoing messages which could not |
   |                 | be transmitted immediately, due to a full       |
   |                 | network buffer, and had to be queued for later  |
   |                 | delivery.                                       |
   +-----------------+-------------------------------------------------+
   | msgs_dropped    | The number of outgoing messages that were       |
   |                 | completely dropped, because the outgoing        |
   |                 | message queue was full. (Berkeley DB            |
   |                 | replication is tolerant of dropped messages,    |
   |                 | and will automatically request retransmission   |
   |                 | of any missing messages as needed.)             |
   +-----------------+-------------------------------------------------+
   | connection_drop | The number of times an existing TCP/IP          |
   |                 | connection failed.                              |
   +-----------------+-------------------------------------------------+
   | connect_fail    | The number of times an attempt to open a new    |
   |                 | TCP/IP connection failed.                       |
   +-----------------+-------------------------------------------------+

   :OracleAPIC:`More info... <repmgrstat.html>`

.. function:: repmgr_stat_print(flags=0)

   Displays the replication manager statistical information.
   :OracleAPIC:`More info... <repmgrstat_print.html>`


DBEnv Replication Methods
-------------------------

This section provides the raw methods for replication. If possible,
it is recommended to use the Replication Manager.

.. function:: rep_elect(nsites, nvotes)

   Holds an election for the master of a replication group.
   :OracleAPIC:`More info... <repelect.html>`

.. function:: rep_set_transport(envid, transportFunc)

   Initializes the communication infrastructure for a database
   environment participating in a replicated application.
   :OracleAPIC:`More info... <reptransport.html>`

.. function:: rep_process_messsage(control, rec, envid)

   Processes an incoming replication message sent by a member of the
   replication group to the local database environment.

   Returns a two element tuple.

   :OracleAPIC:`More info... <repmessage.html>`

.. function:: rep_start(flags, cdata=None)

   Configures the database environment as a client or master in a group
   of replicated database environments.

   The DB_ENV->rep_start method is not called by most replication
   applications. It should only be called by applications implementing
   their own network transport layer, explicitly holding replication
   group elections and handling replication messages outside of the
   replication manager framework.

   :OracleAPIC:`More info... <repstart.html>`

.. function:: rep_sync()

   Forces master synchronization to begin for this client. This method
   is the other half of setting the DB_REP_CONF_DELAYCLIENT flag via the
   DB_ENV->rep_set_config method.
   :OracleAPIC:`More info... <repsync.html>`

.. function:: rep_set_config(which, onoff)

   Configures the Berkeley DB replication subsystem.
   :OracleAPIC:`More info... <repconfig.html>`

.. function:: rep_get_config(which)

   Returns whether the specified which parameter is currently set or
   not.
   :OracleAPIC:`More info... <repget_config.html>`

.. function:: rep_set_limit(bytes)

   Sets a byte-count limit on the amount of data that will be
   transmitted from a site in response to a single message processed by
   the DB_ENV->rep_process_message method. The limit is not a hard
   limit, and the record that exceeds the limit is the last record to be
   sent.
   :OracleAPIC:`More info... <repset_limit.html>`

.. function:: rep_get_limit()

   Gets a byte-count limit on the amount of data that will be
   transmitted from a site in response to a single message processed by
   the DB_ENV->rep_process_message method. The limit is not a hard
   limit, and the record that exceeds the limit is the last record to be
   sent.
   :OracleAPIC:`More info... <repget_limit.html>`

.. function:: rep_set_request(minimum, maximum)

   Sets a threshold for the minimum and maximum time that a client
   waits before requesting retransmission of a missing message.
   Specifically, if the client detects a gap in the sequence of incoming
   log records or database pages, Berkeley DB will wait for at least min
   microseconds before requesting retransmission of the missing record.
   Berkeley DB will double that amount before requesting the same
   missing record again, and so on, up to a maximum threshold of max
   microseconds.
   :OracleAPIC:`More info... <repset_request.html>`

.. function:: rep_get_request()

   Returns a tuple with the minimum and maximum number of microseconds a
   client waits before requesting retransmission.
   :OracleAPIC:`More info... <repget_request.html>`

.. function:: rep_set_nsites(nsites)

   Specifies the total number of sites in a replication group.
   :OracleAPIC:`More info... <repnsites.html>`

.. function:: rep_get_nsites()

   Returns the total number of sites in the replication group.
   :OracleAPIC:`More info... <repget_nsites.html>`

.. function:: rep_set_priority(priority)

   Specifies the database environment's priority in replication group
   elections. The priority must be a positive integer, or 0 if this
   environment cannot be a replication group master.
   :OracleAPIC:`More info... <reppriority.html>`

.. function:: rep_get_priority()

   Returns the database environment priority.
   :OracleAPIC:`More info... <repget_priority.html>`

.. function:: rep_set_timeout(which, timeout)

   Specifies a variety of replication timeout values.
   :OracleAPIC:`More info... <repset_timeout.html>`

.. function:: rep_get_timeout(which)

   Returns the timeout value for the specified *which* parameter.
   :OracleAPIC:`More info... <repget_timeout.html>`

.. function:: rep_set_clockskew(fast, slow)

   Sets the clock skew ratio among replication group members based on
   the fastest and slowest measurements among the group for use with
   master leases.
   :OracleAPIC:`More info... <repclockskew.html>`

.. function:: rep_get_clockskew()

   Returns a tuple with the current clock skew values.
   :OracleAPIC:`More info... <repget_clockskew.html>`
   
.. function:: rep_stat(flags=0)

   Returns a dictionary with the replication subsystem statistics. Keys
   are:

   +---------------------+---------------------------------------------+
   | st_bulk_fills       | The number of times the bulk buffer filled  |
   |                     | up, forcing the buffer content to be sent.  |
   +---------------------+---------------------------------------------+
   | bulk_overflows      | The number of times a record was bigger     |
   |                     | than the entire bulk buffer, and therefore  |
   |                     | had to be sent as a singleton.              |
   +---------------------+---------------------------------------------+
   | bulk_records        | The number of records added to a bulk       |
   |                     | buffer.                                     |
   +---------------------+---------------------------------------------+
   | bulk_transfers      | The number of bulk buffers transferred (via |
   |                     | a call to the application's send function). |
   +---------------------+---------------------------------------------+
   | client_rerequests   | The number of times this client site        |
   |                     | received a "re-request" message, indicating |
   |                     | that a request it previously sent to        |
   |                     | another client could not be serviced by     |
   |                     | that client. (Compare to client_svc_miss.)  |
   +---------------------+---------------------------------------------+
   | client_svc_miss     | The number of "request" type messages       |
   |                     | received by this client that could not be   |
   |                     | processed, forcing the originating          |
   |                     | requester to try sending the request to the |
   |                     | master (or another client).                 |
   +---------------------+---------------------------------------------+
   | client_svc_req      | The number of "request" type messages       |
   |                     | received by this client. ("Request"         |
   |                     | messages are usually sent from a client to  |
   |                     | the master, but a message marked with the   |
   |                     | DB_REP_ANYWHERE flag in the invocation of   |
   |                     | the application's send function may be sent |
   |                     | to another client instead.)                 |
   +---------------------+---------------------------------------------+
   | dupmasters          | The number of duplicate master conditions   |
   |                     | originally detected at this site.           |
   +---------------------+---------------------------------------------+
   | egen                | The current election generation number.     |
   +---------------------+---------------------------------------------+
   | election_cur_winner | The election winner.                        |
   +---------------------+---------------------------------------------+
   | election_gen        | The election generation number.             |
   +---------------------+---------------------------------------------+
   | election_lsn        | The maximum LSN of election winner.         |
   +---------------------+---------------------------------------------+
   | election_nsites     | The number sites responding to this site    |
   |                     | during the last election.                   |
   +---------------------+---------------------------------------------+
   | election_nvotes     | The number of votes required in the last    |
   |                     | election.                                   |
   +---------------------+---------------------------------------------+
   | election_priority   | The election priority.                      |
   +---------------------+---------------------------------------------+
   | election_sec        | The number of seconds the last election     |
   |                     | took (the total election time is            |
   |                     | election_sec plus election_usec).           |
   +---------------------+---------------------------------------------+
   | election_status     | The current election phase (0 if no         |
   |                     | election is in progress).                   |
   +---------------------+---------------------------------------------+
   | election_tiebreaker | The election tiebreaker value.              |
   +---------------------+---------------------------------------------+
   | election_usec       | The number of microseconds the last         |
   |                     | election took (the total election time is   |
   |                     | election_sec plus election_usec).           |
   +---------------------+---------------------------------------------+
   | election_votes      | The number of votes received in the last    |
   |                     | election.                                   |
   +---------------------+---------------------------------------------+
   | elections           | The number of elections held.               |
   +---------------------+---------------------------------------------+
   | elections_won       | The number of elections won.                |
   +---------------------+---------------------------------------------+
   | env_id              | The current environment ID.                 |
   +---------------------+---------------------------------------------+
   | env_priority        | The current environment priority.           |
   +---------------------+---------------------------------------------+
   | gen                 | The current generation number.              |
   +---------------------+---------------------------------------------+
   | log_duplicated      | The number of duplicate log records         |
   |                     | received.                                   |
   +---------------------+---------------------------------------------+
   | log_queued          | The number of log records currently queued. |
   +---------------------+---------------------------------------------+
   | log_queued_max      | The maximum number of log records ever      |
   |                     | queued at once.                             |
   +---------------------+---------------------------------------------+
   | log_queued_total    | The total number of log records queued.     |
   +---------------------+---------------------------------------------+
   | log_records         | The number of log records received and      |
   |                     | appended to the log.                        |
   +---------------------+---------------------------------------------+
   | log_requested       | The number of times log records were missed |
   |                     | and requested.                              |
   +---------------------+---------------------------------------------+
   | master              | The current master environment ID.          |
   +---------------------+---------------------------------------------+
   | master_changes      | The number of times the master has changed. |
   +---------------------+---------------------------------------------+
   | max_lease_sec       | The number of seconds of the longest lease  |
   |                     | (the total lease time is max_lease_sec plus |
   |                     | max_lease_usec).                            |
   +---------------------+---------------------------------------------+
   | max_lease_usec      | The number of microseconds of the longest   |
   |                     | lease (the total lease time is              |
   |                     | max_lease_sec plus max_lease_usec).         |
   +---------------------+---------------------------------------------+
   | max_perm_lsn        | The LSN of the maximum permanent log        |
   |                     | record, or 0 if there are no permanent log  |
   |                     | records.                                    |
   +---------------------+---------------------------------------------+
   | msgs_badgen         | The number of messages received with a bad  |
   |                     | generation number.                          |
   +---------------------+---------------------------------------------+
   | msgs_processed      | The number of messages received and         |
   |                     | processed.                                  |
   +---------------------+---------------------------------------------+
   | msgs_recover        | The number of messages ignored due to       |
   |                     | pending recovery.                           |
   +---------------------+---------------------------------------------+
   | msgs_send_failures  | The number of failed message sends.         |
   +---------------------+---------------------------------------------+
   | msgs_sent           | The number of messages sent.                |
   +---------------------+---------------------------------------------+
   | newsites            | The number of new site messages received.   |
   +---------------------+---------------------------------------------+
   | next_lsn            | In replication environments configured as   |
   |                     | masters, the next LSN expected. In          |
   |                     | replication environments configured as      |
   |                     | clients, the next LSN to be used.           |
   +---------------------+---------------------------------------------+
   | next_pg             | The next page number we expect to receive.  |
   +---------------------+---------------------------------------------+
   | nsites              | The number of sites used in the last        |
   |                     | election.                                   |
   +---------------------+---------------------------------------------+
   | nthrottles          | Transmission limited. This indicates the    |
   |                     | number of times that data transmission was  |
   |                     | stopped to limit the amount of data sent in |
   |                     | response to a single call to                |
   |                     | DB_ENV->rep_process_message.                |
   +---------------------+---------------------------------------------+
   | outdated            | The number of outdated conditions detected. |
   +---------------------+---------------------------------------------+
   | pg_duplicated       | The number of duplicate pages received.     |
   +---------------------+---------------------------------------------+
   | pg_records          | The number of pages received and stored.    |
   +---------------------+---------------------------------------------+
   | pg_requested        | The number of pages missed and requested    |
   |                     | from the master.                            |
   +---------------------+---------------------------------------------+
   | startsync_delayed   | The number of times the client had to delay |
   |                     | the start of a cache flush operation        |
   |                     | (initiated by the master for an impending   |
   |                     | checkpoint) because it was missing some     |
   |                     | previous log record(s).                     |
   +---------------------+---------------------------------------------+
   | startup_complete    | The client site has completed its startup   |
   |                     | procedures and is now handling live records |
   |                     | from the master.                            |
   +---------------------+---------------------------------------------+
   | status              |The current replication mode. Set to         |
   |                     | DB_REP_MASTER if the environment is a       |
   |                     | replication master, DB_REP_CLIENT if the    |
   |                     | environment is a replication client, or 0   |
   |                     | if replication is not configured.           |
   +---------------------+---------------------------------------------+
   | txns_applied        | The number of transactions applied.         |
   +---------------------+---------------------------------------------+
   | waiting_lsn         | The LSN of the first log record we have     |
   |                     | after missing log records being waited for, |
   |                     | or 0 if no log records are currently        |
   |                     | missing.                                    |
   +---------------------+---------------------------------------------+
   | waiting_pg          | The page number of the first page we have   |
   |                     | after missing pages being waited for, or 0  |
   |                     | if no pages are currently missing.          |
   +---------------------+---------------------------------------------+

   :OracleAPIC:`More info... <repstat.html>`

.. function:: rep_stat_print(flags=0)

   Displays the replication subsystem statistical information.
   :OracleAPIC:`More info... <repstat_print.html>`

