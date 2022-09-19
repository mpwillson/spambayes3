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

"""Miscellaneous berkeleydb module test cases
"""

import os, sys
import unittest

from .test_all import db, dbshelve, hashopen, rmtree, unlink, \
        get_new_environment_path, get_new_database_path

#----------------------------------------------------------------------

class MiscTestCase(unittest.TestCase):
    def setUp(self):
        self.filename = get_new_database_path()
        self.homeDir = get_new_environment_path()

    def tearDown(self):
        unlink(self.filename)
        rmtree(self.homeDir)

    def test01_badpointer(self):
        dbs = dbshelve.open(self.filename)
        dbs.close()
        self.assertRaises(db.DBError, dbs.get, "foo")

    def test02_db_home(self):
        env = db.DBEnv()
        # check for crash fixed when db_home is used before open()
        self.assertTrue(env.db_home is None)
        env.open(self.homeDir, db.DB_CREATE)
        self.assertEqual(bytes(self.homeDir, "ascii"), env.db_home)

    def test03_repr_closed_db(self):
        db = hashopen(self.filename)
        db.close()
        rp = repr(db)
        self.assertEqual(rp, "{}")

    def test04_repr_db(self) :
        db = hashopen(self.filename)
        d = {}
        for i in range(100) :
            db[b'%d' % i] = b'%d' % 100*i
            d[b'%d' % i] = b'%d' % 100*i
        db.close()
        db = hashopen(self.filename)
        rp = repr(sorted(db.items()))
        rd = repr(sorted(d.items()))
        self.assertEqual(rp, rd)
        db.close()

    # http://sourceforge.net/tracker/index.php?func=detail&aid=1708868&group_id=13900&atid=313900
    #
    # See the bug report for details.
    #
    # The problem was that make_key_dbt() was not allocating a copy of
    # string keys but FREE_DBT() was always being told to free it when the
    # database was opened with DB_THREAD.
    def test05_double_free_make_key_dbt(self):
        try:
            db1 = db.DB()
            db1.open(self.filename, None, db.DB_BTREE,
                     db.DB_CREATE | db.DB_THREAD)

            curs = db1.cursor()
            t = curs.get(b'/foo', db.DB_SET)
            # double free happened during exit from DBC_get
        finally:
            db1.close()
            unlink(self.filename)

    def test06_key_with_null_bytes(self):
        try:
            db1 = db.DB()
            db1.open(self.filename, None, db.DB_HASH, db.DB_CREATE)
            db1[b'a'] = b'eh?'
            db1[b'a\x00'] = b'eh zed.'
            db1[b'a\x00a'] = b'eh zed eh?'
            db1[b'aaa'] = b'eh eh eh!'
            keys = list(db1.keys())
            keys.sort()
            self.assertEqual([b'a', b'a\x00', b'a\x00a', b'aaa'], keys)
            self.assertEqual(db1[b'a'], b'eh?')
            self.assertEqual(db1[b'a\x00'], b'eh zed.')
            self.assertEqual(db1[b'a\x00a'], b'eh zed eh?')
            self.assertEqual(db1[b'aaa'], b'eh eh eh!')
        finally:
            db1.close()
            unlink(self.filename)

    def test07_DB_set_flags_persists(self):
        try:
            db1 = db.DB()
            db1.set_flags(db.DB_DUPSORT)
            db1.open(self.filename, db.DB_HASH, db.DB_CREATE)
            db1[b'a'] = b'eh'
            db1[b'a'] = b'A'
            self.assertEqual([(b'a', b'A')], list(db1.items()))
            db1.put(b'a', b'Aa')
            self.assertEqual([(b'a', b'A'), (b'a', b'Aa')], list(db1.items()))
            db1.close()
            db1 = db.DB()
            # no set_flags call, we're testing that it reads and obeys
            # the flags on open.
            db1.open(self.filename, db.DB_HASH)
            self.assertEqual([(b'a', b'A'), (b'a', b'Aa')], list(db1.items()))
            # if it read the flags right this will replace all values
            # for key 'a' instead of adding a new one.  (as a dict should)
            db1[b'a'] = b'new A'
            self.assertEqual([(b'a', b'new A')], list(db1.items()))
        finally:
            db1.close()
            unlink(self.filename)


    def test08_ExceptionTypes(self) :
        self.assertTrue(issubclass(db.DBError, Exception))
        for i, j in list(db.__dict__.items()) :
            if i.startswith("DB") and i.endswith("Error") :
                self.assertTrue(issubclass(j, db.DBError), msg=i)
                if i not in ("DBKeyEmptyError", "DBNotFoundError") :
                    self.assertFalse(issubclass(j, KeyError), msg=i)

        # This two exceptions have two bases
        self.assertTrue(issubclass(db.DBKeyEmptyError, KeyError))
        self.assertTrue(issubclass(db.DBNotFoundError, KeyError))


#----------------------------------------------------------------------


def test_suite():
    suite = unittest.TestSuite()
    for test in (MiscTestCase,):
        test = unittest.defaultTestLoader.loadTestsFromTestCase(test)
        suite.addTest(test)

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
