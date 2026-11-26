<!-- Taken from https://github.com/openedx/edx-documentation/blob/67136d0c8f77592ca542992df167a57b6ed82156/en_us/shared/student_progress/Section_course_student.rst?plain=1 -->

# Using the Learner Engagement Report

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

<a id="understanding-the-learner-engagement-report"></a>

## Understanding the Learner Engagement Report

<a id="reported-problem-types"></a>

### Reported Problem Types

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
[Adding Exercises and Tools](https://edx.readthedocs.io/projects/edx-partner-course-staff/en/latest/exercises_tools/index.html#exercises-and-tools-index).

<a id="report-columns"></a>

### Report Columns

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

<a id="download-the-learner-engagement-report"></a>

## Download the Learner Engagement Report

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
