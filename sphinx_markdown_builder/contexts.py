"""
Custom context handlers for markdown.
"""

import re
import textwrap
import typing
from dataclasses import dataclass, replace
from typing import Any, Callable, Dict, Generic, Iterator, List, Optional, Tuple, Type, TypeVar, Union

from tabulate import tabulate

from sphinx_markdown_builder import escape


class UniqueString(str):
    pass


Target = typing.Literal["body", "head"]

DEFAULT_TARGET = "body"
CONTENT_START = UniqueString("content start")
EOL = "\n"
SPACE = " "
SPACE_CHARS = re.compile(r"\s+")
WRAP_REGEXP = re.compile(r"(\s*)(?=\S)([\s\S]+?)(?<=\S)(\s*)", re.M)
MULTI_LINE_BREAK = re.compile(r"(?<=\n)\n")
COMMENT_END = re.compile(r"--(!?>)")  # HTML ends a comment at `-->` and also at `--!>`


@dataclass(frozen=True)
class Spacing:
    """
    What a value needs from its neighbors: EOLs, a space if one of the given characters touches it, and a mark to merge
    with a neighbor that has the same mark.
    """

    prefix_eol: int = 0
    suffix_eol: int = 0
    # Regex character classes, e.g., `\w`.
    prefix_chars: str = ""
    suffix_chars: str = ""
    # A wrapper's mark on each edge, e.g., `*`. Where a value's suffix mark touches the same prefix mark of the next
    # value, both are dropped, so the two spans become one.
    prefix_mark: str = ""
    suffix_mark: str = ""


@dataclass(frozen=True)
class BaseParams(Spacing):
    target: Target = DEFAULT_TARGET
    include_empty_values: bool = False


class ListMarker:
    def __init__(self, marker: Union[str, int]):
        self._marker = marker

    def inc(self):
        if isinstance(self._marker, int):
            self._marker += 1

    def __repr__(self):
        if isinstance(self._marker, int):
            return f"{self._marker}. "
        return self._marker


@dataclass(frozen=True)
class Status:
    escape_text: bool = True  # Whether to escape characters
    preserve_line_breaks: bool = False  # Whether to preserve line breaks in text nodes
    section_level: int = 0  # Current section heading level
    list_marker: Optional[ListMarker] = None  # Current list marker
    desc_type: Optional[str] = None  # Current descriptor type
    in_signature: bool = False  # Whether inside a descriptor signature
    default_ref_internal: bool = False  # Current default for internal reference


class Base:
    def __init__(self, params=BaseParams()):
        self.params: BaseParams = params
        self.body: List[str] = []
        # The suffix spacing of the last value, which the next value is checked against (see `add()` and `Spacing`).
        self.suffix_eol: int = 0
        self.suffix_chars: str = ""
        self.suffix_mark: str = ""

    @property
    def nesting_key(self) -> Optional[Tuple[str, ...]]:
        """A context with a key doesn't nest inside an open context with the same key. `None` nests freely."""
        return None

    def add(self, value: str, spacing: Spacing = Spacing(), **kwargs):
        """
        Add `value` to current context.

        Parameters
        ----------
        value : str
            String to add to output document
        spacing : Spacing
            The EOLs and spaces `value` needs from its neighbors
        **kwargs
            Fields of `spacing` to replace (see Other Parameters)

        Other Parameters
        ----------------
        prefix_eol : int
            Ensures prefix EOL
        suffix_eol : int
            Ensures suffix EOL
        prefix_chars : str
            Ensures a space before `value` if the content ends with one of these characters (a regex character class)
        suffix_chars : str
            Ensures a space after `value` if the next value starts with one of these characters
        prefix_mark : str
            Merges `value` with the content if the content ends with this mark and `value` starts with it
        suffix_mark : str
            Merges the next value with `value` if it starts with this mark and `value` ends with it
        """
        if not value and not self.params.include_empty_values:
            return

        spacing = replace(spacing, **kwargs)

        self.force_eol(spacing.prefix_eol)
        if value:
            if self._merges(value, spacing):
                self.content[-1] = self.content[-1].removesuffix(spacing.prefix_mark)
                value = value.removeprefix(spacing.prefix_mark)
            elif self._needs_space(value, spacing):
                value = SPACE + value
            self.suffix_chars = spacing.suffix_chars
            self.suffix_mark = spacing.suffix_mark
        self.content.append(value)
        self.suffix_eol = spacing.suffix_eol

    def force_eol(self, count: int = 1):
        """Force adding the ensured EOLs"""
        self.ensure_eol(count)
        missing_eol = self._count_missing_eol()
        if missing_eol > 0:
            self.content.append(EOL * missing_eol)

    def ensure_eol(self, count: int = 1):
        """Ensures EOLs will be added before the next appended value"""
        self.suffix_eol = max(self.suffix_eol, count)

    def _count_missing_eol(self) -> int:
        """
        Count the number of EOL characters.
        Avoids adding EOL at the beginning of the content.
        Ignores spaces when traversing the content.
        """
        missing_count = self.suffix_eol
        for value in self._iter_reverse_char():
            if is_content_start(value):
                missing_count = 0
            if missing_count <= 0 or not is_space(value):
                break

            # This can only happen if the node's text had trailing EOL.
            # But docutils nodes are expected to be without.
            # So this validation is to avoid redundant EOLs if this behaviour changes in future releases.
            if is_eol(value):
                missing_count -= 1

        return max(0, missing_count)

    def _iter_reverse_char(self) -> Iterator[str]:
        for value in reversed(self.content):
            yield from reversed(value)

        yield CONTENT_START

    @property
    def content(self) -> List[str]:
        return self.body

    def _merges(self, value: str, spacing: Spacing) -> bool:
        """Whether `value` opens with the mark that the content closes with, e.g., `*a*` and `*b*` make `*ab*`"""
        mark = spacing.prefix_mark
        if not mark or mark != self.suffix_mark:
            return False
        return self.content[-1].endswith(mark) and value.startswith(mark)

    def _needs_space(self, value: str, spacing: Spacing) -> bool:
        last, first = self.last_char, value[0]
        if last.isspace() or first.isspace():
            return False  # A space or EOL is already there, as `force_eol()` doesn't repeat EOLs.
        return is_in(last, spacing.prefix_chars) or is_in(first, self.suffix_chars)

    @property
    def last_char(self) -> str:
        value = next(self._iter_reverse_char())
        return "" if is_content_start(value) else value

    def make(self) -> str:
        """Generate the context's content"""
        return "".join(self.content)


def is_content_start(value: str) -> bool:
    return isinstance(value, UniqueString) and value is CONTENT_START


def is_space(value: str) -> bool:
    return SPACE_CHARS.fullmatch(value) is not None


def is_eol(value: str) -> bool:
    return value == EOL


def is_in(value: str, chars: str) -> bool:
    """Whether `value` is one of `chars`, a regex character class"""
    return bool(chars) and re.fullmatch(f"[{chars}]", value) is not None


class Wrapped(Base):
    def __init__(
        self,
        prefix,
        suffix: Optional[str] = None,
        wrap_empty=False,
        params=BaseParams(),
    ):
        super().__init__(params)
        self.prefix = prefix
        self.suffix = suffix if suffix is not None else prefix
        self.wrap_empty = wrap_empty

    @property
    def nesting_key(self) -> Optional[Tuple[str, ...]]:
        """The same wrapper inside it would stack its prefix and suffix: `*` around `*a*` makes `**a**` (bold)"""
        return type(self).__name__, self.prefix, self.suffix

    def make(self):
        content = super().make()
        match = WRAP_REGEXP.fullmatch(content)
        if match is None:
            # The expression has no match only when there is no non-space character.
            if self.wrap_empty:
                return f"{self.prefix}{content}{self.suffix}"
            return content

        # We need to make sure the emphasis mark is near a non-space char,
        # but we want to preserve the existing spaces.
        prefix_space, text, suffix_space = match.groups()
        return f"{prefix_space}{self.prefix}{text}{self.suffix}{suffix_space}"


class Comment(Wrapped):
    """An HTML comment. Its text can't contain `-->` or `--!>`, which would end the comment early."""

    def __init__(self, params=BaseParams()):
        super().__init__("<!-- ", " -->", params=params)

    def make(self):
        self.body = [COMMENT_END.sub(r"- -\1", "".join(self.content))]
        return super().make()


class InlineCode(Base):
    """Inline code, e.g., `x`"""

    # Another inline code right next to it would merge their fences, e.g., `a` and `b` would read as `a``b`.
    def __init__(self, params=BaseParams(prefix_chars="`", suffix_chars="`")):
        super().__init__(params)

    def make(self):
        code = super().make()
        fence = code_fence(code, min_length=1)

        # A backtick at either end of the code would merge with the fence.
        # CommonMark strips one space from each end of inline code, so padding with a space keeps them apart.
        # E.g., `x` in backticks is written as `` `x` ``.
        if code.startswith("`") or code.endswith("`"):
            code = f" {code} "

        return f"{fence}{code}{fence}"


def code_fence(code: str, min_length: int) -> str:
    """
    The backticks that open and close `code`.
    The fence must be longer than the longest run of backticks in the code. Otherwise, that run would close it early.
    """
    longest_run = max((len(run) for run in re.findall("`+", code)), default=0)
    return "`" * max(min_length, longest_run + 1)


class CodeBlock(Base):
    """A fenced code block, e.g., ```python ... ```"""

    def __init__(self, language: str, params=BaseParams(1, 2)):
        super().__init__(params)
        self.language = language

    def make(self):
        # The closing fence goes on its own line, so a trailing line break in the code is not needed.
        code = super().make().removesuffix(EOL)
        fence = code_fence(code, min_length=3)

        lines = [f"{fence}{self.language}"]
        if code:
            lines.append(code)
        lines.append(fence)
        return EOL.join(lines)


class ParameterList(Base):
    """
    A signature's parameter list. Each finished parameter or optional group becomes one string in the body, and the
    separator before it goes inside the adjacent bracket, so the list reads correctly with or without any optional
    group: `f(a[, b], c)`, `f([a, ]b)`, `f([[a, ]b])`.
    """

    def __init__(self, params=BaseParams(include_empty_values=True)):
        super().__init__(params)
        # Where the item being visited starts (text before a param becomes part of it).
        self.parameters: list[tuple[int, bool]] = []

    def enter_parameter(self, is_required: bool):
        self.parameters.append((len(self.body), is_required))

    def make(self):
        return "".join(self._iter_body())

    def _iter_body(self):
        body_pos = 0
        required_indices = [idx for idx, (_, required) in enumerate(self.parameters) if required]
        min_required = min(required_indices, default=len(self.parameters))
        max_required = max(required_indices, default=0)

        for idx, (item_pos, is_required) in enumerate(self.parameters):
            # Yield non parameters values.
            yield from self.body[body_pos:item_pos]

            text = self.body[item_pos] if item_pos < len(self.body) else ""
            body_pos = item_pos + 1
            # The items go through `add()` before the brackets and separators between them are known, so `add()` checks
            # each item against the previous one rather than against what comes before it in the output. That is always
            # a bracket or a separator, so the space `add()` may have put before the item isn't needed (see
            # `Base._needs_space()`).
            text = text.removeprefix(SPACE)

            has_required_before = idx > min_required
            has_required_after = idx < max_required

            if is_required:
                if not has_required_before:
                    # Leading required parameter.
                    yield text
                else:
                    # Trailing required parameter.
                    yield f", {text}"
            elif not has_required_before and has_required_after:
                # Leading optional group: the separator follows it, so omitting it keeps the next item intact.
                yield f"[{text}, ]"
            elif idx > 0:
                # Trailing optional group: the separator precedes it, so omitting it keeps the previous item intact.
                yield f"[, {text}]"
            else:
                yield f"[{text}]"

        # Yield remaining non parameters values.
        yield from self.body[body_pos:]


class Table(Base):  # pylint: disable=too-many-instance-attributes
    def __init__(self, params=BaseParams(), *, compact=False):
        super().__init__(params)
        self.body: List[List[List[str]]] = []
        self.headers: List[List[List[str]]] = []
        self.internal_context = Base()
        self.compact = compact

        self.is_entry = False
        self.is_header = False
        self.is_body = False

    @property
    def content(self):
        if self.is_entry:
            return self.active_output[-1][-1]
        return self.internal_context.content

    @property
    def active_output(self) -> List[List[List[str]]]:
        if self.is_header:
            return self.headers
        assert self.is_body
        return self.body

    def enter_head(self):
        assert not self.is_header and not self.is_body
        self.is_header = True

    def exit_head(self):
        assert self.is_header and not self.is_body
        self.is_header = False

    def enter_body(self):
        assert not self.is_header and not self.is_body
        self.is_body = True

    def exit_body(self):
        assert self.is_body and not self.is_header
        self.is_body = False

    def enter_row(self):
        self.active_output.append([])

    def exit_row(self):
        pass

    def enter_entry(self):
        self.is_entry = True
        self.active_output[-1].append([])
        self.suffix_eol = 0

    def exit_entry(self):
        assert self.is_entry
        self.is_entry = False

    def make(self):
        ctx = Base()
        prefix = self.internal_context.make()
        if prefix:
            ctx.add(prefix)

        content = [*self.headers, *self.body]
        if content:
            headers = self.make_row(content[0])
            body = list(map(self.make_row, content[1:]))

            if self.compact:
                column_count = max(len(headers), max((len(r) for r in body), default=0))
                delimiter = ["---"] * column_count

                def render_row(row: List[str]) -> str:
                    cells = row + [""] * (column_count - len(row))
                    return f"| {' | '.join(cells)} |"

                all_rows = [headers, delimiter, *body]
                table = "\n".join(render_row(r) for r in all_rows)
            else:
                table = tabulate(body, headers=headers, tablefmt="github", disable_numparse=True)

            ctx.add(table, prefix_eol=2)

        return ctx.make()

    @staticmethod
    def make_row(row):
        return ["".join(entries).replace("\n", "<br/>").replace("|", r"\|") for entries in row]


class Indent(Base):
    def __init__(
        self,
        prefix,
        only_first=False,
        support_multi_line_break=False,
        empty=False,
        params=BaseParams(1, 1),
    ):
        super().__init__(params)
        self.support_multi_line_break = support_multi_line_break
        self.empty = empty
        prefix = str(prefix)
        if only_first:
            self.prefix = " " * len(prefix)
            self.first_prefix = prefix
        else:
            self.prefix = prefix
            self.first_prefix = None

    def make(self):
        content = super().make()
        if self.support_multi_line_break:
            content = replace_multi_line_break(content)
        content = textwrap.indent(content, self.prefix, predicate=(lambda _: True) if self.empty else None)
        if self.first_prefix is None:
            return content
        return content.replace(self.prefix, self.first_prefix, 1)


def replace_multi_line_break(value: str):
    return MULTI_LINE_BREAK.sub("<br/>\n", value)


class NoLineBreak(Base):
    def __init__(self, breaker=" ", params=BaseParams()):
        super().__init__(params)
        self.breaker = breaker

    def make(self):
        return super().make().strip().replace(EOL, self.breaker)


class Title(NoLineBreak):
    def __init__(self, level: int, params=BaseParams(2, 2)):
        super().__init__("<br/>", params)
        self.level = level

    def make(self):
        content = super().make()
        assert len(content) > 0, "Empty title"
        return f"{self.section_prefix} {content}"

    @property
    def section_prefix(self):
        return "#" * self.level


class Meta(NoLineBreak):
    def __init__(self, name: str, params=BaseParams(1, 1, target="head")):
        super().__init__("<br/>", params)
        assert name, "Empty meta name"
        self.name = name

    def make(self):
        content = super().make()
        if not content:
            return ""
        return f'<meta name="{escape.html_quote(self.name)}" content="{escape.html_quote(content)}"/>'


class FootNote(NoLineBreak):
    def __init__(self, ids, names, params=BaseParams(1, 1)):
        super().__init__(" ", params)
        self.ids = ids
        self.names = names
        self.label_body = Base()
        self.is_label = False

    @property
    def content(self):
        if self.is_label:
            return self.label_body.content
        return super().content

    def visit_label(self):
        self.is_label = True

    def depart_label(self):
        self.is_label = False

    def make(self):
        content = super().make()
        label = self.label_body.make() or self.names
        return f"* <a id='{self.ids}'>**[{label}]**</a> {content}"


BaseT = TypeVar("BaseT", bound=Base)

Translator = Callable[[Any, Any], Dict[str, Any]]
default_translator: Translator = lambda _node, _elem: {}


class PushContext(Generic[BaseT]):  # pylint: disable=too-few-public-methods
    def __init__(
        self,
        ctx: Type[BaseT],
        *args,
        translator: Translator = default_translator,
        **kwargs,
    ):
        self.ctx = ctx
        self.translator = translator
        self.args = args
        self.kwargs = kwargs

    def create(self, node, element_key) -> BaseT:
        kwargs = dict(self.kwargs)
        kwargs.update(self.translator(node, element_key))
        return self.ctx(*self.args, **kwargs)


def emphasis(mark: str) -> PushContext:
    """
    CommonMark only reads an emphasis mark that fits its neighbors (the "flanking" rules). A space between the mark and
    a word or another mark always fits, though it is redundant when the character inside the mark is a word.
    Touching spans with the same mark merge, so a type hint like `Optional[int]`, which Sphinx splits into a node per
    token, reads as one span.
    """
    params = BaseParams(prefix_chars=r"\w*", suffix_chars=r"\w*", prefix_mark=mark, suffix_mark=mark)
    return PushContext(Wrapped, mark, params=params)


ITALIC = emphasis("*")  # _ is more restrictive
STRONG = emphasis("**")  # _ is more restrictive
SUBSCRIPT = PushContext(Wrapped, "<sub>", "</sub>")
DOC_INFO = PushContext(
    Meta,
    translator=lambda _node, elem: {"name": f"{elem}: "},
)


@dataclass(frozen=True)
class PushBox:
    title: str
    heading: str | None = None
