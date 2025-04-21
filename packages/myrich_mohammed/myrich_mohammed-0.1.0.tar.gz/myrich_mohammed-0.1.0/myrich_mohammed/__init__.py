from rich.console import Console as Con
from rich.text import Text

con = Con(color_system="256")

def rich_input(prompt_text: str = "Enter input: ", style: str = "45") -> str:
    try:
        style_int = int(style)
        if not (1 <= style_int <= 255):
            raise ValueError
        style = f"color({style})"
    except ValueError:
        con.print("Invalid style code, using default color.", style="bold red")
        style = "color(45)"

    prompt = Text(prompt_text, style=style)
    con.print(prompt, end="")
    return input()

def show_all_colors() -> None:
    for i in range(1, 256):
        con.print(f"{i}: Sample Text", style=f"color({i})")