#!/usr/bin/env python

"""
Copyright (c) 2008-2018, Jesus Cea Avion <jcea@jcea.es>
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

import sys, os
refactor_path="/usr/local/lib/python3.5/"

def copy2to3(path_from, path_to) :
    files_to_convert = {}
    if os.path.isdir(path_from) :
        if path_from.endswith(".hg") : return {}
        try :
            os.mkdir(path_to)
        except :
            pass
        for i in os.listdir(path_from) :
            files_to_convert.update(copy2to3(path_from+"/"+i,path_to+"/"+i))
        return files_to_convert

    cwd = os.getcwd()
    if (not path_from.endswith(".py")) or (os.path.exists(path_to) and \
        (os.stat(path_from).st_mtime < os.stat(path_to).st_mtime)) :
            return {}
    if path_from[0] != "/" :
        path_from = cwd+"/"+path_from
    if path_to[0] != "/" :
        path_to = cwd+"/"+path_to
    files_to_convert[path_from] = path_to

    try :
        open(path_to, "w").write(open(path_from, "r").read())
    except :
        os.remove(path_to)
        raise
    return files_to_convert

def make2to3(path_from, path_to) :
    files_to_convert = copy2to3(path_from, path_to)
    retcode = 0
    for path_from, path_to in files_to_convert.iteritems() :
        print "*** Converting", path_to

        try :
            import subprocess
            process = subprocess.Popen(["2to3", "-w", path_to], cwd=refactor_path)
            retcode = process.wait()
        except :
            os.remove(path_to)
            raise

        try :
            os.remove(path_to+".bak")
        except :
            pass

        if retcode :
            os.remove(path_to)
            print "ERROR!"
            return bool(retcode)

    return bool(retcode)

print "Using '%s' for 2to3 conversion tool" %refactor_path

make2to3("setup2.py", "setup3.py")
make2to3("test2.py", "test3.py")
make2to3("Lib", "Lib3")

