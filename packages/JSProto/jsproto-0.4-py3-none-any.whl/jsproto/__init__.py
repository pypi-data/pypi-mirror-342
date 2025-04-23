from typing import Any, Callable, Dict, List, Tuple, Self

class var:
    def __init__(self, value: Any) -> None:
        object.__setattr__(self, 'value', value)

    def __add__(self, other: Self) -> Self:
        return var(self.value + other.value)

    def __sub__(self, other: Self) -> Self:
        return var(self.value - other.value)

    def __mul__(self, other: Self) -> Self:
        return var(self.value * other.value)

    def __truediv__(self, other: Self) -> Self:
        return var(self.value / other.value)

    def __floordiv__(self, other: Self) -> Self:
        return var(self.value // other.value)

    def __mod__(self, other: Self) -> Self:
        return var(self.value % other.value)

    def __pow__(self, other: Self) -> Self:
        return var(self.value ** other.value)

    def __neg__(self) -> Self:
        return var(-self.value)

    def __pos__(self) -> Self:
        return var(+self.value)

    def __abs__(self) -> Self:
        return var(abs(self.value))

    def __round__(self, ndigits: int | None = None) -> Self:
        return var(round(self.value, ndigits))

    def __getattr__(self, attr: str) -> Self:
        try:
            value = super().__getattribute__('value')
            if isinstance(value, Dict):
                new_value = value.get(attr)
                return var(new_value) if new_value is not None else var(None)
            new_value = getattr(value, attr)
            return var(new_value)
        except AttributeError:
            return var(None)

    def __setattr__(self, attr: str, value: Any) -> Self:
        try:
            current_value = super().__getattribute__('value')
            if isinstance(current_value, Dict):
                current_value[attr] = value
            else:
                setattr(current_value, attr, value)
        except AttributeError:
            super().__setattr__(attr, value)
        return self

    def __getitem__(self, key: int) -> Self:
        if isinstance(self.value, List) and 0 <= key < len(self.value):
            return var(self.value[key])
        return var(None)

    def __setitem__(self, key: int, value: Any) -> Self:
        if isinstance(self.value, List) and 0 <= key < len(self.value):
            self.value[key] = value
        return self

    def __call__(self, default: Any = None) -> Any:
        return self.value if self.value is not None else default

    def forEach(self, func: Callable[..., None]) -> Self:
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

    def map(self, func: Callable[..., Any]) -> Self:
        if isinstance(self.value, List):
            return var([func(item) for item in self.value])
        elif isinstance(self.value, Dict):
            return var({key: func(key, value) for key, value in self.value.items()})
        elif isinstance(self.value, Tuple):
            return var(tuple(map(func, self.value)))
        return var(None)

    def then(self, func: Callable[..., Any]) -> Self:
        if isinstance(self.value, List):
            return var(func(self.value))
        elif isinstance(self.value, Dict):
            return var({key: func(value) for key, value in self.value.items()})
        return var(func(self.value))

class function:
    def __init__(self, func: Callable[..., Any]) -> None:
        self.func = func

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.func(*args, **kwargs)

    def __getattr__(self, attr: str) -> Self:
        return function(lambda *args, **kwargs: getattr(self.func(*args, **kwargs), attr))

    def __setattr__(self, attr: str, value: Any) -> None:
        if attr == 'func':
            super().__setattr__(attr, value)
        else:
            setattr(self.func, attr, value)

    def __getitem__(self, key: int) -> Self:
        return function(lambda *args, **kwargs: self.func(*args, **kwargs)[key])

    def __setitem__(self, key: int, value: Any) -> None:
        self.func[key] = value

    def then(self, func: Callable[..., Any]) -> Self:
        return function(lambda *args, **kwargs: func(self.func(*args, **kwargs)))
    