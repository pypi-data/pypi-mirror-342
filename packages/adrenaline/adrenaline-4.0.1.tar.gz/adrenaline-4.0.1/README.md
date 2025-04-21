`adrenaline`
============

Simple Python module to prevent your computer from going to sleep. Supports
Windows and macOS at the moment; Linux support is coming soon (hopefully).

Usage
-----

The module provides a context manager named `prevent_sleep()`. The computer
will not go to sleep while the execution is in this context:

```python
from adrenaline import prevent_sleep


with prevent_sleep():
    # do something important here
    ...
```

Optionally, you can also prevent the screen from turning off:

```python
with prevent_sleep(display=True):
    # do something important here
    ...
```

Command line interface
----------------------

You can also use this module from the command line as follows:

```sh
$ python -m adrenaline
```

The command line interface will prevent sleep mode as long as it is running.


Acknowledgments
---------------

Thanks to [Michael Lynn](https://github.com/pudquick/pypmset) for figuring out
how to do this on macOS.

Thanks to [Niko Pasanen](https://github.com/np-8/wakepy) for the Windows
version.
