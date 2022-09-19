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

import unittest
import os, glob

from .test_all import db, rmtree, get_new_environment_path, \
        get_new_database_path

#----------------------------------------------------------------------

class pget_bugTestCase(unittest.TestCase):
    """Verify that cursor.pget works properly"""
    db_name = 'test-cursor_pget.db'

    def setUp(self):
        self.homeDir = get_new_environment_path()
        self.env = db.DBEnv()
        self.env.open(self.homeDir, db.DB_CREATE | db.DB_INIT_MPOOL)
        self.primary_db = db.DB(self.env)
        self.primary_db.open(self.db_name, 'primary', db.DB_BTREE, db.DB_CREATE)
        self.secondary_db = db.DB(self.env)
        self.secondary_db.set_flags(db.DB_DUP)
        self.secondary_db.open(self.db_name, 'secondary', db.DB_BTREE, db.DB_CREATE)
        self.primary_db.associate(self.secondary_db, lambda key, data: data)
        self.primary_db.put(b'salad', b'eggs')
        self.primary_db.put(b'spam', b'ham')
        self.primary_db.put(b'omelet', b'eggs')


    def tearDown(self):
        self.secondary_db.close()
        self.primary_db.close()
        self.env.close()
        del self.secondary_db
        del self.primary_db
        del self.env
        rmtree(self.homeDir)

    def test_pget(self):
        cursor = self.secondary_db.cursor()

        self.assertEqual((b'eggs', b'salad', b'eggs'),
                         cursor.pget(key=b'eggs', flags=db.DB_SET))
        self.assertEqual((b'eggs', b'omelet', b'eggs'),
                         cursor.pget(db.DB_NEXT_DUP))
        self.assertEqual(None, cursor.pget(db.DB_NEXT_DUP))

        self.assertEqual((b'ham', b'spam', b'ham'), cursor.pget(b'ham', b'spam', flags=db.DB_SET))
        self.assertEqual(None, cursor.pget(db.DB_NEXT_DUP))

        cursor.close()


def test_suite():
    suite = unittest.TestSuite()
    for test in (pget_bugTestCase,):
        test = unittest.defaultTestLoader.loadTestsFromTestCase(test)
        suite.addTest(test)

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
