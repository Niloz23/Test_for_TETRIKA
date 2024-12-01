def strict(func):
    def wrapper(*args, **kwargs):
        # Получаем аннотации типов аргументов функции
        annotations = func.__annotations__

        # Проверяем соответствие типов аргументов
        for (arg_name, arg_type), arg_value in zip(annotations.items(), args):
            if not isinstance(arg_value, arg_type):
                raise TypeError(f"Argument '{arg_name}' must be of type {arg_type.__name__}, "
                                f"but got {type(arg_value).__name__}.")

        # Вызываем оригинальную функцию
        return func(*args, **kwargs)

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


# Пример использования
print(sum_two(1, 2))  # >>> 3
print(sum_two(1, 2.4))  # >>> TypeError
