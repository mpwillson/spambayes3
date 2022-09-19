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


from __future__ import print_function
import sys


if sys.version_info < (3, 6):
    print()
    print('******* COMPILATION ABORTED *******')
    print()
    print("Since release 18, this project doesn't support Python 2.7 ")
    print("neither Python 3 < 3.6 anymore.")
    print()
    print('You can try to install legacy "bsddb3" library, ')
    print('supporting Python 2.7 and Python 3.3-3.5, ')
    print('running the following command:')
    print()
    print('    pip install bsddb3')
    print()
    sys.exit(1)

if sys.version_info < (3, 7):
    print()
    print('******* COMPILATION ABORTED *******')
    print()
    print('This release is not compatible with your Python version.')
    print('If you can not upgrade your Python environment, you can pin')
    print('last supported releases as:')
    print()
    print('For Python 3.6:')
    print()
    print('    pip3.6 install berkeleydb==18.1.4')
    print()
    print("Of course you won't get new bug fixes, new features, support")
    print("for new Oracle Berkeley DB releases, and so on.")
    print()
    sys.exit(1)


import setup3
