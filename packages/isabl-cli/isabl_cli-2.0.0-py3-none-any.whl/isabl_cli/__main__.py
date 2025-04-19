"""
Entrypoint module, in case you use `python -m isabl_cli`.

Why does this file exist, and why __main__? For more info, read:

- https://www.python.org/dev/peps/pep-0338/
- https://docs.python.org/3/using/cmdline.html#cmdoption-m
"""

from isabl_cli.cli import main

if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
