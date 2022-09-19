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

import os
import pickle
import sys
import unittest

from .test_all import db, rmtree, get_new_environment_path, get_new_database_path

#----------------------------------------------------------------------

class pickleTestCase(unittest.TestCase):
    """Verify that DBError can be pickled and unpickled"""
    db_name = 'test-dbobj.db'

    def setUp(self):
        self.homeDir = get_new_environment_path()

    def tearDown(self):
        if hasattr(self, 'db'):
            del self.db
        if hasattr(self, 'env'):
            del self.env
        rmtree(self.homeDir)

    def _base_test_pickle_DBError(self, pickle):
        self.env = db.DBEnv()
        self.env.open(self.homeDir, db.DB_CREATE | db.DB_INIT_MPOOL)
        self.db = db.DB(self.env)
        self.db.open(self.db_name, db.DB_HASH, db.DB_CREATE)
        self.db.put(b'spam', b'eggs')
        self.assertEqual(self.db[b'spam'], b'eggs')
        try:
            self.db.put(b'spam', b'ham', flags=db.DB_NOOVERWRITE)
        except db.DBError as egg:
            pickledEgg = pickle.dumps(egg)
            #print repr(pickledEgg)
            rottenEgg = pickle.loads(pickledEgg)
            if rottenEgg.args != egg.args or type(rottenEgg) != type(egg):
                raise Exception(rottenEgg, '!=', egg)
        else:
            raise Exception("where's my DBError exception?!?")

        self.db.close()
        self.env.close()

    def test01_pickle_DBError(self):
        self._base_test_pickle_DBError(pickle=pickle)

#----------------------------------------------------------------------

def test_suite():
    suite = unittest.TestSuite()
    for test in (pickleTestCase,):
        test = unittest.defaultTestLoader.loadTestsFromTestCase(test)
        suite.addTest(test)

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
