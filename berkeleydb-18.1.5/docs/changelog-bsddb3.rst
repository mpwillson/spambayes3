Changelog of legacy "bsddb3" project
====================================

6.2.9 - 2020-11-26:
-------------------
  * For some reason, 6.2.8 release was incomplete. Let's try again.

6.2.8 - 2020-11-20:
-------------------
  * In Python 3.9, "find_unused_port" has been moved to
    "test.support.socket_helper". Reported by Michał Górny.
  * If we use "set_get_returns_none()" in the environment,
    the value could not be correctly inherited by the child
    databases. Reported by Patrick Laimbock and modern GCC
    warnings.
  * If you install this library under Python 3 >= 3.6, let
    you know this is a legacy library and urgess you to
    migrate to "berkeleydb" library.

6.2.7:
------
  * Update copyright notices.
  * https links.
  * Fix Python 3 deprecation warning.
    Notified by Arthur Gautier.
  * Fix compilation Python 3.8 deprecation warnings.
  * Fix compilation Python 3.9 deprecation warnings.
  * Python 3.8 and 3.9 are explicitly supported.

6.2.6:
------
  * Correctly detect Berkeley DB when installed via Homebrew on Mac OS X.
    Patch by Matthew Peveler.
  * Python 3.6 and 3.7 are explicitly supported.

6.2.5:
------
  * We should be able to install inside a PYPY virtualenv.
    Reported by Zhihao Yuan.

6.2.4:
------
  * More complete fix for pkgsrc.

6.2.3:
------
  * Update copyright notices.
  * Solve a conflict between different installations of Berkeley DB
    on some pkgsrc configurations.

6.2.2:
------
  * Correctly detect Berkeley DB installations in SmartOS native zones.
  * "Probably" (not tested) correctly detect Berkeley DB in pkgsrc systems.

6.2.1:
------
  * Correctly detect Berkeley DB installations in modern 64 bits Debians.

6.2.0:
------
  * Support Berkeley DB 6.2.x.
  * Declare Python 3.5 support for PyPI.
  * Drop support for Python 3.2. If you need
    compatibility with that version, you can keep using
    old releases of these bindings.
  * Drop support for Berkeley DB 5.0, 5.2 and 6.0. If you need
    compatibility with those versions, you can keep using old
    releases of these bindings.

6.1.1:
------
  * Compatibility with Python 3.5.
  * Code cleanup after dropping Python 2.4/2.5 support.
  * PGP key changed.
  * Support for DB_FORCESYNCENV flag in "DB_ENV.close()".
  * Support for DB_LOG_NOSYNC flag in "DB_ENV.log_set_config()".
  * Fix tests under Windows. See https://bugs.python.org/issue22943 .
  * Solve an incorrect parameter verification with the
    "DB.compact()" method call.
  * Solve a compilation warning when compiling the bindings for
    Python 3.5 and Berkeley DB 4.8, 5.0 or 5.1.

6.1.0:
------
  * Support Berkeley DB 6.1.x.
  * Solve a ResourceWarning when compiling.
  * Drop support for Python 2.4, 2.5 and 3.1. If you need
    compatibility with those versions, you can keep using old
    releases of these bindings.
  * Drop support for Berkeley DB 4.3, 4.4, 4.5, 4.6. If you need
    compatibility with those versions, you can keep using old
    releases of these bindings.
  * From now on, our support reference is Red Hat Enterprise Linux 6.
  * Drop modules attributes "cvsid".
  * Drop (hidden) $Id: changelog-bsddb3.rst,v 2a174b277731 2020/12/11 01:35:38 jcea $ keyword in the documentation.

6.0.1:
------
  * Clarification of license. Thanks to
    Jan Staněk <jstanek@redhat.com> for bringing this issue up.
    This work is now explicitly licensed under 3-clause BSD license.
  * Fixed a long standing bug (August 2008, rev 9fd52748fa59)
    on "dbtables.py". Notified by Maxime Labelle.
  * If you want to link with Oracle Berkeley DB 6.0, you will
    need to create the environment variable
    'YES_I_HAVE_THE_RIGHT_TO_USE_THIS_BERKELEY_DB_VERSION'
    to signal to the pybsddb that you are legal. To be legal,
    your code MUST be AGPL3 *OR* you have to buy a commercial
    license from Oracle.

    If you are not legally entitled to use Berkeley DB 6.0 and
    you have previous versions of Berkeley DB on your system,
    you can a) delete Berkeley DB 6.0 and try again, OR
    b) instruct pybsddb to use a previous Berkeley DB version,
    using environment variables or command line options.

    Sorry for the inconvenience. I am trying to protect you.

    Some details:

        https://forums.oracle.com/message/11184885
        http://lists.debian.org/debian-legal/2013/07/

6.0.0:
------
  * Support Berkeley DB 6.0.x.
  * HEADS UP: If you are using "bsddb3._bsddb" in your code,
    for example for exceptions, change it to "bsddb3._db".
  * Print test working directory when running the testsuite.
    You can control it using "TMPDIR" environment variable.
    Defaults to "/tmp/z-Berkeley_DB/".
  * Support for "DB_EVENT_REP_AUTOTAKEOVER_FAILED" event.
  * Support for "DB_REPMGR_ISVIEW", "DB_DBT_BLOB", "DB_LOG_BLOB",
    "DB_STREAM_READ", "DB_STREAM_WRITE" and "DB_STREAM_SYNC_WRITE" flags.
  * Some DB_SEQUENCE function signatures changed in Berkeley DB 6.0.x.
  * Erratic behaviour of "DBEnv->rep_elect()" because a typo.
  * The testsuite prints Python bitness (32/64).
  * Tests compatible with hash randomization, default
    in Python 3.3. See http://bugs.python.org/issue13703 .
  * Errors when trying to calculate the length of a DB were
    masked, and an unuseful and unrelated exception was raised.
  * Code cleanup since pybsddb is not in the Python 3.x stdlib
    anymore, and the version in Python 2.6/2.7 is being
    maintained separately.
  * Improvements to documentation generation.

5.3.0:
------
  * Support Berkeley DB 5.3.x.
  * Drop support for Berkeley DB 4.2 and Python 2.3. Our reference
    is Red Hat Enterprise Linux 5, until march 2014.
    After that, RHEL6 has Python 2.6 and BDB 4.7.
    * According to http://superuser.com/questions/189931/python-and-berkeley-db-versions-in-redhat-enterprise-linux-3-4-5-and-upcoming-6 :

      * RHEL3: Python 2.2.3, BDB 4.1.25
      * RHEL4: Python 2.3.4, BDB 4.2.52
      * RHEL5: Python 2.4.3, BDB 4.3.29
      * RHEL6: Python 2.6.2, BDB 4.7.25

  * Support for "DBEnv->set_intermediate_dir()", available in
    Berkeley DB 4.3-4.6.  Patch by Garret Cooper.
  * Support for "DB->set_dup_compare()".  Original patches by
    Nikita M. Kozlovsky and Ben Schmeckpeper.
  * Fixed a testsuite compatibility problem with BDB 5.2.
  * If we are running Solaris or derivatives, and 64bit python,
    try to find the library under "/usr/local/Berkeley.*.*/64/".
  * Solaris 10 Update 10 exposes a very old race condition in the replication
    master election tests. Some details in
    https://forums.oracle.com/forums/thread.jspa?messageID=9902860 .
    Workaround proposed in a private email from Paula Bingham (Oracle),
    in 20110929.
  * When doing the full matrix test for a release, stop the verification
    if any test failed.

5.2.0:
------
  * Support for Berkeley DB 5.2.
  * Support for the newly available replication manager events:
    DB_EVENT_REP_SITE_ADDED, DB_EVENT_REP_SITE_REMOVED,
    DB_EVENT_REP_LOCAL_SITE_REMOVED, DB_EVENT_REP_CONNECT_BROKEN,
    DB_EVENT_REP_CONNECT_ESTD, DB_EVENT_REP_CONNECT_TRY_FAILED,
    DB_EVENT_REP_INIT_DONE.
  * New Object: "DB_SITE". Support for all its methods.
  * Parameters for "DB_SITE->set_config()": DB_BOOTSTRAP_HELPER,
    DB_GROUP_CREATOR, DB_LEGACY, DB_LOCAL_SITE, DB_REPMGR_PEER.
  * Support for some stuff in the new "Dynamic Environment Configuration":
    DB_MEM_LOCK, DB_MEM_LOCKOBJECT, DB_MEM_LOCKER, DB_MEM_LOGID,
    DB_MEM_TRANSACTION, DB_MEM_THREAD.
  * Add "bytes" to "DBEnv_memp_stat()". Original patch from Garrett Cooper.

5.1.2:
------
  * 5.1.1 install fails if the bsddb in the standard library is not installed,
    under Python 2.7. Reported by Arfrever Frehtes Taifersar Arahesis.
  * Since 5.0.0, we can't find 4.x libraries unless we specify a
    "--berkeley-db=/path/to/bsddb" option. Reported by Wen Heping.
  * Support "DB_ENV->get_open_flags()", "DB_ENV->set_intermediate_dir_mode()",
    "DB_ENV->get_intermediate_dir_mode()".
  * Support "DB->get_dbname()", "DB->get_open_flags()".
  * Support "db_full_version()".
  * Document "version()". This top-level function has been supported forever.
  * Bugfix when calling "DB->get_size()" on a zero length record.
    Reported by Austin Bingham.
  * 'assertEquals()' is deprecated in Python 3.2.
  * 'assert_()' is deprecated in Python 3.2.
  * Solved 'ResourceWarning' under Python 3.2.

5.1.1:
------
  * Recent pre-releases of Python 3.2 issue ResourceWarnings about
    fileshandles deallocated without being closed first. Fix testsuite.
  * Current "*.pyc" and "*.pyo" cleaning is not working in a PEP 3147
    world ("__pycache__"). I don't think this code is actually
    necessary anymore. Deleted.
  * Python 2.7.0 deprecates CObject incorrectly. See Python issue #9675.
  * Testsuite for "DB->get_transactional()" should not create databases
    outside the TMP directory, neither leave the files behind.
  * If something happens while creating the CObject/Capsule object,
    keep going, even without exporting the C API, instead of crashing.
  * Support for "DB_FORCESYNC", "DB_FAILCHK", "DB_SET_REG_TIMEOUT",
    "DB_TXN_BULK", "DB_HOTBACKUP_IN_PROGRESS".
  * Support "DB_EVENT_REG_ALIVE", "DB_EVENT_REG_PANIC",
    "DB_EVENT_REP_DUPMASTER", "DB_REPMGR_CONF_ELECTIONS",
    "DB_EVENT_REP_ELECTION_FAILED", "DB_EVENT_REP_MASTER_FAILURE".
  * Support for "DB_VERB_REP_ELECT", "DB_VERB_REP_LEASE", "DB_VERB_REP_MISC",
    "DB_VERB_REP_MSGS", "DB_VERB_REP_SYNC", "DB_VERB_REP_SYSTEM",
    "DB_VERB_REPMGR_CONNFAIL", "DB_VERB_REPMGR_MISC".
  * Support for "DB_STAT_LOCK_CONF", "DB_STAT_LOCK_LOCKERS",
    "DB_STAT_LOCK_OBJECTS", "DB_STAT_LOCK_PARAMS".
  * Support for "DB_REP_CONF_INMEM".
  * Support for "DB_TIMEOUT ".
  * Support for "DB_CURSOR_BULK".

5.1.0:
------
  * Support for Berkeley DB 5.1.
  * Drop support for Berkeley DB 4.1. Our reference
    is Red Hat Enterprise Linux 4, until February 2012.
    After that, RHEL5 has Python 2.4 and BDB 4.3.
    * According to http://superuser.com/questions/189931/python-and-berkeley-db-versions-in-redhat-enterprise-linux-3-4-5-and-upcoming-6 :

      * RHEL3: Python 2.2.3, BDB 4.1.25
      * RHEL4: Python 2.3.4, BDB 4.2.52
      * RHEL5: Python 2.4.3, BDB 4.3.29
      * RHEL6: Python 2.6.2, BDB 4.7.25 (Currently in BETA)

  * Include documentation source (\*.rst) in the EGG.
  * Include processed HTML documentation in the EGG.
  * Update the external links in documentation, since Oracle changed its web
    structure.
  * Some link fixes for external documentation.
  * Links added in the documentation to Oracle Berkeley DB programmer
    reference.
  * Support for "DB->get_transactional()".
  * Support for "DB_REPMGR_ACKS_ALL_AVAILABLE".

5.0.0:
------
  * Support for Berkeley DB 5.0.
  * Drop support for Python 3.0.
  * Now you can use TMPDIR env variable to override default
    test directory ("/tmp").
  * Versioning of C API. If you use the code from C, please
    check the bsddb_api->api_version number against
    PYBSDDB_API_VERSION macro.
  * In C code, the bsddb_api->dbsequence_type component is always available,
    even if the Berkeley DB version used doesn't support sequences. In that
    case, the component will be NULL.
  * In C code, "DBSequenceObject_Check()" macro always exists, even if the
    Berkeley DB version used doesn't suport sequences. In that case, the test
    macro always returns "false".
  * For a long time, the API has been accesible via C using "_bsddb.api" or
    "_pybsddb.api". If you are using Python >=2.7, you acquire access to that
    API via the new Capsule protocol (see "bsddb.h").  If you use the C API and
    upgrade to Python 2.7 and up, you must update the access code (see
    "bsddb.h"). The Capsule protocol is not supported in Python 3.0, but
    pybsddb 5.0.x doesn't support Python 3.0 anymore.
  * Capsule support was buggy. The string passed in to PyCapsule_New() must
    outlive the capsule.  (Larry Hastings)
  * Solve an "Overflow" warning in the testsuite running under python 2.3.
  * When doing a complete full-matrix test, any warning will be considered
    an error.

4.8.4:
------
  * When doing the full matrix testing with python >=2.6, we
    activate the deprecation warnings (py3k).
  * Split dependencies in the Replication testsuite.
  * Help the Gargabe Collection freeing resources when the
    replication testsuite is completed.
  * Import warning when used as stdlib "bsddb" instead of
    pybsddb project as "bsddb3", when using python >=2.6 and
    py3k warnings are active.
  * Old regression: dbshelve objects are iterable again. The bug was
    introduced in pybsddb 4.7.2. Added relevant testcases.
  * Patches ported from Python developers:

    * Memory leaks: #7808 - http://bugs.python.org/issue7808 - Florent Xicluna
    * Floating point rounding in testcases:
      #5073 - http://bugs.python.org/issue5073 - Mark Dickinson
    * Orthograpy: #5341 - http://bugs.python.org/issue5341
    * Py3k warnings in Python >=2.6: #7092 - http://bugs.python.org/issue7092
    * Correct path for tests:
      #7269 - http://bugs.python.org/issue7269 - Florent Xicluna
    * Shebang: benjamin.peterson
    * Use new Python 2.7 assert()'s: Florent Xicluna

  * Solve a spurious stdlib warning in python >=2.6 with -3 flags.
  * Remove "DBIncompleteError", for sure this time. There were traces
    in "dbtables", in some tests and in the docs.
  * The DBKeyEmptyError exception raised by the library is not the same
    DBKeyEmptyError available in the lib. So the raised exception was
    uncatchable unless you catch DBError. And you can not identify it.
  * Solved last point, document that DBKeyEmptyError exception derives also
    from KeyError, just like DBNotFoundError exception.
  * Update documentation to describe all exceptions provided by this module.

4.8.3:
------
  * "bsddb.h" inclusion in PYPI is inconsistent. Solved.
  * Support for "DB_ENV->mutex_stat()", "DB_ENV->mutex_stat_print()",
    "DB->stat_print()", "DB_ENV->lock_stat_print()",
    "DB_ENV->log_stat_print()", "DB_ENV->stat_print()",
    "DB_ENV->memp_stat()" and "DB_ENV->memp_stat_print()".
  * Support for "DB_ENV->get_tmp_dir()".
  * Support for "DB_STAT_SUBSYSTEM", "DB_STAT_MEMP_HASH" flags.
  * Support for "DB_ENV->set_mp_max_openfd()", "DB_ENV->get_mp_max_openfd()",
    "DB_ENV->set_mp_max_write()", "DB_ENV->get_mp_max_write()",
    "DB_ENV->get_mp_mmapsize()".
  * New DataType: DBLogCursor. If you are using the C api, you could need
    to recompile your code because the changes in the api interface
    structure.
  * Support for "DB_ENV->log_file()", "DB_ENV->log_printf()".
  * Solve a core dump if something bad happens while trying to create a
    transaction object.
  * We protect ourselves of failures in creation of Locks and Sequences
    objects.
  * EGG file is a ZIP file again, not a directory. This requires that
    any program importing the module can write in the ".python-eggs"
    of its user.
  * Keeping a cached copy of the database stats is a bad idea if we have
    several processes working together. We drop all this code. So "len()"
    will require a database scanning always, not only when there is any
    write. If you need an accurate and fast "len()", the application must
    keep that information manually in a database register.

4.8.2:
------
  * Support for "DB_OVERWRITE_DUP", "DB_FOREIGN_ABORT",
    "DB_FOREIGN_CASCADE", "DB_FOREIGN_NULLIFY", "DB_PRINTABLE", "DB_INORDER"
    flags.
  * Support for "DB_FOREIGN_CONFLICT" exception.
  * Support for "DB_ENV->memp_trickle()", "DB_ENV->memp_sync()",
    "DB_ENV->get_lg_bsize()", "DB_ENV->get_lg_dir()",
    "DB_ENV->get_lg_filemode()", "DB_ENV->set_lg_filemode()",
    "DB_ENV->get_lk_detect()", "DB_ENV->get_lg_regionmax()",
    "DB_ENV->get_lk_max_lockers()", "DB_ENV->set_lk_max_locks()",
    "DB_ENV->get_lk_max_objects()", "DB_ENV->set_lk_partitions()",
    "DB_ENV->get_lk_partitions()", "DB_ENV->get_flags()",
    "DB_ENV->set_cache_max()", "DB_ENV->get_cache_max()",
    "DB_ENV->set_thread_count()", "DB_ENV->get_thread_count()",
    "DB_ENV->log_set_config()", "DB_ENV->log_get_config()"
    functions.
  * Support for "DB->get_h_ffactor()", "DB->set_h_nelem()",
    "DB->get_h_nelem()", "DB->get_lorder()", "DB->get_pagesize()",
    "DB->get_re_pad()", "DB->get_re_len()", "DB->get_re_delim()",
    "DB->get_flags()", "DB->get_bt_minkey()",
    "DB->set_priority()", "DB->get_priority()",
    "DB->set_q_extentsize()", "DB->get_q_extentsize()",
    "DB->set_re_source()", "DB->get_re_source()"
    functions.
  * Unlock the Python GIL when doing "DB_ENV->db_home_get()". This is
    slower, because the function is very fast so we add overhead, but it is
    called very infrequently and we do the change for consistency.

4.8.1:
------
  * Support for "DB_ENV->mutex_set_align()" and
    "DB_ENV->mutex_get_align()".
  * Support for "DB_ENV->mutex_set_increment()" and
    "DB_ENV->mutex_get_increment()".
  * Support for "DB_ENV->mutex_set_tas_spins()" and
    "DB_ENV->mutex_get_tas_spins()".
  * Support for "DB_ENV->get_encrypt_flags()".
  * Support for "DB->get_encrypt_flags()".
  * Support for "DB_ENV->get_shm_key()".
  * Support for "DB_ENV->get_cachesize()".
  * Support for "DB->get_cachesize()".
  * Support for "DB_ENV->get_data_dirs()".
  * Testsuite compatibility with recent releases of
    Python 3.0 and 3.1, where cPickle has been removed.
  * Compatibility with development versions of
    Python 2.7 and 3.2 (r76123).
  * For a long time, the API has been accesible via C
    using "_bsddb.api" or "_pybsddb.api". If you are
    using Python 3.2 or up, you acquire access to
    that API via the new Capsule protocol (see "bsddb.h").
    If you use the C API and upgrade to Python 3.2 and up,
    you must update the access code (see "bsddb.h").

4.8.0:
------
  * Support for Berkeley DB 4.8.
  * Compatibility with Python 3.1.
  * The "DB_XIDDATASIZE" constant has been renamed
    to "DB_GID_SIZE". Update your code!. If linked
    to BDB 4.8, only "DB_GID_SIZE" is defined.
    If linked to previous BDB versions, we keep
    "DB_XIDDATASIZE" but define "DB_GID_SIZE" too,
    to be the same value. So, new code can use
    the updated constant when used against old
    BDB releases.
  * "DB_XA_CREATE" is removed. BDB 4.8 has eliminated
    XA Resource Manager support.
  * Drop support for Berkeley DB 4.0. Our reference
    is Red Hat Enterprise Linux 3, until October 2010.
    After that, RHEL4 has Python 2.3 and BDB 4.2.
  * Remove "DBIncompleteError" exception. It was only
    used in BDB 4.0.
  * Remove "DB_INCOMPLETE", "DB_CHECKPOINT",
    "DB_CURLSN". They came from BDB 4.0 too.
  * RPC is dropped in Berkeley DB 4.8. The bindings
    still keep the API if you link to previous BDB
    releases.
  * In recno/queue databases, "set_re_delim()" and "set_re_pad()"
    require a byte instead of a unicode char, under Python3.
  * Support for "DB_ENV->mutex_set_max()" and "DB_ENV->mutex_get_max()".

4.7.6:
------
  * Compatibility with Python 3.0.1.
  * Add support for "DB_ENV->stat()" and "DB_ENV->stat_print()".
  * Add support for "DB_ENV->rep_set_clockskew()" and
    "DB_ENV->rep_get_clockskew()". The binding support
    for base replication is now complete.
  * "DB.has_key()" used to return 0 or 1. Changed to return
    True or False instead. Check your code!.
  * As requested by several users, implement "DB.__contains__()",
    to allow constructions like "if key in DB" without
    iterating over the entire database. But, BEWARE, this
    test is not protected by transactions!. This is the same
    problem we already have with "DB.has_key()".
  * Change "DBSequence.init_value()" to "DBSequence.initial_value()",
    for consistence with Berkeley DB real method name. This could
    require minimal changes in your code. The documentation was
    right. Noted by "anan".
  * Implements "DBCursor->prev_dup()".
  * Add support for "DB_GET_BOTH_RANGE", "DB_PREV_DUP",
    and "DB_IGNORE_LEASE" flags.
  * Export exception "DBRepLeaseExpiredError".
  * Add support for "DB_PRIORITY_VERY_LOW", "DB_PRIORITY_LOW",
    "DB_PRIORITY_DEFAULT", "DB_PRIORITY_HIGH",
    "DB_PRIORITY_VERY_HIGH", and "DB_PRIORITY_UNCHANGED" flags.
  * Add support for "DBCursor->set_priority()" and
    "DBCursor->get_priority()". The binding support for cursors
    is now complete.

4.7.5:
------
  * Add support for "DB_EID_INVALID" and "DB_EID_BROADCAST" flags.
  * Add support for "DB_SEQUENCE->stat_print()". The binding
    support for "DB_SEQUENCE" is now complete.
  * Add support for "DB_ENV->txn_stat_print()".
  * Add support for "DB_ENV->get_timeout()".
  * Document that "DB_ENV->txn_stat()" accepts a flag.
  * Unlock the GIL when doing "DB_ENV->set_tx_max()" and
    "DB_ENV->set_tx_timestamp()".
  * Add support for "DB_ENV->get_tx_max()".
  * Add support for "DB_ENV->get_tx_timestamp()".
  * Add support for "DB_TXN_WAIT" flag.
  * Add support for "DB_TXN->set_timeout()".
  * Add support for "DB_TXN->set_name()" and
    "DB_TXN->get_name()". Under Python 3.0, the name
    is an Unicode string. The binding support for
    "DB_TXN" is now complete.
  * Add support for "DB_REP_PERMANENT", "DB_REP_CONF_NOAUTOINIT",
    "DB_REP_CONF_DELAYCLIENT", "DB_REP_CONF_BULK",
    "DB_REP_CONF_NOWAIT", "DB_REP_LEASE_EXPIRED",
    "DB_REP_CONF_LEASE", "DB_REPMGR_CONF_2SITE_STRICT",
    "DB_REP_ANYWHERE", "DB_REP_NOBUFFER" and "DB_REP_REREQUEST"
    flags.

4.7.4:
------
  * Under Python 3.0, "bsddb.db.DB_VERSION_STRING",
    "bsddb.db.__version__" and "bsddb.db.cvsid" must
    return (unicode) strings instead of bytes. Solved.
  * Use the new (20081018) trove classifiers in PyPI
    to identify Python supported versions.
  * In "DB_ENV->rep_set_timeout()" and "DB_ENV->rep_get_timeout()",
    support flags "DB_REP_LEASE_TIMEOUT".
  * In "DB_ENV->rep_set_timeout()" and "DB_ENV->rep_get_timeout()",
    support flags "DB_REP_HEARTBEAT_MONITOR" and
    "DB_REP_HEARTBEAT_SEND". These flags are used in the Replication
    Manager framework, ignored if using Base Replication.
  * Implements "DB->exists()".
  * Add support for "DB_IMMUTABLE_KEY" flag.
  * Add support for "DB_REP_LOCKOUT" exception.
  * Support returning a list of strings in "associate()"
    callback.  (Kung Phu)
  * Testsuite and Python 3.0 compatibility for "associate()"
    returning a list. In particular, in Python 3.0 the list
    must contain bytes.
  * Implements "DBEnv->fileid_reset()".  (Duncan Findlay)
  * Implements "DB->compact()".  (Gregory P. Smith)
    Berkeley DB 4.6 implementation is buggy, so we only
    support this function from Berkeley DB 4.7 and newer.
    We also support related flags "DB_FREELIST_ONLY"
    and "DB_FREE_SPACE".

4.7.3: (Python 2.6 release. First release with Python 3.0 support)
------------------------------------------------------------------
  * "private" is a keyword in C++.  (Duncan Grisby)
  * setup.py should install "bsddb.h".  (Duncan Grisby)
  * "DB_remove" memory corruption & crash.  (Duncan Grisby)
  * Under Python 3.0, you can't use string keys/values, but
    bytes ones. Print the right error message.
  * "DB.has_key()" allowed transactions as a positional parameter.
    We allow, now, transactions as a keyword parameter also, as
    documented.
  * Correct "DB.associate()" parameter order in the documentation.
  * "DB.append()" recognizes "txn" both as a positional and a
    keyword parameter.
  * Small fix in "dbshelve" for compatibility with Python 3.0.
  * A lot of changes in "dbtables" for compatibility with Python 3.0.
  * Huge work making the testsuite compatible with Python 3.0.
  * In some cases the C module returned Unicode strings under
    Python 3.0. It should return "bytes", ALWAYS. Solved.
  * Remove a dict.has_key() use to silence a warning raised under
    Python2.6 -3 parameter. Python SVN r65391, Brett Cannon.
  * Solve some memory leaks - Neal Norwitz
  * If DBEnv creation fails, library can crash.  (Victor Stinner)
  * Raising exceptions while doing a garbage collection
    will kill the interpreter.  (Victor Stinner)
  * Crash in "DB.verify()". Noted by solsTiCe d'Hiver.

4.7.2:
------
  * Solved a race condition in Replication Manager testcode.
  * Changing any python code, automatically regenerates the
    Python3 version. The master version is Python2.
  * Compatibility with Python 3.0.
  * Solved a crash when DB handle creation fails.
    STINNER Victor - http://bugs.python.org/issue3307
  * Improve internal error checking, as suggested by Neal Norwitz
    when reviewing commit 63207 in Python SVN.
  * Routines without parameters should be defined so, as
    suggested by Neal Norwitz when reviewing commit 63207 in Python SVN.
    The resulting code is (marginally) faster, smaller and clearer.
  * Routines with a simple object parameter are defines so, as
    suggested by Neal Norwitz when reviewing commit 63207 in Python SVN.
    The resulting code is (marginally) faster, smaller and clearer.
  * Routines taking objects as arguments can parse them better, as
    suggested by Neal Norwitz when reviewing commit 63207 in Python SVN.
    The resulting code is (marginally) faster, smaller and clearer.
  * Improve testsuite behaviour under MS Windows.
  * Use ABC (Abstract Base Classes) under Python 2.6 and 3.0.
  * Support for "relative imports".
  * Replication testcode behaves better in heavily loaded machines.

4.7.1:
------
  * Workaround a problem with un-initialized threads with the
    replication callback.
  * Export "DBRepUnavailError" exception.
  * Get rid of Berkeley DB 3.3 support. Rationale:
    http://mailman.jcea.es/pipermail/pybsddb/2008-March/000019.html
  * Better integration between Python test framework and bsddb3.
  * Improved Python 3.0 support in the C code.
  * Iteration over the database, using the legacy interface, now
    raises a RuntimeError if the database changes while iterating.
    http://bugs.python.org/issue2669 - gregory.p.smith
  * Create "set_private()" and "get_private()" methods for DB and DBEnv
    objects, to allow applications to link an arbitrary object to
    a DB/DBEnv. Useful for callbacks.
  * Support some more base replication calls: "DB_ENV->rep_start",
    "DB_ENV->rep_sync", "DB_ENV->rep_set_config", "DB_ENV->rep_get_config",
    "DB_ENV->rep_set_limit", "DB_ENV->rep_get_limit",
    "DB_ENV->rep_set_request", "DB_ENV->rep_get_request".
  * Support more base replication calls:  "DB_ENV->rep_elect",
    "DB_ENV->rep_set_transport" and "DB_ENV->rep_process_message".
    Support also related flags.

4.7.0:
------
  * Support for Berkeley DB 4.7.
  * Support "DB_ENV->log_set_config", and related flags.
  * Complete the Berkeley DB Replication Manager support:
    "DB_ENV->repmgr_site_list" and related flags.
    "DB_ENV->repmgr_stat", "DB_ENV->repmgr_stat_print" and related flags.
  * Solved an old crash when building with debug python. (Neal Norwitz)
  * Extend the testsuite driver to check also against Python 2.6 (a3).
  * Support for RPC client service.

4.6.4:
------
  * Basic support for Berkeley DB Replication Manager.
  * Support for a few replication calls, for benefice of Berkeley DB
    Replication Manager: "DB_ENV->rep_set_priority",
    "DB_ENV->rep_get_priority", "DB_ENV->rep_set_nsites",
    "DB_ENV->rep_get_nsites", "DB_ENV->rep_set_timeout",
    "DB_ENV->rep_get_timeout".
  * Implemented "DB_ENV->set_event_notify" and related flags.
  * Export flags related to replication timeouts.
  * Export "DBRepHandleDeadError" exception.
  * Implemented "DB_ENV->set_verbose", "DB_ENV->get_verbose"
    and related flags.
  * Implemented "DB_ENV->get_lg_max".
  * Improved performance and coverage of following tests: lock,
    threaded ConcurrentDataStore, threaded simple locks, threaded
    transactions.
  * New exported flags: "DB_LOCK_EXPIRE" and "DB_LOCK_MAXWRITE".

4.6.3:
------
  * Be sure all DBEnv/DB paths in the TestSuite are generated in a
    way compatible with launching the tests in multiple
    threads/processes.
  * Move all the "assert" in the TestSuite to the version in the
    framework. This is very convenient, for example, to generate the
    final report, or better automation.
  * Implements "dbenv.log_flush()".
  * Regression: bug when creating a transaction and its
    parent is explicitly set to 'None'.
  * Regression: bug when duplicationg cursors. Solved.
  * Provide "dbenv.txn_recover()" and "txn.discard()", for fully
    support recovery of distributed transactions. Any user of this
    service should use Berkeley DB 4.5 or up.
  * If a transaction is in "prepare" or "recover" state, we MUST NOT
    abort it implicitly if the transaction goes out of scope, it is
    garbaged collected, etc. Better to leak than sorry.
  * In the previous case, we don't show any warning either.
  * Export "DB_XIDDATASIZE", for GID of distributed transactions.
  * If "db_seq_t" and PY_LONG_LONG are not compatible, compiler
    should show a warning while compiling, and the generated code
    would be incorrect but safe to use. No crash. Added sanity
    check in the testunit to verify this is not the case, and
    the datatypes are 64 bit width in fact.
  * Solve a compilation warning when including "bsddb.h"
    in other projects. (George Feinberg)

4.6.2:
------
  * Support for MVCC (MultiVersion Concurrency Control).
  * Support for DB_DSYNC_LOG, DB_DSYNC_DB and DB_OVERWRITE flags.
  * Move old documentation to ReST format. This is important for several
    reasons, notably to be able to integrate the documentation "as is"
    in python official docs (from Python 2.6).
  * Don't include Berkeley DB documentation. Link to the online version.
  * DBSequence objects documented.
  * DBSequence.get_key() didn't check for parameters. Fixed.
  * If a DB is closed, its children DBSequences will be
    closed also.
  * To be consistent with other close methods, you can call
    "DBSequence.close()" several times without error.
  * If a Sequence is opened inside a transaction, it will be
    automatically closed if the transaction is aborted. If the
    transaction is committed and it is actually a subtransaction, the
    sequence will be inherited by the parent transaction.
  * Be sure "db_seq_t" and "long long" are compatible. **Disabled because
    MS Windows issues to be investigated.**
  * Documented the already available DBEnv methods: "dbremove",
    "dbrename", "set_encrypt", "set_timeout", "set_shm_key",
    "lock_id_free", "set_tx_timestamp", "lsn_reset" and "log_stat".
  * Completed and documented "DBEnv.txn_stat()".
  * Completed and documented "DBEnv.lock_stat()".
  * Documented the already available DB methods: "set_encrypt", "pget".
  * Completed documentation of DB methods: "associate", "open".
  * Completed and documented "DB.stat()".
  * Documented the already available DBCursor methods: "pget" (several
    flavours).
  * Completed documentation of DBCursor methods: "consume", "join_item".

4.6.1: (first release from Jesús Cea Avión)
-------------------------------------------
  * 'egg' (setuptools) support.
  * Environments, database handles and cursors are
    maintained in a logical tree. Closing any element
    of the tree, implicitly closes its children.
  * Transactions are managed in a logical tree. When
    aborting transactions, enclosed db handles, cursors
    and transactions, are closed. If transaction commits,
    the enclosed db handles are "inherited" by the parent
    transaction/environment.
  * Solved a bug when a DBEnv goes out of scope
    without closing first.
  * Add transactions to the management of closing
    of nested objects. (not completed yet!)
  * Fix memory leaks.
  * Previous versions were inconsistent when key or
    value were "" (the null string), according to
    opening the database in thread safe mode or not.
    In one case the lib gives "" and in the other
    it gives None.

4.6.0:
------

  * Adds support for compiling and linking with BerkeleyDB 4.6.21.
  * Fixes a double free bug with DBCursor.get and friends.  Based on
    submitted pybsddb patch #1708868. (jjjhhhll)
  * Adds a basic C API to the module so that other extensions or
    third party modules can access types directly. Based on pybsddb
    patch #1551895. (Duncan Grisby)
  * bsddb.dbshelve now uses the most recent cPickle protocol, based on
    pybsddb patch #1551443. (w_barnes)
  * Fix the bsddb.dbshelve.DBShelf append method to work for RECNO dbs.
  * Fix Bug #477182 - Load the database flags at database open time
    so that opening a database previously created with the DB_DUP or
    DB_DUPSORT flag set will keep the proper behavior on subsequent opens.
    Specifically dictionary assignment to a DB object.  It will now replace
    all values for a given key when the database allows duplicate values.
    DB users should use DB.put(k, v) when they want to store duplicates; not
    DB[k] = v.  This only works with BerkeleyDB >= 4.2.
  * Add the DBEnv.lock_id_free method.
  * Removes any remnants of support for Python older than 2.1.
  * Removes any remnants of support for BerkeleyDB 3.2.

4.5.0:
------

  * Adds supports for compiling and linking with BerkeleyDB 4.5
  * Python Bug #1599782: Fix segfault on bsddb.db.DB().type() due to
    releasing the GIL when it shouldn't.  (nnorowitz)
  * Fixes a bug with bsddb.DB.stat where the flags and txn keyword
    arguments are transposed.
  * change test cases to use tempfile.gettempdir()

4.4.5:
------

  * pybsddb Bug #1527939: bsddb module DBEnv dbremove and dbrename
    methods now allow their database parameter to be None as the
    sleepycat API allows.

4.4.4:
------

  * fix DBCursor.pget() bug with keyword argument names when no data= is
    supplied [SF pybsddb bug #1477863]
  * add support for DBSequence objects [patch #1466734]
  * support DBEnv.log_stat() method on BerkeleyDB >= 4.0 [patch #1494885]
  * support DBEnv.lsn_reset() method on BerkeleyDB >= 4.4 [patch #1494902]
  * add DB_ARCH_REMOVE flag and fix DBEnv.log_archive() to accept it without
    potentially following an uninitialized pointer.

4.4.3:
------

  * fix DBEnv.set_tx_timestamp to not crash on Win64 platforms (thomas.wouters)
  * tons of memory leak fixes all over the code (thomas.wouters)
  * fixes ability to unpickle DBError (and children) exceptions

4.4.2:
------

  * Wrap the DBEnv.set_tx_timeout method
  * fix problem when DBEnv deleted before Txn sf bug #1413192 (Neal Norwitz)

4.4.1:
------

  * sf.net patch 1407992 - fixes associate tests on BerkeleyDB 3.3 thru 4.1
    (contributed by Neal Norwitz)

4.4.0:
------

  * Added support for compiling and linking with BerkeleyDB 4.4.20.

4.3.3:
------

 * NOTICE: set_bt_compare() callback function arguments CHANGED to only
   require two arguments (left, right) rather than (db, left, right).
 * DB.associate() would crash when a DBError occurred.  fixed.
   [pybsddb SF bug id 1215432].

4.3.2:
------

 * the has_key() method was not raising a DBError when a database error
   had occurred. [SF patch id 1212590]
 * added a wrapper for the DBEnv.set_lg_regionmax method [SF patch id 1212590]
 * DBKeyEmptyError now derives from KeyError just like DBNotFoundError.
 * internally everywhere DB_NOTFOUND was checked for has been updated
   to also check for DB_KEYEMPTY.  This fixes the semantics of a couple
   operations on recno and queue databases to be more intuitive and results
   in less unexpected DBKeyEmptyError exceptions being raised.

4.3.1:
------

 * Added support for DB.set_bt_compare() method to use a user
   supplied python comparison function taking (db, left, right)
   args as the database's B-Tree comparison function.

4.3.0:
------

 * Added support for building properly against BerkeleyDB 4.3.21.
 * fixed bug introduced in 4.2.8 that prevent the module from
   compiling against BerkeleyDB 3.2 (which doesn't support pget).
 * setup.py was cleaned up a bit to search for and find the latest
   version of the correct combo of db.h and libdb.

4.2.9:
------

 * DB keys() values() and items() methods were ignoring their optional
   txn parameter.  This would lead to deadlocks in applications
   needing those to be transaction protected.

4.2.8:
------

 * Adds support for DB and DBCursor pget methods.  Based on a patch
   submitted to the mailing list by Ian Ward <ian@arevco.ca>
 * Added weakref support to all bsddb.db objects.
 * Make DBTxn objects automatically call abort() in their destructor if
   not yet finalized and raise a RuntimeWarning to that effect.

4.2.7:
------

 * fix an error with the legacy interface relying on the DB_TRUNCATE
   flag that changed behaviour to not work in a locking environment
   with BerkeleyDB 4.2.52.  [SF bug id 897820]
 * fixed memory leaks in DB.get, DBC.set_range and potentially several
   other methods that would occur primarily when using queue | recno
   format databases with integer keys. [SF patch id 967763]

4.2.6:
------

 * the DB.has_key method was not honoring its txn parameter to perform
   its lookup within the specified (optional) transaction.  fixed.
   [SF bug id 914019]

4.2.5:
------

 * Fixed a bug in the compatibility interface set_location() method
   where it would not properly search to the next nearest key when
   used on BTree databases.  [SF bug id 788421]
 * Fixed a bug in the compatibility interface set_location() method
   where it could crash when looking up keys in a hash or recno
   format database due to an incorrect free().

4.2.4:
------

 * changed DB and DBEnv set_get_returns_none() default from 1 to 2.
 * cleaned up compatibility iterator interface.

4.2.3:
------

 * the legacy compatibility dict-like interface now support iterators
   and generators and allows multithreaded access to the database.
 * fixed a tuple memory leak when raising "object has been closed"
   exceptions for DB, DBEnv and DBCursor objects.  I doubt much
   previous code triggered this.
 * use of a closed DBCursor now raises a DBCursorClosedError exception
   subclass of DBError rather than a boring old DBError.

4.2.2:
------

 * added DBCursor.get_current_size() method to return the length in bytes
   of the value pointed to by the cursor without reading the actual data.

4.2.1:
------

 * Standalone pybsddb builds now use a _pybsddb dynamic/shared library
   rather than _bsddb.  This allows for pybsddb to be built, installed
   and used on python >= 2.3 which includes an older version of pybsddb
   as its bsddb library.

4.2.0:
------

 * Can now compile and link with BerkeleyDB 4.2.x (when its released).
 * the legacy bsddb module supports the iterator interface on python 2.3.

4.1.x:
------

 * Support the DBEnv.set_shm_key() method.
 * Fixed setup.py include/{db4,db3} header file searching (SF bug #789740).

4.1.6:
------

 * Extended DB & DBEnv set_get_returns_none functionality to take a
   "level" instead of a boolean flag.  The boolean 0 and 1 values still
   have the same effect.  A value of 2 extends the "return None instead
   of raising an exception" behaviour to the DBCursor set methods.
   This will become the default behaviour in pybsddb 4.2.
 * Updated documentation for set_get_returns_none.  Regenerated the
   stale html docs from the text documentation.
 * Fixed a typo in DBCursor.join_item method that made it crash instead
   of returning a value.  Obviously nobody uses it.  Wrote a test case
   for join and join_item.
 * Added the dbobj wrapper for DBEnv set_timeout method.
 * Updated README.txt

4.1.5:
------

 * Added the DBEnv.set_timeout method.

4.1.4:
------

 * rebuilt the windows 4.1.3 package, the original package was corrupt due
   to bad ram on my build host.

4.1.3 - 2003-02-02:
-------------------

 * code cleanup to use python 2.x features in .py files
 * the standalone pybsddb distribution will install a module
   called bsddb3 while the module included with python >= 2.3
   will be known as bsddb.

4.1.2 - 2003-01-17:
-------------------

 * Shared all .py and .c source with the Python project.
 * Fixed DBTxn objects to raise an exception if they are used after
   the underlying DB_TXN handle becomes invalid. (rather than
   potentially causing a segfault)
 * Fixed module to work when compiled against a python without thread
   support.
 * Do not attempt to double-close DB cursor's whos underlying DB
   has already been closed (fixes a segfault).
 * Close DB objects when DB.open fails to prevent an exception about
   databases still being open when calling DBEnv.close.

4.1.1 - 2002-12-20:
-------------------

 * Fixed a memory leak when raising exceptions from the database
   library.  Debugged and fixed by Josh Hoyt <josh@janrain.com>.  Thanks!
   (sourceforge patch 656517)

4.1.0 - 2002-12-13:
-------------------

 * Updated our version number to track the latest BerkeleyDB interface
   version that we support.
 * Simplified the build and test process.  Now you should just be able
   to say "python setup.py build" and "python setup.py install".  Also
   added a nice test.py harness.  Do "python test.py -h" for details.
 * The windows binary is build against BerkeleyDB 4.1.24 with current
   eight patches issued by Sleepycat applied.
 * REMINDER: BerkeleyDB 4.1 requires code changes if you use database
   transactions.  See the upgrade docs on http://www.sleepycat.com/.

3.4.3 - 2002-10-18:
-------------------

 * added support for BerkeleyDB 4.1:  DB.open and DB.associate
   will now accept a txn keyword argument when using BerkeleyDB 4.1.
   DBEnv.dbremove, DBEnv.dbrename, DBEnv.set_encrypt and DB.set_encrypt
   methods have been exposed for 4.1.

3.4.2 - 2002-08-14:
-------------------

 * dbtables.py: serious bug fix.  The Select, Modify and Delete methods could
   all act upon rows that did not match all of the conditions.  (bug # 590449)
   A test case was added.
 * dbutils.py: updated DeadlockWrap
 * test_threads.py: fixed to use dbutils.DeadlockWrap to catch and avoid
   DBLockDeadlockError exceptions during simple threading tests.

3.4.1:
------

 * fixed typo cut and paste bugs in test_dbsimple.py and test_threads.py
 * fixed bug with cursors where calling DBCursor.close() would cause
   the object's destructor __del__() method to raise an exception when
   it was called by the gc.
 * fixed a bug in associated callbacks that could cause a null pointer
   dereference when python threading had not yet been initialized.

3.4.0:
------

 * many bugfixes, its been a long while since a new package was created.
 * ChangeLog started.

