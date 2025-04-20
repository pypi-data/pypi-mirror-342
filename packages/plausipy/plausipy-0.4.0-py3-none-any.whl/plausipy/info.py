import re
import shutil
from typing import TYPE_CHECKING, Literal

from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import clear

from .user import Consent

if TYPE_CHECKING:
    from plausipy import Plausipy


def show_tracking_info(package: "Plausipy", packages: list["Plausipy"]) -> Consent:
    # title and message
    # NOTE: packages includes the main package
    title = "Usage Data Collection Information"
    message = f"This python package ({package.name}) and {len(packages) - 1} related packages collect anonymous usage information.\nThe information is fully anonymized and cannot be traced back to your person. This information is important for the package maintainers to improve their services."

    # options
    options = [
        ("Allow", "y"),
        ("Deny", "n"),
        ("Ask every time", "a"),
        ("More Information", "i"),
    ]

    selected_index = _print_interactive_box(title, message, options)
    consent = Consent(options[selected_index][1])

    if options[selected_index][1] == "i":
        title = "More Information"
        message = ""

        for package in packages:
            message += f"- {package.name}\n"

        selected_index = _print_interactive_box(title, message, options[:3])
        consent = Consent(options[selected_index][1])

    # return consent
    return consent


def show_tracking_required(packages: list["Plausipy"]) -> Literal["a", "w", "x"]:
    # title and message
    title = "Tracking Required"
    message = "Tracking is required for the following packages:\n"

    for package in packages:
        message += f"- {package.name} ({package.profile.name})\n"

    # options
    options = [
        ("Allow Once", "a"),
        ("Whitelist Packages", "w"),
        ("End Program", "x"),
    ]

    # print box
    selected_index = _print_interactive_box(title, message, options)

    # return
    return options[selected_index][1]


def show_setup_plausipy_box(request_whitelist: list["Plausipy"]):
    title = "Plausipy Setup"
    message = "Some packages would like to collect anonymous usage information.\n"
    message += "Please setup Plausipy with your preference or visit https://plausipy.com to learn more.\n"

    # Add commands explanation
    message += "\nYou can allow or deny tracking globally:\n"
    message += "  \033[90mplausipy consent --allow\033[0m Allow tracking.\n"
    message += "  \033[90mplausipy consent --deny\033[0m  Deny tracking.\n"

    if len(request_whitelist):
        message += "\nThe following packages require usage statistics and can be whitelisted:\n"
        message += (
            "  \033[90mplausipy consent --whitelist "
            + " ".join(p.name for p in request_whitelist)
            + "\033[0m"
        )

    _print_box(title, message)


def _print_box(
    title: str,
    message: str,
    options: list[tuple[str, str]] | None = None,
    selected_index: int = 0,
):
    # Get terminal width
    terminal_width = shutil.get_terminal_size().columns

    # Create a border
    border = "═" * (terminal_width - 2)  # -2 for borders on both sides

    # print top border
    print("╔" + border + "╗")

    # Print title
    title_line = f" {title} ".center(terminal_width - 2)  # Center title
    print("║" + title_line + "║")

    # Print message
    message_lines = message.split("\n")

    def vlen(s):
        # Remove ANSI escape sequences to calculate visible length
        return len(re.sub(r"\033\[[0-9;]*m", "", s))

    # split all lines at the terminal width if they are too long
    # Process lines that are too long
    i = 0
    while i < len(message_lines):
        line = message_lines[i]
        if vlen(line) > terminal_width - 4:
            # Find the last space or dash before the width limit
            split_pos = terminal_width - 4
            for j in range(terminal_width - 4, 0, -1):
                if line[j] in [" ", "-"]:
                    split_pos = j + 1
                    break

            # Split the line
            message_lines[i] = line[:split_pos].rstrip()
            message_lines.insert(i + 1, line[split_pos:].lstrip())
        i += 1

    for line in message_lines:
        message_line = f" {line} " + " " * (
            terminal_width - vlen(line) - 4
        )  # Left justify message
        print("║" + message_line + "║")

    # Print a new line before options
    print("║" + " " * (terminal_width - 2) + "║")

    # Print options horizontally
    if options is not None and len(options) > 0:
        options_line = "  ".join(
            [
                f"{'●' if i == selected_index else '○'} {options[i][0]} ({options[i][1]})"
                for i in range(len(options))
            ]
        )
        print("║" + options_line.center(terminal_width - 2) + "║")

    # brint bottom border
    print("╚" + border + "╝")


def _print_interactive_box(
    title: str, message: str, options: list[tuple[str, str]]
) -> int:
    selected_index = 0
    session = PromptSession()
    kb = KeyBindings()

    # Key bindings for arrow keys
    @kb.add("left")
    def _(event):
        nonlocal selected_index
        selected_index = (selected_index - 1) % len(options)
        refresh_display(selected_index)

    @kb.add("right")
    def _(event):
        nonlocal selected_index
        selected_index = (selected_index + 1) % len(options)
        refresh_display(selected_index)

    @kb.add("tab")
    def _(event):
        nonlocal selected_index
        selected_index = (selected_index + 1) % len(options)
        refresh_display(selected_index)

    @kb.add("enter")
    def _(event):
        session.app.exit()

    # Adding shortcut keys for options
    for index, (_option, shortcut) in enumerate(options):

        @kb.add(shortcut)
        def _(event, index=index):
            nonlocal selected_index
            selected_index = index
            session.app.exit()

    def refresh_display(selected_index):
        clear()  # Clear the console
        _print_box(title, message, options, selected_index)

    # Display the initial options
    refresh_display(selected_index)

    # display prompt
    session.prompt(key_bindings=kb)

    # return (sync)
    return selected_index
