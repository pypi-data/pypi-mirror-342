from importlib.metadata import entry_points
import collections, sys

dotpy = '.py'
inf = float('inf')
null_exc_info = None, None, None

class NoSuchPathException(Exception): pass

class UnparseNoSuchPathException(NoSuchPathException):

    def __str__(self):
        path, = self.args
        return ' '.join(path)

class TreeNoSuchPathException(NoSuchPathException):

    def __str__(self):
        path, causes = self.args # XXX: Also collect (and show) where in the tree the causes happened?
        causestrtocount = collections.OrderedDict()
        for causestr in map(str, causes):
            try:
                causestrtocount[causestr] += 1
            except KeyError:
                causestrtocount[causestr] = 1
        lines = [' '.join(path)]
        for causestr, count in causestrtocount.items():
            causelines = causestr.splitlines()
            lines.append(f"{count}x {causelines[0]}")
            for l in causelines[1:]:
                lines.append(f"    {l}")
        return '\n'.join(lines)

class CycleException(UnparseNoSuchPathException): pass

class UnsupportedEntryException(Exception): pass

class OrderedDictWrapper:

    def __init__(self, *args):
        self.d = collections.OrderedDict(*args)

    def __bool__(self):
        return bool(self.d)

    def __nonzero__(self):
        return self.__bool__()

class OrderedDict(OrderedDictWrapper):

    def __setitem__(self, k, v):
        self.d[k] = v

    def __getitem__(self, k):
        return self.d[k]

    def __delitem__(self, k):
        del self.d[k]

    def get(self, k, default = None):
        return self.d.get(k, default)

    def keys(self):
        return self.d.keys()

    def values(self):
        return self.d.values()

    def items(self):
        return self.d.items()

    def __iter__(self):
        return iter(self.d.values())

    def __eq__(self, that):
        return self.d == that

    def __repr__(self):
        return repr(self.d)

    def update(self, other):
        return self.d.update(other)

def openresource(package_or_name, resource_name, encoding = 'ascii'):
    'Like `pkg_resources.resource_stream` but text mode.'
    from .model import Resource
    return Resource(package_or_name, resource_name, encoding).open(False)

def solo(v):
    'Assert exactly one object in the given sequence and return it.'
    x, = v
    return x

def qualname(obj):
    try:
        return obj.__qualname__
    except AttributeError:
        name = obj.__name__
        if getattr(sys.modules[obj.__module__], name) is not obj:
            raise
        return name

def selectentrypoints(group):
    obj = entry_points()
    try:
        select = obj.select
    except AttributeError:
        return obj[group]
    return select(group = group)

def popattr(obj, name):
    val = getattr(obj, name)
    delattr(obj, name)
    return val
