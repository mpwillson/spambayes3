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
TestCases for checking dbShelve objects.
"""

import os, string, sys
import random
import unittest

printable_bytes = string.printable.encode('iso-8859-1')  # Transparent_encoding


from .test_all import db, dbshelve, rmtree, unlink, verbose, \
        get_new_environment_path, get_new_database_path





#----------------------------------------------------------------------

# We want the objects to be comparable so we can test dbshelve.values
# later on.
class DataClass:
    def __init__(self):
        self.value = random.random()

    def __repr__(self):
        return "DataClass %f" % self.value


class DBShelveTestCase(unittest.TestCase):
    def setUp(self):
        self.filename = get_new_database_path()
        self.do_open()

    def tearDown(self):
        self.do_close()
        unlink(self.filename)

    def mk(self, key):
        """Turn key into an appropriate key type for this db"""
        # override in child class for RECNO
        return key

    def populateDB(self, d):
        for x in printable_bytes:
            xx = b'%c' % x
            d[self.mk(b'S%c' % x)] = 10 * xx    # add bytes
            d[self.mk(b'I%c' % x)] = x          # add an integer
            d[self.mk(b'L%c' % x)] = [xx] * 10  # add a list

            inst = DataClass()            # add an instance
            inst.S = 10 * xx
            inst.I = x
            inst.L = [xx] * 10
            d[self.mk(b'O%c' % x)] = inst


    # overridable in derived classes to affect how the shelf is created/opened
    def do_open(self):
        self.d = dbshelve.open(self.filename)

    # and closed...
    def do_close(self):
        self.d.close()



    def test01_basics(self):
        if verbose:
            print('\n', '-=' * 30)
            print("Running %s.test01_basics..." % self.__class__.__name__)

        self.populateDB(self.d)
        self.d.sync()
        self.do_close()
        self.do_open()
        d = self.d

        l = len(d)
        k = list(d.keys())
        s = d.stat()
        f = d.fd()

        if verbose:
            print("length:", l)
            print("keys:", k)
            print("stats:", s)

        self.assertEqual(0, self.mk(b'bad key') in d)
        self.assertEqual(1, self.mk(b'IA') in d)
        self.assertEqual(1, self.mk(b'OA') in d)

        d.delete(self.mk(b'IA'))
        del d[self.mk(b'OA')]
        self.assertEqual(0, self.mk(b'IA') in d)
        self.assertEqual(0, self.mk(b'OA') in d)
        self.assertEqual(len(d), l-2)

        values = []
        for key in list(d.keys()):
            value = d[key]
            values.append(value)
            if verbose:
                print("%s: %s" % (key, value))
            self.checkrec(key, value)

        dbvalues = list(d.values())
        self.assertEqual(len(dbvalues), len(list(d.keys())))
        # XXX: Convert all to strings. Please, improve
        values.sort(key=lambda x: repr(x))
        dbvalues.sort(key=lambda x: repr(x))
        self.assertEqual(repr(values), repr(dbvalues))

        items = list(d.items())
        self.assertEqual(len(items), len(values))

        for key, value in items:
            self.checkrec(key, value)

        self.assertEqual(d.get(self.mk(b'bad key')), None)
        self.assertEqual(d.get(self.mk(b'bad key'), None), None)
        self.assertEqual(d.get(self.mk(b'bad key'), b'a string'), b'a string')
        self.assertEqual(d.get(self.mk(b'bad key'), [1, 2, 3]), [1, 2, 3])

        d.set_get_returns_none(0)
        self.assertRaises(db.DBNotFoundError, d.get, self.mk(b'bad key'))
        d.set_get_returns_none(1)

        d.put(self.mk(b'new key'), b'new data')
        self.assertEqual(d.get(self.mk(b'new key')), b'new data')
        self.assertEqual(d[self.mk(b'new key')], b'new data')



    def test02_cursors(self):
        if verbose:
            print('\n', '-=' * 30)
            print("Running %s.test02_cursors..." % self.__class__.__name__)

        self.populateDB(self.d)
        d = self.d

        count = 0
        c = d.cursor()
        rec = c.first()
        while rec is not None:
            count = count + 1
            if verbose:
                print(rec)
            key, value = rec
            self.checkrec(key, value)
            rec = c.next()
        del c

        self.assertEqual(count, len(d))

        count = 0
        c = d.cursor()
        rec = c.last()
        while rec is not None:
            count = count + 1
            if verbose:
                print(rec)
            key, value = rec
            self.checkrec(key, value)
            rec = c.prev()

        self.assertEqual(count, len(d))

        c.set(self.mk(b'SS'))
        key, value = c.current()
        self.checkrec(key, value)
        del c


    def test03_append(self):
        # NOTE: this is overridden in RECNO subclass, don't change its name.
        if verbose:
            print('\n', '-=' * 30)
            print("Running %s.test03_append..." % self.__class__.__name__)

        self.assertRaises(dbshelve.DBShelveError,
                          self.d.append, 'unit test was here')


    def test04_iterable(self) :
        self.populateDB(self.d)
        d = self.d
        keys = list(d.keys())
        keyset = set(keys)
        self.assertEqual(len(keyset), len(keys))

        for key in d :
            self.assertIn(key, keyset)
            keyset.remove(key)
        self.assertEqual(len(keyset), 0)

    def checkrec(self, key, value):
        # override this in a subclass if the key type is different

        x = key[1:2]
        if key[0:1] == b'S':
            self.assertEqual(type(value), bytes)
            self.assertEqual(value, 10 * x)

        elif key[0:1] == b'I':
            self.assertEqual(type(value), int)
            self.assertEqual(value, ord(x))

        elif key[0:1] == b'L':
            self.assertEqual(type(value), list)
            self.assertEqual(value, [x] * 10)

        elif key[0:1] == b'O':
            self.assertEqual(type(value), DataClass)

            self.assertEqual(value.S, 10 * x)
            self.assertEqual(value.I, ord(x))
            self.assertEqual(value.L, [x] * 10)

        else:
            self.assertTrue(0, 'Unknown key type, fix the test')

#----------------------------------------------------------------------

class BasicShelveTestCase(DBShelveTestCase):
    def do_open(self):
        self.d = dbshelve.DBShelf()
        self.d.open(self.filename, self.dbtype, self.dbflags)

    def do_close(self):
        self.d.close()


class BTreeShelveTestCase(BasicShelveTestCase):
    dbtype = db.DB_BTREE
    dbflags = db.DB_CREATE


class HashShelveTestCase(BasicShelveTestCase):
    dbtype = db.DB_HASH
    dbflags = db.DB_CREATE


class ThreadBTreeShelveTestCase(BasicShelveTestCase):
    dbtype = db.DB_BTREE
    dbflags = db.DB_CREATE | db.DB_THREAD


class ThreadHashShelveTestCase(BasicShelveTestCase):
    dbtype = db.DB_HASH
    dbflags = db.DB_CREATE | db.DB_THREAD


#----------------------------------------------------------------------

class BasicEnvShelveTestCase(DBShelveTestCase):
    def do_open(self):
        self.env = db.DBEnv()
        self.env.open(self.homeDir,
                self.envflags | db.DB_INIT_MPOOL | db.DB_CREATE)

        self.filename = os.path.split(self.filename)[1]
        self.d = dbshelve.DBShelf(self.env)
        self.d.open(self.filename, self.dbtype, self.dbflags)


    def do_close(self):
        self.d.close()
        self.env.close()


    def setUp(self) :
        self.homeDir = get_new_environment_path()
        DBShelveTestCase.setUp(self)

    def tearDown(self):
        self.do_close()
        rmtree(self.homeDir)


class EnvBTreeShelveTestCase(BasicEnvShelveTestCase):
    envflags = 0
    dbtype = db.DB_BTREE
    dbflags = db.DB_CREATE


class EnvHashShelveTestCase(BasicEnvShelveTestCase):
    envflags = 0
    dbtype = db.DB_HASH
    dbflags = db.DB_CREATE


class EnvThreadBTreeShelveTestCase(BasicEnvShelveTestCase):
    envflags = db.DB_THREAD
    dbtype = db.DB_BTREE
    dbflags = db.DB_CREATE | db.DB_THREAD


class EnvThreadHashShelveTestCase(BasicEnvShelveTestCase):
    envflags = db.DB_THREAD
    dbtype = db.DB_HASH
    dbflags = db.DB_CREATE | db.DB_THREAD


#----------------------------------------------------------------------
# test cases for a DBShelf in a RECNO DB.

class RecNoShelveTestCase(BasicShelveTestCase):
    dbtype = db.DB_RECNO
    dbflags = db.DB_CREATE

    def setUp(self):
        BasicShelveTestCase.setUp(self)

        # pool to assign integer key values out of
        self.key_pool = list(range(1, 5000))
        self.key_map = {}     # map string keys to the number we gave them
        self.intkey_map = {}  # reverse map of above

    def mk(self, key):
        if key not in self.key_map:
            self.key_map[key] = self.key_pool.pop(0)
            self.intkey_map[self.key_map[key]] = key
        return self.key_map[key]

    def checkrec(self, intkey, value):
        key = self.intkey_map[intkey]
        BasicShelveTestCase.checkrec(self, key, value)

    def test03_append(self):
        if verbose:
            print('\n', '-=' * 30)
            print("Running %s.test03_append..." % self.__class__.__name__)

        self.d[1] = b'spam'
        self.d[5] = b'eggs'
        self.assertEqual(6, self.d.append(b'spam'))
        self.assertEqual(7, self.d.append(b'baked beans'))
        self.assertEqual(b'spam', self.d.get(6))
        self.assertEqual(b'spam', self.d.get(1))
        self.assertEqual(b'baked beans', self.d.get(7))
        self.assertEqual(b'eggs', self.d.get(5))


#----------------------------------------------------------------------

def test_suite():
    suite = unittest.TestSuite()
    for test in (DBShelveTestCase,
                    BTreeShelveTestCase,
                    HashShelveTestCase,
                    ThreadBTreeShelveTestCase,
                    ThreadHashShelveTestCase,
                    EnvBTreeShelveTestCase,
                    EnvHashShelveTestCase,
                    EnvThreadBTreeShelveTestCase,
                    EnvThreadHashShelveTestCase,
                    RecNoShelveTestCase,):

        test = unittest.defaultTestLoader.loadTestsFromTestCase(test)
        suite.addTest(test)

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
