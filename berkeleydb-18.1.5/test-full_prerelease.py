#!/usr/bin/env python3

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

info = """
This program checks all the matrix formed by
several Python and Berkeley DB versions.

This code is only intented to be used by the
maintainer, just before a berkeleydb release, to
verify compatibility and regresions. It contains
local details only applicable to maintainer. If
you try it as is, it would fail.
"""

import subprocess
import sys
import os

# We need to be able to test BDB releases, even if the license is incompatible
os.environ['YES_I_HAVE_THE_RIGHT_TO_USE_THIS_BERKELEY_DB_VERSION'] = ''

def do_matrix_check() :
  python_versions = ('3.7', '3.8', '3.9', '3.10', '3.11')

  berkeleydb_versions=('4.8', '5.3', '6.2', '18.1')

  warning_level=("-Wdefault", "-Werror")[1]

  for py in python_versions :
    for bdb in berkeleydb_versions :
      print()
      print("*** Testing bindings for Python %s and Berkeley DB %s" %(py,bdb))
      extra_params = [warning_level, '-tt', '-bb']
      params = extra_params + ["setup.py", "-q", \
                 "--berkeley-db=/usr/local/BerkeleyDB."+bdb,"build", "-f"]
      params = ["/usr/local/bin/python"+py] + params
      print("EXECUTING:", " ".join(params))
      ret=subprocess.call(params)
      if not ret :
        params = ["/usr/local/bin/python"+py] + extra_params + ["test.py","-p"]
        print("EXECUTING:", " ".join(params))
        ret = subprocess.call(params)
      if ret :
        print()
        print(">>> WE HAVE A PROBLEM!")
        print()
        sys.exit(1)

if __name__=="__main__" :
  print(info)
  do_matrix_check()

