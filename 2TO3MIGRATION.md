# Python 2 to 3 Change Log

# Running 2to3.7.py

First target of conversion was scripts/sb_filter.py, on the basis it
would run against the existing spambayes database.

# Spambayes modules

These are used by sb_filter.py and exist in the spambayes directory.

## dnscache.py

Converted by hand.

    intermed = map(None, list(map(getattr, seq, (attr,)*len(seq))), range(len(seq)), seq)
    intermed = itertools.zip_longest(list(map(getattr, seq, (attr,)*len(seq))), range(len(seq)), seq)

2to3 would not convert automatically due to change in handling lists
of differing lengths..  See:

[Stackoverflow](https://stackoverflow.com/questions/1277278/python-zip-like-function-that-pads-to-longest-length)

## Reran 2to3

Got these errors:

    RefactoringTool: There were 17 errors:
    RefactoringTool: Can't parse chi2.py: ParseError: bad input: type=22, value='=', context=('', (158, 18))
    RefactoringTool: Can't parse classifier.py: ParseError: bad input: type=22, value='=', context=('', (578, 58))
    RefactoringTool: Can't parse Corpus.py: ParseError: bad input: type=22, value='=', context=('', (271, 23))
    RefactoringTool: Can't parse Dibbler.py: ParseError: bad input: type=22, value='=', context=('', (285, 46))
    RefactoringTool: Can't parse dnscache.py: ParseError: bad input: type=22, value='=', context=('', (109, 55))
    RefactoringTool: Can't parse hammiebulk.py: ParseError: bad input: type=22, value='=', context=('', (113, 81))
    RefactoringTool: Can't parse Histogram.py: ParseError: bad input: type=22, value='=', context=('', (182, 57))
    RefactoringTool: Can't parse ImageStripper.py: ParseError: bad input: type=22, value='=', context=('', (314, 39))
    RefactoringTool: Can't parse message.py: ParseError: bad input: type=22, value='=', context=('', (179, 46))
    RefactoringTool: Can't parse oe_mailbox.py: ParseError: bad input: type=22, value='=', context=('', (700, 47))
    RefactoringTool: Can't parse Options.py: ParseError: bad input: type=22, value='=', context=('', (1367, 81))
    RefactoringTool: Can't parse OptionsClass.py: ParseError: bad input: type=22, value='=', context=('', (200, 43))
    RefactoringTool: Can't parse postfixproxy.py: ParseError: bad input: type=22, value='=', context=('', (83, 60))
    RefactoringTool: Can't parse safepickle.py: ParseError: bad input: type=22, value='=', context=('', (36, 54))
    RefactoringTool: Can't parse storage.py: ParseError: bad input: type=22, value='=', context=('', (101, 68))
    RefactoringTool: Can't parse TestDriver.py: ParseError: bad input: type=22, value='=', context=('', (32, 46))
    RefactoringTool: Can't parse TestToolsUI.py: ParseError: bad input: type=22, value='=', context=('', (300, 27))

Seems this is because these scripts had already been converted to Python 3

# Running sb_filter.py

To run the spambayes scripts in the dev directory, needed to set PYTHONPATH="."

## email Module

    [mark@opal:~/dev/spambayes-1.1a6-3]$ python scripts/sb_filter.py
    Traceback (most recent call last):
      File "scripts/sb_filter.py", line 83, in <module>
        from spambayes import hammie, Options, mboxutils, storage
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/hammie.py", line 5, in <module>
        from spambayes import mboxutils
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/mboxutils.py", line 28, in <module>
        import email.Message
    ModuleNotFoundError: No module named 'email.Message'

email.Message has been renamed to email.message in 3

## lockfile Module

    [mark@opal:~/dev/spambayes-1.1a6-3]$ python scripts/sb_filter.py
    Traceback (most recent call last):
      File "scripts/sb_filter.py", line 83, in <module>
        from spambayes import hammie, Options, mboxutils, storage
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/hammie.py", line 6, in <module>
        from spambayes import storage
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/storage.py", line 62, in <module>
        from spambayes import classifier
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/classifier.py", line 60, in <module>
        from spambayes.safepickle import pickle_read, pickle_write
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/safepickle.py", line 7, in <module>
        import lockfile
    ModuleNotFoundError: No module named 'lockfile'

lockfile not included with Python 3. Replaced with local copy of
[filelock](https://pypi.org/project/filelock/#description)

## tokenizer.py

    [mark@opal:~/dev/spambayes-1.1a6-3]$ python scripts/sb_filter.py
    Traceback (most recent call last):
      File "scripts/sb_filter.py", line 83, in <module>
        from spambayes import hammie, Options, mboxutils, storage
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/hammie.py", line 8, in <module>
        from spambayes.tokenizer import tokenize
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/tokenizer.py", line 7, in <module>
        import email.Message
    ModuleNotFoundError: No module named 'email.Message'

Changed `email.Message` to `email.message` (also `email.Header`,
`email.Utils` and `email.Errors` lose the uppercase letter)

## mboxutils.py

     mark@opal:~/dev/spambayes-1.1a6-3]$ python scripts/sb_filter.py
     /home/mark/dev/spambayes-1.1a6-3/spambayes/tokenizer.py:662: FutureWarning: Possible nested set at position 1
       received_ip_re = re.compile(r'[[(]((\d{1,3}\.?){4})[])]')
     Traceback (most recent call last):
       File "scripts/sb_filter.py", line 277, in <module>
         main()
       File "scripts/sb_filter.py", line 265, in main
         mbox = mboxutils.getmbox(fname)
       File "/home/mark/dev/spambayes-1.1a6-3/spambayes/mboxutils.py", line 85, in getmbox
         return [get_message(sys.stdin)]
       File "/home/mark/dev/spambayes-1.1a6-3/spambayes/mboxutils.py", line 174, in get_message
         if isinstance(obj, email.Message.Message):
     AttributeError: module 'email' has no attribute 'Message'

Replaced `email.Message.Message` with `email.message.EmailMessage`

## tokenizer.py (again)

    /home/mark/dev/spambayes-1.1a6-3/spambayes/tokenizer.py:662: FutureWarning: Possible nested set at position 1
      received_ip_re = re.compile(r'[[(]((\d{1,3}\.?){4})[])]')

Replaced re string with `r'\[[(]((\d{1,3}\.?){4})[])]'`

# Run-time Problems

## dbmstorage.py

    [mark@opal:~/dev/spambayes-1.1a6-3]$ cat xx| python scripts/sb_filter.py
    Traceback (most recent call last):
      File "scripts/sb_filter.py", line 277, in <module>
        main()
      File "scripts/sb_filter.py", line 268, in main
        action(msg)
      File "scripts/sb_filter.py", line 185, in filter
        self.open('r')
      File "scripts/sb_filter.py", line 166, in open
        self.h = hammie.open(self.dbname, self.usedb, self.mode)
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/hammie.py", line 272, in open
        return Hammie(storage.open_storage(filename, useDB, mode), mode)
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/storage.py", line 998, in open_storage
        return klass(data_source_name, mode)
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/storage.py", line 154, in __init__
        self.load()
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/storage.py", line 180, in load
        self.dbm = dbmstorage.open(self.db_name, self.mode)
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/dbmstorage.py", line 70, in open
        return f(db_name, mode)
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/dbmstorage.py", line 40, in open_best
        return f(*args)
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/dbmstorage.py", line 20, in open_dbhash
        return bsddb.hashopen(*args)
    AttributeError: 'NoneType' object has no attribute 'hashopen'

bsddb has been removed from Python 3. Used bsddb3 from PyPI as a
drop-in replacement. [pypi.org](https://pypi.org/project/bsddb3/)

Installed via `python setup.py build` and `doas python setup.py install`

## mboxutils.py

Looks like a bad call in the email module.

    [mark@opal:~/dev/spambayes-1.1a6-3]$ cat xx| python scripts/sb_filter.py
    Traceback (most recent call last):
      File "scripts/sb_filter.py", line 277, in <module>
        main()
      File "scripts/sb_filter.py", line 268, in main
        action(msg)
      File "scripts/sb_filter.py", line 186, in filter
        return self.h.filter(msg)
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/hammie.py", line 149, in filter
        debug, train)
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/hammie.py", line 97, in score_and_filter
        msg = mboxutils.get_message(msg)
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/mboxutils.py", line 180, in get_message
        msg = email.message_from_string(obj)
      File "/usr/local/lib/python3.7/email/__init__.py", line 38, in message_from_string
        return Parser(*args, **kws).parsestr(s)
      File "/usr/local/lib/python3.7/email/parser.py", line 67, in parsestr
        return self.parse(StringIO(text), headersonly=headersonly)
    TypeError: initial_value must be str or None, not Message

I'd replaced `email.Message.Message` with `email.message.EmailMessage`.
The replacement should have been `email.message.Message`. This change
to `email.message.EmailMessage` was wrong.  See later.

## tokenizer.py

    [mark@opal:~/dev/spambayes-1.1a6-3]$ cat xx| python scripts/sb_filter.py
    <class '_io.TextIOWrapper'>
    <class 'email.message.Message'>
    <class 'email.message.Message'>
    Traceback (most recent call last):
      File "scripts/sb_filter.py", line 277, in <module>
        main()
      File "scripts/sb_filter.py", line 268, in main
        action(msg)
      File "scripts/sb_filter.py", line 186, in filter
        return self.h.filter(msg)
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/hammie.py", line 149, in filter
        debug, train)
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/hammie.py", line 104, in score_and_filter
        prob, clues = self._scoremsg(msg, True)
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/hammie.py", line 33, in _scoremsg
        return self.bayes.spamprob(tokenize(msg), evidence)
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/classifier.py", line 169, in chi2_spamprob
        clues = self._getclues(wordstream)
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/classifier.py", line 471, in _getclues
        for word in set(wordstream):
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/tokenizer.py", line 1255, in tokenize
        for tok in self.tokenize_body(msg):
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/tokenizer.py", line 1645, in tokenize_body
        text = numeric_entity_re.sub(numeric_entity_replacer, text)
    TypeError: cannot use a string pattern on a bytes-like object

Replaced

    text = numeric_entity_re.sub(numeric_entity_replacer, text)

with

    text = numeric_entity_re.sub(numeric_entity_replacer,
         text.decode('utf-8','ignore'))

This is where it's going to get messy.  Perhaps the conversion to
Unicode should happen earlier, or perhaps we should just handle bytes
throughout (e.g. define regex strings as `rb'something'`).

N.B.  Added the `'ignore'` option to decode, as if original message is
in UTF-8 (rather than ASCII), the spambayes decoding process (in
tokenizer.py) will return bytes that can't be decoded.  Seems to be
due to the use of the legacy `email.message.Message.get_payload`, which
always returns binary data.  Should we convert to using the mainstream
`email.message.EmailMessage`?

## storage.py


    [mark@opal:~/dev/spambayes-1.1a6-3]$ cat xx| python scripts/sb_filter.py
    <class '_io.TextIOWrapper'>
    <class 'email.message.Message'>
    <class 'email.message.Message'>
    Traceback (most recent call last):
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/storage.py", line 249, in _wordinfoget
        return self.wordinfo[word]
    KeyError: b'look'

    During handling of the above exception, another exception occurred:

    Traceback (most recent call last):
      File "scripts/sb_filter.py", line 277, in <module>
        main()
      File "scripts/sb_filter.py", line 268, in main
        action(msg)
      File "scripts/sb_filter.py", line 186, in filter
        return self.h.filter(msg)
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/hammie.py", line 149, in filter
        debug, train)
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/hammie.py", line 104, in score_and_filter
        prob, clues = self._scoremsg(msg, True)
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/hammie.py", line 33, in _scoremsg
        return self.bayes.spamprob(tokenize(msg), evidence)
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/classifier.py", line 169, in chi2_spamprob
        clues = self._getclues(wordstream)
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/classifier.py", line 472, in _getclues
        tup = self._worddistanceget(word)
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/classifier.py", line 483, in _worddistanceget
        record = self._wordinfoget(word)
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/storage.py", line 253, in _wordinfoget
        r = self.db.get(word)
      File "/usr/local/lib/python3.7/shelve.py", line 105, in get
        if key.encode(self.keyencoding) in self.dict:
    AttributeError: 'bytes' object has no attribute 'encode'

Fixed by redefining all instances of `isinstance(word,str)` as
`isinstance(word,bytes)`.

## classifier.py

    [mark@opal:~/dev/spambayes-1.1a6-3]$ cat xx|python scripts/sb_filter.py
    <class '_io.TextIOWrapper'>
    <class 'email.message.Message'>
    <class 'email.message.Message'>
    Traceback (most recent call last):
      File "scripts/sb_filter.py", line 277, in <module>
        main()
      File "scripts/sb_filter.py", line 268, in main
        action(msg)
      File "scripts/sb_filter.py", line 186, in filter
        return self.h.filter(msg)
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/hammie.py", line 149, in filter    debug, train)
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/hammie.py", line 104, in score_and_filter
        prob, clues = self._scoremsg(msg, True)
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/hammie.py", line 33, in _scoremsg
        return self.bayes.spamprob(tokenize(msg), evidence)
      File "/home/mark/dev/spambayes-1.1a6-3/spambayes/classifier.py", line 203, in chi2_spamprob
        clues.sort(lambda a, b: cmp(a[1], b[1]))
    TypeError: sort() takes no positional arguments

Fixed by replacing:
    clues.sort(lambda a, b: cmp(a[1], b[1]))
by:
    clues.sort(key=lambda c: c[1])

# scripts/sb_mboxtrain.py - converted using 2to3-3.7

    [mark@opal:~/dev/spambayes-1.1a6-3]$ python scripts/sb_mboxtrain.py -g ~/mail/mbox -s ~/mail/spam
    Training ham (/home/mark/mail/mbox):
      Reading as Unix mbox
    Traceback (most recent call last):
      File "scripts/sb_mboxtrain.py", line 349, in <module>
        main()
      File "scripts/sb_mboxtrain.py", line 333, in main
        train(h, g, False, force, trainnew, removetrained)
      File "scripts/sb_mboxtrain.py", line 262, in train
        mbox_train(h, path, is_spam, force)
      File "scripts/sb_mboxtrain.py", line 168, in mbox_train
        f = file(path, "r+b")
    NameError: name 'file' is not defined

file builtin removed in 3; changed to use open.

    [mark@opal:~/dev/spambayes-1.1a6-3]$ python scripts/sb_mboxtrain.py -g ~/mail/mbox -s ~/mail/spam
    Training ham (/home/mark/mail/mbox):
      Reading as Unix mbox
    Traceback (most recent call last):
      File "scripts/sb_mboxtrain.py", line 349, in <module>
        main()
      File "scripts/sb_mboxtrain.py", line 333, in main
        train(h, g, False, force, trainnew, removetrained)
      File "scripts/sb_mboxtrain.py", line 262, in train
        mbox_train(h, path, is_spam, force)
      File "scripts/sb_mboxtrain.py", line 170, in mbox_train
        mbox = mailbox.PortableUnixMailbox(f, get_message)
    AttributeError: module 'mailbox' has no attribute 'PortableUnixMailbox'

Convert to using `mailbox.mbox`.  Modified mbox_train to use mbox update
capability, which removes need to re-copy temp mailbox when
`options["Headers", "include_trained"]` is set.

TODO Other handlers (e.g. maildir) should also be modified.

## mboxutils.py

Use of `email.message.Message` (legacy) replaced by `email.message.EmailMessage`

## tokenizer.py

Reworked tokenize_body to work primarily with utf-8 strings when
tokenizing textual parts of an email.  Some background can be found
here: [pytyhon](https://bugs.python.org/issue18271)

## message.py

All instances of `email.Message.Message` changed to
`email.message.EmailMessage`.  Untested.

## mboxutils.py

Totally mishandled the creation of an `email.message.EmailMessage`
instance from a file/string in `get_message`.  The code I had intially
used (obj is a str):

    mag = email.message.EmailMessage()
    msg.set_content(obj)

actually assumes all of obj is content (duh) so the email has no
headers (they are content, natch).  This caused the email resulting
from spam analysis to lose all the header info.  Replaced by:

    msg = email.message_from_string(obj,policy=email.policy.default)

Policy must be specified, as default policy is compat32, which returns an
`email.message.Message` instance.  Note this means that `email.policy`
must be imported.

# scripts/sb_mboxtrain.py

The above change broke sb_mboxtrain.py:

    [mark@opal:~/dev/spambayes3] python scripts/sb_mboxtrain.py -s ~/mail/spam
    Training spam (/home/mark/mail/spam):
      Reading as Unix mbox
    Traceback (most recent call last):
      File "scripts/sb_mboxtrain.py", line 325, in <module>
        main()
      File "scripts/sb_mboxtrain.py", line 316, in main
        train(h, s, True, force, trainnew, removetrained)
      File "scripts/sb_mboxtrain.py", line 238, in train
        mbox_train(h, path, is_spam, force)
      File "scripts/sb_mboxtrain.py", line 180, in mbox_train
        if msg_train(h, msg, is_spam, force):
      File "scripts/sb_mboxtrain.py", line 100, in msg_train
        h.train(msg, is_spam)
      File "/home/mark/dev/spambayes3/spambayes/hammie.py", line 164, in train          self.bayes.learn(tokenize(msg), is_spam)
      File "/home/mark/dev/spambayes3/spambayes/classifier.py", line 253, in learn      self._add_msg(wordstream, is_spam)
      File "/home/mark/dev/spambayes3/spambayes/classifier.py", line 354, in _add_msg
        for word in set(wordstream):
      File "/home/mark/dev/spambayes3/spambayes/tokenizer.py", line 1251, in tokenize
        msg = self.get_message(obj)
      File "/home/mark/dev/spambayes3/spambayes/tokenizer.py", line 1248, in get_message
        return get_message(obj)
      File "/home/mark/dev/spambayes3/spambayes/mboxutils.py", line 181, in get_message
        msg = email.message_from_string(obj,policy=email.policy.default)
      File "/usr/local/lib/python3.7/email/__init__.py", line 38, in message_from_string
        return Parser(*args, **kws).parsestr(s)
      File "/usr/local/lib/python3.7/email/parser.py", line 67, in parsestr
        return self.parse(StringIO(text), headersonly=headersonly)
    TypeError: initial_value must be str or None, not mboxMessage

Changed mboxutils.get_message to treat obj or type mailbox.mboxMessage
the same as email.message.EmailMessage and just return it. 

    if isinstance(obj, email.message.EmailMessage) or \
       isinstance(obj, mailbox.mboxMessage):
        return obj
    # Create an email Message object.

That didn't work.  The result was this:

    [mark@opal:~/dev/spambayes3]$ python scripts/sb_mboxtrain.py -s ~/mail/spam
    Training spam (/home/mark/mail/spam):
      Reading as Unix mbox
    Traceback (most recent call last):
      File "/home/mark/dev/spambayes3/spambayes/tokenizer.py", line 1633, in tokenize_body
        text = part.get_content()
    AttributeError: 'Message' object has no attribute 'get_content'

    During handling of the above exception, another exception occurred:

    Traceback (most recent call last):
      File "scripts/sb_mboxtrain.py", line 325, in <module>
        main()
      File "scripts/sb_mboxtrain.py", line 316, in main
        train(h, s, True, force, trainnew, removetrained)
      File "scripts/sb_mboxtrain.py", line 238, in train
        mbox_train(h, path, is_spam, force)
      File "scripts/sb_mboxtrain.py", line 180, in mbox_train
        if msg_train(h, msg, is_spam, force):
      File "scripts/sb_mboxtrain.py", line 100, in msg_train
        h.train(msg, is_spam)
      File "/home/mark/dev/spambayes3/spambayes/hammie.py", line 164, in train          self.bayes.learn(tokenize(msg), is_spam)
      File "/home/mark/dev/spambayes3/spambayes/classifier.py", line 253, in learn      self._add_msg(wordstream, is_spam)
      File "/home/mark/dev/spambayes3/spambayes/classifier.py", line 354, in _add_msg
        for word in set(wordstream):
      File "/home/mark/dev/spambayes3/spambayes/tokenizer.py", line 1255, in tokenize
        for tok in self.tokenize_body(msg):
      File "/home/mark/dev/spambayes3/spambayes/tokenizer.py", line 1638, in tokenize_body
        text = try_to_repair_damaged_base64(text)
      File "/home/mark/dev/spambayes3/spambayes/tokenizer.py", line 885, in try_to_repair_damaged_base64
        m = base64_re.match(text, i)
    TypeError: cannot use a string pattern on a bytes-like object

The correct fix was to read mbox messages as
email.message.EmailMessage, using a factory. Fix is to sb_mboxtrain.py
in mbox_train.

From: [Stackoverflow](https://stackoverflow.com/questions/57456080/in-python-how-to-convert-an-email-message-message-object-into-an-email-messag)
