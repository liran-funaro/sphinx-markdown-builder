"""
Escaping text for markdown and html.

Characters that should be escaped in Markdown:
----------------------------------------------
Emphasis chars: * and _
  Emphasis char prefix/postfix should have a non-space char to its right/left.
  _ prefix/postfix must have a space char to its left/right (or beginning/end of the text).
  We cannot make the destination between prefix/postfix in regular expression, so we will enforce both for all.
Quote/Title: > and #
  Should only precede by space chars in the line.
Block char: `
  One ` only requires not to have double line break in between
  Double `` seems to be ignored
  Three ``` must be at the beginning of the line
Title: ----
  A line that only have - or =
  No spaces between them
Horizontal line: ----
  A line that only have 3 consecutive -, _, or * or more.
  Precedes an empty line or beginng of text.
Links: [text](link)
Images: ![alt](link)
Lists: +, -, *, 1.
Tables: |
Anything starting with 4 spaces is considered a block.
  Should add force spaces (\\ ) to avoid it.
Escape char: \
  Should be followed by:
  Character Name
  \\        backslash
  `         backtick (see also escaping backticks in code)
  *         asterisk
  _         underscore
  { }       curly braces
  [ ]       brackets
  < >       angle brackets
  ( )       parentheses
  #         pound sign
  +         plus sign
  -         minus sign (hyphen)
  .         dot
  !         exclamation mark
  |         pipe (see also escaping pipe in tables)
"""

import re

# Markdown syntax anywhere in the text (`_` only at the start of a word),
# and a heading, quote or bullet-list marker at the start of a line.
ESCAPE_RE = re.compile(r"([\\*`\[\]<]|^[#>+-]|(?:^|(?<=\s|_))_)", re.M)
# The `.` or `)` of an ordered-list marker at the start of a line (`1. `), but not of a number (`1.10`).
ORDERED_LIST_RE = re.compile(r"^(\d+)([.)])(?=\s|$)", re.M)
# A bare link destination: no spaces or angle brackets, and parentheses only in balanced pairs (one level deep).
BARE_LINK_DESTINATION_RE = re.compile(r"[^\s<>()]*(?:\([^\s<>()]*\)[^\s<>()]*)*")
# A `[`, `]` or `\` in image alt text, which would end or break the `![alt]` brackets.
ALT_TEXT_ESCAPE_RE = re.compile(r"([\\\[\]])")


def markdown_chars(txt: str):
    """Escape (some) characters with special meaning for Markdown"""
    txt = ESCAPE_RE.sub(r"\\\1", txt)
    return ORDERED_LIST_RE.sub(r"\1\\\2", txt)


def link_destination(url: str):
    """Wrap a link destination in <...> only when it cannot be written bare"""
    if BARE_LINK_DESTINATION_RE.fullmatch(url):
        return url
    return "<" + url.replace("<", "\\<").replace(">", "\\>") + ">"


def alt_text(alt: str):
    """Escape the characters that end or break the alt text of an image (`![alt](uri)`)"""
    return ALT_TEXT_ESCAPE_RE.sub(r"\\\1", alt)


def html_quote(value: str):
    return value.replace('"', "&quot;")
