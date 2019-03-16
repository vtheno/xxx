#coding=utf-8
import types
import threading

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

class context:
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

class pattern:
    def __init__(self, pat: function):
        self.__ctx__ = context(pat, {})
    def __repr__(self):
        return repr(self.__ctx__)
    def match(self, target: object):
        def __case__(case: function):
            name = case.__name__
            if name == '_':
                self.__ctx__.route[target] = case
            else:
                raise SyntaxError(f'case name require is `_` but get `{name}`')
        return __case__
    def __call__(self, *args, **kws):
        source = self.__ctx__.pat(*args, **kws)
        case = self.__ctx__.route.get(source, None)
        if case:
            try:
                return case(*args, **kws)
            except RecursionError:
                return async(case)(*args, **kws).wait()
        else:
            raise NotMatch(repr(self))

class NotAsyncTask(Exception): pass

class async_env(object):
    def __init__(self):
        self.ret = None
        self.thread = None
    def add(self, thread: threading.Thread):
        self.thread = thread
        self.thread.start()
    def push(self, value):
        self.ret = value
    def wait(self):
        """
        while self.ret == None:
            continue
        return self.ret
        """
        if self.thread:
            self.thread.join() # wait thread finished
            return self.ret
        else:
            raise NotAsyncTask

class async(object):
    def __init__(self, task):
        self.task = task
    def __call__(self, *args, **kws):
        ctx = async_env()
        def __task__(*args, **kws):
            ctx.push( self.task(*args, **kws) )
        t = threading.Thread(target=__task__,
                             args=args,
                             kwargs=kws,
                             daemon=False)
        ctx.add(t)
        return ctx

__all__ = [
    "debug", "format_func",
    "pattern", "NotMatch",
    "async", "async_env", "NotAsyncTask"
]
