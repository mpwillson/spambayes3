Changelog
=========

18.1.6 -:
---------

  - x

18.1.5 - 2022-01-21:
--------------------

  - **WARNING - BREAKING CHANGE:** Drop support for Python 3.6.

    This breaking change should usually require a major and/or minor
    number update. Since ``berkeleydb`` traditional numbering is
    related to the higher Oracle Berkeley DB supported, I would
    usually wait until Oracle releases a new version to upgrade my
    own version and deprecate old Python support at the same time.
    Given that Oracle has not released a new Oracle Berkeley DB in
    almost four years, I must break this practice for now.

    I am sorry if this update breaks your Python 3.6 environment.
    In that case, please pin your ``berkeleydb`` installation to
    version 18.1.4, the last Python 3.6 compatible release.

    Send me constructive feedback if appropiate.

  - Python 3.10 support.

  - Testsuite works now in Python 3.11.0a4.

  - Python 3.11 added to the full test matrix.

  - Python 3.11 deprecates the ancient but undocumented method
    ``unittest.makeSuite()`` and it will be deleted in Python
    3.13. We migrate the tests to
    ``unittest.TestLoader.loadTestsFromTestCase()``.

  - Experimental Python 3.11 support. Tested in 3.11.0a4.

18.1.4 - 2021-05-19:
--------------------

  - If your "pip" is modern enough, "setuptools" is automatically
    added as a built-time dependency.

    If not, you **MUST** install "setuptools" package first.

18.1.3 - 2021-05-19:
--------------------

  - Docs in https://docs.jcea.es/berkeleydb/.

  - ``make publish`` build and publish the documentation online.

  - Python 3.10 deprecated ``distutils``. ``setuptools`` is now an
    installation dependency.

  - ``make dist`` will generate the HTML documentation and will
    include it in the released package. You can unpack the package
    to read the docs.

  - Do not install tests anymore when doing ``pip install``,
    although the tests are included in the package. You can unpack
    the package to study the tests, maybe in order to learn about
    how to use advanced Oracle Berkeley DB features.

    This change had an unexpected ripple effect in all code. Hopefully for the
    better.

  - Python 3.10 couldn't find build directory.

  - Python 3.10.0a2 test suite compatibility.

  - Python 3.10 added to the full test matrix.

  - After Python 3.7, threads are always available. Take them for granted,
    even in Python 3.6.

  - In the same direction, now some libraries are always available: pathlib,
    warnings, queue, gc.

  - Support ``DB.get_lk_exclusive()`` and
    ``DB.set_lk_exclusive()`` if you are linking against Oracle
    Berkeley DB 5.3 or newer.

  - **WARNING - BREAKING CHANGE:** The record number in the tuple
    returned by ``DB.consume()`` is now a number instead of a
    binary key.

  - **WARNING - BREAKING CHANGE:** The record number in the tuple
    returned by ``DB.consume_wait()`` is now a number instead of a
    binary key.

  - ``DB.consume()`` and ``DB.consume_wait()`` now can request
    partial records.

  - ``DB.get()`` and ``DB.pget()`` could misunderstand flags.

  - If you are using Oracle Berkeley DB 5.3 or newer, you have
    these new flags: ``DB_BACKUP_CLEAN``, ``DB_BACKUP_FILES``,
    ``DB_BACKUP_NO_LOGS``, ``DB_BACKUP_SINGLE_DIR`` and
    ``DB_BACKUP_UPDATE``, ``DB_BACKUP_WRITE_DIRECT``,
    ``DB_BACKUP_READ_COUNT``, ``DB_BACKUP_READ_SLEEP``,
    ``DB_BACKUP_SIZE``.

  - If you are using Oracle Berkeley DB 18.1 or newer, you have these new
    flags: ``DB_BACKUP_DEEP_COPY``.

  - ``DBEnv.backup()``, ``DBEnv.dbbackup()``
    ``DB.get_backup_config()`` and ``DB.set_backup_config()``
    available if you are using Oracle Berkeley DB 5.3 or newer.
    These methods allow you to do hot backups without needing to
    follow a careful procedure, and they can be incremental.

  - Changelog moved to Sphinx documentation.

18.1.2 - 2020-12-07:
--------------------

  * Releases 18.1.0 and 18.1.1 were incomplete. Thanks to Mihai.i
    for reporting.

  * Export exception ``DBMetaChksumFail`` (from error
    ``DB_META_CHKSUM_FAIL``) if running Oracle Berkeley DB version
    6.2 or newer.

  * Support Heap access method if you are linking against Oracle Berkeley DB
    5.3 or newer.

    - ``DB.put()`` can add new records or overwrite old ones in
      Heap access method.

    - ``DB.append()`` was extended to support Heap access method.

    - ``DB.cursor()`` was extended to support Heap access method.

    - Implement, test and document ``DB.get_heapsize()``,
      ``DB.set_heapsize()``, ``DB.get_heap_regionsize()`` and
      ``DB.set_heap_regionsize()``.

    - Export exception ``DBHeapFull`` (from error
      ``DB_HEAP_FULL``).

    - ``DB.stats()`` provides stats for Heap access method.

  * **WARNING - BREAKING CHANGE:** Add ``dbtype`` member in
    ``DBObject`` object in the C API. Increase C API version. This
    change has ripple effect in the code.

  * **WARNING - BREAKING CHANGE:** ``primaryDBType`` member in
    ``DBObject`` object in the C API is now type ``DBTYPE``.
    Increase C API version. This change has ripple effect in the
    code.

  * Now ``DB.get_type()`` can be called anytime and it doesn't
    raise an exception if called before the database is open. If
    the database type is not known, ``DB_UNKNOWN`` is returned.
    This is a deviation from the Oracle Berkeley DB C API.

  * **WARNING - BREAKING CHANGE:** ``DB.type()`` method is
    dropped. It was never documented. Use ``DB.get_type()``.

  * ``DB.stats()`` returns new keys in the dictionary:

    - Hash, Btree and Recno access methods: Added ``metaflags``
      (always) and ``ext_files`` (if linked against Oracle
      Berkeley DB 6.2 or newer).

    - Queue access method: Added ``metaflags`` (always).

18.1.1 - 2020-12-01:
--------------------

  * If you try to install this library in an unsupported Python
    environment, instruct the user about how to install legacy
    ``bsddb3`` library.

  * Expose ``DBSite`` object in the C API. Increase C API version.

  * **WARNING - BREAKING CHANGE:** Ancient release 4.2.8 added
    weakref support to all bsddb.db objects, but from now on this
    feature requires at least Python 3.9 because I have migrated
    from static types to heap types. Let me know if this is a
    problem for you. I could, for example, keep the old types in
    Python < 3.9, if needed.

    Details:

    Py_tp_dictoffset / Py_tp_finalize are unsettable in stable API
    https://bugs.python.org/issue38140

    bpo-38140: Make dict and weakref offsets opaque for C heap types (#16076)
    https://github.com/python/cpython/commit/3368f3c6ae4140a0883e19350e672fd09c9db616

  * ``_iter_mixin`` and ``_DBWithCursor`` classes have been
    rewritten to avoid the need of getting a weak reference to
    ``DBCursor`` objects, since now it is problematic if Python <
    3.9.

  * Wai Keen Woon and Nik Adam sent some weeks ago a patch to
    solve a problem with ``DB.verify()`` always succeeding.
    Refactoring in that area in 18.1.0 made that patch unneeded,
    but I added the test case provided to the test suite.

  * ``DBEnv.cdsgroup_begin()`` implemented.

  * ``DBTxn.set_priority()`` and ``DBTxn.get_priority()``
    implemented. You need to link this library against Oracle
    Berkeley DB >= 5.3.

  * ``DBEnv.set_lk_max()`` was deprecated and deleted long time
    ago. Time to delete it from documentation too.

  * **WARNING - BREAKING CHANGE:** ``DB.compact()`` used to return
    a number, but now it returns a dictionary. If you need access
    to the old return value, you can do
    ``DB.compact()['pages_truncated']``.

  * ``DB.compact()`` has been supported ``txn`` parameter for a
    long time, but it was not documented.

  * The dictionary returned by ``DB.compact()`` has an ``end``
    entry marking the database key/page number where the
    compaction stopped. You could use it to do partial/incremental
    database compaction.

  * Add an optional parameter to ``DBEnv.log_flush()``.

  * You can override the directory where the tests are run with TMPDIR
    environment variable. If that environment variable is not
    defined, test will run in ``/tmp/ram/`` if exists and in
    ``/tmp`` if ``/tmp/ram/`` doesn't exists or it is not a
    directory. The idea is that ``/tmp/ram/`` is a ramdisk and the
    test will run faster.

18.1.0 - 2020-11-12:
--------------------

  * ``bsddb`` name is reserved in PYPI, so we rename the project
    to ``berkeleydb``. This has been a long trip:
    http://mailman.jcea.es/pipermail/pybsddb/2008-March/000019.html

18.1.0-pre:
-----------

  * Support Oracle Berkeley DB 18.1.x.
  * Drop support for Oracle Berkeley DB 4.7, 5.1 and 6.1.
  * Drop support for Python 2.6, 2.7, 3.3, 3.4 and 3.5.
  * The library name is migrated from ``bsddb3`` to ``bsddb``. Reasons:

    - In the old days, ``bsddb`` module was integrated with Python < 3 . The
      release rate of new Python interpreters was slow, so ``bsddb`` was
      also distributed as an external package for faster deployment of
      improvements and support of new Oracle Berkeley DB releases. In order to
      be able to install a new version of this package without conflicting
      with the internal python ``bsddb``, a new package name was required.
      At the time, the chosen name was ``bsddb3`` because it was the major
      release version of the supported Oracle Berkeley DB library.

      After Oracle released Berkeley DB major versions 4, 5, 6 and 18, ``bsddb3``
      name was retained for compatibility, although it didn't make sense
      anymore.

    - ``bsddb3`` seems to refer to the Python 3 version of ``bsddb``. This
      was never the case, and that was confusing. Even more now that
      legacy ``bsddb3`` is the Python 2/3 codebase and the new ``bsddb`` is
      Python 3 only.

    - Since from now on this library is Python 3 only, I would hate that
      Python 2 users upgrading their Berkeley DB libraries would render
      their installation unable to run. In order to avoid that, a new name
      for the package is a good idea.

    - I decided to go back to ``bsddb``, since Python 2.7 is/should be dead.

    - If your are running Python 3, please update your code to use
      ``bsddb`` instead of ``bsddb3``.

      The old practice was to do:

          ``import bsddb3 as bsddb``

      Now you can change that to:

          ``import bsddb``

  * This library was usually know as ``bsddb``, ``bsddb3`` or ``pybsddb``.
    From now on, it is ``bsddb`` everywhere.
  * Testsuite driver migrated to Python 3.
  * Since Oracle Berkeley DB 4.7 is not supported anymore,
    ancient method ``DBEnv.set_rpc_server()`` is not available anymore.
  * If you try to install this package on Python 2,
    an appropriate error is raised and directions are provided.
  * Remove dead code for unsupported Python releases.
  * Remove dead code for unsupported Oracle Berkeley DB releases.
  * **WARNING:** Now **ALL** keys and values must be bytes (or ints when
    appropriate). Previous releases did mostly transparent encoding. This
    is not the case anymore. All needed encoding must be explicit in
    your code, both when reading and when writing to the database.
  * In previous releases, database cursors were iterable under Python 3,
    but not under Python 2. For this release, database cursors are not
    iterable anymore. This will be improved in a future release.
  * In previous releases, log cursors were iterable under Python 3,
    but not under Python 2. For this release, log cursors are not
    iterable anymore. This will be improved in a future release.
  * Support for ``DB_REPMGR_CONF_DISABLE_SSL`` flag in
    ``DB_ENV.rep_set_config()``.
  * **WARNING:** In Oracle Berkeley DB 18.1 and up, Replication Manager uses
    SSL by default.

    This configuration is currently unsupported.

    If you use Oracle Berkeley DB 18.1 and up and Replication Manager,
    you *MUST* configure the DB environment to not use SSL. You must do

        ``DB_ENV.rep_set_config(db.DB_REPMGR_CONF_DISABLE_SSL, 1)``

    in your code.

    This limitation will be overcomed in a future release of this project.

  * ``open()`` methods allow path-like objects.
  * ``DBEnv.open()`` accepts keyword arguments.
  * ``DBEnv.open()`` allows no homedir and a homedir of ``None``.
  * ``DB.set_re_source()`` uses local filename encoding.
  * ``DB.set_re_source()`` accepts path-like objects if using Python 3.6 or up.
  * ``DB.verify()`` was doing nothing at all. Now actually do the job.
  * ``DB.verify()`` accepts path-like objects for ``filename`` and ``outfile`` if
    using Python 3.6 or up.
  * ``DB.upgrade()`` accepts path-like objects if using Python 3.6 or up.
  * ``DB.remove()`` accepts path-like objects if using Python 3.6 or up.
  * ``DB.remove()`` could leak objects.
  * ``DB.rename()`` accepts path-like objects if using Python 3.6 or up.
  * ``DB.rename()`` correctly invalidates the DB handle.
  * ``DB.get_re_source()`` returns unicode objects with the local
    filename encoding.
  * ``DB_ENV.fileid_reset()`` accepts path-like objects if using Python 3.6 or
    up.
  * ``DB_ENV.log_file()`` correctly encode the filename according to the
    system FS encoding.
  * ``DB_ENV.log_archive()`` correctly encode the filenames according to the
    system FS encoding.
  * ``DB_ENV.lsn_reset()`` accepts path-like objects if using Python 3.6 or up.
  * ``DB_ENV.remove()`` accepts path-like objects if using Python 3.6 or up.
  * ``DB_ENV.remove()`` used to leave the DBENV handle in an unstable state.
  * ``DB_ENV.dbrename()`` accepts path-like objects for ``filename`` and ``newname``
    if using Python 3.6 or up.
  * ``DB_ENV.dbremove()`` accepts path-like objects if using Python 3.6 or up.
  * ``DB_ENV.set_lg_dir()`` uses local filename encoding.
  * ``DB_ENV.set_lg_dir()`` accepts path-like objects if using Python 3.6 or up.
  * ``DB_ENV.get_lg_dir()`` returns unicode objects with the local
    filename encoding.
  * ``DB_ENV.set_tmp_dir()`` uses local filename encoding.
  * ``DB_ENV.set_tmp_dir()`` accepts path-like objects if using Python 3.6 or up.
  * ``DB_ENV.get_tmp_dir()`` returns unicode objects with the local
    filename encoding.
  * ``DB_ENV.set_data_dir()`` uses local filename encoding.
  * ``DB_ENV.set_data_dir()`` accepts path-like objects if using Python 3.6 or
    up.
  * ``DB_ENV.get_data_dirs()`` returns a tuple of unicode objects encoded with
    the local filename encoding.
  * ``DB_ENV.log_prinf()`` requires a bytes object not containing '\0'.
  * The ``DB_ENV.lock_get()`` name can not be None.
  * ``DB_ENV.set_re_pad()`` param must be bytes or integer.
  * ``DB_ENV.get_re_pad()`` returns bytes.
  * ``DB_ENV.set_re_delim()`` param must be bytes or integer.
  * ``DB_ENV.get_re_delim()`` returns bytes.
  * In the C code we don't need ``statichere`` neither ``staticforward``
    workarounds anymore.
  * ``db.DB*`` objects are created via the native classes, not via
    factories anymore.
  * Drop support for ``dbtables``. If you need it back, let me know.
  * In Python 3.9, ``find_unused_port`` has been moved to
    ``test.support.socket_helper``. Reported by Michał Górny.
  * If we use ``set_get_returns_none()`` in the environment,
    the value could not be correctly inherited by the child
    databases. Reported by Patrick Laimbock and modern GCC
    warnings.
  * Do not leak test files and directories.
