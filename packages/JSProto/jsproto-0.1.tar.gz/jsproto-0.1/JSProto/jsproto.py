from typing import Any, Dict, List, Tuple

class JSProto:
    def __add__(self, other):
        return JSProto(self.value + other.value)

    def __sub__(self, other):
        return JSProto(self.value - other.value)

    def __mul__(self, other):
        return JSProto(self.value * other.value)

    def __truediv__(self, other):
        return JSProto(self.value / other.value)

    def __floordiv__(self, other):
        return JSProto(self.value // other.value)

    def __mod__(self, other):
        return JSProto(self.value % other.value)

    def __pow__(self, other):
        return JSProto(self.value ** other.value)

    def __neg__(self):
        return JSProto(-self.value)

    def __pos__(self):
        return JSProto(+self.value)

    def __abs__(self):
        return JSProto(abs(self.value))

    def __round__(self, ndigits=None):
        return JSProto(round(self.value, ndigits))

    def __init__(self, value):
        self.value = value

    def __getattr__(self, attr):
        if isinstance(self.value, Dict):
            new_value = self.value.get(attr)
            return JSProto(new_value) if new_value is not None else JSProto(None)
        return JSProto(None)

    def __getitem__(self, key):
        if isinstance(self.value, List) and 0 <= key < len(self.value):
            return JSProto(self.value[key])
        return JSProto(None)

    def __call__(self, default: Any = None) -> Any:
        return self.value if self.value is not None else default

    def forEach(self, func):
        if isinstance(self.value, List):
            for item in self.value:
                func(item)
        elif isinstance(self.value, Dict):
            for key, value in self.value.items():
                func(key, value)
        elif isinstance(self.value, Tuple):
            for item in self.value:
                func(item)
        return self

    def map(self, func):
        if isinstance(self.value, List):
            return JSProto([func(item) for item in self.value])
        elif isinstance(self.value, Dict):
            return JSProto({key: func(key, value) for key, value in self.value.items()})
        elif isinstance(self.value, Tuple):
            return JSProto(tuple(map(func, self.value)))
        return JSProto(None)

    def then(self, func):
        if isinstance(self.value, List):
            return JSProto(func(self.value))
        elif isinstance(self.value, Dict):
            return JSProto({key: func(value) for key, value in self.value.items()})
        return JSProto(func(self.value))

def int(value):
    return JSProto(value)
def float(value):
    return JSProto(value)
def str(value):
    return JSProto(value)
def bool(value):
    return JSProto(value)
def set(value):
    return JSProto(value)
def list(value):
    return JSProto(value)
def dict(value):
    return JSProto(value)
def tuple(value):
    return JSProto(value)

def function(func):
    return func
