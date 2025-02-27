#! /usr/bin/env python

### Train spambayes on all previously-untrained messages in a mailbox.
###
### This keeps track of messages it's already trained by adding an
### X-Spambayes-Trained: header to each one.  Then, if you move one to
### another folder, it will retrain that message.  You would want to run
### this from a cron job on your server.

"""Usage: %(program)s [OPTIONS] ...

Where OPTIONS is one or more of:
    -h
        show usage and exit
    -d DBNAME
        use the DBM store.  A DBM file is larger than the pickle and
        creating it is slower, but loading it is much faster,
        especially for large word databases.  Recommended for use with
        sb_filter or any procmail-based filter.
    -p DBNAME
        use the pickle store.  A pickle is smaller and faster to create,
        but much slower to load.  Recommended for use with sb_server and
        sb_xmlrpcserver.
    -g PATH
        mbox or directory of known good messages (non-spam) to train on.
        Can be specified more than once.
    -s PATH
        mbox or directory of known spam messages to train on.
        Can be specified more than once.
    -f
        force training, ignoring the trained header.  Use this if you
        need to rebuild your database from scratch.
    -q
        quiet mode; no output

    -n  train mail residing in "new" directory, in addition to "cur"
        directory, which is always trained (Maildir only)

    -r  remove mail which was trained on (Maildir only)

    -o section:option:value
        set [section, option] in the options database to value
"""

import sys, os, getopt, email
import shutil
import re
from spambayes import hammie, storage, mboxutils
from spambayes.Options import options, get_pathname_option

program = sys.argv[0]
loud = True

def get_message(obj):
    """Return an email Message object.

    This works like mboxutils.get_message, except it doesn't junk the
    headers if there's an error.  Doing so would cause a headerless
    message to be written back out!

    """

    if isinstance(obj, email.message.EmailMessage):
        return obj
    # Create an email Message object.
    if hasattr(obj, "read"):
        obj = obj.read().decode('utf-8','ignore')
    try:
        msg = email.message_from_string(obj,policy=email.policy.default)
    except email.errors.MessageParseError:
        msg = None
    return msg

def msg_train(h, msg, is_spam, force):
    """Train bayes with a single message."""

    # XXX: big hack -- why is email.Message unable to represent
    # multipart/alternative?
    try:
        mboxutils.as_string(msg)
    except TypeError:
        # We'll be unable to represent this as text :(
        return False

    if is_spam:
        spamtxt = options["Headers", "header_spam_string"]
    else:
        spamtxt = options["Headers", "header_ham_string"]
    oldtxt = msg.get(options["Headers", "trained_header_name"])
    if force:
        # Train no matter what.
        if oldtxt != None:
            del msg[options["Headers", "trained_header_name"]]
    elif oldtxt == spamtxt:
        # Skip this one, we've already trained with it.
        return False
    elif oldtxt != None:
        # It's been trained, but as something else.  Untrain.
        del msg[options["Headers", "trained_header_name"]]
        h.untrain(msg, not is_spam)
    h.train(msg, is_spam)
    msg.add_header(options["Headers", "trained_header_name"], spamtxt)

    return True

def maildir_train(h, path, is_spam, force, removetrained):
    """Train bayes with all messages from a maildir."""

    if loud:
        print("  Reading %s as Maildir" % (path,))

    import time
    import socket

    pid = os.getpid()
    host = socket.gethostname()
    counter = 0
    trained = 0

    for fn in os.listdir(path):
        cfn = os.path.join(path, fn)
        tfn = os.path.normpath(os.path.join(path, "..", "tmp",
                           "%d.%d_%d.%s" % (time.time(), pid,
                                            counter, host)))
        if (os.path.isdir(cfn)):
            continue
        counter += 1
        if loud and counter % 10 == 0:
            sys.stdout.write("\r%6d" % counter)
            sys.stdout.flush()
        f = open(cfn, "rb")
        msg = get_message(f)
        f.close()
        if not msg:
            print("Malformed message: %s.  Skipping..." % cfn)
            continue
        if not msg_train(h, msg, is_spam, force):
            continue
        trained += 1
        if not options["Headers", "include_trained"]:
            continue
        f = open(tfn, "wb")
        f.write(mboxutils.as_string(msg).encode())
        f.close()
        # update file name with new size
        new_cfn= re.sub(r'S=([0-9]+)',f'S={os.path.getsize(tfn)},',fn)
        shutil.copystat(cfn, tfn)

        # XXX: This will raise an exception on Windows.  Do any Windows
        # people actually use Maildirs?
        os.rename(tfn, new_cfn)
        if cfn != new_cfn: os.unlink(cfn)
        if (removetrained):
            os.unlink(new_cfn)

    if loud:
        sys.stdout.write("\r%6d" % counter)
        sys.stdout.write("\r  Trained %d out of %d messages\n" %
                         (trained, counter))

def mbox_factory(f):
    """Return mbox messages as EmailMessage"""

    return email.message_from_binary_file(f,policy=email.policy.default)

def mbox_train(h, path, is_spam, force):
    """Train bayes with a Unix mbox"""

    if loud:
        print("  Reading as Unix mbox")

    import mailbox

    mbox = mailbox.mbox(path,factory=mbox_factory,create=False)
    mbox.lock()

    counter = -1
    trained = 0
    malformed = []

    for key,msg in mbox.items():
        counter += 1
        if not msg:
            malformed.append(counter)
            continue
        if loud and counter % 10 == 0:
            sys.stdout.write("\r%6d" % counter)
            sys.stdout.flush()
        if msg_train(h, msg, is_spam, force):
            trained += 1
        if options["Headers", "include_trained"]:
            mbox.update({key: msg})
    mbox.close()

    if loud:
        sys.stdout.write("\r%6d" % counter)
        sys.stdout.write("\r  Trained %d out of %d messages\n" %
                         (trained, counter))
        nmalformed = len(malformed)
        if nmalformed != 0:
            sys.stdout.write("\r  Encountered %d malformed messages: " %
                             (nmalformed,))
            sys.stdout.write('[%s]\n'%(','.join([str(i) for i in malformed])),)
    return

def mhdir_train(h, path, is_spam, force):
    """Train bayes with an mh directory"""

    if loud:
        print("  Reading as MH mailbox")

    import glob

    counter = 0
    trained = 0

    for fn in glob.glob(os.path.join(path, "[0-9]*")):
        counter += 1

        cfn = fn
        tfn = os.path.join(path, "spambayes.tmp")
        if loud and counter % 10 == 0:
            sys.stdout.write("\r%6d" % counter)
            sys.stdout.flush()
        f = file(fn, "rb")
        msg = get_message(f)
        f.close()
        if not msg:
            print("Malformed message: %s.  Skipping..." % cfn)
            continue
        msg_train(h, msg, is_spam, force)
        trained += 1
        if not options["Headers", "include_trained"]:
            continue
        f = file(tfn, "wb")
        f.write(mboxutils.as_string(msg))
        f.close()
        shutil.copystat(cfn, tfn)

        # XXX: This will raise an exception on Windows.  Do any Windows
        # people actually use MH directories?
        os.rename(tfn, cfn)

    if loud:
        sys.stdout.write("\r%6d" % counter)
        sys.stdout.write("\r  Trained %d out of %d messages\n" %
                         (trained, counter))

def train(h, path, is_spam, force, trainnew, removetrained):
    path = os.path.expanduser(os.path.expandvars(path))
    if not os.path.exists(path):
        raise ValueError("Nonexistent path: %s" % path)
    elif os.path.isfile(path):
        mbox_train(h, path, is_spam, force)
    elif os.path.isdir(os.path.join(path, "cur")):
        maildir_train(h, os.path.join(path, "cur"), is_spam, force,
                      removetrained)
        if trainnew:
            maildir_train(h, os.path.join(path, "new"), is_spam, force,
                          removetrained)
    elif os.path.isdir(path):
        mhdir_train(h, path, is_spam, force)
    else:
        raise ValueError("Unable to determine mailbox type: " + path)


def usage(code, msg=''):
    """Print usage message and sys.exit(code)."""
    if msg:
        print(msg, file=sys.stderr)
        print(file=sys.stderr)
    print(__doc__ % globals(), file=sys.stderr)
    sys.exit(code)

def main():
    """Main program; parse options and go."""

    global loud

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hfqnrd:p:g:s:o:')
    except getopt.error as msg:
        usage(2, msg)

    if not opts:
        usage(2, "No options given")

    force = False
    trainnew = False
    removetrained = False
    good = []
    spam = []
    for opt, arg in opts:
        if opt == '-h':
            usage(0)
        elif opt == "-f":
            force = True
        elif opt == "-n":
            trainnew = True
        elif opt == "-q":
            loud = False
        elif opt == '-g':
            good.append(arg)
        elif opt == '-s':
            spam.append(arg)
        elif opt == "-r":
            removetrained = True
        elif opt == '-o':
            options.set_from_cmdline(arg, sys.stderr)
    pck, usedb = storage.database_type(opts)
    if args:
        usage(2, "Positional arguments not allowed")

    if usedb == None:
        # Use settings in configuration file.
        usedb = options["Storage", "persistent_use_database"]
        pck = get_pathname_option("Storage",
                                          "persistent_storage_file")

    h = hammie.open(pck, usedb, "c")

    for g in good:
        if loud:
            print("Training ham (%s):" % g)
        train(h, g, False, force, trainnew, removetrained)
        sys.stdout.flush()
        save = True

    for s in spam:
        if loud:
            print("Training spam (%s):" % s)
        train(h, s, True, force, trainnew, removetrained)
        sys.stdout.flush()
        save = True

    if save:
        h.store()

    h.close()

if __name__ == "__main__":
    main()
