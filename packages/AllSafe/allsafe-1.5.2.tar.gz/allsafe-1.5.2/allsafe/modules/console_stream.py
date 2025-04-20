from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel


class Style:
    RED = "#cc3333"
    GREEN = "#00a693"
    GRAY = "#6c757d"
    PASSWD = f"bold {GREEN}"

    def __getattr__(self, name):
        def _get_md(text: str) -> str:
            color = getattr(self, name.upper())
            return self.get_md(color, text)

        return _get_md

    def get_md(self, color, text):
        return f"[{color}]{text}[/{color}]"  # [color]text[/color]


class ConsoleStream:
    """Control and style console input and output"""
    def __init__(self) -> None:
        self.writer = Console()
        self.styles = Style()

    def panel(self, title, text, **kwargs):
        """Write a styled panel with the provided title and text to the console"""
        panel = Panel.fit(text, title=title, **kwargs)
        self.write(panel, justify="left")

    def ask(self, prompt, **kwargs):
        """
        Prompts the user for input and filters the result using a callback
        function, if provided.
        """
        func = kwargs.pop("func", None)
        style = kwargs.pop("style", None)
        if style is not None:  # might be needed in the future
            prompt = self.styles.get_md(style, prompt)
        input_string = ""
        while not input_string:
            input_string = Prompt.ask(prompt, console=self.writer, **kwargs)
            if callable(func):
                try:
                    result = func(input_string)
                    return result
                except ValueError as e:
                    self.error(e)
                    input_string = ""
        return input_string

    def write(self, text, **kwargs):
        """Write the given styled text to the console"""
        self.writer.print(text, **kwargs)

    def error(self, text):
        """Write the given text in error style to the console"""
        self.write(text, style=self.styles.RED)
