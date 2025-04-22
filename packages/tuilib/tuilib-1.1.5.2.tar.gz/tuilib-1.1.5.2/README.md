# number selector
```python

from tuilib import tui

def main(stdscr):
    num:int = tui.number_selector(stdscr,0,0,10) #starts at 0, minimum 0, maximum 10
    tui.func_exit(stdscr)
    print(num)
tui.main(main)
```

# list selector
```python
from tuilib import tui
def main(stdscr):
    options = ["banana","fruit","cherry","apple"]
    choice = tui.list_selector(stdscr,options)
    tui.func_exit(stdscr)
    print("you chose",choice)
tui.main(main)
```

# real time input

ok I fixed it anyway

```python

from tuilib import tui
def main(stdscr):
    name:str = tui.real_time_input(stdscr,"what is yourt name?: ")
    tui.func_exit(stdscr)
    print("hello",name)
tui.main(main)
```

# stdscr functions

same as the curses library


to install:

```bash

pip install tuilib
```