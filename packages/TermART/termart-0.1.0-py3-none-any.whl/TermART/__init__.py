def reset(type=None):
    if type == "Font_style":
        return "\033[22m\033[23m\033[24m\033[25m\033[29m"
    if type == "Bold":
        return "\033[22m"
    if type == "Underline":
        return "\033[24m"
    if type == "Italic":
        return "\033[23m"
    if type == "tc":
        return "\033[39m"
    if type == "bg":
        return "\033[49m"
    return "\033[0m"
def tc(colour):
    colour_list = {
        "RED": "\033[91m",
        "GREEN": "\033[92m",
        "BLUE": "\033[94m",
        "YELLOW": "\033[33m",
        "MAGENTA": "\033[35m",
        "CYAN": "\033[36m",
        "WHITE": "\033[37m",
        "BLACK": "\033[30m",
    }
    return colour_list.get(colour.upper(), "")

def bg(colour):
    colour_list = {
        "RED": "\033[101m",
        "GREEN": "\033[102m",
        "BLUE": "\033[104m",
        "YELLOW": "\033[103m",
        "MAGENTA": "\033[105m",
        "CYAN": "\033[106m",
        "WHITE": "\033[107m",
        "BLACK": "\033[40m"
    }
    return colour_list.get(colour.upper(), "")

def tc_rgb(r,g,b):
    return f"\033[38;2;{r};{g};{b}m"
def bg_rgb(r,g,b):
    return f"\033[48;2;{r};{g};{b}m"

def fs(style):
    if style == "Bold":
        return "\033[1m"
    if style == "Underline":
        return "\033[4m"
    if style == "Reversed":
        return "\033[7m"
    if style == "Italic":
        return "\033[3m"