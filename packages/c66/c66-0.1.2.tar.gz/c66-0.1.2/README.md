# c66

A collection of handy Python utilities.

## Installation

```bash
pip install c66
```

## Usage

- `pp`: Prints the names and values of variables from the calling line.

  ```python
  from c66 import pp

  x = 10
  y = "hello"
  pp(x, y + " world")
  ```

  Output:
  ```
  x: 10
  y + " world": hello world
  ```

- `pps`: Prints the shapes.

  ```python
  from c66 import pps
  import torch
  x = torch.randn(2,5,1)
  y = torch.randn(3,)
  pps(x,y)
  ```

  Output:
  ```
  from c66 import pps
  x's shape: torch.Size([2, 5, 1])
  y's shape: torch.Size([3])
  ```

- `print`: Prints the provided arguments when `c66.show_print` is `True`. If `c66.show_print` is False, it returns `None` without printing.
  The default of `c66.show_print` is `True`

  ```python
  from c66 import print, show_print

  x = 42
  y = "test"

  # Default behavior (show_print = True)
  print(x, y)  # Prints: 42 test

  # Disable printing
  c66.show_print = False
  print(x, y)  # No output

  # Re-enable printing
  c66.show_print = True
  print(x, y)  # Prints: 42 test
  ```

### More Tools
Additional utilities will be added in future updates. Stay tuned!

## Author
ChoCho66

## License
MIT
