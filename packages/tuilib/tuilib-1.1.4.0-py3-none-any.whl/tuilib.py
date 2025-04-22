import curses


class tui:
    def __init__(self):
        curses.initscr()
        curses.cbreak()  # Enable cbreak mode to capture input immediately
        curses.noecho()  # Disable automatic echoing of input

    def number_selector(stdscr,start_value=0,min_value=-999999999,max_value=9999999):
        value = start_value
        while True:
            stdscr.clear()
            stdscr.addstr(str(value))
            stdscr.refresh()
            key = stdscr.getch()

            if key == curses.KEY_DOWN and value > min_value:
                value -= 1
            elif key == curses.KEY_UP and value < max_value:
                value += 1
            elif key == 10:
                break
        return value

    def list_selector(stdscr, options, start_index=0):
        curses.curs_set(0)  # Hide cursor
        current_index = start_index

        while True:
            stdscr.clear()

        # Display the list with arrow for selection
            for idx, option in enumerate(options):
                if idx == current_index:
                    stdscr.addstr(f"> {option}\n", curses.A_REVERSE)  # Highlight selected item
                else:
                    stdscr.addstr(f"  {option}\n")

            stdscr.refresh()

            key = stdscr.getch()

            if key == curses.KEY_UP and current_index > 0:
                current_index -= 1
            elif key == curses.KEY_DOWN and current_index < len(options) - 1:
                current_index += 1
            elif key == 10:  # Enter key
                break

        return options[current_index]


    def real_time_input(stdscr, prompt=""):
        curses.curs_set(1)  # Show cursor
        input_str = ""
        stdscr.clear()
        while True:
            stdscr.clear()
            stdscr.addstr(f"{prompt}{input_str}")
            stdscr.refresh()

            key = stdscr.getch()

            if key == 27:  # ESC key to exit the input loop
                break
            elif key == 10:  # Enter key
                break
            elif key == 127:  # Backspace key
                input_str = input_str[:-1]
            else:
                input_str += chr(key)

        return input_str
    
    def func_exit(stdscr):
        curses.endwin()


    def country_selector(stdscr):
        COUNTRIES = [
            "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia",
            "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium",
            "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria",
            "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad",
            "Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic",
            "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "East Timor", 
            "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji",
            "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", 
            "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran",
            "Iraq", "Ireland", "Israel", "Italy", "Ivory Coast", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya",
            "Kiribati", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein",
            "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands",
            "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco",
            "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger",
            "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Palestine", "Panama",
            "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia",
            "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino",
            "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore",
            "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", "Spain",
            "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania",
            "Thailand", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda",
            "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu",
            "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe",
        ]
        return tui.list_selector(stdscr, COUNTRIES)



    def main(func):
        curses.wrapper(func)