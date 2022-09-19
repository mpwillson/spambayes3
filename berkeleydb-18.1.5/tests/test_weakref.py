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


import sys
import weakref
import unittest

from .test_all import db, dbobj, rmtree, get_new_environment_path, \
        get_new_database_path

#----------------------------------------------------------------------

class db_weakref(unittest.TestCase):
    def _test(self, obj, *args, **kwargs):
        obj = obj(*args, **kwargs)
        ref = weakref.ref(obj)
        self.assertEqual(obj, ref())
        del obj
        self.assertEqual(None, ref())


    @unittest.skipIf(sys.version_info < (3, 9),
                     'No weakref support for heaptypes')
    def test_DBEnv(self):
        return self._test(db.DBEnv)


    @unittest.skipIf(sys.version_info < (3, 9),
                     'No weakref support for heaptypes')
    def test_DB(self):
        return self._test(db.DB)


class db_weakrefDBEnv(unittest.TestCase):
    def setUp(self):
        self.homeDir = get_new_environment_path()
        self.dbenv = db.DBEnv()
        self.dbenv.open(self.homeDir, db.DB_CREATE | db.DB_INIT_MPOOL |
                        db.DB_INIT_LOG | db.DB_INIT_LOCK | db.DB_INIT_TXN |
                        db.DB_INIT_REP)
        self.db = db.DB(self.dbenv)
        self.db.open(None, None, db.DB_HASH, db.DB_CREATE)


    def tearDown(self):
        self.db.close()

        self.dbenv.close()
        rmtree(self.homeDir)


    def _test(self, obj, *args, **kwargs):
        obj = obj(*args, **kwargs)
        ref = weakref.ref(obj)
        self.assertEqual(obj, ref())
        del obj
        self.assertEqual(None, ref())


    @unittest.skipIf(sys.version_info < (3, 9),
                     'No weakref support for heaptypes')
    def test_DBCursor(self):
        self._test(self.db.cursor)


    @unittest.skipIf(sys.version_info < (3, 9),
                     'No weakref support for heaptypes')
    def test_DBLogCursor(self):
        self._test(self.dbenv.log_cursor)


    @unittest.skipIf(sys.version_info < (3, 9),
                     'No weakref support for heaptypes')
    def test_DBSequence(self):
        self._test(db.DBSequence, self.db)


    @unittest.skipIf(sys.version_info < (3, 9),
                     'No weakref support for heaptypes')
    def test_DBTxn(self):
        txn = self.dbenv.txn_begin()
        ref = weakref.ref(txn)
        self.assertEqual(txn, ref())
        txn.abort()
        del txn
        self.assertEqual(None, ref())


    @unittest.skipIf(sys.version_info < (3, 9),
                     'No weakref support for heaptypes')
    def test_DBLock(self):
        lock_id = self.dbenv.lock_id()
        try:
            lock = self.dbenv.lock_get(lock_id, 'test', db.DB_LOCK_READ)
            ref = weakref.ref(lock)
            self.assertEqual(lock, ref())
            self.dbenv.lock_put(lock)
            del lock
            self.assertEqual(None, ref())
        finally:
            self.dbenv.lock_id_free(lock_id)


    @unittest.skipIf(sys.version_info < (3, 9),
                     'No weakref support for heaptypes')
    @unittest.skipIf(db.version() < (5, 3),
                     f'Oracle Berkeley DB {db.version()} has no support '
                     'for DBSite')
    def test_DBSite(self):
        dbsite = self.dbenv.repmgr_site('0.0.0.0', 1234)
        ref = weakref.ref(dbsite)
        self.assertEqual(dbsite, ref())
        del dbsite
        self.assertEqual(None, ref())


#----------------------------------------------------------------------

def test_suite():
    suite = unittest.TestSuite()
    for test in (db_weakref, db_weakrefDBEnv):
        test = unittest.defaultTestLoader.loadTestsFromTestCase(test)
        suite.addTest(test)

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
