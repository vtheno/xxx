#coding=utf-8
import types
function = types.FunctionType
def debug(*obj: object):
    print( *['[DEBUG]:'] + list(obj))
class NotMatch(Exception): pass
def format_func(func: function):
    maps = func.__annotations__
    rettype = maps.get('return', 'unit')
    rettype = getattr(rettype, '__name__', str(rettype))
    argstype = ' * '.join(getattr(v, '__name__', str(v)) for k, v in maps.items() if k != 'return')
    return f'{argstype} -> {rettype}'
class Context(object):
    def __init__(self, pat: function, route: dict):
        self.pat = pat
        self.route = route
    def __repr__(self):
        return f'{self.pat.__name__}: ' + ' | '.join(format_func(v) for v in self.route.values() )
class Pattern(object):
    def __init__(self, pat: function):
        self.__ctx__ = Context(pat, {})
    def __repr__(self):
        return repr(self.__ctx__)
    def match(self, target: object):
        return Of(self.__ctx__, target, self)
    def __call__(self, *args, **kws):
        source = self.__ctx__.pat(*args, **kws)
        case = self.__ctx__.route.get(source, None)
        if case:
            return case(*args, **kws)
        else:
            raise NotMatch(repr(self))
class Of(object):
    def __init__(self, ctx: Context, target: object, parent: Pattern):
        self.__ctx__ = ctx
        self.__target__ = target
        self.__parent__ = parent
    def __repr__(self):
        return repr(self.__ctx__)
    def __call__(self, case: function):
        self.__ctx__.route[self.__target__] = case
        return self.__parent__

__all__ = [
    "debug", "format_func",
    "Pattern",
]
"""
@Pattern
def toString(node: object): 
    # type : object -> class
    # type : object -> type
    return type(node)
debug('[def pattern]', toString)

@toString.match(int)
def toString(node: int) -> str:
    return f'{node}'

@toString.match(tuple)
def toString(node: tuple) -> str:
    return f'{node}'

debug('[toString]', toString)
debug("[match]", toString.match(str) )
"""
