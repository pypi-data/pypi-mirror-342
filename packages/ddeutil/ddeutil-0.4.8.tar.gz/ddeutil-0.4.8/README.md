# Core Utility

[![test](https://github.com/ddeutils/ddeutil/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/ddeutils/ddeutil/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/ddeutils/ddeutil/graph/badge.svg?token=G3XGBSRKA6)](https://codecov.io/gh/ddeutils/ddeutil)
[![pypi version](https://img.shields.io/pypi/v/ddeutil)](https://pypi.org/project/ddeutil/)
[![python support version](https://img.shields.io/pypi/pyversions/ddeutil)](https://pypi.org/project/ddeutil/)
[![size](https://img.shields.io/github/languages/code-size/ddeutils/ddeutil)](https://github.com/ddeutils/ddeutil)
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![type check: mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

A **Core Utility** package that implements the data utility functions and objects.

I was created this package base on sub-package namespace, `ddeutil` (This 
feature use for independent installation). This package able to extend with 
any sub-extension with this namespace.
So, this namespace able to scale-out the requirement with folder level design.
You can add any custom features and import it by `import ddeutil.{extension}`.

> [!NOTE]
> This package provide the base utility functions and objects for any sub-namespace
> `ddeutil` package.

## :round_pushpin: Installation

```shell
pip install -U ddeutil
```

**Python version supported**:

| Python Version | Installation                        |  Support Fixed Bug  |
|----------------|-------------------------------------|:-------------------:|
| `>=3.9,<3.14`  | `pip install -U ddeutil`            | :heavy_check_mark:  |

> [!NOTE]
> If you want to install all optional dependencies for this package, you can use
> `pip install -U ddeutil[all]`. For optional dependencies that use on this
> package, it will list on below table;
> 
> | Optional deps     | Installation         | Modules                                                 |
> |-------------------|----------------------|---------------------------------------------------------|
> | `ujson`           | `ddeutil[checksum]`  | `hash.checksum`                                         |
> | `python-dateutil` | `ddeutil[dateutil]`  | `dtutils.next_date_with_freq`, `dtutils.calc_data_freq` | 
> | `psutil`          | `ddeutil[memory]`    | `threader.MonitorThread`.                               |

## :dart: Features

This data package implements all of utility functions and objects that does not
re-create again when the sub-namespace package want it because it is a basic utility
but has a lot of using require.

| Module          |          Name           | Description                                                                                                                                                                                       | Remark      |
|:----------------|:-----------------------:|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
| base            |   `isinstance_check`    | Return True if a data is instance of the respect instance.                                                                                                                                        |             |
|                 |     `import_string`     | Import a dotted module path and return the attribute/class designated by the last name in the path.                                                                                               | no coverage |
|                 |         `lazy`          | Lazy use import_string function that wrapped with partial function.                                                                                                                               |             |
|                 |       `round_up`        | Round up the number with decimals precision size.                                                                                                                                                 |             |
|                 |      `remove_pad`       | Remove zero padding of zero prefix string.                                                                                                                                                        |             |
|                 |         `first`         | Returns the first item in the `iterable` that satisfies the `condition`.                                                                                                                          |             |
|                 |        `onlyone`        | Get only one element from check list that exists in match list.                                                                                                                                   |             |
|                 |        `hasdot`         | Return True value if dot searching exists in content data.                                                                                                                                        |             |
|                 |        `getdot`         | Return the value if dot searching exists in content data.                                                                                                                                         |             |
|                 |        `setdot`         | Set the value if dot searching exists in content data.                                                                                                                                            |             |
|                 |      `filter_dict`      | Filter dict value with excluded and included collections.                                                                                                                                         |             |
|                 |      `random_str`       | Random string from uppercase ASCII and number 0-9.                                                                                                                                                | no coverage |
|                 |       `coalesce`        | Coalesce function that is a just naming define function.                                                                                                                                          | no coverage |
| base.checker    |        `can_int`        | Check an input value that can be integer type or not (but some value does not use int() to convert it such as 0.0 or 3.0)                                                                         |             |
|                 |        `is_int`         | Check an input value that be integer type or not.                                                                                                                                                 |             |
| base.convert    |       `must_bool`       | Return the boolean value that was converted from string, integer, or boolean value.                                                                                                               |             |
|                 |       `must_list`       | Return the list value that was converted from string or list value.                                                                                                                               |             |
|                 |        `str2any`        | Convert an input string value to the real type of that object. Note that this convert function do not force or try-hard to convert type such as a boolean value should be 'True' or 'False' only. |             |
|                 |       `str2args`        | Convert an input string to `args` and `kwargs` values.                                                                                                                                            |             |
|                 |       `str2bool`        | Convert an input string value to boolean (`True` or `False`).                                                                                                                                     |             |
|                 |       `str2dict`        | Convert an input string value to `dict`.                                                                                                                                                          |             |
|                 |     `str2int_float`     | Convert an input string value to `int` or `float`.                                                                                                                                                |             |
|                 |       `str2list`        | Convert an input string value to `list`.                                                                                                                                                          |             |
| base.hash       |       `checksum`        |                                                                                                                                                                                                   |             |
|                 |        `freeze`         |                                                                                                                                                                                                   | no coverage |
|                 |      `freeze_args`      |                                                                                                                                                                                                   | no coverage |
|                 |      `hash_value`       |                                                                                                                                                                                                   |             |
|                 |       `hash_str`        |                                                                                                                                                                                                   |             |
| base.merge      |      `merge_dict`       | Given any number of dictionaries, shallow copy and merge into a new dict, precedence goes to key-value pairs in latter dictionaries.                                                              |             |
|                 |   `merge_dict_value`    | Merge value of dicts together if it has a same key.                                                                                                                                               |             |
|                 | `merge_dict_value_list` | Merge value that be list type of dicts together if it has a same key.                                                                                                                             |             |
|                 |      `merge_list`       | Merge lists together.                                                                                                                                                                             |             |
|                 |      `sum_values`       | Sum all values in an input dict value with start and end index.                                                                                                                                   |             |
|                 |       `zip_equal`       |                                                                                                                                                                                                   |             |
|                 |    `add_list_value`     | Add value to dict with an input specific key that should be appended or make a new list of this value if key does not exist.                                                                      |             |
| base.sorting    |        `ordered`        |                                                                                                                                                                                                   |             |
|                 |     `sort_priority`     |                                                                                                                                                                                                   |             |
| base.splitter   |        `isplit`         |                                                                                                                                                                                                   |             |
|                 |      `must_rsplit`      |                                                                                                                                                                                                   |             |
|                 |      `must_split`       |                                                                                                                                                                                                   |             |
| decorator       |       `deepcopy`        | Deep-copy any args and kwargs for func and method.                                                                                                                                                |             |
|                 |         `retry`         | Retry decorator with sequential.                                                                                                                                                                  |             |
|                 |        `profile`        | Profile the current memory and cpu usage while wrapped function running.                                                                                                                          |             |
| dtutils         |     `replace_date`      | Replace datetime matrix that less than an input mode to origin value.                                                                                                                             |             |
|                 |       `next_date`       | Return the next date with specific unit mode.                                                                                                                                                     |             |
|                 |    `closest_quarter`    | Return closest quarter datetime of an input datetime.                                                                                                                                             |             |
|                 |       `last_dom`        | Get the latest day of month that relate with an input datetime value.                                                                                                                             |             |
|                 |       `last_doq`        | Get the latest day of quarter that relate with an input datetime value.                                                                                                                           |             |
|                 |    `next_date_freq`     | Prepare datetime to next datetime with frequency value.                                                                                                                                           |             |
|                 |    `calc_date_freq`     | Prepare datetime to calculate datetime with frequency value.                                                                                                                                      |             |
| threader        |   `ThreadWithControl`   | Threading object that can control maximum background agent and result after complete.                                                                                                             |             |
|                 |     `MonitorThread`     | Monitoring threading object that log the current memory and cpu usage.                                                                                                                            |             |

## :star: Usages

I will show some examples of function in this package. If you want to use
complex or adjust some parameter, please see doc-string or real source code
(I think it does not complex, and you can see how that function work).

### OnlyOne

```python
from ddeutil.core import onlyone

assert 'a' == onlyone(['a', 'b'], ['a', 'b', 'c'])
assert 'c' == onlyone(('a', 'b'), ['c', 'e', 'f'])
assert onlyone(['a', 'b'], ['c', 'e', 'f'], default=False) is None
```

### Instance Check

```python
from ddeutil.core import isinstance_check
from typing import Union, Optional, NoReturn, Any

assert isinstance_check("s", str)
assert isinstance_check(["s"], list[str])
assert isinstance_check(("s", "t"), tuple[str, ...])
assert not isinstance_check(("s", "t"), tuple[str])
assert isinstance_check({"s": 1, "d": "r"}, dict[str, Union[int, str]])
assert isinstance_check("s", Optional[str])
assert isinstance_check(1, Optional[Union[str, int]])
assert not isinstance_check("s", list[str])
assert isinstance_check([1, "2"], list[Union[str, int]])
assert not isinstance_check("s", NoReturn)
assert isinstance_check(None, NoReturn)
assert isinstance_check("A", Any)
assert isinstance_check([1, [1, 2, 3]], list[Union[list[int], int]])
assert not isinstance_check([1], Union[str, int])
assert isinstance_check((1, "foo", True), tuple[int, str, bool])
```

### String to Any

```python
from ddeutil.core import str2any

assert str2any('22') == 22
assert str2any("1245") == 1245
assert str2any('"string"') == "string"
assert str2any("[1, 2, 3]") == [1, 2, 3]
assert str2any('{"key": "value"}') == {"key": "value"}
assert str2any("1245.123") == 1245.123
assert str2any("True")
assert str2any("[1, 2") == "[1, 2"
assert str2any("1.232.1") == "1.232.1"
```

## :speech_balloon: Contribute

I do not think this project will go around the world because it has specific propose,
and you can create by your coding without this project dependency for long term
solution. So, on this time, you can open [the GitHub issue on this project :raised_hands:](https://github.com/ddeutils/ddeutil/issues)
for fix bug or request new feature if you want it.
