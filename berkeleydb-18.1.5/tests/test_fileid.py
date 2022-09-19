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

"""TestCase for reseting File ID.
"""

import os, sys
import shutil
import pathlib
import unittest

from .test_all import db, rmtree, unlink, get_new_environment_path, get_new_database_path

class FileidResetTestCase(unittest.TestCase):
    def setUp(self):
        self.db_path_1 = get_new_database_path()
        self.db_path_2 = get_new_database_path()
        self.db_env_path = get_new_environment_path()

    def _fileid_reset(self, path1, path2):
        # create DB 1
        self.db1 = db.DB()
        self.db1.open(path1, dbtype=db.DB_HASH, flags=(db.DB_CREATE|db.DB_EXCL))
        self.db1.put(b'spam', b'eggs')
        self.db1.close()

        shutil.copy(path1, path2)

        self.db2 = db.DB()
        self.db2.open(path2, dbtype=db.DB_HASH)
        self.db2.put(b'spam', b'spam')
        self.db2.close()

        self.db_env = db.DBEnv()
        self.db_env.open(self.db_env_path, db.DB_CREATE|db.DB_INIT_MPOOL)

        # use fileid_reset() here
        self.db_env.fileid_reset(path2)

        self.db1 = db.DB(self.db_env)
        self.db1.open(path1, dbtype=db.DB_HASH, flags=db.DB_RDONLY)
        self.assertEqual(self.db1.get(b'spam'), b'eggs')

        self.db2 = db.DB(self.db_env)
        self.db2.open(path2, dbtype=db.DB_HASH, flags=db.DB_RDONLY)
        self.assertEqual(self.db2.get(b'spam'), b'spam')

        self.db1.close()
        self.db2.close()

        self.db_env.close()

    def test_fileid_reset(self):
        return self._fileid_reset(self.db_path_1, self.db_path_2)

    def test_fileid_reset_path(self):
        db_path_1 = pathlib.Path(self.db_path_1)
        db_path_2 = pathlib.Path(self.db_path_2)
        return self._fileid_reset(db_path_1, db_path_2)

    def tearDown(self):
        unlink(self.db_path_1)
        unlink(self.db_path_2)
        rmtree(self.db_env_path)

def test_suite():
    suite = unittest.TestSuite()
    for test in (FileidResetTestCase,):
        test = unittest.defaultTestLoader.loadTestsFromTestCase(test)
        suite.addTest(test)

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
