#coding=utf-8
import types
function = types.FunctionType
def debug(*obj: object):
    print( *['[DEBUG]:'] + list(obj))

class NotMatch(Exception): pass

def get_name(obj):
    return getattr(obj, '__name__', obj)

def safe_pop(maps, key, val='unknow'):
    if maps.get(key, None):
        val = get_name(maps.pop(key))
    if key != 'return':
        return f'({key}: {val})'
    return val

def has_args(co_flags):
    # bin: 100, num: 4
    # binary or is add
    # 100 & 0...100 => 0...100 
    co_flags = bin(co_flags)
    return co_flags[-3] == '1'

def has_kws(co_flags):
    # bin: 1000, num: 8
    co_flags = bin(co_flags)
    return co_flags[-4] == '1'

def format_func(func: function):
    name = func.__name__
    code = func.__code__
    flags = code.co_flags
    unknow = 'unknow'
    if has_args(flags) or has_kws(flags):
        return unknow
    maps = func.__annotations__
    rettype = safe_pop(maps, 'return', unknow)
    varnames = code.co_varnames[0:code.co_argcount]
    argstype = ' * '.join(safe_pop(maps, k, unknow) for k in varnames)
    if not maps:
        return f'{name}: {argstype} -> {rettype}'
    return f'{name}: {unknow}'

class context(object):
    def __init__(self, pat: function, route: dict):
        self.pat = pat
        self.route = route
    def __repr__(self):
        base = format_func(self.pat)
        if self.route:
            buff = ''
            buff += base + ' | '
            buff += ' | '.join(format_func(v) for v in self.route.values())
            return buff
        return base

class pattern(object):
    def __init__(self, pat: function):
        self.__ctx__ = context(pat, {})
    def __repr__(self):
        return repr(self.__ctx__)
    def match(self, target: object):
        return of(self.__ctx__, target, self)
    def __call__(self, *args, **kws):
        source = self.__ctx__.pat(*args, **kws)
        case = self.__ctx__.route.get(source, None)
        if case:
            return case(*args, **kws)
        else:
            raise NotMatch(repr(self))

class of(object):
    def __init__(self, ctx: context, target: object, parent: pattern):
        self.__ctx__ = ctx
        self.__target__ = target
        self.__parent__ = parent
    def __repr__(self):
        return repr(self.__ctx__)
    def __call__(self, case: function):
        name = case.__name__
        if name == '_':
            self.__ctx__.route[self.__target__] = case
        else:
            raise SyntaxError(f'case name require is `_` but get {name!r}')

__all__ = [
    "debug", "format_func",
    "pattern", "NotMatch"
]
