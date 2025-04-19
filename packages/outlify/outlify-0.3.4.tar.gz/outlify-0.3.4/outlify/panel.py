from abc import ABC, abstractmethod
from typing import Any, Mapping, Iterable, Optional, Union
import shutil
import textwrap

from outlify.styles import Align, BorderStyle


__all__ = ['Panel', 'ParamsPanel']


class PanelBase(ABC):
    def __init__(
            self, content: Any, *, width: Optional[int],
            title: str, title_align: Union[str, Align],
            subtitle: str, subtitle_align: Union[str, Align],
            border_style: Union[str | BorderStyle]
    ):
        border_style = self._parse_border_style(border_style)
        self.width = self._resolve_width(width)
        self.header = self.get_header(
            title, align=self._resolve_title_align(title_align), width=self.width,
            left=border_style.lt, char=border_style.headers, right=border_style.rt
        )
        self.footer = self.get_header(
            subtitle, align=self._resolve_title_align(subtitle_align), width=self.width,
            left=border_style.lb, char=border_style.headers, right=border_style.rb
        )
        self.content = self.get_content(content, width=self.width, char=border_style.sides)

    @staticmethod
    def _resolve_title_align(align: Union[str, Align]) -> Align:
        if isinstance(align, Align):
            return align
        return Align(align.lower())

    @abstractmethod
    def get_content(self, content: str, *, width: int, char: str) -> str:
        pass

    @staticmethod
    def _parse_border_style(style: str) -> BorderStyle:
        if isinstance(style, BorderStyle):
            return style
        if not isinstance(style, str):
            raise ValueError(
                f'Invalid type for border_style: {style} ({type(style)}) variable is not str or BorderStyle'
            )
        if len(style) not in [5, 6]:
            raise ValueError(f'Invalid length for border_style (!= 5 or != 6): length of {style} = {len(style)}')
        return BorderStyle(
            lt=style[0], rt=style[1],
            lb=style[2], rb=style[3],
            headers=style[4],
            sides=style[5] if len(style) == 6 else '',
        )

    @staticmethod
    def _resolve_width(width: Optional[int]) -> int:
        if isinstance(width, int):
            return width
        if width is not None:
            raise ValueError(f'Invalid type for width: {width} is not int')

        try:
            return shutil.get_terminal_size().columns
        except (AttributeError, OSError):
            return 80  # Fallback width

    def get_header(self, title: str, *, width: int, align: Align, left: str, char: str, right: str) -> str:
        return f'{left}{self._fill_header(title, width=width - 2, align=align, char=char)}{right}'

    @staticmethod
    def _fill_header(title: str, *, width: int, align: Align, char: str) -> str:
        title = f' {title} ' if title else ''
        if align == Align.left:
            title = f'{char}{title}'
            return f'{title.ljust(width, char)}'
        elif align == Align.center:
            return title.center(width, char)
        title = f'{title}{char}'
        return title.rjust(width, char)

    @staticmethod
    def fill(line: str, *, width: int, char: str, indent: str = '') -> str:
        """ Fill a single line

        :param line: the content to be placed inside the panel
        :param width: total available width for the content (excluding side borders)
        :param char: border character to be placed on both sides of the line
        :param indent: indentation added before the content
        :return: a string representing the line wrapped with borders and padded to match the specified width
        """
        return f'{char} {indent}{line.ljust(width - len(indent))} {char}'

    def __str__(self) -> str:
        return '\n'.join([self.header, self.content, self.footer])

    def __repr__(self) -> str:
        return self.__str__()


class Panel(PanelBase):
    def __init__(
            self, content: str, *, width: Optional[int] = None,
            title: str = '', title_align: Union[str, Align] = 'center',
            subtitle: str = '', subtitle_align: Union[str, Align] = 'center',
            border_style: Union[str | BorderStyle] = '╭╮╰╯─│'
    ):
        """ A simple panel for displaying plain text with customizable borders, title, and subtitle.

        This class inherits from `PanelBase` and provides a way to create a terminal panel with
        plain text content. It allows you to configure the panel's width, title, subtitle, alignment,
        and border style. The panel is designed to be used directly in the terminal for displaying information
        in a visually appealing way.

        :param content: the plain text content to be displayed inside the panel. It supports multi-line strings.
        :param width: total panel width (including borders)
        :param title: title displayed at the top of the panel
        :param title_align: alignment of the title. Can be a string ('left', 'center', 'right') or an Align enum/type
        :param subtitle: subtitle displayed below the title
        :param subtitle_align: alignment of the subtitle. Same format as title_align
        :param border_style: Border character style. Can be a string representing custom border characters
                             or an instance of BorderStyle
        """
        super().__init__(
            content, width=width,
            title=title, title_align=title_align,
            subtitle=subtitle, subtitle_align=subtitle_align,
            border_style=border_style
        )

    def get_content(self, content: str, *, width: int, char: str) -> str:
        """ Get prepared panel content

        :param content: multi-line string to display in the panel
        :param width: total panel width (including borders)
        :param char: character for the side borders. If empty string, disables wrapping and borders
        :return: panel with prepared content
        """
        if not isinstance(content, str):
            raise ValueError(f'Invalid type for content: {type(content)} is not str')
        if width < 4:
            raise ValueError(f'Invalid value for width: {width} < 4')
        width = width - 4

        lines = []
        for line in content.splitlines():
            if char == '' or (line := line.strip()) == '':
                lines.append(line)
                continue

            wrapped = textwrap.wrap(
                line, width=width, replace_whitespace=False,
                drop_whitespace=False, break_on_hyphens=False
            )
            lines.extend(wrapped)

        lines = [self.fill(line, width=width, char=char) for line in lines]
        return '\n'.join(lines)


class ParamsPanel(PanelBase):
    def __init__(
            self, content: Mapping[str, str], *, width: Optional[int] = None,
            title: str = '', title_align: Union[str, Align] = 'center',
            subtitle: str = '', subtitle_align: Union[str, Align] = 'center',
            border_style: Union[str | BorderStyle] = '╭╮╰╯─│',
            hidden: Iterable[str] = (), separator: str = ' = '
    ):
        """ A panel for displaying key-value parameters in a formatted layout.

        Inherits from `PanelBase` and is used to present a set of parameters, e.g. configuration settings,
        metadata, etc. in a styled, optionally bordered panel. Supports custom title, subtitle, alignment,
        and the ability to hide selected parameters.

        :param content: a mapping of keys to string values to display in the panel.
                        For example: {'learning_rate': '0.001', 'batch_size': '64'}.
        :param width: total panel width (including borders)
        :param title: title displayed at the top of the panel
        :param title_align: alignment of the title. Can be a string ('left', 'center', 'right') or an Align enum/type
        :param subtitle: subtitle displayed below the title
        :param subtitle_align: alignment of the subtitle. Same format as title_align
        :param border_style: Border character style. Can be a string representing custom border characters
                             or an instance of BorderStyle
        :param hidden: Iterable of keys from `content` that should be excluded from display.
                       Useful for filtering out sensitive or irrelevant data
        :param separator: key-value separator
        """
        self.hidden = hidden
        self.separator = separator
        super().__init__(
            content, width=width,
            title=title, title_align=title_align,
            subtitle=subtitle, subtitle_align=subtitle_align,
            border_style=border_style
        )

    def get_content(self, content: Mapping[Any, Any], *, width: int, char: str) -> str:
        """ Get prepared panel content

        :param content: parameters that should be in the panel
        :param width: total panel width (including borders)
        :param char: character for the side borders. If empty string, disables wrapping and borders
        :return: panel with prepared content
        """
        if not isinstance(content, Mapping):
            raise ValueError(f'Invalid type for content: {type(content)} is not Mapping')
        if width < 4:
            raise ValueError(f'Invalid value for width: {width} < 4')
        width = width - 4
        params: Mapping[str, str] = {str(key): str(value) for key, value in content.items()}

        lines = []
        max_key_length = max(len(key) for key in params.keys())
        width_inside = width - max_key_length - len(self.separator)
        indent = ' ' * (max_key_length + len(self.separator))
        for key, value in params.items():
            displayed_value = "*****" if key in self.hidden else value
            line = f"{key.ljust(max_key_length)}{self.separator}{displayed_value}"

            if not char:  # mode without border in sides
                lines.append(f'  {line}')
                continue

            if len(line) <= width:  # the whole line fits in the panel
                lines.append(self.fill(line, width=width, char=char))
                continue

            # it's necessary to split the string
            head, tail = line[:width], line[width:]
            wrapped = textwrap.wrap(
                tail, width=width_inside, replace_whitespace=False,
                drop_whitespace=False, break_on_hyphens=False
            )
            lines.append(self.fill(head, width=width, char=char))
            for line in wrapped:
                lines.append(self.fill(line, width=width, char=char, indent=indent))
        return '\n'.join(lines)


if __name__ == '__main__':
    text = (
        "Outlify helps you render beautiful command-line panels.\n"
        "You can customize borders, alignment, etc.\n\n"
        "This is just a simple text panel."
    )
    print(Panel(
        text, title='Welcome to Outlify', subtitle='Text Panel Demo', title_align='left', subtitle_align='right'
    ), '', sep='\n')

    long_text = (
        "In a world where CLI tools are often boring and unstructured, "
        "Outlify brings beauty and structure to your terminal output. "
        "It allows developers to create elegant panels with customizable borders, titles, subtitles, "
        "and aligned content — all directly in the terminal.\n\n"
        "Outlify is lightweight and dependency-free — it uses only Python’s standard libraries, "
        "so you can easily integrate it into any project without worrying about bloat or compatibility issues.\n\n"
        "Whether you're building debugging tools, reporting pipelines, or just want to print data in a cleaner way, "
        "Outlify helps you do it with style."
    )
    print(Panel(
        long_text, title='Long Text Panel Example', subtitle='using another border style', border_style='╔╗╚╝═║'
    ), '', sep='\n')

    text = (
        'or maybe you want to output parameters that came to your CLI input, '
        'but you do not want to output it in raw form or write a nice wrapper yourself, '
        'and the sensitive data should not be visible in the terminal, but you want to know that it is specified'
    )
    print(Panel(text, subtitle='See ↓ below', border_style='┌┐└┘  '), '', sep='\n')
    parameters = {
        'first name': 'Vladislav',
        'last name': 'Kishkin',
        'username': 'k1shk1n',
        'password': 'fake-password',
        'description': 'This is a fake description to show you how Outlify can wrap text in the Parameters Panel'
    }
    print(ParamsPanel(
        parameters, title='Start Parameters', hidden=('password',)
    ))
