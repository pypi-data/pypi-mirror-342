# number selector
```

from tuilib import tui

def main(stdscr):
    num:int = tui.number_selector(stdscr,0,0,10) #starts at 0, minimum 0, maximum 10
    tui.func_exit(stdscr)
    print(num)
tui.main(main)
```

# list selector
```
from tuilib import tui
def main(stdscr):
    options = ["banana","fruit","cherry","apple"]
    choice = tui.list_selector(stdscr,options)
    tui.func_exit(stdscr)
    print("you chose",choice)
tui.main(main)
```

# real time input

dosn't work, too lazy to fix

# stdscr functions

same as the curses library