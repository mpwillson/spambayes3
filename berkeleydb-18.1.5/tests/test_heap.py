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
import unittest

from .test_all import db, rmtree, get_new_environment_path, get_new_database_path

@unittest.skipIf(db.version() < (5, 3),
                 'Oracle Berkeley DB 4.8 has no HEAP access method support')
class HeapTestCase(unittest.TestCase):
    def setUp(self):
        self.homeDir = get_new_environment_path()
        self.env = db.DBEnv()
        self.env.open(self.homeDir, db.DB_CREATE | db.DB_INIT_MPOOL |
                                    db.DB_INIT_LOG | db.DB_INIT_TXN)
        self.db = db.DB(self.env)

    def tearDown(self):
        self.db.close()
        self.env.close()
        rmtree(self.homeDir)

class HeapTestCaseNoOpen(HeapTestCase):
    def test_heapsize_preOpen(self):
        self.assertEqual((0, 0), self.db.get_heapsize())
        self.db.set_heapsize(12, 3456789)
        self.assertEqual((12, 3456789), self.db.get_heapsize())

    def test_heap_regionsize_preOpen(self):
        self.assertEqual(0, self.db.get_heap_regionsize())
        self.db.set_heap_regionsize(123456789)
        self.assertEqual(123456789, self.db.get_heap_regionsize())


class HeapTestCaseOpen(HeapTestCase):
    def setUp(self):
        super().setUp()
        self.db.open(flags=db.DB_CREATE, dbtype=db.DB_HEAP)

    def test_heapsize_postOpen(self):
        self.assertEqual((0, 0), self.db.get_heapsize())
        self.assertRaises(db.DBInvalidArgError,
                          self.db.set_heapsize, 12, 3456789)

    def test_heap_regionsize_postOpen(self):
        self.assertLess(0, self.db.get_heap_regionsize())
        self.assertRaises(db.DBInvalidArgError,
                          self.db.set_heap_regionsize, 123456789)
    def test_stats(self):
        stat = self.db.stat()
        self.assertEqual(1, stat['nregions'])
        self.assertLess(0, stat['pagecnt'])
        self.assertLess(0, stat['pagesize'])
        self.assertEqual(0, stat['nrecs'])

    def test_append(self):
        self.assertIsInstance(self.db.append(data=b'value'), bytes)
        self.assertEqual(1, self.db.stat()['nrecs'])

    def test_put_overwrite(self):
        key = self.db.append(data=b'value')
        self.assertIsNone(self.db.put(key=key, data=b'value2'))
        self.assertEqual(1, self.db.stat()['nrecs'])

    def test_put_append(self):
        key = self.db.append(data=b'value')
        # If db.DB_APPEND, the key is ignored and a new record is stored
        key2 = self.db.put(key=key, data=b'value2', flags = db.DB_APPEND)
        self.assertNotEqual(key, key2)
        self.assertEqual(2, self.db.stat()['nrecs'])

    def test_append_get(self):
        key = self.db.append(data=b'value')
        value = self.db.get(key)
        self.assertEqual(value, b'value')

    @unittest.skipIf(db.version()[:2] != (5, 3),
                     'Oracle Berkeley DB 6.2 and 18.1 are faulty. Check '
                     'https://community.oracle.com/tech/developers/discussion/4478383/oracle-berkeley-db-heap-access-method-misscounts-records-in-db-stat/p1?new=1')
    def test_append_delete(self):
        key = self.db.append(data=b'value')
        self.assertEqual(1, self.db.stat()['nrecs'])
        self.db.delete(key)
        self.assertEqual(0, self.db.stat()['nrecs'])

    def test_not_found(self):
        self.assertIsNone(self.db.get(key=b'012345'))

    def test_cursor(self):
        keys = []
        for i in range(5):
            data = f'value{i}'.encode('ascii')
            keys.append((self.db.append(data=data), data))

        cursor = self.db.cursor()
        rec = cursor.first()
        while rec:
            self.assertIn(rec, keys)
            keys.remove(rec)
            rec = cursor.next()
        self.assertIsNone(rec)
        self.assertFalse(keys)  # Empty



def test_suite():
    suite = unittest.TestSuite()
    for test in (HeapTestCaseNoOpen, HeapTestCaseOpen,):
        test = unittest.defaultTestLoader.loadTestsFromTestCase(test)
        suite.addTest(test)

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
