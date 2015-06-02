import importlib
import importlib.machinery
import io
import sys
from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP
import ast

def _call_with_frames_removed(f, *args, **kwargs):
    return f(*args, **kwargs)

def retokenize(tokens):
    lastnum = lastval = None
    for num, val, *stuff in tokens:
        if lastnum == NUMBER and num == NAME:
            yield NAME, 'user_literal_' + val
            yield OP, '('
            yield STRING, repr(lastval)
            yield OP, ')'
            lastnum = lastval = None
        else:
            if lastnum is not None:
                yield lastnum, lastval
            lastnum, lastval = num, val
    if lastnum is not None:
        yield lastnum, lastval           

class UserLiteralLoader(importlib.machinery.SourceFileLoader):
    def source_to_code(self, data, path, *, _optimize=-1):
        print(path)
        source = importlib._bootstrap.decode_source(data)
        tokens = tokenize(io.BytesIO(source.encode('utf-8')).readline)
        tokens = retokenize(tokens)
        source = untokenize(retokenize(tokens)).decode('utf-8')
        return _call_with_frames_removed(compile, source, path, 'exec',
                                         dont_inherit=True,
                                         optimize=_optimize)

_real_pathfinder = sys.meta_path[-1]

class UserLiteralFinder(type(_real_pathfinder)):
    @classmethod
    def find_module(cls, fullname, path=None):
        spec = _real_pathfinder.find_spec(fullname, path)
        if not spec: return spec
        loader = spec.loader
        if type(loader).__name__ == 'SourceFileLoader':
            loader.__class__ = UserLiteralLoader
        return loader

sys.meta_path[-1] = UserLiteralFinder
