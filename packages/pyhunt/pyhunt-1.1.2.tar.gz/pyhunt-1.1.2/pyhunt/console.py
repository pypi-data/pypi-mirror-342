import re
import sys
import os


class Console:
    """
    Supports basic styles, hex colors (#RRGGBB, bg#RRGGBB), and OSC 8 hyperlinks.
    """

    # --- Class Constants for ANSI/VT Codes ---
    _STYLE_CODES = {
        # Foregrounds (Basic)
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        # Backgrounds (Basic)
        "bgblack": "\033[40m",
        "bgred": "\033[41m",
        "bggreen": "\033[42m",
        "bgyellow": "\033[43m",
        "bgblue": "\033[44m",
        "bgmagenta": "\033[45m",
        "bgcyan": "\033[46m",
        "bgwhite": "\033[47m",
        # Attributes
        "bold": "\033[1m",
        "dim": "\033[2m",
        "italic": "\033[3m",
        "underline": "\033[4m",
        "blink": "\033[5m",
        "reverse": "\033[7m",
        "hidden": "\033[8m",
        "strikethrough": "\033[9m",
    }
    _RESET = "\033[0m"
    _OSC_8_START = "\033]8;;"
    _OSC_8_END = "\a"  # BEL character, some terminals prefer \033\\ (ST)

    # --- Static Helper Method ---
    @staticmethod
    def _hex_to_ansi_rgb(hex_code, background=False):
        """Converts a hex color code (e.g., #RRGGBB) to an ANSI 24-bit color code."""
        hex_code = hex_code.lstrip("#")
        if len(hex_code) != 6:
            return ""  # Return empty string for invalid hex length
        try:
            r = int(hex_code[0:2], 16)
            g = int(hex_code[2:4], 16)
            b = int(hex_code[4:6], 16)
        except ValueError:
            return ""  # Return empty string for invalid hex characters

        prefix = "\033[48;2;" if background else "\033[38;2;"
        return f"{prefix}{r};{g};{b}m"

    # --- Instance Methods ---
    def __init__(self, file=None):
        """
        Initializes the Console instance.

        Args:
            file: The file object to write to. Defaults to sys.stdout.
        """
        self._file = file if file is not None else sys.stdout

    def print(self, text, *, end="\n"):
        """
        Parses text with markup and prints it directly to the console (self.file).

        Args:
            text (str): The text string containing markup.
            end (str, optional): String appended after the processed text. Defaults to "\\n".

        Markup examples:
        - [bold red]Text[/]
        - [#ff0000]Red Text[/]
        - [bg#00ff00 white]White on Green[/]
        - [underline link=https://example.com]Link[/]
        """

        # Define the replacer function inside the print method
        # It can access class constants via Console._ GGG
        def replacer(match):
            attributes_str = match.group(1).strip()
            content = match.group(2)

            link = None
            active_codes = []

            parts = attributes_str.split()
            for part in parts:
                lowered_part = part.lower()

                if lowered_part.startswith("link="):
                    link = part[len("link=") :]
                elif lowered_part.startswith("#") and len(lowered_part) == 7:
                    ansi_code = Console._hex_to_ansi_rgb(lowered_part, background=False)
                    if ansi_code:
                        active_codes.append(ansi_code)
                elif lowered_part.startswith("bg#") and len(lowered_part) == 9:
                    ansi_code = Console._hex_to_ansi_rgb(
                        lowered_part[2:], background=True
                    )
                    if ansi_code:
                        active_codes.append(ansi_code)
                elif lowered_part in Console._STYLE_CODES:
                    active_codes.append(Console._STYLE_CODES[lowered_part])

            style_sequence = "".join(active_codes)

            if link:
                formatted_content = f"{style_sequence}{content}{Console._RESET}"
                return f"{Console._OSC_8_START}{link}{Console._OSC_8_END}{formatted_content}{Console._OSC_8_START}{Console._OSC_8_END}"
            else:
                return f"{style_sequence}{content}{Console._RESET}"

        # The regex pattern (same as before)
        # Using Console._RESET ensures access to the class constant
        processed_text = re.sub(
            r"\[([^\]]+)\](.*?)\[\/.*?\]", replacer, text, flags=re.IGNORECASE
        )

        # Print the final processed string to the instance's file
        # Use os.write to output bytes directly
        output_bytes = (processed_text + end).encode()
        os.write(self._file.fileno(), output_bytes)
