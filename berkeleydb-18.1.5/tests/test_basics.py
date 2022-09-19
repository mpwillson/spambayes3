"""
Copyright (c) 2008-2022, Jesus Cea Avion <jcea@jcea.es>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

    1. Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above
    copyright notice, this list of conditions and the following
    disclaimer in the documentation and/or other materials provided
    with the distribution.

    3. Neither the name of Jesus Cea Avion nor the names of its
    contributors may be used to endorse or promote products derived
    from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
    CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
    MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS
    BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
            TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
            DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
    ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
    TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
    THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
    SUCH DAMAGE.
    """

"""
Basic TestCases for BTree and hash DBs, with and without a DBEnv, with
various DB flags, etc.
"""

import os
import errno
import string
from pprint import pprint
import unittest
import time
import sys
import pathlib

from .test_all import db, rmtree, verbose, get_new_environment_path, \
        get_new_database_path, printable_bytes

DASH = b'-'


#----------------------------------------------------------------------

class VersionTestCase(unittest.TestCase):
    def test00_version(self):
        info = db.version()
        if verbose:
            print('\n', '-=' * 20)
            print('berkeleydb.db.version(): %s' % (info, ))
            print(db.DB_VERSION_STRING)
            print('-=' * 20)
        self.assertEqual(info, (db.DB_VERSION_MAJOR, db.DB_VERSION_MINOR,
                        db.DB_VERSION_PATCH))

#----------------------------------------------------------------------

class BasicTestCase(unittest.TestCase):
    dbtype       = db.DB_UNKNOWN  # must be set in derived class
    cachesize    = (0, 1024*1024, 1)
    dbopenflags  = 0
    dbsetflags   = 0
    dbmode       = 0o660
    dbname       = None
    useEnv       = 0
    envflags     = 0
    envsetflags  = 0

    _numKeys      = 1002    # PRIVATE.  NOTE: must be an even value

    def setUp(self):
        if self.useEnv:
            self.homeDir=get_new_environment_path()
            try:
                self.env = db.DBEnv()
                self.env.set_lg_max(1024*1024)
                self.env.set_tx_max(30)
                self._t = int(time.time())
                self.env.set_tx_timestamp(self._t)
                self.env.set_flags(self.envsetflags, 1)
                self.env.open(self.homeDir, self.envflags | db.DB_CREATE)
                self.filename = "test"
            # Yes, a bare except is intended, since we're re-raising the exc.
            except Exception:
                rmtree(self.homeDir)
                raise
        else:
            self.env = None
            self.filename = get_new_database_path()

        # create and open the DB
        self.d = db.DB(self.env)
        if not self.useEnv :
            self.d.set_cachesize(*self.cachesize)
            cachesize = self.d.get_cachesize()
            self.assertEqual(cachesize[0], self.cachesize[0])
            self.assertEqual(cachesize[2], self.cachesize[2])
            # Berkeley DB expands the cache 25% accounting overhead,
            # if the cache is small.
            self.assertEqual(125, int(100.0*cachesize[1]/self.cachesize[1]))
        self.d.set_flags(self.dbsetflags)
        if self.dbname:
            self.d.open(self.filename, self.dbname, self.dbtype,
                        self.dbopenflags|db.DB_CREATE, self.dbmode)
        else:
            self.d.open(self.filename,   # try out keyword args
                        mode = self.dbmode,
                        dbtype = self.dbtype,
                        flags = self.dbopenflags|db.DB_CREATE)

        if not self.useEnv:
            self.assertRaises(db.DBInvalidArgError,
                    self.d.set_cachesize, *self.cachesize)

        self.populateDB()


    def tearDown(self):
        self.d.close()
        if self.env is not None:
            self.env.close()
            rmtree(self.homeDir)
        else:
            os.remove(self.filename)



    def populateDB(self, _txn=None):
        d = self.d

        for x in range(self._numKeys//2):
            key = b'%04d' % (self._numKeys - x)  # insert keys in reverse order
            data = self.makeData(key)
            d.put(key, data, _txn)

        d.put(b'empty value', b'', _txn)

        for x in range(self._numKeys//2-1):
            key = b'%04d' % x  # and now some in forward order
            data = self.makeData(key)
            d.put(key, data, _txn)

        if _txn:
            _txn.commit()

        num = len(d)
        if verbose:
            print("created %d records" % num)


    def makeData(self, key):
        return DASH.join([key] * 5)



    #----------------------------------------

    def test01_GetsAndPuts(self):
        d = self.d

        if verbose:
            print('\n', '-=' * 30)
            print("Running %s.test01_GetsAndPuts..." % self.__class__.__name__)

        for key in [b'0001', b'0100', b'0400', b'0700', b'0999']:
            data = d.get(key)
            if verbose:
                print(data)

        self.assertEqual(d.get(b'0321'), b'0321-0321-0321-0321-0321')

        # By default non-existent keys return None...
        self.assertEqual(d.get(b'abcd'), None)

        # ...but they raise exceptions in other situations.  Call
        # set_get_returns_none() to change it.
        try:
            d.delete(b'abcd')
        except db.DBNotFoundError as val:
            self.assertEqual(val.args[0], db.DB_NOTFOUND)
            if verbose: print(val)
        else:
            self.fail("expected exception")


        d.put(b'abcd', b'a new record')
        self.assertEqual(d.get(b'abcd'), b'a new record')

        d.put(b'abcd', b'same key')
        if self.dbsetflags & db.DB_DUP:
            self.assertEqual(d.get(b'abcd'), b'a new record')
        else:
            self.assertEqual(d.get(b'abcd'), b'same key')


        try:
            d.put(b'abcd', b'this should fail', flags=db.DB_NOOVERWRITE)
        except db.DBKeyExistError as val:
            self.assertEqual(val.args[0], db.DB_KEYEXIST)
            if verbose: print(val)
        else:
            self.fail("expected exception")

        if self.dbsetflags & db.DB_DUP:
            self.assertEqual(d.get(b'abcd'), b'a new record')
        else:
            self.assertEqual(d.get(b'abcd'), b'same key')


        d.sync()
        d.close()
        del d

        self.d = db.DB(self.env)
        if self.dbname:
            self.d.open(self.filename, self.dbname)
        else:
            self.d.open(self.filename)
        d = self.d

        self.assertEqual(d.get(b'0321'), b'0321-0321-0321-0321-0321')
        if self.dbsetflags & db.DB_DUP:
            self.assertEqual(d.get(b'abcd'), b'a new record')
        else:
            self.assertEqual(d.get(b'abcd'), b'same key')

        rec = d.get_both(b'0555', b'0555-0555-0555-0555-0555')
        if verbose:
            print(rec)

        self.assertEqual(d.get_both(b'0555', b'bad data'), None)

        # test default value
        data = d.get(b'bad key', b'bad data')
        self.assertEqual(data, b'bad data')

        # any object can pass through
        data = d.get(b'bad key', self)
        self.assertEqual(data, self)

        s = d.stat()
        self.assertEqual(type(s), type({}))
        if verbose:
            print('d.stat() returned this dictionary:')
            pprint(s)


    #----------------------------------------

    def test02_DictionaryMethods(self):
        d = self.d

        if verbose:
            print('\n', '-=' * 30)
            print("Running %s.test02_DictionaryMethods..." % \
                  self.__class__.__name__)

        for key in [b'0002', b'0101', b'0401', b'0701', b'0998']:
            data = d[key]
            self.assertEqual(data, self.makeData(key))
            if verbose:
                print(data)

        self.assertEqual(len(d), self._numKeys)
        keys = list(d.keys())
        self.assertEqual(len(keys), self._numKeys)
        self.assertEqual(type(keys), type([]))

        d[b'new record'] = b'a new record'
        self.assertEqual(len(d), self._numKeys+1)
        keys = list(d.keys())
        self.assertEqual(len(keys), self._numKeys+1)

        d[b'new record'] = b'a replacement record'
        self.assertEqual(len(d), self._numKeys+1)
        keys = list(d.keys())
        self.assertEqual(len(keys), self._numKeys+1)

        if verbose:
            print("the first 10 keys are:")
            pprint(keys[:10])

        self.assertEqual(d[b'new record'], b'a replacement record')

# We check also the positional parameter
        self.assertEqual(d.has_key(b'0001', None), 1)
# We check also the keyword parameter
        self.assertEqual(d.has_key(b'spam', txn=None), 0)

        items = list(d.items())
        self.assertEqual(len(items), self._numKeys+1)
        self.assertEqual(type(items), type([]))
        self.assertEqual(type(items[0]), type(()))
        self.assertEqual(len(items[0]), 2)

        if verbose:
            print("the first 10 items are:")
            pprint(items[:10])

        values = list(d.values())
        self.assertEqual(len(values), self._numKeys+1)
        self.assertEqual(type(values), type([]))

        if verbose:
            print("the first 10 values are:")
            pprint(values[:10])


    #----------------------------------------

    def test02b_SequenceMethods(self):
        d = self.d

        for key in [b'0002', b'0101', b'0401', b'0701', b'0998']:
            data = d[key]
            self.assertEqual(data, self.makeData(key))
            if verbose:
                print(data)

        self.assertTrue(hasattr(d, "__contains__"))
        self.assertTrue(b'0401' in d)
        self.assertFalse(b'1234' in d)


    #----------------------------------------

    def test03_SimpleCursorStuff(self, get_raises_error=0, set_raises_error=0):
        if verbose:
            print('\n', '-=' * 30)
            print("Running %s.test03_SimpleCursorStuff (get_error %s, set_error %s)..." % \
                  (self.__class__.__name__, get_raises_error, set_raises_error))

        if self.env and self.dbopenflags & db.DB_AUTO_COMMIT:
            txn = self.env.txn_begin()
        else:
            txn = None
        c = self.d.cursor(txn=txn)

        rec = c.first()
        count = 0
        while rec is not None:
            count = count + 1
            if verbose and count % 100 == 0:
                print(rec)
            try:
                rec = c.next()
            except db.DBNotFoundError as val:
                if get_raises_error:
                    self.assertEqual(val.args[0], db.DB_NOTFOUND)
                    if verbose: print(val)
                    rec = None
                else:
                    self.fail("unexpected DBNotFoundError")
            self.assertEqual(c.get_current_size(), len(c.current()[1]),
                    "%s != len(%r)" % (c.get_current_size(), c.current()[1]))

        self.assertEqual(count, self._numKeys)


        rec = c.last()
        count = 0
        while rec is not None:
            count = count + 1
            if verbose and count % 100 == 0:
                print(rec)
            try:
                rec = c.prev()
            except db.DBNotFoundError as val:
                if get_raises_error:
                    self.assertEqual(val.args[0], db.DB_NOTFOUND)
                    if verbose: print(val)
                    rec = None
                else:
                    self.fail("unexpected DBNotFoundError")

        self.assertEqual(count, self._numKeys)

        rec = c.set(b'0505')
        rec2 = c.current()
        self.assertEqual(rec, rec2)
        self.assertEqual(rec[0], b'0505')
        self.assertEqual(rec[1], self.makeData(b'0505'))
        self.assertEqual(c.get_current_size(), len(rec[1]))

        # make sure we get empty values properly
        rec = c.set(b'empty value')
        self.assertEqual(rec[1], b'')
        self.assertEqual(c.get_current_size(), 0)

        try:
            n = c.set(b'bad key')
        except db.DBNotFoundError as val:
            self.assertEqual(val.args[0], db.DB_NOTFOUND)
            if verbose: print(val)
        else:
            if set_raises_error:
                self.fail("expected exception")
            if n is not None:
                self.fail("expected None: %r" % (n,))

        rec = c.get_both(b'0404', self.makeData(b'0404'))
        self.assertEqual(rec, (b'0404', self.makeData(b'0404')))

        try:
            n = c.get_both(b'0404', b'bad data')
        except db.DBNotFoundError as val:
            self.assertEqual(val.args[0], db.DB_NOTFOUND)
            if verbose: print(val)
        else:
            if get_raises_error:
                self.fail("expected exception")
            if n is not None:
                self.fail("expected None: %r" % (n,))

        if self.d.get_type() == db.DB_BTREE:
            rec = c.set_range(b'011')
            if verbose:
                print("searched for b'011', found: ", rec)

            rec = c.set_range(b'011', dlen=0, doff=0)
            if verbose:
                print("searched (partial) for b'011', found: ", rec)
            if rec[1] != b'': self.fail('expected empty data portion')

            ev = c.set_range(b'empty value')
            if verbose:
                print("search for b'empty value' returned", ev)
            if ev[1] != b'': self.fail('empty value lookup failed')

        c.set(b'0499')
        c.delete()
        try:
            rec = c.current()
        except db.DBKeyEmptyError as val:
            if get_raises_error:
                self.assertEqual(val.args[0], db.DB_KEYEMPTY)
                if verbose: print(val)
            else:
                self.fail("unexpected DBKeyEmptyError")
        else:
            if get_raises_error:
                self.fail('DBKeyEmptyError exception expected')

        c.next()
        c2 = c.dup(db.DB_POSITION)
        self.assertEqual(c.current(), c2.current())

        c2.put(b'', b'a new value', db.DB_CURRENT)
        self.assertEqual(c.current(), c2.current())
        self.assertEqual(c.current()[1], b'a new value')

        c2.put(b'', b'er', db.DB_CURRENT, dlen=0, doff=5)
        self.assertEqual(c2.current()[1], b'a newer value')

        c.close()
        c2.close()
        if txn:
            txn.commit()

        # time to abuse the closed cursors and hope we don't crash
        methods_to_test = {
            'current': (),
            'delete': (),
            'dup': (db.DB_POSITION,),
            'first': (),
            'get': (0,),
            'next': (),
            'prev': (),
            'last': (),
            'put':(b'', b'spam', db.DB_CURRENT),
            'set': (b'0505',),
        }
        for method, args in list(methods_to_test.items()):
            try:
                if verbose:
                    print("attempting to use a closed cursor's %s method" % \
                          method)
                # a bug may cause a NULL pointer dereference...
                getattr(c, method)(*args)
            except db.DBError as val:
                self.assertEqual(val.args[0], 0)
                if verbose: print(val)
            else:
                self.fail("no exception raised when using a buggy cursor's"
                          "%s method" % method)

        #
        # free cursor referencing a closed database, it should not barf:
        #
        oldcursor = self.d.cursor(txn=txn)
        self.d.close()

        # this would originally cause a segfault when the cursor for a
        # closed database was cleaned up.  it should not anymore.
        # SF pybsddb bug id 667343
        del oldcursor

    def test03b_SimpleCursorWithoutGetReturnsNone0(self):
        # same test but raise exceptions instead of returning None
        if verbose:
            print('\n', '-=' * 30)
            print("Running %s.test03b_SimpleCursorStuffWithoutGetReturnsNone..." % \
                  self.__class__.__name__)

        old = self.d.set_get_returns_none(0)
        self.assertEqual(old, 2)
        self.test03_SimpleCursorStuff(get_raises_error=1, set_raises_error=1)

    def test03b_SimpleCursorWithGetReturnsNone1(self):
        # same test but raise exceptions instead of returning None
        if verbose:
            print('\n', '-=' * 30)
            print("Running %s.test03b_SimpleCursorStuffWithoutGetReturnsNone..." % \
                  self.__class__.__name__)

        old = self.d.set_get_returns_none(1)
        self.test03_SimpleCursorStuff(get_raises_error=0, set_raises_error=1)


    def test03c_SimpleCursorGetReturnsNone2(self):
        # same test but raise exceptions instead of returning None
        if verbose:
            print('\n', '-=' * 30)
            print("Running %s.test03c_SimpleCursorStuffWithoutSetReturnsNone..." % \
                  self.__class__.__name__)

        old = self.d.set_get_returns_none(1)
        self.assertEqual(old, 2)
        old = self.d.set_get_returns_none(2)
        self.assertEqual(old, 1)
        self.test03_SimpleCursorStuff(get_raises_error=0, set_raises_error=0)

    def test03d_SimpleCursorPriority(self) :
        c = self.d.cursor()
        c.set_priority(db.DB_PRIORITY_VERY_LOW)  # Positional
        self.assertEqual(db.DB_PRIORITY_VERY_LOW, c.get_priority())
        c.set_priority(priority=db.DB_PRIORITY_HIGH)  # Keyword
        self.assertEqual(db.DB_PRIORITY_HIGH, c.get_priority())
        c.close()

    #----------------------------------------

    def test04_PartialGetAndPut(self):
        d = self.d
        if verbose:
            print('\n', '-=' * 30)
            print("Running %s.test04_PartialGetAndPut..." % \
                  self.__class__.__name__)

        key = b'partialTest'
        data = b'1' * 1000 + b'2' * 1000
        d.put(key, data)
        self.assertEqual(d.get(key), data)
        self.assertEqual(d.get(key, dlen=20, doff=990),
                (b'1' * 10) + (b'2' * 10))

        d.put(b'partialtest2', (b'1' * 30000) + b'robin')
        self.assertEqual(d.get(b'partialtest2', dlen=5, doff=30000), b'robin')

        # There seems to be a bug in DB here...  Commented out the test for
        # now.
        ##self.assertEqual(d.get(b'partialtest2', dlen=5, doff=30010), b'')

        if self.dbsetflags != db.DB_DUP:
            # Partial put with duplicate records requires a cursor
            d.put(key, b'0000', dlen=2000, doff=0)
            self.assertEqual(d.get(key), b'0000')

            d.put(key, b'1111', dlen=1, doff=2)
            self.assertEqual(d.get(key), b'0011110')

    #----------------------------------------

    def test05_GetSize(self):
        d = self.d
        if verbose:
            print('\n', '-=' * 30)
            print("Running %s.test05_GetSize..." % self.__class__.__name__)

        for i in range(1, 50000, 500):
            key = b'size%d' % i
            d.put(key, b'1' * i)
            self.assertEqual(d.get_size(key), i)

    #----------------------------------------

    def test06_Truncate(self):
        d = self.d
        if verbose:
            print('\n', '-=' * 30)
            print("Running %s.test06_Truncate..." % self.__class__.__name__)

        d.put(b'abcde', b'ABCDE');
        num = d.truncate()
        self.assertTrue(num >= 1, "truncate returned <= 0 on non-empty database")
        num = d.truncate()
        self.assertEqual(num, 0,
                "truncate on empty DB returned nonzero (%r)" % (num,))

    #----------------------------------------

    def test07_verify(self):
        # Verify bug solved in 4.7.3pre8
        self.d.close()
        d = db.DB(self.env)
        d.verify(self.filename)

    def test07_verify_must_fail(self):
        # truncate the database file. verify() must fail.
        self.d.close()
        d = db.DB(self.env)

        if self.env:
            db_filename = os.path.join(self.homeDir, self.filename)
        else:
            db_filename = self.filename
        open(db_filename, "w").close()

        with self.assertRaises(db.DBVerifyBadError):
            d.verify(db_filename)

    def test07_verify_outfile(self):
        self.d.close()
        d = db.DB(self.env)
        d.verify(self.filename, outfile=self.filename + '.dump')
        os.remove(self.filename+'.dump')

    def test07_verify_outfile_none(self):
        self.d.close()
        d = db.DB(self.env)
        d.verify(self.filename, outfile=None)

    def test07_verify_path(self):
        self.d.close()
        d = db.DB(self.env)
        filename = pathlib.Path(self.filename)
        d.verify(filename)

    def test07_verify_path_outfile(self):
        self.d.close()
        d = db.DB(self.env)
        filename = pathlib.Path(self.filename)
        filename_dump = pathlib.Path(self.filename + '.dump')
        d.verify(filename, outfile=filename_dump)
        filename_dump.unlink()

    def test07_upgrade(self):
        self.d.close()
        d = db.DB(self.env)
        d.upgrade(self.filename)

    def test07_upgrade_path(self):
        self.d.close()
        d = db.DB(self.env)
        filename = pathlib.Path(self.filename)
        d.upgrade(filename)

    def test07_rename(self):
        self.d.close()
        d = db.DB(self.env)
        d.rename(self.filename, None, self.filename + '.NEW')
        d = db.DB(self.env)
        d.rename(self.filename + '.NEW', None, self.filename)

    def test07_rename_path(self):
        self.d.close()
        filename = pathlib.Path(self.filename)
        filename_new = pathlib.Path(self.filename + '.NEW')
        d = db.DB(self.env)
        d.rename(filename, None, filename_new)
        d = db.DB(self.env)
        d.rename(filename_new, None, filename)

    def test07_remove(self):
        self.d.close()
        d = db.DB(self.env)
        d.remove(self.filename)
        open(self.filename, 'w').close()  # Touch

    def test07_remove_None(self):
        self.d.close()
        d = db.DB(self.env)
        d.remove(self.filename, None)
        open(self.filename, 'w').close()  # Touch

    def test07_remove_path(self):
        self.d.close()
        filename = pathlib.Path(self.filename)
        d = db.DB(self.env)
        d.remove(filename)
        filename.touch()

    def test07_remove_path_None(self):
        self.d.close()
        filename = pathlib.Path(self.filename)
        d = db.DB(self.env)
        d.remove(filename, None)
        filename.touch()

    #----------------------------------------

    def test08_exists(self) :
        self.d.put(b'abcde', b'ABCDE')
        self.assertTrue(self.d.exists(b'abcde') == True,
                "DB->exists() returns wrong value")
        self.assertTrue(self.d.exists(b'x') == False,
                "DB->exists() returns wrong value")

    #----------------------------------------

    def test_compact(self) :
        d = self.d
        keys = {'deadlock', 'pages_examine', 'pages_free',
                'levels', 'pages_truncated', 'end'}
        if db.version() >= (5, 3):
            keys.add('empty_buckets')
        ret = d.compact(flags=db.DB_FREELIST_ONLY)
        self.assertEqual(0, ret['pages_truncated'])
        self.assertEqual(keys, set(ret.keys()))
        d.put(b'abcde', b'ABCDE');
        d.put(b'bcde', b'BCDE');
        d.put(b'abc', b'ABC');
        d.put(b'monty', b'python');
        d.delete(b'abc')
        d.delete(b'bcde')
        d.compact(start=b'abcde', stop=b'monty', txn=None,
                compact_fillpercent=42, compact_pages=1,
                compact_timeout=50000000,
                flags=db.DB_FREELIST_ONLY | db.DB_FREE_SPACE)

    @unittest.skipIf(db.version() < (5, 3),
                     'Oracle Berkeley DB 4.8 is ancient and quirky. Move on')
    def test_compact_really_do_something(self):
        for i in range(1024):
            self.d.put(repr(i).encode('ascii'), b'1234' * 256)

        for i in range(256, 512):
            self.d.delete(repr(i).encode('ascii'))
        for i in range(768, 1024):
            self.d.delete(repr(i).encode('ascii'))

        ret = self.d.compact(flags=db.DB_FREE_SPACE)

        self.assertEqual(0, ret['deadlock'])
        self.assertEqual(0, ret['levels'])
        self.assertNotEqual(0, ret['pages_examine'])
        self.assertNotEqual(0, ret['pages_free'])
        self.assertNotEqual(0, ret['pages_truncated'])
        self.assertNotEqual(b'', ret['end'])
        if db.version() >= (5, 3):
            self.assertEqual(0, ret['empty_buckets'])

    @unittest.skipIf(db.version() < (5, 3),
                     'Oracle Berkeley DB 4.8 has no get/set_lk_exclusive')
    def test_getset_lk_exclusive(self):
        self.assertEqual((False, False), self.d.get_lk_exclusive())
        d2 = db.DB(self.env)
        try:
            self.assertEqual((False, False), d2.get_lk_exclusive())
            d2.set_lk_exclusive(False)
            self.assertEqual((True, False), d2.get_lk_exclusive())
            d2.set_lk_exclusive(True)
            self.assertEqual((True, True), d2.get_lk_exclusive())
        finally:
            d2.close()


    #----------------------------------------

#----------------------------------------------------------------------


class BasicBTreeTestCase(BasicTestCase):
    dbtype = db.DB_BTREE


class BasicHashTestCase(BasicTestCase):
    dbtype = db.DB_HASH


class BasicBTreeWithThreadFlagTestCase(BasicTestCase):
    dbtype = db.DB_BTREE
    dbopenflags = db.DB_THREAD


class BasicHashWithThreadFlagTestCase(BasicTestCase):
    dbtype = db.DB_HASH
    dbopenflags = db.DB_THREAD


class BasicWithEnvTestCase(BasicTestCase):
    dbopenflags = db.DB_THREAD
    useEnv = 1
    envflags = db.DB_THREAD | db.DB_INIT_MPOOL | db.DB_INIT_LOCK

    #----------------------------------------

    def test09_EnvRemoveAndRename(self):
        if not self.env:
            return

        if verbose:
            print('\n', '-=' * 30)
            print("Running %s.test09_EnvRemoveAndRename..." % self.__class__.__name__)

        # can't rename or remove an open DB
        self.d.close()

        newname = self.filename + '.renamed'
        self.env.dbrename(self.filename, None, newname)
        self.env.dbremove(newname)

    def test09_EnvRemoveAndRename_path(self):
        if not self.env:
            return

        if verbose:
            print('\n', '-=' * 30)
            print("Running %s.test09_EnvRemoveAndRename..." % self.__class__.__name__)

        # can't rename or remove an open DB
        self.d.close()

        filename = pathlib.Path(self.filename)
        newname = pathlib.Path(self.filename + '.renamed')
        self.env.dbrename(filename, None, newname)
        self.env.dbremove(newname)

    #----------------------------------------

class BasicBTreeWithEnvTestCase(BasicWithEnvTestCase):
    dbtype = db.DB_BTREE


class BasicHashWithEnvTestCase(BasicWithEnvTestCase):
    dbtype = db.DB_HASH


#----------------------------------------------------------------------

class BasicTransactionTestCase(BasicTestCase):
    dbopenflags = db.DB_THREAD | db.DB_AUTO_COMMIT
    useEnv = 1
    envflags = (db.DB_THREAD | db.DB_INIT_MPOOL | db.DB_INIT_LOCK |
                db.DB_INIT_LOG | db.DB_INIT_TXN)
    envsetflags = db.DB_AUTO_COMMIT


    def tearDown(self):
        self.txn.commit()
        BasicTestCase.tearDown(self)


    def populateDB(self):
        txn = self.env.txn_begin()
        BasicTestCase.populateDB(self, _txn=txn)

        self.txn = self.env.txn_begin()


    def test06_Transactions(self):
        d = self.d
        if verbose:
            print('\n', '-=' * 30)
            print("Running %s.test06_Transactions..." % self.__class__.__name__)

        self.assertEqual(d.get(b'new rec', txn=self.txn), None)
        d.put(b'new rec', b'this is a new record', self.txn)
        self.assertEqual(d.get(b'new rec', txn=self.txn),
                b'this is a new record')
        self.txn.abort()
        self.assertEqual(d.get(b'new rec'), None)

        self.txn = self.env.txn_begin()

        self.assertEqual(d.get(b'new rec', txn=self.txn), None)
        d.put(b'new rec', b'this is a new record', self.txn)
        self.assertEqual(d.get(b'new rec', txn=self.txn),
                b'this is a new record')
        self.txn.commit()
        self.assertEqual(d.get(b'new rec'), b'this is a new record')

        self.txn = self.env.txn_begin()
        c = d.cursor(self.txn)
        rec = c.first()
        count = 0
        while rec is not None:
            count = count + 1
            if verbose and count % 100 == 0:
                print(rec)
            rec = c.next()
        self.assertEqual(count, self._numKeys+1)

        c.close()                # Cursors *MUST* be closed before commit!
        self.txn.commit()

        # flush pending updates
        self.env.txn_checkpoint (0, 0, 0)

        statDict = self.env.log_stat(0);
        self.assertIn('magic', statDict)
        self.assertIn('version', statDict)
        self.assertIn('cur_file', statDict)
        self.assertIn('region_nowait', statDict)

        # must have at least one log file present:
        logs = self.env.log_archive(db.DB_ARCH_ABS | db.DB_ARCH_LOG)
        self.assertEqual(logs[0][-14:], 'log.0000000001')
        self.assertNotEqual(logs, None)
        for log in logs:
            if verbose:
                print('log file: ' + log)
        logs = self.env.log_archive(db.DB_ARCH_REMOVE)
        self.assertTrue(not logs)

        self.txn = self.env.txn_begin()

    #----------------------------------------

    def test08_exists(self) :
        txn = self.env.txn_begin()
        self.d.put(b'abcde', b'ABCDE', txn=txn)
        txn.commit()
        txn = self.env.txn_begin()
        self.assertTrue(self.d.exists(b'abcde', txn=txn) == True,
                "DB->exists() returns wrong value")
        self.assertTrue(self.d.exists(b'x', txn=txn) == False,
                "DB->exists() returns wrong value")
        txn.abort()

    #----------------------------------------

    def test09_TxnTruncate(self):
        d = self.d
        if verbose:
            print('\n', '-=' * 30)
            print("Running %s.test09_TxnTruncate..." % self.__class__.__name__)

        d.put(b'abcde', b'ABCDE');
        txn = self.env.txn_begin()
        num = d.truncate(txn)
        self.assertTrue(num >= 1, "truncate returned <= 0 on non-empty database")
        num = d.truncate(txn)
        self.assertEqual(num, 0,
                "truncate on empty DB returned nonzero (%r)" % (num,))
        txn.commit()

    #----------------------------------------

    def test10_TxnLateUse(self):
        txn = self.env.txn_begin()
        txn.abort()
        try:
            txn.abort()
        except db.DBError as e:
            pass
        else:
            raise RuntimeError("DBTxn.abort() called after DB_TXN no longer valid w/o an exception")

        txn = self.env.txn_begin()
        txn.commit()
        try:
            txn.commit()
        except db.DBError as e:
            pass
        else:
            raise RuntimeError("DBTxn.commit() called after DB_TXN no longer valid w/o an exception")


    #----------------------------------------


    def test_txn_name(self) :
        txn=self.env.txn_begin()
        self.assertEqual(txn.get_name(), "")
        txn.set_name("XXYY")
        self.assertEqual(txn.get_name(), "XXYY")
        txn.set_name("ABC")
        self.assertEqual(txn.get_name(), "ABC")
        txn.abort()

    #----------------------------------------


    def test_txn_set_timeout(self) :
        txn=self.env.txn_begin()
        txn.set_timeout(1234567, db.DB_SET_LOCK_TIMEOUT)
        txn.set_timeout(2345678, flags=db.DB_SET_TXN_TIMEOUT)
        txn.abort()

    #----------------------------------------

    def test_get_tx_max(self) :
        self.assertEqual(self.env.get_tx_max(), 30)

    def test_get_tx_timestamp(self) :
        self.assertEqual(self.env.get_tx_timestamp(), self._t)

    #----------------------------------------

    @unittest.skipIf(db.version() < (5, 3),
                     'Requires Oracle Berkeley DB >= 5.3')
    def test_txn_get_priority(self):
        txn = self.env.txn_begin()
        self.assertEqual(100, txn.get_priority())
        txn.abort()

    @unittest.skipIf(db.version() < (5, 3),
                     'Requires Oracle Berkeley DB >= 5.3')
    def test_txn_set_priority(self):
        txn = self.env.txn_begin()
        txn.set_priority(12345)
        self.assertEqual(12345, txn.get_priority())
        txn.abort()

    def test_log_flush(self):
        txn = self.env.txn_begin(flags=db.DB_TXN_NOSYNC)
        self.d.put(b'test', b'result', txn=txn)
        txn.commit()
        log_stat = self.env.log_stat()
        pos_mem = (log_stat['cur_file'], log_stat['cur_offset'])
        pos_disk = (log_stat['disk_file'], log_stat['disk_offset'])
        self.assertGreater(pos_mem, pos_disk)
        self.env.log_flush()
        log_stat = self.env.log_stat()
        pos_mem2 = (log_stat['cur_file'], log_stat['cur_offset'])
        pos_disk2 = (log_stat['disk_file'], log_stat['disk_offset'])
        self.assertEqual(pos_mem2, pos_disk2)
        self.assertEqual(pos_mem, pos_disk2)

        # (cur_file, cur_lsn) says what offset will be used to write
        # the next transaction. Oracle Berkeley DB should allow to
        # flush up to that, but it doesn't work. So we create two
        # quite a few ACI transactions and flush only the first one.
        #
        # Oracle Berkeley DB will actually flush more than required,
        # probably as an optimization.

        txn = self.env.txn_begin(flags=db.DB_TXN_NOSYNC)
        self.d.put(b'test2', b'result2', txn=txn)
        txn.commit()
        log_stat = self.env.log_stat()
        pos_mem = (log_stat['cur_file'], log_stat['cur_offset'])
        pos_disk = (log_stat['disk_file'], log_stat['disk_offset'])
        self.assertGreater(pos_mem, pos_disk)
        for i in range(1000):
            txn = self.env.txn_begin(flags=db.DB_TXN_NOSYNC)
            self.d.put(f'test_{i}'.encode('ascii'),
                       f'result_{i}'.encode('ascii'), txn=txn)
            txn.commit()
        self.env.log_flush(pos_mem)
        log_stat = self.env.log_stat()
        pos_mem2 = (log_stat['cur_file'], log_stat['cur_offset'])
        pos_disk2 = (log_stat['disk_file'], log_stat['disk_offset'])
        self.assertLess(pos_mem, pos_disk2)
        self.assertGreaterEqual(pos_mem2, pos_disk2)

    @unittest.skipIf(db.version() < (5, 3),
                     'Oracle Berkeley DB 4.8 has no get/set_lk_exclusive')
    def test_set_lk_exclusive(self):
        d2 = db.DB(self.env)
        try:
            d2.set_lk_exclusive(True)
            self.assertRaises(db.DBLockNotGrantedError,
                              d2.open, self.filename)
        finally:
            d2.close()



class BTreeTransactionTestCase(BasicTransactionTestCase):
    dbtype = db.DB_BTREE

class HashTransactionTestCase(BasicTransactionTestCase):
    dbtype = db.DB_HASH



#----------------------------------------------------------------------

class BTreeRecnoTestCase(BasicTestCase):
    dbtype     = db.DB_BTREE
    dbsetflags = db.DB_RECNUM

    def test09_RecnoInBTree(self):
        d = self.d
        if verbose:
            print('\n', '-=' * 30)
            print("Running %s.test09_RecnoInBTree..." % self.__class__.__name__)

        rec = d.get(200)
        self.assertEqual(type(rec), type(()))
        self.assertEqual(len(rec), 2)
        if verbose:
            print("Record #200 is ", rec)

        c = d.cursor()
        c.set(b'0200')
        num = c.get_recno()
        self.assertEqual(type(num), type(1))
        if verbose:
            print("recno of d[b'0200'] is ", num)

        rec = c.current()
        self.assertEqual(c.set_recno(num), rec)

        c.close()



class BTreeRecnoWithThreadFlagTestCase(BTreeRecnoTestCase):
    dbopenflags = db.DB_THREAD

#----------------------------------------------------------------------

class BasicDUPTestCase(BasicTestCase):
    dbsetflags = db.DB_DUP

    def test10_DuplicateKeys(self):
        d = self.d
        if verbose:
            print('\n', '-=' * 30)
            print("Running %s.test10_DuplicateKeys..." % \
                  self.__class__.__name__)

        d.put(b'dup0', b'before')
        for x in b'The quick brown fox jumped over the lazy dog.'.split():
            d.put(b'dup1', x)
        d.put(b'dup2', b'after')

        data = d.get(b'dup1')
        self.assertEqual(data, b'The')
        if verbose:
            print(data)

        c = d.cursor()
        rec = c.set(b'dup1')
        self.assertEqual(rec, (b'dup1', b'The'))

        next_reg = c.next()
        self.assertEqual(next_reg, (b'dup1', b'quick'))

        rec = c.set(b'dup1')
        count = c.count()
        self.assertEqual(count, 9)

        next_dup = c.next_dup()
        self.assertEqual(next_dup, (b'dup1', b'quick'))

        rec = c.set(b'dup1')
        while rec is not None:
            if verbose:
                print(rec)
            rec = c.next_dup()

        c.set(b'dup1')
        rec = c.next_nodup()
        self.assertNotEqual(rec[0], b'dup1')
        if verbose:
            print(rec)

        c.close()



class BTreeDUPTestCase(BasicDUPTestCase):
    dbtype = db.DB_BTREE

class HashDUPTestCase(BasicDUPTestCase):
    dbtype = db.DB_HASH

class BTreeDUPWithThreadTestCase(BasicDUPTestCase):
    dbtype = db.DB_BTREE
    dbopenflags = db.DB_THREAD

class HashDUPWithThreadTestCase(BasicDUPTestCase):
    dbtype = db.DB_HASH
    dbopenflags = db.DB_THREAD


#----------------------------------------------------------------------

class BasicMultiDBTestCase(BasicTestCase):
    dbname = 'first'

    def otherType(self):
        if self.dbtype == db.DB_BTREE:
            return db.DB_HASH
        else:
            return db.DB_BTREE

    def test11_MultiDB(self):
        d1 = self.d
        if verbose:
            print('\n', '-=' * 30)
            print("Running %s.test11_MultiDB..." % self.__class__.__name__)

        d2 = db.DB(self.env)
        d2.open(self.filename, "second", self.dbtype,
                self.dbopenflags|db.DB_CREATE)
        d3 = db.DB(self.env)
        d3.open(self.filename, "third", self.otherType(),
                self.dbopenflags|db.DB_CREATE)

        for x in b'The quick brown fox jumped over the lazy dog'.split():
            d2.put(x, self.makeData(x))

        for x in printable_bytes:
            d3.put(x, x*70)

        d1.sync()
        d2.sync()
        d3.sync()
        d1.close()
        d2.close()
        d3.close()

        self.d = d1 = d2 = d3 = None

        self.d = d1 = db.DB(self.env)
        d1.open(self.filename, self.dbname, flags = self.dbopenflags)
        d2 = db.DB(self.env)
        d2.open(self.filename, "second",  flags = self.dbopenflags)
        d3 = db.DB(self.env)
        d3.open(self.filename, "third", flags = self.dbopenflags)

        c1 = d1.cursor()
        c2 = d2.cursor()
        c3 = d3.cursor()

        count = 0
        rec = c1.first()
        while rec is not None:
            count = count + 1
            if verbose and (count % 50) == 0:
                print(rec)
            rec = c1.next()
        self.assertEqual(count, self._numKeys)

        count = 0
        rec = c2.first()
        while rec is not None:
            count = count + 1
            if verbose:
                print(rec)
            rec = c2.next()
        self.assertEqual(count, 9)

        count = 0
        rec = c3.first()
        while rec is not None:
            count = count + 1
            if verbose:
                print(rec)
            rec = c3.next()
        self.assertEqual(count, len(printable_bytes))


        c1.close()
        c2.close()
        c3.close()

        d2.close()
        d3.close()



# Strange things happen if you try to use Multiple DBs per file without a
# DBEnv with MPOOL and LOCKing...

class BTreeMultiDBTestCase(BasicMultiDBTestCase):
    dbtype = db.DB_BTREE
    dbopenflags = db.DB_THREAD
    useEnv = 1
    envflags = db.DB_THREAD | db.DB_INIT_MPOOL | db.DB_INIT_LOCK

class HashMultiDBTestCase(BasicMultiDBTestCase):
    dbtype = db.DB_HASH
    dbopenflags = db.DB_THREAD
    useEnv = 1
    envflags = db.DB_THREAD | db.DB_INIT_MPOOL | db.DB_INIT_LOCK


class PrivateObject(unittest.TestCase) :
    def tearDown(self) :
        del self.obj

    def test01_DefaultIsNone(self) :
        self.assertEqual(self.obj.get_private(), None)

    def test02_assignment(self) :
        a = "example of private object"
        self.obj.set_private(a)
        b = self.obj.get_private()
        self.assertTrue(a is b)  # Object identity

    def test03_leak_assignment(self) :
        a = "example of private object"
        refcount = sys.getrefcount(a)
        self.obj.set_private(a)
        self.assertEqual(refcount+1, sys.getrefcount(a))
        self.obj.set_private(None)
        self.assertEqual(refcount, sys.getrefcount(a))

    def test04_leak_GC(self) :
        a = "example of private object"
        refcount = sys.getrefcount(a)
        self.obj.set_private(a)
        self.obj = None
        self.assertEqual(refcount, sys.getrefcount(a))

class DBEnvPrivateObject(PrivateObject) :
    def setUp(self) :
        self.obj = db.DBEnv()

class DBPrivateObject(PrivateObject) :
    def setUp(self) :
        self.obj = db.DB()


class open_path(unittest.TestCase):
    def test01_open_env_path(self):
        homeDir = pathlib.Path(get_new_environment_path())
        env = db.DBEnv()
        try:
            env.open(homeDir, db.DB_CREATE)
        finally:
            env.close()
            rmtree(homeDir)

    def test02_open_env_None(self):
        env = db.DBEnv()
        try:
            os.environ['DB_HOME'] = get_new_environment_path()
            env.open(None, db.DB_CREATE | db.DB_USE_ENVIRON)
        finally:
            env.close()
            rmtree(os.environ['DB_HOME'])

    def test03_open_env_None_keywords(self):
        env = db.DBEnv()
        try:
            os.environ['DB_HOME'] = get_new_environment_path()
            env.open(flags=db.DB_CREATE | db.DB_USE_ENVIRON)
        finally:
            env.close()
            rmtree(os.environ['DB_HOME'])

    def test04_open_db_path(self):
        filename = pathlib.Path(get_new_database_path())
        dbname = 'test'
        database = db.DB()
        try:
            database.open(filename, dbname, db.DB_HASH, db.DB_CREATE, 0o660)
            self.assertEqual(database.get_dbname(),
                    (filename.as_posix(), 'test'))
        finally:
            database.close()
            os.remove(filename)

    def test05_open_db_path_keywords(self):
        filename = pathlib.Path(get_new_database_path())
        dbname = 'test'
        database = db.DB()
        try:
            database.open(filename, dbname=dbname, dbtype=db.DB_HASH,
                          flags=db.DB_CREATE, mode=0o660)
            self.assertEqual(database.get_dbname(),
                    (filename.as_posix(), 'test'))
        finally:
            database.close()
            os.remove(filename)

    def test06_open_db_path_no_dbname(self):
        filename = pathlib.Path(get_new_database_path())
        database = db.DB()
        try:
            database.open(filename, db.DB_HASH, db.DB_CREATE, 0o660)
            self.assertEqual(database.get_dbname(),
                    (filename.as_posix(), None))
        finally:
            database.close()
            os.remove(filename)

    def test07_open_db_path_no_dbname_keywords(self):
        filename = pathlib.Path(get_new_database_path())
        database = db.DB()
        try:
            database.open(filename, dbtype=db.DB_HASH,
                          flags=db.DB_CREATE, mode=0o660)
            self.assertEqual(database.get_dbname(),
                    (filename.as_posix(), None))
        finally:
            database.close()
            os.remove(filename)

    def test08_open_db_missing(self):
        database = db.DB()
        self.assertRaises(TypeError, database.open,
                          db.DB_HASH, db.DB_CREATE, 0o660)

    def test09_open_db_missing_keywords(self):
        database = db.DB()
        try:
            database.open(dbtype=db.DB_HASH,
                          flags=db.DB_CREATE, mode=0o660)
            self.assertEqual(database.get_dbname(), (None, None))
        finally:
            database.close()

    def test10_open_db_none(self):
        database = db.DB()
        try:
            database.open(None, db.DB_HASH, db.DB_CREATE, 0o660)
            self.assertEqual(database.get_dbname(), (None, None))
        finally:
            database.close()

    def test11_open_db_none_keywords(self):
        database = db.DB()
        try:
            database.open(None, dbtype=db.DB_HASH,
                          flags=db.DB_CREATE, mode=0o660)
            self.assertEqual(database.get_dbname(), (None, None))
        finally:
            database.close()

    def test12_open_db_none_none(self):
        database = db.DB()
        try:
            database.open(None, None, db.DB_HASH, db.DB_CREATE, 0o660)
            self.assertEqual(database.get_dbname(), (None, None))
        finally:
            database.close()

    def test13_open_db_none_none_keywords(self):
        database = db.DB()
        try:
            database.open(None, dbname=None, dbtype=db.DB_HASH,
                          flags=db.DB_CREATE, mode=0o660)
            self.assertEqual(database.get_dbname(), (None, None))
        finally:
            database.close()

    def test14_open_db_none_dbname(self):
        database = db.DB()
        try:
            database.open(None, 'test', db.DB_HASH, db.DB_CREATE, 0o660)
            self.assertEqual(database.get_dbname(), (None, 'test'))
        finally:
            database.close()

    def test15_open_db_none_dbname_keywords(self):
        database = db.DB()
        try:
            database.open(None, dbname='test', dbtype=db.DB_HASH,
                          flags=db.DB_CREATE, mode=0o660)
            self.assertEqual(database.get_dbname(), (None, 'test'))
        finally:
            database.close()

    def test16_open_db_missing_dbname_keywords(self):
        database = db.DB()
        try:
            database.open(dbname='test', dbtype=db.DB_HASH,
                          flags=db.DB_CREATE, mode=0o660)
            self.assertEqual(database.get_dbname(), (None, 'test'))
        finally:
            database.close()


#----------------------------------------------------------------------
#----------------------------------------------------------------------

def test_suite():
    suite = unittest.TestSuite()
    for test in (VersionTestCase,
                    BasicBTreeTestCase,
                    BasicHashTestCase,
                    BasicBTreeWithThreadFlagTestCase,
                    BasicHashWithThreadFlagTestCase,
                    BasicBTreeWithEnvTestCase,
                    BasicHashWithEnvTestCase,
                    BTreeTransactionTestCase,
                    HashTransactionTestCase,
                    BTreeRecnoTestCase,
                    BTreeRecnoWithThreadFlagTestCase,
                    BTreeDUPTestCase,
                    HashDUPTestCase,
                    BTreeDUPWithThreadTestCase,
                    HashDUPWithThreadTestCase,
                    BTreeMultiDBTestCase,
                    HashMultiDBTestCase,
                    DBEnvPrivateObject,
                    DBPrivateObject,
                    open_path,):

        test = unittest.defaultTestLoader.loadTestsFromTestCase(test)
        suite.addTest(test)

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
