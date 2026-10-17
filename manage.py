#!/usr/bin/env python
import os
import sys


def main():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "config.settings",
    )

    try:
        from django.core.management import execute_from_command_line
    except ImportError as error:
        raise ImportError(
            "Не удалось импортировать Django. "
            "Проверь установку зависимостей и виртуальное окружение."
        ) from error

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()