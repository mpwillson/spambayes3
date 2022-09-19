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

"""TestCases for checking that it does not segfault when a DBEnv object
is closed before its DB objects.
"""

import os, sys
import unittest

from .test_all import db, rmtree, verbose, get_new_environment_path, get_new_database_path

#----------------------------------------------------------------------

class DBEnvConcurrent_Data_Store(unittest.TestCase):
    def setUp(self):
        self.homeDir = get_new_environment_path()
        self.dbenv = db.DBEnv()
        self.dbenv.open(self.homeDir,
                        db.DB_INIT_CDB | db.DB_INIT_MPOOL | db.DB_CREATE,
                        0o666)

    def tearDown(self):
        self.dbenv.close()
        rmtree(self.homeDir)

    def test01_cdsgroup_begin_commit(self):
        txn = self.dbenv.cdsgroup_begin()
        txn.commit()

    def test02_cdsgroup_begin_abort(self):
        txn = self.dbenv.cdsgroup_begin()
        # Concurrent Data Store can't abort transactions
        with self.assertRaises(db.DBError):
            txn.abort()

#----------------------------------------------------------------------

def test_suite():
    suite = unittest.TestSuite()
    for test in (DBEnvConcurrent_Data_Store,):
        test = unittest.defaultTestLoader.loadTestsFromTestCase(test)
        suite.addTest(test)

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
