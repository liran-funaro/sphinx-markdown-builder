# Changelog

## Unreleased

- Render admonitions as GitHub-style alerts and support generic admonitions and sidebars. ([liran-funaro/sphinx-markdown-builder#64](https://github.com/liran-funaro/sphinx-markdown-builder/pull/64)) — [Liran Funaro](https://github.com/liran-funaro)

## 0.6.11

- Include `LICENSE` in distribution packages by correcting the license-files path. ([liran-funaro/sphinx-markdown-builder#60](https://github.com/liran-funaro/sphinx-markdown-builder/pull/60)) — [Adrian](https://github.com/AdrianAtZyte)
- Preserve line breaks in code, doctest, and math blocks when generating GitHub-flavored Markdown. ([liran-funaro/sphinx-markdown-builder#59](https://github.com/liran-funaro/sphinx-markdown-builder/pull/59)) — [Mal Curtis](https://github.com/snikch)
- Copy downloadable files into the output and generate correct relative links while preserving external download URLs. ([liran-funaro/sphinx-markdown-builder#58](https://github.com/liran-funaro/sphinx-markdown-builder/pull/58)) — [Jacob Tomlinson](https://github.com/jacobtomlinson)
- Support tip, caution, danger, and error admonition directives. ([liran-funaro/sphinx-markdown-builder#50](https://github.com/liran-funaro/sphinx-markdown-builder/pull/50)) — [Caleb Smith](https://github.com/calsmith1-nokia)

## 0.6.10

- Remove the `ExtensionMetadata` import to restore compatibility with Sphinx versions that do not provide it. ([1d489a5](https://github.com/liran-funaro/sphinx-markdown-builder/commit/1d489a566d4fa5ac2519a8cae0e57200bf50ff87)) — [Liran Funaro](https://github.com/liran-funaro)

## 0.6.9

- Add `markdown_flavor=github` to remove unwanted paragraph line breaks on GitHub. ([liran-funaro/sphinx-markdown-builder#41](https://github.com/liran-funaro/sphinx-markdown-builder/pull/41)) — [Johannes Altmanninger](https://github.com/krobelus)
- Enable safe parallel reading and writing in Sphinx builds. ([liran-funaro/sphinx-markdown-builder#38](https://github.com/liran-funaro/sphinx-markdown-builder/pull/38)) — [Johannes Altmanninger](https://github.com/krobelus)
- Raise build requirements to setuptools 80.9 and wheel 0.45.1 for modern license metadata. ([fe24764](https://github.com/liran-funaro/sphinx-markdown-builder/commit/fe24764940e8bd013484a9157af33ccf0f51ca26)) — [Liran Funaro](https://github.com/liran-funaro)
- Use PEP 639 SPDX license metadata for modern packaging tools. ([liran-funaro/sphinx-markdown-builder#39](https://github.com/liran-funaro/sphinx-markdown-builder/pull/39)) — [Terje Røsten](https://github.com/terjeros)
- Add `markdown_file_suffix` to configure the extension of generated Markdown files. ([liran-funaro/sphinx-markdown-builder#40](https://github.com/liran-funaro/sphinx-markdown-builder/pull/40)) — [Jared Dillard](https://github.com/jdillard)
- Support multiline C-domain signatures and correctly type Markdown configuration values. ([967edca](https://github.com/liran-funaro/sphinx-markdown-builder/commit/967edca036a73f7644251abd52a5da8451a10dd4)) — [Liran Funaro](https://github.com/liran-funaro)

## 0.6.8

- Add `markdown_bullet` to configure the default bullet marker and rebuild output when Markdown settings change. ([81ccbda](https://github.com/liran-funaro/sphinx-markdown-builder/commit/81ccbdac20bda62e59d577ce87da3a4313e600f7)) — [Liran Funaro](https://github.com/liran-funaro)
- Handle labels outside footnotes without assertion failures. ([71a666c](https://github.com/liran-funaro/sphinx-markdown-builder/commit/71a666c15ee2cd588549f59803913729857bb887)) — [Liran Funaro](https://github.com/liran-funaro)
- Support the hint admonition directive. ([liran-funaro/sphinx-markdown-builder#29](https://github.com/liran-funaro/sphinx-markdown-builder/pull/29)) — [dreamz](https://github.com/dreamz12345)

## 0.6.7

- Support the important admonition directive. ([f11af7b](https://github.com/liran-funaro/sphinx-markdown-builder/commit/f11af7b23a97aa8626e1608036c9a1d7e5d8014a)) — [Liran Funaro](https://github.com/liran-funaro)
- Render return type hints when `autodoc_typehints` is set to signature. ([f844521](https://github.com/liran-funaro/sphinx-markdown-builder/commit/f844521dbaf19ed1f0e228657e704272b7c8711c)) — [Liran Funaro](https://github.com/liran-funaro)
- Render footnotes and linked superscript references with stable anchors. ([liran-funaro/sphinx-markdown-builder#20](https://github.com/liran-funaro/sphinx-markdown-builder/pull/20)) — [Yashar Zolmajdi](https://github.com/yashicon21) and [Liran Funaro](https://github.com/liran-funaro)
- Support figure directives without skipping their image content. ([liran-funaro/sphinx-markdown-builder#16](https://github.com/liran-funaro/sphinx-markdown-builder/pull/16)) — [Yashar Zolmajdi](https://github.com/yashicon21)

## 0.6.6

- Allow annotations inside API parameter lists without assertion failures. ([d85121e](https://github.com/liran-funaro/sphinx-markdown-builder/commit/d85121eb6a6f45cb5fb55050450f0badedd14940)) — [Liran Funaro](https://github.com/liran-funaro)
- Register the Markdown builder through standard Sphinx entry-point discovery. ([767c5db](https://github.com/liran-funaro/sphinx-markdown-builder/commit/767c5dbc175e51c037e1fb308a638f33ba22e567)) — [Liran Funaro](https://github.com/liran-funaro)
- Require Sphinx 5.1 or newer to match the APIs used by the extension. ([8c5efd1](https://github.com/liran-funaro/sphinx-markdown-builder/commit/8c5efd1454ac2a04c7955b7489c121fb1ca6ba01)) — [Liran Funaro](https://github.com/liran-funaro)
- Fix italic formatting when emphasized text begins with punctuation. ([900f42e](https://github.com/liran-funaro/sphinx-markdown-builder/commit/900f42eac7adbdf3cbac629de4ba316085981ef1)) — [Liran Funaro](https://github.com/liran-funaro)
- Support glossary terms, definitions, and links to term anchors. ([liran-funaro/sphinx-markdown-builder#10](https://github.com/liran-funaro/sphinx-markdown-builder/pull/10)) — [Adam Zlatniczki](https://github.com/adam-zlatniczki) and [Liran Funaro](https://github.com/liran-funaro)

## 0.6.5

- Preserve table titles and other content outside table cells. ([808c5b6](https://github.com/liran-funaro/sphinx-markdown-builder/commit/808c5b6dfa92d3fab437de3661df90c0472777df)) — [Liran Funaro](https://github.com/liran-funaro)
- Avoid spurious file-access warnings when output files have not been generated yet. ([49aa351](https://github.com/liran-funaro/sphinx-markdown-builder/commit/49aa3517a2c69595bda9f139786c191dcf809f1c)) — [Liran Funaro](https://github.com/liran-funaro)

## 0.6.4

- Handle empty tables without raising an assertion. ([960cb08](https://github.com/liran-funaro/sphinx-markdown-builder/commit/960cb08ba574321d678c5ed6950dc01853cf0268)) — [Liran Funaro](https://github.com/liran-funaro)

## 0.6.3

- Add colons to parameter and other field labels. ([75f7540](https://github.com/liran-funaro/sphinx-markdown-builder/commit/75f7540dca3c60ff2dd74c1d15014b9772804599)) — [Liran Funaro](https://github.com/liran-funaro)

## 0.6.2

- Avoid extra blank lines between nested list items. ([906712c](https://github.com/liran-funaro/sphinx-markdown-builder/commit/906712c90ca8a25fef9b8590d3dc4ec42231049b)) — [Liran Funaro](https://github.com/liran-funaro)

## 0.6.1

- Separate explicit reference anchors from surrounding text with blank lines. ([4fa43c9](https://github.com/liran-funaro/sphinx-markdown-builder/commit/4fa43c9bce677a0a5b7f058c62b924605aa5c156)) — [Liran Funaro](https://github.com/liran-funaro)
- Render topic directives as blockquotes with working internal links. ([454b8f4](https://github.com/liran-funaro/sphinx-markdown-builder/commit/454b8f4663798c45b25cf4e9db359e20bbf4eebe)) — [Liran Funaro](https://github.com/liran-funaro)
- Add optional document-info HTML metadata, preserve line-block breaks, and normalize multiline headings. ([5caf038](https://github.com/liran-funaro/sphinx-markdown-builder/commit/5caf0380163624d68570812b557334b4230a9a76)) — [Liran Funaro](https://github.com/liran-funaro)
- Resolve download references from their source targets. ([1f6449a](https://github.com/liran-funaro/sphinx-markdown-builder/commit/1f6449a362449cae091c62db151e1ace4aaefec1)) — [Liran Funaro](https://github.com/liran-funaro)
- Render definition lists with definition markers and preserve multiline definitions. ([6064a7e](https://github.com/liran-funaro/sphinx-markdown-builder/commit/6064a7e75efcc715f6fed08096e9142952baed7f)) — [Liran Funaro](https://github.com/liran-funaro)
- Rebuild missing or unreadable output files and handle file-access errors without aborting the build. ([fe3d27c](https://github.com/liran-funaro/sphinx-markdown-builder/commit/fe3d27cfe14b8b4edd4539c0a6ae952372dce487)) — [Liran Funaro](https://github.com/liran-funaro)
- Render admonitions and version notices as separate boxes and label doctest blocks as `pycon`. ([5da581f](https://github.com/liran-funaro/sphinx-markdown-builder/commit/5da581faf1663bc619029133544340145e838f8a)) — [Liran Funaro](https://github.com/liran-funaro)

## 0.6.0

- Preserve empty API parameter parentheses and render version-added, version-changed, and deprecated notices. ([9f63537](https://github.com/liran-funaro/sphinx-markdown-builder/commit/9f6353788e7e74fe94f83e5f6e448a71018ca236)) — [Liran Funaro](https://github.com/liran-funaro)
- Add `markdown_anchor_sections` and `markdown_anchor_signatures` settings for explicit HTML anchors. ([e270402](https://github.com/liran-funaro/sphinx-markdown-builder/commit/e27040266a433958c49c53c20f1b1e76af606a95)) — [Liran Funaro](https://github.com/liran-funaro)
- Improve whitespace-aware emphasis, underscore escaping, API parameter lists, field lists, and explicit reference anchors. ([e4e712b](https://github.com/liran-funaro/sphinx-markdown-builder/commit/e4e712b51154d41940ef5c23927fe27743f6683e)) — [Liran Funaro](https://github.com/liran-funaro)
- Normalize carriage returns in text and correctly use indentation contexts for nested content. ([524665f](https://github.com/liran-funaro/sphinx-markdown-builder/commit/524665f15fefc07f280d360b7ed3fada8e80d471)) — [Liran Funaro](https://github.com/liran-funaro)
- Modernize package metadata and require Python 3.7 or newer and Sphinx 2.2 or newer. ([e91e463](https://github.com/liran-funaro/sphinx-markdown-builder/commit/e91e463721c729486bbaac0f98090f5a49b53f2e)) — [Liran Funaro](https://github.com/liran-funaro)
- Fix spacing around block content, API annotations, and parameter fields. ([68c2fe4](https://github.com/liran-funaro/sphinx-markdown-builder/commit/68c2fe4209839c75373a3f1d87ecec7e33ea7879)) — [Liran Funaro](https://github.com/liran-funaro)
- Preserve image alternative text in generated Markdown. ([9fed39e](https://github.com/liran-funaro/sphinx-markdown-builder/commit/9fed39e867247eec131d17f52bff4c61f048eaba)) — [Liran Funaro](https://github.com/liran-funaro)
- Add `markdown_http_base` and `markdown_uri_doc_suffix` settings for links to externally hosted documentation. ([ef3d414](https://github.com/liran-funaro/sphinx-markdown-builder/commit/ef3d414a5e43b09dd99dee82a0aead60a7312674)) — [Liran Funaro](https://github.com/liran-funaro)
- Generate correctly structured Markdown tables with `tabulate`. ([c1ada2a](https://github.com/liran-funaro/sphinx-markdown-builder/commit/c1ada2a28c3d63e3c8ca7b2317756bc4a3698585)) — [Liran Funaro](https://github.com/liran-funaro)
- Fix nested-list spacing and images used as link targets. ([4b1786b](https://github.com/liran-funaro/sphinx-markdown-builder/commit/4b1786b798f9a63d3579f0e26343c8e8b6634239)) — [Liran Funaro](https://github.com/liran-funaro)
- Avoid unwanted paragraph line breaks inside table cells and list items. ([clayrisser/sphinx-markdown-builder#57](https://github.com/clayrisser/sphinx-markdown-builder/pull/57)) — [Shengyu Zhang](https://github.com/SilverRainZ)
- Preserve inline literals and signature text, fix same-page anchors, and allow signature anchors. ([clayrisser/sphinx-markdown-builder#55](https://github.com/clayrisser/sphinx-markdown-builder/pull/55)) — [Sergey Gruntovsky](https://github.com/wncm)
- Fix links to generated Markdown documents, including toctree references. ([clayrisser/sphinx-markdown-builder#51](https://github.com/clayrisser/sphinx-markdown-builder/pull/51)) — [Fabian Niehaus](https://github.com/FabianNiehaus)
- Create translators through the Sphinx builder API so extensions can register custom node handlers. ([clayrisser/sphinx-markdown-builder#50](https://github.com/clayrisser/sphinx-markdown-builder/pull/50)) — [Olivier Cayrol](https://github.com/ocayrol)
- Keep internal reference targets when no HTTP base is configured. ([clayrisser/sphinx-markdown-builder#45](https://github.com/clayrisser/sphinx-markdown-builder/pull/45)) — [Liam Howell](https://github.com/symbiont-liam-howell)
- Use language-specific highlighting for code blocks without requiring forced highlighting. ([clayrisser/sphinx-markdown-builder#43](https://github.com/clayrisser/sphinx-markdown-builder/pull/43)) — [Faris Lama](https://github.com/frslm)
- Render API annotations in italics. ([clayrisser/sphinx-markdown-builder#42](https://github.com/clayrisser/sphinx-markdown-builder/pull/42)) — [terryzhuo110](https://github.com/terryyz)
- Keep code-block language annotations compatible with newer Sphinx highlighting attributes. ([clayrisser/sphinx-markdown-builder#41](https://github.com/clayrisser/sphinx-markdown-builder/pull/41)) — [Christian Duffau-Rasmussen](https://github.com/duffau)
- Render class headings above method headings and tolerate signatures without a class attribute. ([clayrisser/sphinx-markdown-builder#39](https://github.com/clayrisser/sphinx-markdown-builder/pull/39)) — [Adrien VALIENTE](https://github.com/avaliente-bc) and [Jam Risser](https://github.com/clayrisser)
- Escape Python special-method names so double underscores do not become Markdown emphasis. ([clayrisser/sphinx-markdown-builder#37](https://github.com/clayrisser/sphinx-markdown-builder/pull/37)) — [Adrien VALIENTE](https://github.com/avaliente-bc)
- Improve numbering and indentation of nested ordered and unordered lists. ([c75f9b5](https://github.com/liran-funaro/sphinx-markdown-builder/commit/c75f9b56bf1681f8306cb886847f06830694c4eb)) — [Jam Risser](https://github.com/clayrisser)
- Remove the installation-time Pandoc requirement, unnecessary typing dependency, and strict dependency pins. ([clayrisser/sphinx-markdown-builder#29](https://github.com/clayrisser/sphinx-markdown-builder/pull/29)) — [Zac Hatfield-Dodds](https://github.com/Zac-HD)
- Preserve nested inline formatting in link text. ([clayrisser/sphinx-markdown-builder#28](https://github.com/clayrisser/sphinx-markdown-builder/pull/28)) — [Joe Wallis](https://github.com/Peilonrayz)
- Remove redundant newlines from generated Markdown. ([clayrisser/sphinx-markdown-builder#26](https://github.com/clayrisser/sphinx-markdown-builder/pull/26)) — [Joe Wallis](https://github.com/Peilonrayz)
- Render inline literal text correctly inside links. ([clayrisser/sphinx-markdown-builder#24](https://github.com/clayrisser/sphinx-markdown-builder/pull/24)) — [Joe Wallis](https://github.com/Peilonrayz)
- Preserve the configured language on highlighted code blocks. ([clayrisser/sphinx-markdown-builder#23](https://github.com/clayrisser/sphinx-markdown-builder/pull/23)) — [Gaute Lindkvist](https://github.com/lindkvis)
- Avoid an `IndexError` when completing a table row. ([clayrisser/sphinx-markdown-builder#12](https://github.com/clayrisser/sphinx-markdown-builder/pull/12)) — [Liam Deacon](https://github.com/Liam-Deacon)
- Render native tables as aligned Markdown tables. ([179a99f](https://github.com/liran-funaro/sphinx-markdown-builder/commit/179a99f83af1818602fe6efb07c529b66d76ea7f)) — [Jam Risser](https://github.com/clayrisser)
- Render images with valid Markdown image syntax. ([164f594](https://github.com/liran-funaro/sphinx-markdown-builder/commit/164f5946e21a3a714daa323caf6ff19a4160dfc9)) — [Manne Öhrström](https://github.com/manneohrstrom)
- Render Sphinx API signatures, parameter fields, notes, warnings, rubrics, and version-change directives. ([b1e2334](https://github.com/liran-funaro/sphinx-markdown-builder/commit/b1e2334f66918c47013755f7ff8aeefff9002ccb)) — [Manne Öhrström](https://github.com/manneohrstrom)
- Render document titles and subtitles at the correct Markdown heading levels. ([f3d5f52](https://github.com/liran-funaro/sphinx-markdown-builder/commit/f3d5f52cc86c19a0ddec357bbb209f71ccc5ad80)) — [Jam Risser](https://github.com/clayrisser)
- Remove the missing nbplots import so the bundled translator can load. ([fbc6e53](https://github.com/liran-funaro/sphinx-markdown-builder/commit/fbc6e532b6361e12ba4516df604f5e21fb99797d)) — [Jam Risser](https://github.com/clayrisser)
- Introduce the Markdown builder and bundle its doctree translator to generate Markdown from Sphinx documents. ([00e60eb](https://github.com/liran-funaro/sphinx-markdown-builder/commit/00e60eb6cd03028597712b82b2c51c3316b821f1)) — [Jam Risser](https://github.com/clayrisser)
