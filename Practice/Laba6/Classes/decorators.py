import functools


def log_action(func):
    """Декоратор, отслеживающий вызовы методов героев."""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        print(
            f"[LOG] {self.__class__.__name__} '{self.name}' начинает: {func.__name__}"
        )
        result = func(self, *args, **kwargs)
        print(f"[LOG] Действие '{func.__name__}' завершено.\n")
        return result

    return wrapper
