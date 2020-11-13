"""
This code is a companion to the article "Ridge energy for thin nematic polymer networks", by
    Andrea Pedrini (andrea.pedrini@unipv.it) - Dipartimento di Matematica, Università di Pavia, via Ferrata 5, 27100 Pavia, Italy;
    Epifanio G. Virga (eg.virga@unipv.it) - Dipartimento di Matematica, Università di Pavia, via Ferrata 5, 27100 Pavia, Italy.

"""

import sys
import os
import datetime


def safe_mkdir(path):
    """ Create a directory if there isn't one already. """
    try:
        os.mkdir(path)
    except OSError:
        pass


def generate_timestamp():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def experiment_name(n, a):
    basename = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    name = '{0}_{1}_{2:.2f}'.format(basename, n, a, generate_timestamp())
    return name


class stream_tee(object):
    # Based on https://gist.github.com/327585 by Anand Kunal
    def __init__(self, stream1, stream2):
        self.stream1 = stream1
        self.stream2 = stream2
        self.__missing_method_name = None  # Hack!

    def __getattribute__(self, name):
        return object.__getattribute__(self, name)

    def __getattr__(self, name):
        self.__missing_method_name = name  # Could also be a property
        return getattr(self, '__methodmissing__')

    def __methodmissing__(self, *args, **kwargs):
        # Emit method call to the log copy
        callable2 = getattr(self.stream2, self.__missing_method_name)
        callable2(*args, **kwargs)

        # Emit method call to stdout (stream 1)
        callable1 = getattr(self.stream1, self.__missing_method_name)
        return callable1(*args, **kwargs)
