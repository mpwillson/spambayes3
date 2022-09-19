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
TestCases for checking set_get_returns_none.
"""

import os
import unittest


from .test_all import db, verbose, rmtree, get_new_environment_path, \
        get_new_database_path, printable_bytes


#----------------------------------------------------------------------

class GetReturnsNoneTestCase(unittest.TestCase):
    def _getEnv(self):
        return None

    def setUp(self):
        self.Env = self._getEnv()
        self.filename = "test_db" if self.Env else get_new_database_path()
        self.db = db.DB(self.Env)
        self.db.open(self.filename, db.DB_BTREE, db.DB_CREATE)

    def tearDown(self):
        self.db.close()
        try:
            os.remove(self.filename)
        except os.error:
            pass
        if self.Env:
            self.Env.close()
            rmtree(self.homeDir)


    def test01_get_returns_none_default(self):
        d = self.db

        for x in printable_bytes:
            d.put(x, x * 40)

        data = d.get(b'bad key')
        self.assertEqual(data, None)

        data = d.get(printable_bytes[31])
        self.assertEqual(data, printable_bytes[31]*40)

        count = 0
        c = d.cursor()
        try:
            rec = c.first()
            while rec:
                count = count + 1
                rec = c.next()

            self.assertEqual(rec, None)
            self.assertEqual(count, len(printable_bytes))
        finally:
            c.close()


    def test02_get_returns_none(self):
        self.db.set_get_returns_none(1)
        return self.test01_get_returns_none_default()


    def test03_get_raises_exception(self):
        d = self.db
        d.set_get_returns_none(0)

        for x in printable_bytes:
            d.put(x, x * 40)

        self.assertRaises(db.DBNotFoundError, d.get, b'bad key')
        self.assertRaises(KeyError, d.get, b'bad key')

        data = d.get(printable_bytes[11])
        self.assertEqual(data, printable_bytes[11]*40)

        count = 0
        exceptionHappened = 0
        c = d.cursor()
        try:
            rec = c.first()
            while rec:
                count = count + 1
                try:
                    rec = c.next()
                except db.DBNotFoundError:  # end of the records
                    exceptionHappened = 1
                    break

            self.assertNotEqual(rec, None)
            self.assertTrue(exceptionHappened)
            self.assertEqual(count, len(printable_bytes))
        finally:
            c.close()


class GetEnvReturnsNoneTestCase(GetReturnsNoneTestCase):
    def _getEnv(self):
        self.homeDir = get_new_environment_path()
        dbenv = db.DBEnv()
        dbenv.open(self.homeDir, db.DB_CREATE | db.DB_INIT_MPOOL |
                   db.DB_INIT_LOG | db.DB_INIT_LOCK | db.DB_INIT_TXN)
        return dbenv


class GetEnvReturnsNoneBUG(unittest.TestCase):
    def test01_Env_flags_not_inherited(self):
        homeDir = get_new_environment_path()
        dbenv = db.DBEnv()
        dbenv.open(homeDir, db.DB_CREATE | db.DB_INIT_MPOOL |
                   db.DB_INIT_LOG | db.DB_INIT_LOCK | db.DB_INIT_TXN)

        for flag in (0, 1, 2):
            dbenv.set_get_returns_none(flag)
            d = db.DB(dbenv)
            d.open('test_db', db.DB_BTREE, db.DB_CREATE)

            # The function should return previous value
            # inherited from the environment.
            self.assertEqual(flag, d.set_get_returns_none(flag))
            d.close()

        dbenv.close()
        rmtree(homeDir)


#----------------------------------------------------------------------

def test_suite():
    suite = unittest.TestSuite()
    for test in (GetReturnsNoneTestCase,
                    GetEnvReturnsNoneTestCase,
                    GetEnvReturnsNoneBUG,):

        test = unittest.defaultTestLoader.loadTestsFromTestCase(test)
        suite.addTest(test)

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
