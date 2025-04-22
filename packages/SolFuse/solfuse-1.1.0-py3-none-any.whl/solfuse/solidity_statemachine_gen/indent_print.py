from io import StringIO
from sys import stdout
from rich import print


def indent_print(*args, indent=0, width=2, file=stdout):
  """
  adding uniform indent width to each line of output of `print(obj)`.

  using `StringIO` to achieve this.
  """
  sfile = StringIO()
  print(*args, file=sfile)
  for line in sfile.getvalue().splitlines():
    print(indent * width * " " + line, file=file)
