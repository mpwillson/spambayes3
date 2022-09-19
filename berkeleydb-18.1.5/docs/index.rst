=============================================================
Python Bindings for Oracle Berkeley DB 4.8, 5.3, 6.2 and 18.1
=============================================================

Introduction
------------

.. _Oracle Berkeley DB: http://www.oracle.com/technetwork/database/berkeleydb/overview/index.html

This handcrafted package contains Python wrappers for `Oracle Berkeley DB`_,
the Open Source embedded database system. Oracle Berkeley DB is a programmatic
toolkit that provides high-performance built-in database support for
desktop and server applications.

The Oracle Berkeley DB access methods include B+tree, Extended Linear Hashing,
Fixed and Variable-length records, and Queues. Oracle Berkeley DB provides full
transactional support, database recovery, online backups, multi-threaded
and multi-process access, etc.

The Python wrappers allow you to store Python string objects of any
length, keyed either by strings or integers depending on the database
access method. With the use of another module in the package standard
shelve-like functionality is provided allowing you to store any
picklable Python object!

Oracle Berkeley DB is very powerful and versatile, but it is complex to
use correctly. :Oracle:`Oracle documentation <toc.htm>` is very
complete. Please, review it.

Since June 2013 (release 6.0.0), this project accepts donations. Please,
contribute if you can. :doc:`Details <donate>`.

Documentation Index
-------------------

.. toctree::

  introduction.rst
  dbenv.rst
  db.rst
  dbcursor.rst
  dblogcursor.rst
  dbtxn.rst
  dblock.rst
  dbsequence.rst
  dbsite.rst
  history.rst
  changelog.rst
  changelog-bsddb3.rst
  license.rst
  donate.rst

