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
TestCases for DB.associate.
"""

import sys, os, string
import time
from pprint import pprint

import unittest
from .test_all import db, dbshelve, rmtree, verbose, \
        get_new_environment_path


#----------------------------------------------------------------------


musicdata = {
1 : (b"Bad English", b"The Price Of Love", b"Rock"),
2 : (b"DNA featuring Suzanne Vega", b"Tom's Diner", b"Rock"),
3 : (b"George Michael", b"Praying For Time", b"Rock"),
4 : (b"Gloria Estefan", b"Here We Are", b"Rock"),
5 : (b"Linda Ronstadt", b"Don't Know Much", b"Rock"),
6 : (b"Michael Bolton", b"How Am I Supposed To Live Without You", b"Blues"),
7 : (b"Paul Young", b"Oh Girl", b"Rock"),
8 : (b"Paula Abdul", b"Opposites Attract", b"Rock"),
9 : (b"Richard Marx", b"Should've Known Better", b"Rock"),
10: (b"Rod Stewart", b"Forever Young", b"Rock"),
11: (b"Roxette", b"Dangerous", b"Rock"),
12: (b"Sheena Easton", b"The Lover In Me", b"Rock"),
13: (b"Sinead O'Connor", b"Nothing Compares 2 U", b"Rock"),
14: (b"Stevie B.", b"Because I Love You", b"Rock"),
15: (b"Taylor Dayne", b"Love Will Lead You Back", b"Rock"),
16: (b"The Bangles", b"Eternal Flame", b"Rock"),
17: (b"Wilson Phillips", b"Release Me", b"Rock"),
18: (b"Billy Joel", b"Blonde Over Blue", b"Rock"),
19: (b"Billy Joel", b"Famous Last Words", b"Rock"),
20: (b"Billy Joel", b"Lullabye (Goodnight, My Angel)", b"Rock"),
21: (b"Billy Joel", b"The River Of Dreams", b"Rock"),
22: (b"Billy Joel", b"Two Thousand Years", b"Rock"),
23: (b"Janet Jackson", b"Alright", b"Rock"),
24: (b"Janet Jackson", b"Black Cat", b"Rock"),
25: (b"Janet Jackson", b"Come Back To Me", b"Rock"),
26: (b"Janet Jackson", b"Escapade", b"Rock"),
27: (b"Janet Jackson", b"Love Will Never Do (Without You)", b"Rock"),
28: (b"Janet Jackson", b"Miss You Much", b"Rock"),
29: (b"Janet Jackson", b"Rhythm Nation", b"Rock"),
30: (b"Janet Jackson", b"State Of The World", b"Rock"),
31: (b"Janet Jackson", b"The Knowledge", b"Rock"),
32: (b"Spyro Gyra", b"End of Romanticism", b"Jazz"),
33: (b"Spyro Gyra", b"Heliopolis", b"Jazz"),
34: (b"Spyro Gyra", b"Jubilee", b"Jazz"),
35: (b"Spyro Gyra", b"Little Linda", b"Jazz"),
36: (b"Spyro Gyra", b"Morning Dance", b"Jazz"),
37: (b"Spyro Gyra", b"Song for Lorraine", b"Jazz"),
38: (b"Yes", b"Owner Of A Lonely Heart", b"Rock"),
39: (b"Yes", b"Rhythm Of Love", b"Rock"),
40: (b"Cusco", b"Dream Catcher", b"New Age"),
41: (b"Cusco", b"Geronimos Laughter", b"New Age"),
42: (b"Cusco", b"Ghost Dance", b"New Age"),
43: (b"Blue Man Group", b"Drumbone", b"New Age"),
44: (b"Blue Man Group", b"Endless Column", b"New Age"),
45: (b"Blue Man Group", b"Klein Mandelbrot", b"New Age"),
46: (b"Kenny G", b"Silhouette", b"Jazz"),
47: (b"Sade", b"Smooth Operator", b"Jazz"),
48: (b"David Arkenstone", b"Papillon (On The Wings Of The Butterfly)",
     b"New Age"),
49: (b"David Arkenstone", b"Stepping Stars", b"New Age"),
50: (b"David Arkenstone", b"Carnation Lily Lily Rose", b"New Age"),
51: (b"David Lanz", b"Behind The Waterfall", b"New Age"),
52: (b"David Lanz", b"Cristofori's Dream", b"New Age"),
53: (b"David Lanz", b"Heartsounds", b"New Age"),
54: (b"David Lanz", b"Leaves on the Seine", b"New Age"),
99: (b"unknown artist", b"Unnamed song", b"Unknown"),
}

#----------------------------------------------------------------------

class AssociateErrorTestCase(unittest.TestCase):
    def setUp(self):
        self.filename = self.__class__.__name__ + '.db'
        self.homeDir = get_new_environment_path()
        self.env = db.DBEnv()
        self.env.open(self.homeDir, db.DB_CREATE | db.DB_INIT_MPOOL)

    def tearDown(self):
        self.env.close()
        self.env = None
        rmtree(self.homeDir)

    def test00_associateDBError(self):
        if verbose:
            print('\n', '-=' * 30)
            print("Running %s.test00_associateDBError..." % \
                  self.__class__.__name__)

        dupDB = db.DB(self.env)
        dupDB.set_flags(db.DB_DUP)
        dupDB.open(self.filename, "primary", db.DB_BTREE, db.DB_CREATE)

        secDB = db.DB(self.env)
        secDB.open(self.filename, "secondary", db.DB_BTREE, db.DB_CREATE)

        # dupDB has been configured to allow duplicates, it can't
        # associate with a secondary.  Berkeley DB will return an error.
        try:
            def f(a,b): return a+b
            dupDB.associate(secDB, f)
        except db.DBError:
            # good
            secDB.close()
            dupDB.close()
        else:
            secDB.close()
            dupDB.close()
            self.fail("DBError exception was expected")



#----------------------------------------------------------------------


class AssociateTestCase(unittest.TestCase):
    keytype = b''
    envFlags = 0
    dbFlags = 0

    def setUp(self):
        self.filename = self.__class__.__name__ + '.db'
        self.homeDir = get_new_environment_path()
        self.env = db.DBEnv()
        self.env.open(self.homeDir, db.DB_CREATE | db.DB_INIT_MPOOL |
                               db.DB_INIT_LOCK | db.DB_THREAD | self.envFlags)

    def tearDown(self):
        self.closeDB()
        self.env.close()
        self.env = None
        rmtree(self.homeDir)

    def addDataToDB(self, d, txn=None):
        for key, value in list(musicdata.items()):
            if (db.version() >= (5, 3)) and (self.dbtype == db.DB_HEAP):
                d.append(b'%02d|' % key + b'|'.join(value), txn=txn)
            else:
                if type(self.keytype) == type(b''):
                    key = b'%02d' % key
                d.put(key, b'|'.join(value), txn=txn)

    def _openDB(self, database, typ, dbtype, flags, txn=None):
        if (db.version() >= (5, 3)) and (self.dbtype == db.DB_HEAP):
            # Heap can not share other databases in the same file
            database.open(f'{self.filename}.{typ}', dbtype,
                          flags, txn=txn)
        else:
            database.open(self.filename, typ, dbtype, flags, txn=txn)


    def createDB(self, txn=None):
        self.cur = None
        self.secDB = None
        self.primary = db.DB(self.env)
        self.primary.set_get_returns_none(2)
        self._openDB(self.primary, 'primary', self.dbtype,
                     db.DB_CREATE | db.DB_THREAD | self.dbFlags, txn=txn)

    def closeDB(self):
        if self.cur:
            self.cur.close()
            self.cur = None
        if self.secDB:
            self.secDB.close()
            self.secDB = None
        self.primary.close()
        self.primary = None

    def getDB(self):
        return self.primary


    def _associateWithDB(self, getGenre):
        self.createDB()

        self.secDB = db.DB(self.env)
        self.secDB.set_flags(db.DB_DUP)
        self.secDB.set_get_returns_none(2)
        self._openDB(self.secDB, 'secondary', db.DB_BTREE,
                   db.DB_CREATE | db.DB_THREAD | self.dbFlags)
        self.getDB().associate(self.secDB, getGenre)

        self.addDataToDB(self.getDB())

        self.finish_test(self.secDB)

    def test01_associateWithDB(self):
        if verbose:
            print('\n', '-=' * 30)
            print("Running %s.test01_associateWithDB..." % \
                  self.__class__.__name__)

        return self._associateWithDB(self.getGenre)

    def _associateAfterDB(self, getGenre) :
        self.createDB()
        self.addDataToDB(self.getDB())

        self.secDB = db.DB(self.env)
        self.secDB.set_flags(db.DB_DUP)
        self._openDB(self.secDB, 'secondary', db.DB_BTREE,
                   db.DB_CREATE | db.DB_THREAD | self.dbFlags)

        # adding the DB_CREATE flag will cause it to index existing records
        self.getDB().associate(self.secDB, getGenre, db.DB_CREATE)

        self.finish_test(self.secDB)

    def test02_associateAfterDB(self):
        if verbose:
            print('\n', '-=' * 30)
            print("Running %s.test02_associateAfterDB..." % \
                  self.__class__.__name__)

        return self._associateAfterDB(self.getGenre)

    def test03_associateWithDB(self):
        if verbose:
            print('\n', '-=' * 30)
            print("Running %s.test03_associateWithDB..." % \
                  self.__class__.__name__)

        return self._associateWithDB(self.getGenreList)

    def test04_associateAfterDB(self):
        if verbose:
            print('\n', '-=' * 30)
            print("Running %s.test04_associateAfterDB..." % \
                  self.__class__.__name__)

        return self._associateAfterDB(self.getGenreList)


    def finish_test(self, secDB, txn=None):
        # 'Blues' should not be in the secondary database
        vals = secDB.pget(b'Blues', txn=txn)
        self.assertEqual(vals, None, vals)

        vals = secDB.pget(b'Unknown', txn=txn)
        if (db.version() >= (5, 3)) and (self.dbtype == db.DB_HEAP):
            k = vals[1].split(b'|')[0]
        else:
            k = vals[0]
        self.assertTrue((isinstance(k, int) and k == 99) or
                        (isinstance(k, bytes) and k == b'99'), vals)
        vals[1].index(b'Unknown')
        vals[1].index(b'Unnamed')
        vals[1].index(b'unknown')

        if verbose:
            print("Primary key traversal:")
        self.cur = self.getDB().cursor(txn)
        count = 0
        rec = self.cur.first()
        while rec is not None:
            if (db.version() >= (5, 3)) and (self.dbtype == db.DB_HEAP):
                key = rec[1].split(b'|')[0]
            else:
                key = rec[0]
            if type(self.keytype) == type(b''):
                self.assertTrue(int(key))  # for primary db, key is a number
            else:
                self.assertTrue(key and type(key) == type(0))
            count = count + 1
            if verbose:
                print(rec)
            rec = self.cur.next()
        self.assertEqual(count, len(musicdata))  # all items accounted for


        if verbose:
            print("Secondary key traversal:")
        self.cur = secDB.cursor(txn)
        count = 0

        # test cursor pget
        vals = self.cur.pget(b'Unknown', flags=db.DB_LAST)
        if (db.version() >= (5, 3)) and (self.dbtype == db.DB_HEAP):
            k = vals[2].split(b'|')[0]
        else:
            k = vals[1]
        self.assertTrue((isinstance(k, int) and k == 99) or
                        (isinstance(k, bytes) and k == b'99'), vals)
        self.assertEqual(vals[0], b'Unknown')
        vals[2].index(b'Unknown')
        vals[2].index(b'Unnamed')
        vals[2].index(b'unknown')

        vals = self.cur.pget(b'Unknown', data=b'wrong value',
                             flags=db.DB_GET_BOTH)
        self.assertEqual(vals, None, vals)

        rec = self.cur.first()
        self.assertEqual(rec[0], b'Jazz')
        while rec is not None:
            count = count + 1
            if verbose:
                print(rec)
            rec = self.cur.next()
        # all items accounted for EXCEPT for 1 with "Blues" genre
        self.assertEqual(count, len(musicdata)-1)

        self.cur = None

    def getGenre(self, priKey, priData):
        self.assertEqual(type(priData), type(b''))
        genre = 2
        if (db.version() >= (5, 3)) and (self.dbtype == db.DB_HEAP):
            genre = 3
        genre = priData.split(b'|')[genre]

        if verbose:
            print('getGenre key: %r data: %r' % (priKey, priData))

        if genre == b'Blues':
            return db.DB_DONOTINDEX
        else:
            return genre

    def getGenreList(self, priKey, PriData) :
        v = self.getGenre(priKey, PriData)
        if type(v) == type(b'') :
            v = [v]
        return v


#----------------------------------------------------------------------


class AssociateHashTestCase(AssociateTestCase):
    dbtype = db.DB_HASH

class AssociateBTreeTestCase(AssociateTestCase):
    dbtype = db.DB_BTREE

class AssociateRecnoTestCase(AssociateTestCase):
    dbtype = db.DB_RECNO
    keytype = 0

@unittest.skipIf(db.version() < (5, 3),
                 'Oracle Berkeley DB 4.8 has no HEAP access method support')
class AssociateHeapTestCase(AssociateTestCase):
    # Workaround because db.DB_HEAP is not defined if BDB < 5.3
    dbtype = None if db.version() < (5, 3) else db.DB_HEAP

#----------------------------------------------------------------------

class AssociateBTreeTxnTestCase(AssociateBTreeTestCase):
    envFlags = db.DB_INIT_TXN
    dbFlags = 0

    def txn_finish_test(self, sDB, txn):
        try:
            self.finish_test(sDB, txn=txn)
        finally:
            if self.cur:
                self.cur.close()
                self.cur = None
            if txn:
                txn.commit()

    def test13_associate_in_transaction(self):
        if verbose:
            print('\n', '-=' * 30)
            print("Running %s.test13_associateAutoCommit..." % \
                  self.__class__.__name__)

        txn = self.env.txn_begin()
        try:
            self.createDB(txn=txn)

            self.secDB = db.DB(self.env)
            self.secDB.set_flags(db.DB_DUP)
            self.secDB.set_get_returns_none(2)
            self.secDB.open(self.filename, "secondary", db.DB_BTREE,
                       db.DB_CREATE | db.DB_THREAD, txn=txn)
            self.getDB().associate(self.secDB, self.getGenre, txn=txn)

            self.addDataToDB(self.getDB(), txn=txn)
        except Exception:
            txn.abort()
            raise

        self.txn_finish_test(self.secDB, txn=txn)


#----------------------------------------------------------------------

class ShelveAssociateTestCase(AssociateTestCase):

    def createDB(self):
        self.primary = dbshelve.open(self.filename,
                                     dbname="primary",
                                     dbenv=self.env,
                                     filetype=self.dbtype)

    def addDataToDB(self, d):
        for key, value in list(musicdata.items()):
            if type(self.keytype) == type(b''):
                key = b'%02d' % key
            d.put(key, value)    # save the value as is this time


    def getGenre(self, priKey, priData):
        self.assertEqual(type(priData), type(()))
        if verbose:
            print('getGenre key: %r data: %r' % (priKey, priData))
        genre = priData[2]
        if genre == b'Blues':
            return db.DB_DONOTINDEX
        else:
            return genre


class ShelveAssociateHashTestCase(ShelveAssociateTestCase):
    dbtype = db.DB_HASH

class ShelveAssociateBTreeTestCase(ShelveAssociateTestCase):
    dbtype = db.DB_BTREE

class ShelveAssociateRecnoTestCase(ShelveAssociateTestCase):
    dbtype = db.DB_RECNO
    keytype = 0

#----------------------------------------------------------------------

class ThreadedAssociateTestCase(AssociateTestCase):

    def addDataToDB(self, d):
        t1 = Thread(target = self.writer1,
                    args = (d, ))
        t2 = Thread(target = self.writer2,
                    args = (d, ))

        t1.setDaemon(True)
        t2.setDaemon(True)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    def writer1(self, d):
        for key, value in list(musicdata.items()):
            if type(self.keytype) == type(b''):
                key = b'%02d' % key
            d.put(key, b'|'.join(value))

    def writer2(self, d):
        for x in range(100, 600):
            key = 'z%2d' % x
            value = [key] * 4
            d.put(key, b'|'.join(value))


class ThreadedAssociateHashTestCase(ShelveAssociateTestCase):
    dbtype = db.DB_HASH

class ThreadedAssociateBTreeTestCase(ShelveAssociateTestCase):
    dbtype = db.DB_BTREE

class ThreadedAssociateRecnoTestCase(ShelveAssociateTestCase):
    dbtype = db.DB_RECNO
    keytype = 0


#----------------------------------------------------------------------

def test_suite():
    suite = unittest.TestSuite()
    for test in (AssociateErrorTestCase,

                 AssociateHashTestCase,
                 AssociateBTreeTestCase,
                 AssociateRecnoTestCase,
                 AssociateHeapTestCase,

                 AssociateBTreeTxnTestCase,

                 ShelveAssociateHashTestCase,
                 ShelveAssociateBTreeTestCase,
                 ShelveAssociateRecnoTestCase,

                 ThreadedAssociateHashTestCase,
                 ThreadedAssociateBTreeTestCase,
                 ThreadedAssociateRecnoTestCase,):

        test = unittest.defaultTestLoader.loadTestsFromTestCase(test)
        suite.addTest(test)

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
