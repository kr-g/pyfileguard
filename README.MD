
# File Guard and Large File Guard

support for preserving the old content of a file.
support for large files provide access via `seek()` to a specific file position.

# use in own code

use `with context` and `rollback()` to rewind the changes done.

# when to use in own code

there are some typical use cases, such as:
- in test scenarios when you need to rollback for the next test case
- when writing changed config files from your code (falls back to old state)
- when randomly accessing larger files in binary mode

find some [sample.py](https://github.com/kr-g/pyfileguard/blob/master/sample.py) code in github repo


# code for small files

for small files `FileGuard` makes a copy using a `TemporaryFile`.
in error case or when calling `rollback()` the file is copied back.

refer to `sample()`


# code for large files

for large files `LargeFileGuard` provides methods like `seek()` and `tell()`
to set the file pointer position. when writing to `LargeFileGuard` it preserves
the content of the underlying file by writing to a journal or "before-image"
file (also known as copy-on-write).
in error case or by calling `rollback()` the changes are rewinded.

refer to `sample2()`


