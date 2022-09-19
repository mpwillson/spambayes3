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
TestCases for exercising a Queue DB.
"""

import os
from pprint import pprint
import unittest

from .test_all import db, verbose, get_new_database_path, printable_bytes

#----------------------------------------------------------------------

class SimpleQueueTestCase(unittest.TestCase):
    def setUp(self):
        self.filename = get_new_database_path()

    def tearDown(self):
        try:
            os.remove(self.filename)
        except os.error:
            pass


    def test01_basic(self):
        # Basic Queue tests using the deprecated DBCursor.consume method.

        d = db.DB()
        d.set_re_len(40)  # Queues must be fixed length
        d.open(self.filename, db.DB_QUEUE, db.DB_CREATE)

        recnos = []
        for x in printable_bytes:
            recnos.append(d.append(x * 40))

        self.assertEqual(len(d), len(printable_bytes))
        self.assertEqual(len(d), len(recnos))

        for recno, data in ((128, b'some more data'),
                            (129, b'and some more'),
                            (120, b'out of order'),
                            (1, b'replacement data')):
            d.put(recno, data)
            recnos.append(recno)

        self.assertEqual(len(d), len(printable_bytes)+3)
        self.assertEqual(len(recnos), len(d) + 1)  # +1 because replacement

        d.close()
        del d

        d = db.DB()
        d.open(self.filename)

        # Test "txn" as a positional parameter
        recnos.append(d.append(b'one more', None))
        # Test "txn" as a keyword parameter
        recnos.append(d.append(b'another one', txn=None))

        recnos = set(recnos)

        c = d.cursor()
        rec = c.consume()
        while rec:
            self.assertIn(rec[0], recnos)
            recnos.discard(rec[0])
            rec = c.consume()
        c.close()

        self.assertEqual(len(d), 0)
        d.close()
        self.assertFalse(recnos)


    def test02_basicPost32(self):
        # Basic Queue tests using the new DB.consume method in DB 3.2+
        # (No cursor needed)

        d = db.DB()
        d.set_re_len(40)  # Queues must be fixed length
        d.open(self.filename, db.DB_QUEUE, db.DB_CREATE)

        recnos = []
        for x in printable_bytes:
            recnos.append(d.append(x * 40))

        self.assertEqual(len(d), len(printable_bytes))

        for recno, data in ((128, b'some more data'),
                            (129, b'and some more'),
                            (120, b'out of order'),
                            (1, b'replacement data')):
            d.put(recno, data)
            recnos.append(recno)

        self.assertEqual(len(d), len(printable_bytes)+3)
        self.assertEqual(len(recnos), len(d) + 1)  # +1 because replacement

        d.close()
        del d

        d = db.DB()
        d.open(self.filename)

        recnos.append(d.append(b'one more'))
        recnos = set(recnos)

        rec = d.consume_wait()
        while rec:
            self.assertIn(rec[0], recnos)
            recnos.discard(rec[0])
            rec = d.consume()

        self.assertEqual(len(d), 0)
        d.close()
        self.assertFalse(recnos)


    def test03_get_consume(self):
        d = db.DB()
        d.set_re_len(40)  # Queues must be fixed length
        d.open(self.filename, db.DB_QUEUE, db.DB_CREATE)

        recnos = []
        for x in printable_bytes:
            recnos.append(d.append(x * 40))

        self.assertEqual(d.get(20), b'j' * 40)
        # "get" doesn't consume
        self.assertEqual(d.get(20), b'j' * 40)

        # If "DB_CONSUME", the key is ignored. It is easier to
        # use "DB.consume()".
        self.assertEqual((1, b'0' * 40), d.get(20, flags=db.DB_CONSUME))
        self.assertEqual((2, b'1' * 40), d.get(20, flags=db.DB_CONSUME_WAIT))
        self.assertEqual((3, b'2' * 40), d.get(20, flags=db.DB_CONSUME))

        d.close()

    def test04_get_consume_partial(self):
        d = db.DB()
        d.set_re_len(40)  # Queues must be fixed length
        d.open(self.filename, db.DB_QUEUE, db.DB_CREATE)

        d.append(b'1234567890')
        d.append(b'abcdefghij')
        d.append(b'ABCDEFGHIJ')
        self.assertEqual(b'CDEF', d.get(3, dlen=4, doff=2))
        # If "DB_CONSUME", the key is ignored. It is easier to
        # use "DB.consume()".
        self.assertEqual((1, b'3456'), d.get(99999, flags=db.DB_CONSUME_WAIT,
                                             dlen=4, doff=2))
        self.assertEqual((2, b'cdef'), d.get(99999, flags=db.DB_CONSUME,
                                             dlen=4, doff=2))
        d.close()

    def test05_consume_partial(self):
        d = db.DB()
        d.set_re_len(40)  # Queues must be fixed length
        d.open(self.filename, db.DB_QUEUE, db.DB_CREATE)

        d.append(b'1234567890')
        d.append(b'abcdefghij')
        d.append(b'ABCDEFGHIJ')
        self.assertEqual((1, b'3456'), d.consume(dlen=4, doff=2))
        self.assertEqual((2, b'cdef'), d.consume_wait(dlen=4, doff=2))
        d.close()


#----------------------------------------------------------------------

def test_suite():
    suite = unittest.TestSuite()
    for test in (SimpleQueueTestCase,):
        test = unittest.defaultTestLoader.loadTestsFromTestCase(test)
        suite.addTest(test)

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
