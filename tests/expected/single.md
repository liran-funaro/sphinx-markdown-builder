# sphinx_markdown_builder Documentation

## Table of Contents

* [Main Document](#index)
* [Examplerstfile](#ExampleRSTFile)
* [Section Course Student](#Section_course_student)
* [Auto Module](#auto-module)
* [Auto Summery](#auto-summery)
* [Blocks](#blocks)
* [Empty](#empty)
* [Glossaries](#glossaries)
* [Image Target](#image-target)
* [My Module](#library/my_module)
* [My Module.Module Class](#library/my_module.module_class)
* [My Module.Submodule](#library/my_module.submodule)
* [My Module.Submodule.My Class](#library/my_module.submodule.my_class)
* [Links](#links)


<a id="index"></a>

## Main Test File



<a id="ExampleRSTFile"></a>

<!-- Taken form https://github.com/openedx/edx-documentation/blob/master/en_us/edx_style_guide/source/ExampleRSTFile.rst -->

<a id="anchor-for-examplerstfile"></a>

## Example .rst File

If you work with edX documentation source files, you might find this file
helpful as a reference. This file contains examples of .rst formatting.

Explanations and more context for each type of element are provided in
“Work with edX Documentation Source Files”.

This file covers the following topics.

> ###### Table of content
> 
> * [Heading Levels](#heading-levels)
> * [Paragraph Text and Commented Text](#paragraph-text-and-commented-text)
> * [Ordered and Unordered Lists](#ordered-and-unordered-lists)
> * [Conditional Text](#conditional-text)
> * [Notes and Warnings](#notes-and-warnings)
> * [Cross-References](#cross-references)
> * [Image References](#image-references)
> * [Tables](#tables)
> * [Code Formatting](#code-formatting)
> * [Links](#links)

### Heading Levels

The top of the document is heading 1, and this section is heading 2. The following are the rest of the headers.

#### Heading 3

##### Heading 4

###### Heading 5

###### Heading 6

### Paragraph Text and Commented Text

This is an example of regular text in paragraph form. There are no indents. As
a best practice, break lines at about 80 characters, so that each line has its
own line number for commenting in reviews.

##### WARNING
Throughout text and code examples, make sure double quotation
marks and apostrophes are straight (”) or (‘), not curly quotatation marks
and apostrophes, which might be introduced when text is cut and pasted from
other sources or editors.

##### ATTENTION
Boldface is used for labels that are visible in the user interface. The UI
text is surrounded by double asterisks. For example, **bold**.

##### IMPORTANT
This is an important message.

##### HINT
This is a hint message.

Italics are rarely used. Text surrounded by single asterisks is rendered in
*italics*.

Monospace text is used for `code examples`. Text surrounded by double grave
accent characters is rendered in monospace font.

<!-- comments can be added in a file by starting a line with 2 periods and a space. -->

In English source files, look for comments addressed to translators from writers.

`.. Translators:  In this code example, do not translate such and such.`

<!-- Translators:  In this code example, do not translate such and such. -->

### Ordered and Unordered Lists

Use hash symbols for ordered lists.

1. Select **Advanced Settings**.
2. Find the **Course Advertised Start Date** policy key.
3. Enter the value you want to display.

##### NOTE
Ordered lists usually use numerals. Nested ordered lists (ordered lists inside
other ordered lists) use letters.

Use asterisks for unordered (bulleted) lists.

* Who is teaching the course?
* What university or college is the course affiliated with?
* What topics and concepts are covered in your course?
* Why should a learner enroll in your course?

#### Nested Lists or Content

You can include content including additional lists and code examples inside
lists.

##### Unordered List inside Ordered List

To include an unordered list inside an ordered list, indent the unordered list
three spaces. The first bullet in the unordered list must be flush with the
text in the ordered list.

1. Review your entry to verify that the key is accurate and that it is
   surrounded by quotation marks. If there is a list of keys, they must be
   comma separated.
   * In this example, the key for the Annotation Problem tool is the only
     value in the list.
   * In this example, the key for the Annotation Problem tool is added at
     the beginning of a list of other keys.
2. Select **Save Changes**.

![An unordered (bulleted) list inside an ordered (numbered) list.](static/markdown.png)

##### Ordered List inside Unordered List

To include an ordered list inside an unordered list, indent the ordered list
two spaces. The first number or letter of the ordered list must be flush with
the text in the unordered list.

* Review your entry to verify that the key is accurate and that it is
  surrounded by quotation marks. If there is a list of keys, they must be comma
  separated.
  1. In this example, the key for the Annotation Problem tool is the only
     value in the list.
  2. In this example, the key for the Annotation Problem tool is added at the
     beginning of a list of other keys.
* Select **Save Changes**.

<!-- There isn't a screen shot of the above example yet because these lists don't -->
<!-- render correctly locally, and searching for an example in the built docs -->
<!-- online was taking too much time. -->

##### Unordered List inside Unordered List

To include an unordered list inside another unordered list, indent the second
unordered list two spaces. The first bullet of the second unordered list must
be flush with the text in the unordered list.

* Review your entry to verify that the key is accurate and that it is
  surrounded by quotation marks. If there is a list of keys, they must be
  comma separated.
  1. In this example, the key for the Annotation Problem tool is the only
     value in the list.
  2. In this example, the key for the Annotation Problem tool is added at the
     beginning of a list of other keys.
* Select **Save Changes**.

![An ordered (numbered) list inside an unordered (bulleted) list.](static/markdown.png)

##### Ordered List inside Ordered List

To include another ordered list inside an ordered list, indent the second
ordered list three spaces. The second ordered list must be flush with the text
in the numbered list. The first ordered list uses numerals, and the second
uses letters.

1. Review your entry to verify that the key is accurate and that it is
   surrounded by quotation marks. If there is a list of keys, they must be
   comma separated.
   1. In this example, the key for the Annotation Problem tool is the only
      value in the list.
   2. In this example, the key for the Annotation Problem tool is added at
      the beginning of a list of other keys.
2. Select **Save Changes**.

<!-- There isn't a screen shot of the above example yet because these lists don't -->
<!-- render correctly locally, and searching for an example in the built docs -->
<!-- online was taking too much time. -->

##### Code, Images, and Other Content inside Lists

To include content such as code or an image inside a list, position the code or
image directive flush with the text in the list. That is, indent three spaces
for ordered lists and two spaces for unordered lists.

1. In the `lms.yml` and `studio.yml` files, set the value of
   `CERTIFICATES_HTML_VIEW` within the `FEATURES` object  to `true`.
   ```bash
   "FEATURES": {
       ...
       'CERTIFICATES_HTML_VIEW': true,
       ...
   }
   ```
2. Save the `lms.yml` and `studio.yml` files.

### Conditional Text

To conditionalize a single paragraph, use either the `only:: Partners` or
the `only:: Open_edX` directive, and indent the paragraph under the
directive. You can add the conditional text as regular text or as a note.

Make sure to indent the paragraph under the directive.

Data about course enrollment is available from edX Insights. You can access
Insights from the instructor dashboard for your live course: after you select
**Instructor**, follow the link in the banner at the top of each page. For
more information, see [Using edX Insights](http://edx.readthedocs.io/projects/edx-insights/en/latest/).

To conditionalize more than a paragraph, use either the `only:: Partners` or
the `only:: Open_edX` directive, and then use an `include::` directive
indented under the only directive.

### Notes and Warnings

```
.. note::
   This is note text. If note text runs over a line, make sure the lines wrap
   and are indented to the same level as the note tag. If formatting is
   incorrect, part of the note might not render in the HTML output.

   Notes can have more than one paragraph. Successive paragraphs must indent
   to the same level as the rest of the note.
```

##### NOTE
This is note text. If note text runs over a line, make sure the lines wrap
and are indented to the same level as the note tag. If formatting is
incorrect, part of the note might not render in the HTML output.

Notes can have more than one paragraph. Successive paragraphs must indent to
the same level as the rest of the note.

```
.. warning::
   Warnings are formatted in the same way as notes. In the same way, lines
   must be broken and indented under the warning tag.
```

##### WARNING
Warnings are formatted in the same way as notes. In the same way, lines must
be broken and indented under the warning tag.

### Cross-References

In edX documents, you can include cross-references to other locations in the
same edX document, to locations in other edX documents (such as a cross-
reference from a location in the *Building and Running an edX Course* guide to
a location in the *EdX Learner’s Guide*), to JIRA stories, and to external
websites. In this section, “EdX documents” refers to the resources, including
guides and tutorials, that are listed on docs.edx.org.

For more information about creating cross-references using RST and Sphinx, see
[Cross-referencing arbitrary locations](http://www.sphinx-doc.org/en/stable/markup/inline.html#cross-referencing-arbitrary-locations) in the online Sphinx documentation.

#### Cross-References to Locations in the Same Document

Cross-references to locations in the same document use anchors that are located
above the heading for each topic or section. Anchors can contain numbers,
letters, spaces, underscores, and hyphens, but cannot include punctuation.
Anchors use the following syntax.

```
.. _Anchor Text:
```

The following example shows an anchor for a section, followed by the heading
for that section. `SFD SN Keyboard Shortcuts` is the anchor text.

<a id="sfd-sn-keyboard-shortcuts"></a>

##### Keyboard Shortcuts for Notes

To create cross-references to locations in the same document, you can use the
anchor only, or you can use your own text. The anchor text is never visible in
output. It is replaced by the text of the heading that follows the anchor or
the text that you specify.

##### Cross-References Using the Anchor Only

To add a cross-reference to a specific location in a document and use the text
of the heading for that location as link text, use `:ref:`Anchor Text``
syntax, as in the following example.

For more information about using keyboard shortcuts, see SFD SN Keyboard Shortcuts.

In this example, “SFD SN Keyboard Shortcuts” is the anchor text for a section
that is titled “Keyboard Shortcuts for Notes”. Readers will see the following
text, and “Keyboard Shortcuts for Notes” will be an active link.

```
For more information about using keyboard shortcuts, see Keyboard Shortcuts
for Notes.
```

##### Cross-References Using Specified Link Text

For internal cross-references that use text other than the heading for the
section that you’re linking to, use `:ref:`specified text<Anchor Text>``
syntax, as in the following example.

If you want to, you can use keyboard shortcuts to create, edit, and view notes.

##### NOTE
Do not include a space between the last word of the link text and the opening
angle bracket for the anchor text.

In this example, “keyboard shortcuts” is the link text, and “SFD SN Keyboard
Shortcuts” is the anchor text for a section that is titled “Keyboard Shortcuts
for Notes”. Readers will see the following text, and “keyboard shortcuts” will
be an active link.

```
If you want to, you can use keyboard shortcuts to create, edit, and view your
notes.
```

#### Cross-References to Locations in Different edX Documents

You can create cross-references between different edX documents. For example,
you can create a link in *Building and Running an edX Course* to a topic in the
*EdX Learner’s Guide*. To do this, you use the intersphinx map ID of the
document that you want to link to and the anchor text for the section you want.
The cross-reference uses the following syntax.

```
:ref:`intersphinx_map_ID:Anchor Name`
```

For example:

partnercoursestaff:Release Dates

To find the intersphinx map ID for the document that you want, follow these
steps.

1. Open the conf.py file in the [edx-documentation/shared](https://github.com/openedx/edx-documentation/blob/master/shared/conf.py) folder, and then
   locate the following line.

   `intersphinx_mapping = {`
2. In the list that follows this line, find the ID for the document that you
   want. The text between the single quotation marks (’) at the beginning of
   each line is the intersphinx map ID for the document.

The following intersphinx map IDs are the most frequently used.

| Map ID                | Document                                                     |
|-----------------------|--------------------------------------------------------------|
| `partnercoursestaff`  | *Building and Running an edX Course*                         |
| `opencoursestaff`     | *Building and Running an Open edX Course*                    |
| `learners`            | *EdX Learner’s Guide*                                        |
| `openlearners`        | *Open edX Learner’s Guide*                                   |
| `data`                | *EdX Research Guide*                                         |
| `insights`            | *Using edX Insights*                                         |
| `installation`        | *Installing, Configuring, and Running the Open edX Platform* |
| `opendevelopers`      | *Open edX Developer’s Guide*                                 |
| `partnerreleasenotes` | Partner release notes                                        |
| `openreleasenotes`    | Open edX release notes                                       |

<a id="anchor-for-cross-reference"></a>

#### Cross-References to External Web Pages

A cross-reference to an external web page has several elements.

* The URL of the external web page.
* The text to use for the cross-reference. This text becomes an anchor in the
  file that contains the cross-reference.
* An `include` directive in the file that contains the cross-reference to the
  links.rst file that is located in the `edx-documentation/en_us/links/`
  folder.
* An entry in the links.rst file.

To create an external cross-reference, follow these steps.

1. In the paragraph where you want the cross-reference, add the text that you
   want to use for the link, formatted as follows (where “Release Pages” is the
   link text). This creates an anchor out of that text.
   ```
   The edX engineering wiki `Release Pages`_ provide access to detailed
   information about every change made to the edx-platform GitHub
   repository.
   ```
2. In the file that contains the cross-reference, add an `include` directive
   for the `edx-documentation/en_us/links/links.rst` file if one does not
   already exist. These `include` directives are typically at the end of the
   file.
   ```
   .. include:: ../../links/links.rst
   ```

   ##### NOTE
   The path to the links.rst file depends on the location of the file where
   you are creating the link. For example, the path might be
   `../../../links/links.rst` or `../links/links.rst`.
3. In the `edx-documentation/en_us/links/links.rst` file, add an entry for
   the anchor text and the URL of the external website, formatted as follows.
   Make sure that the anchor text in this file matches the anchor text in the
   file that contains the cross-reference exactly, including capitalization.
   ```
   .. _Release Pages: https://openedx.atlassian.net/wiki/display/ENG/Release+Pages
   ```

Readers will see the following text. “Release Pages” will be an active link.

```
The edX engineering wiki Release Pages provide access to detailed
information about every change made to the edx-platform GitHub
repository.
```

The edX engineering wiki [Release Pages](https://openedx.atlassian.net/wiki/pages/viewpage.action?pageId=12550314) provide access to detailed
information about every change made to the edx-platform GitHub
repository.

### Image References

Image references look like this.

![A screen capture showing the elements of the course outline in the LMS.](static/markdown.png)

Image links can include optional specifications such as height, width, or
scale. Alternative text for screen readers is required for each image. Provide
text that is useful to someone who might not be able to see the image.

<a id="examples-of-tables"></a>

### Tables

Each example in this section shows the raw formatting for the table followed
by the table as it would render (if you are viewing this file as part of the
Style Guide).

#### Example of a table with an empty cell

The empty cell is the second column in the first row of this table.

```
.. list-table::
   :widths: 25 25 50

 * - Annotation Problem
   -
   - Annotation problems ask students to respond to questions about a
     specific block of text. The question appears above the text when the
     student hovers the mouse over the highlighted text so that students can
     think about the question as they read.
 * - Example Poll
   - Conditional Module
   - You can create a conditional module to control versions of content that
      groups of students see. For example, students who answer "Yes" to a
      poll question then see a different block of text from the students who
      answer "No" to that question.
 * - Example JavaScript Problem
   - Custom JavaScript
   - Custom JavaScript display and grading problems (also called *custom
     JavaScript problems* or *JS input problems*) allow you to create a
     custom problem or tool that uses JavaScript and then add the problem or
     tool directly into Studio.
```

| Annotation Problem         |                    | Annotation problems ask students to respond to questions about a<br/>specific block of text. The question appears above the text when the<br/>student hovers the mouse over the highlighted text so that students can<br/>think about the question as they read.   |
|----------------------------|--------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Example Poll               | Conditional Module | You can create a conditional module to control versions of content that<br/>groups of students see. For example, students who answer “Yes” to a<br/>poll question then see a different block of text from the students who<br/>answer “No” to that question.       |
| Exampel JavaScript Problem | Custom JavaScript  | Custom JavaScript display and grading problems (also called *custom<br/>JavaScript problems* or *JS input problems*) allow you to create a<br/>custom problem or tool that uses JavaScript and then add the problem or<br/>tool directly into Studio.              |

#### Example of a table with a header row

```
.. list-table::
   :widths: 15 15 70
   :header-rows: 1

   * - First Name
     - Last Name
     - Residence
   * - Elizabeth
     - Bennett
     - Longbourne
   * - Fitzwilliam
     - Darcy
     - Pemberley
```

| First Name   | Last Name   | Residence   |
|--------------|-------------|-------------|
| Elizabeth    | Bennett     | Longbourne  |
| Fitzwilliam  | Darcy       | Pemberley   |

#### Example of a table with a boldface first column

```
.. list-table::
   :widths: 15 15 70
   :stub-columns: 1

   * - First Name
     - Elizabeth
     - Fitzwilliam
   * - Last Name
     - Bennett
     - Darcy
   * - Residence
     - Longboure
     - Pemberley
```

| First Name   | Elizabeth   | Fitzwilliam   |
|--------------|-------------|---------------|
| Last Name    | Bennett     | Darcy         |
| Residence    | Longboure   | Pemberley     |

#### Example of a table with a cell that includes an unordered list

The blank lines before and after the unordered list are critical for the list
to render correctly.

```
.. list-table::
   :widths: 15 15 60
   :header-rows: 1

   * - Field
     - Type
     - Details
   * - ``correct_map``
     - dict
     - For each problem ID value listed by ``answers``, provides:

       * ``correctness``: string; 'correct', 'incorrect'
       * ``hint``: string; Gives optional hint. Nulls allowed.
       * ``hintmode``: string; None, 'on_request', 'always'. Nulls allowed.
       * ``msg``: string; Gives extra message response.
       * ``npoints``: integer; Points awarded for this ``answer_id``. Nulls allowed.
       * ``queuestate``: dict; None when not queued, else ``{key:'', time:''}``
         where ``key`` is a secret string dump of a DateTime object in the form
         '%Y%m%d%H%M%S'. Nulls allowed.

   * - ``grade``
     - integer
     - Current grade value.
   * - ``max_grade``
     - integer
     - Maximum possible grade value.
```

| Field         | Type    | Details                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|---------------|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `correct_map` | dict    | For each problem ID value listed by `answers`, provides:<br/><br/>* `correctness`: string; ‘correct’, ‘incorrect’<br/>* `hint`: string; Gives optional hint. Nulls allowed.<br/>* `hintmode`: string; None, ‘on_request’, ‘always’. Nulls allowed.<br/>* `msg`: string; Gives extra message response.<br/>* `npoints`: integer; Points awarded for this `answer_id`. Nulls allowed.<br/>* `queuestate`: dict; None when not queued, else `{key:'', time:''}`<br/>  where `key` is a secret string dump of a DateTime object in the form<br/>  ‘%Y%m%d%H%M%S’. Nulls allowed. |
| `grade`       | integer | Current grade value.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `max_grade`   | integer | Maximum possible grade value.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |

### Code Formatting

#### Inline code

In inline text, any text can be formatted as code (monospace font) by
enclosing the selection within a pair of double “grave accent” characters (\`).
For example, ```these words``` are formatted in a monospace font when the
documentation is output as PDF or HTML.

#### Code blocks

To set text in a code block, end the previous paragaph with 2 colons, leave
one line before the intended code block, and make sure the code block is
indented beyond the first colon.

```
For example, this is the introductory paragraph
::

 <p>and this is the code block following.</p>
```

Alternatively, use the code-block tag. Optionally, indicate the type of code
after the 2 colons in the tag, which results in the tags within the code block
being displayed in different colors.

```xml
<problem>
  <annotationresponse>
      <annotationinput>
        <text>PLACEHOLDER: Text of annotation</text>
          <comment>PLACEHOLDER: Text of question</comment>
          <comment_prompt>PLACEHOLDER: Type your response below:</comment_prompt>
          <tag_prompt>PLACEHOLDER: In your response to this question, which tag below
          do you choose?</tag_prompt>
        <options>
          <option choice="incorrect">PLACEHOLDER: Incorrect answer (to make this
          option a correct or partially correct answer, change choice="incorrect"
          to choice="correct" or choice="partially-correct")</option>
          <option choice="correct">PLACEHOLDER: Correct answer (to make this option
          an incorrect or partially correct answer, change choice="correct" to
          choice="incorrect" or choice="partially-correct")</option>
          <option choice="partially-correct">PLACEHOLDER: Partially correct answer
          (to make this option a correct or partially correct answer,
          change choice="partially-correct" to choice="correct" or choice="incorrect")
          </option>
        </options>
      </annotationinput>
  </annotationresponse>
  <solution>
    <p>PLACEHOLDER: Detailed explanation of solution</p>
  </solution>
</problem>
```

<!-- Taken from https://github.com/openedx/edx-documentation/blob/master/en_us/links/links.rst -->
<!-- Include this file in any file that includes a non-doc link. -->

### Links

<!-- EdX Links -->
<!-- GitHub Links -->
<!-- EDX VMs -->
<!-- EDX WIKI LINKS -->
<!-- THIRD PARTY LINKS -->
<!-- Release Notes -->
<!-- Browsers -->
<!-- Peer Instruction -->
<!-- Video Catalog -->



<a id="Section_course_student"></a>

<!-- Taken from https://github.com/openedx/edx-documentation/blob/67136d0c8f77592ca542992df167a57b6ed82156/en_us/shared/student_progress/Section_course_student.rst?plain=1 -->

## Using the Learner Engagement Report

With the learner engagement report, you can monitor what individual learners
are doing in your course. The report contains a row for each enrolled learner,
and has columns that quantify overall course activity and engagement with
course problems, videos, discussions, and textbooks.

With this report, you can identify which learners are, and which are not,
visiting course content. Further, you can identify the learners who are
attempting problems, playing videos, participating in discussions, or viewing
textbooks.

The server generates a new learner engagement report every day for the
previous day’s activity. On Mondays, an additional report is generated to
summarize activity during the previous week (Monday through Sunday).

> * [Understanding the Learner Engagement Report](#understanding-the-learner-engagement-report)
>   * [Reported Problem Types](#reported-problem-types)
>   * [Report Columns](#report-columns)
> * [Download the Learner Engagement Report](#download-the-learner-engagement-report)

### Understanding the Learner Engagement Report

#### Reported Problem Types

To measure problem-related activity, the learner engagement report includes
data for capa problems. That is, the report includes data for problems for
which learners can select **Check**, including these problem types.

> * Checkboxes
> * Custom JavaScript
> * Drag and Drop
> * Dropdown
> * Math expression input
> * Multiple choice
> * Numerical input
> * Text input

The report does not include data for open response assessments or LTI
components.

For more information about the problem types that you can add to courses, see
Exercises and Tools Index.

#### Report Columns

The learner engagement report .csv files contain the following columns.

| Column                        | Description                                                                                                                                        |
|-------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| Date                          | Included only in the daily report. The date of the reported activity.                                                                              |
| End Date                      | Included only in the weekly report. The last date of the report<br/>period.                                                                        |
| Course ID                     | The identifier for the course run.                                                                                                                 |
| Username                      | The unique username for an edX account.                                                                                                            |
| Email                         | The unique email address for an edX account.                                                                                                       |
| Cohort                        | Indicates the learner’s assigned cohort. Blank if the learner is not<br/>assigned to a cohort.                                                     |
| Was Active                    | Included only in the daily report. 1 for learners who visited any page<br/>(URL) in the course at least once during the reported day, 0 otherwise. |
| Days Active This Week         | Included only in the weekly report. Identifies the number of days<br/>during the week that the learner visited any page (URL) in the course.       |
| Unique Problems Attempted     | The number of unique problems for which the learner selected **Check**<br/>to submit an answer.                                                    |
| Total Problem Attempts        | The number of times the learner selected **Check** to submit answers,<br/>regardless of the particular problem attempted.                          |
| Unique Problems Correct       | The number of unique problems for which the learner submitted a correct<br/>answer.                                                                |
| Unique Videos Played          | The number of times the learner played a video. Each video that the<br/>learner began to play is included in this count once.                      |
| Discussion Posts              | The number of new posts the learner contributed to the course<br/>discussions.                                                                     |
| Discussion Responses          | The number of responses the learner made to posts in the course<br/>discussions.                                                                   |
| Discussion Comments           | The number of comments the learner made on responses in the course<br/>discussions.                                                                |
| Textbook Pages Viewed         | The number of pages in a .pdf textbook that the learner viewed.                                                                                    |
| URL of Last Subsection Viewed | The URL of the last subsection the learner visited.                                                                                                |

### Download the Learner Engagement Report

An automated process runs daily on the system server to update learner
engagement data and create the daily or weekly .csv file for you to download.
Links to the .csv files are available on the Instructor Dashboard.

To download a learner engagement report, follow these steps.

1. View the live version of your course.
2. Select **Instructor**, then select **Data Download**.
3. At the bottom of the page, select the
   `student_engagement_daily_{date}.csv` or `student_engagement_weekly_{end
   date}.csv` file name. You might have to scroll down to find a specific
   file.

<!-- Victor, should I add a section on what to do with it after you've downloaded it? or refer them to a similar existing section for the student answer distribution report? -->



<a id="auto-module"></a>

## Auto Module

Example module

#### *class* Point(x, y)

A Point

### Attributes

x: int
: The x value

y: str
: The y value

##### x *: int*

X value

##### y *: str*

Y value

* **Parameters:**
  * **x** (*int*)
  * **y** (*str*)

#### deprecated_function()

Some old function.

##### Deprecated
Deprecated since version 3.1: Use `other()` instead.

#### func1(param1)

This is a function with a single parameter.
Thanks to github.com/remiconnesson.

* **Parameters:**
  **param1** (*int*) – This is a single parameter.
* **Return type:**
  int

#### func2(param1, param2)

This is a function with two parameters.

* **Parameters:**
  * **param1** (*int*) – This is the first parameter.
  * **param2** (*int*) – This is the second parameter.
* **Return type:**
  str

#### func3(param1, param2)

This is a function with two parameters.

* **Parameters:**
  * **param1** (*int*) – Alice <sup>[1](#id3)</sup>.
  * **param2** (*int*) – Bon <sup>[2](#id4)</sup>.

### References

* <a id='id3'>**[1]**</a> Alice is commonly used to describe the first actor.
* <a id='id4'>**[2]**</a> Bob is commonly used to describe the second actor.



<a id="auto-summery"></a>

<!-- Taken from https://github.com/FabianNiehaus/sphinx-markdown-builder-toctree-test -->
<!-- Sphinx-Markdown-Builder TocTree Test documentation master file, created by
sphinx-quickstart on Thu Sep  3 12:25:35 2020.
You can adapt this file completely to your liking, but it should at least
contain the root `toctree` directive. -->

## Welcome to Sphinx-Markdown-Builder TocTree Test’s documentation!

### Documentation

| `my_module`   | Example module   |
|---------------|------------------|

Some link to a class `my_module.module_class.ModuleClass`

---

## Indices and tables

* genindex
* modindex
* search



<a id="blocks"></a>

## Math Example

Formula 1
: Definition of the formula as inline math:
  $\frac{ \sum_{t=0}^{N}f(t,k) }{N}$.
  <br/>
  Some more text related to the definition.

Display math:

$$
\frac{ \sum_{t=0}^{N}f(t,k) }{N}
$$

## Code Example

```pycon
>>> print("this is a Doctest block.")
this is a Doctest block.
```

## Line Block

text
sub text
<br/>
more text
<br/>
<br/>
<br/>

### Other text

other text

### Referencing terms from a glossary

Some other text that refers to Glossary2-Term2.

### Http domain directive

#### GET /users/(*int:* user_id)/posts/(tag)

### C domain

#### PyObject \*PyType_GenericAlloc(PyTypeObject \*type, Py_ssize_t nitems)



<a id="empty"></a>

<!-- Package documentation master file, created by
sphinx-quickstart on Thu Sep  2 09:41:50 2021.
You can adapt this file completely to your liking, but it should at least
contain the root ``toctree`` directive. -->

## Empty package



<a id="glossaries"></a>

## Glossary test for multiple glossaries

### Section for first glossary

<a id="term-Glossary1-Term1"></a>

Glossary1-Term1
: Some random text for term 1 in glossary 1.

<a id="term-Glossary1-Term2"></a>

Glossary1-Term2
: Some random text for term 2 in glossary 1. Referencing Glossary1-Term1.

<a id="term-Glossary1-Term3"></a>

Glossary1-Term3
: Some random text for term 3 in glossary 1. Referencing Glossary3-Term1.

### Section for second glossary

<a id="term-Glossary2-Term1"></a>

Glossary2-Term1
: Some random text for term 1 in glossary 2.

<a id="term-Glossary2-Term2"></a>

Glossary2-Term2
: Some random text for term 2 in glossary 2. Some reference for Glossary1-Term3.

### Section for third glossary

<a id="term-Glossary3-Term1"></a>

Glossary3-Term1
: Some random text for term 1 in glossary 3.



<a id="image-target"></a>

## Test Image With Target

[![image](static/markdown.png)](https://github.com/liran-funaro/sphinx-markdown-builder)

Download [`this example image`](/static/markdown.png).

![image](static/markdown.png)



<a id="library/my_module"></a>

## my_module

Example module

#### Sub Modules

| `module_class`   | A module class file.   |
|------------------|------------------------|
| `submodule`      | Example sub-module     |

#### Classes and Functions

#### *class* Point(x, y)

A Point

### Attributes

x: int
: The x value

y: str
: The y value

##### x *: int*

X value

##### y *: str*

Y value

* **Parameters:**
  * **x** (*int*)
  * **y** (*str*)

#### deprecated_function()

Some old function.

##### Deprecated
Deprecated since version 3.1: Use `other()` instead.

#### func1(param1)

This is a function with a single parameter.
Thanks to github.com/remiconnesson.

* **Parameters:**
  **param1** (*int*) – This is a single parameter.
* **Return type:**
  int

#### func2(param1, param2)

This is a function with two parameters.

* **Parameters:**
  * **param1** (*int*) – This is the first parameter.
  * **param2** (*int*) – This is the second parameter.
* **Return type:**
  str

#### func3(param1, param2)

This is a function with two parameters.

* **Parameters:**
  * **param1** (*int*) – Alice <sup>[1](#id3)</sup>.
  * **param2** (*int*) – Bon <sup>[2](#id4)</sup>.

### References

* <a id='id3'>**[1]**</a> Alice is commonly used to describe the first actor.
* <a id='id4'>**[2]**</a> Bob is commonly used to describe the second actor.



<a id="library/my_module.module_class"></a>

## my_module.module_class

A module class file.

#### Classes and Functions

#### default_var *= 'some_default_value'*

A default variable to be used by `SubmoduleClass`

#### *class* ModuleClass

A class inside a module.

Initialize a module class object

##### function(param1, param2)

Do nothing

This is a dummy function that does not do anything.

* **Parameters:**
  * **param1** (*int*) – Does nothing
  * **param2** (*str*) – Does nothing as well
* **Returns:**
  Nothing.
* **Return type:**
  None

##### SEE ALSO
`function()`



<a id="library/my_module.submodule"></a>

## my_module.submodule

Example sub-module

#### Sub Modules

| `my_class`   | A submodule class file.   |
|--------------|---------------------------|

#### Classes and Functions



<a id="library/my_module.submodule.my_class"></a>

## my_module.submodule.my_class

A submodule class file.

#### Classes and Functions

#### *class* SubmoduleClass(var)

A class inside a submodule.

* **Parameters:**
  **var** (*str*) – Does nothing

##### function(param1, param2)

Do nothing

This is a dummy function that does not do anything.

* **Parameters:**
  * **param1** (*int*) – Does nothing
  * **param2** (*str*) – Does nothing as well
* **Returns:**
  Nothing.
* **Return type:**
  None



<a id="links"></a>

<!-- Taken from https://github.com/openedx/edx-documentation/blob/master/en_us/links/links.rst -->
<!-- Include this file in any file that includes a non-doc link. -->

## Links

<!-- EdX Links -->
<!-- GitHub Links -->
<!-- EDX VMs -->
<!-- EDX WIKI LINKS -->
<!-- THIRD PARTY LINKS -->
<!-- Release Notes -->
<!-- Browsers -->
<!-- Peer Instruction -->
<!-- Video Catalog -->


