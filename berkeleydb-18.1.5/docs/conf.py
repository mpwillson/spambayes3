# -*- coding: utf-8 -*-
#
# Python documentation build configuration file
#
# This file is execfile()d with the current directory set to its containing dir.
#
# The contents of this file are pickled, so don't put values in the namespace
# that aren't pickleable (module imports are okay, they're removed automatically).

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

# General configuration
# ---------------------

#extensions = ['sphinx.ext.refcounting', 'sphinx.ext.coverage']
extensions = ["sphinx.ext.extlinks"]
extlinks = {
        "oracleapic":
            ("https://docs.oracle.com/database/bdb181/html/api_reference/C/%s",
            None),
        "oracle":
            ("https://docs.oracle.com/database/bdb181/html/%s",
            None),
        }

# General substitutions.
project = 'BerkeleyDB'
copyright = '2008-2022 Jesús Cea Avión'

# The default replacements for |version| and |release|.
#
# The short X.Y version.
version = '18.1.5'
# The full version, including alpha/beta/rc tags.
release = '18.1.5'

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
today = ''
# Else, today_fmt is used as the format for a strftime call.
today_fmt = '%B %d, %Y'

# List of files that shouldn't be included in the build.
unused_docs = [
    'whatsnew/2.0',
    'whatsnew/2.1',
    'whatsnew/2.2',
    'whatsnew/2.3',
    'whatsnew/2.4',
    'whatsnew/2.5',
    'maclib/scrap',
    'library/xmllib',
    'library/xml.etree',
]

# Relative filename of the reference count data file.
#refcount_file = 'data/refcounts.dat'

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = True


# Options for HTML output
# -----------------------

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
html_use_smartypants = True

# Content template for the index page, filename relative to this file.
#html_index = 'tools/sphinxext/indexcontent.html'

# Custom sidebar templates, filenames relative to this file.
#html_sidebars = {
#    'index': 'tools/sphinxext/indexsidebar.html',
#}

# Additional templates that should be rendered to pages.
#html_additional_pages = {
#    'download': 'tools/sphinxext/download.html',
#}

# Output file base name for HTML help builder.
#htmlhelp_basename = 'python' + release.replace('.', '')

html_copy_source=False

