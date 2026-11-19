# Contributing

We accept contributions of every kind: documentation, code, and artwork. Any help is greatly
appreciated. This document contains everything needed to get started with your first contribution.


## Contributing Code

We keep the source code on [GitHub](https://www.github.com) and take contributions through
[GitHub pull requests](https://help.github.com/articles/using-pull-requests).

For smaller patches and bug fixes just go ahead and either report an issue or submit a pull
request.

It is usually a good idea to discuss major changes with the developers, this will help us
determine whether the contribution would be a good fit for the project and if it is likely to be
accepted. There's nothing worse than seeing your hard work being rejected because it falls outside the scope of the project.

We follow [GitHub Flow](http://scottchacon.com/2011/08/31/github-flow.html) as our git workflow of
choice which boils down to:

* The `main` branch is always stable and deployable.
* To work on something new, branch off `main` and give the new branch a descriptive name (e.g.:
  `sort-packages-by-name`, `issue-32`, etc.).
* Regularly __rebase__ that branch against `main` and push your work to a branch with the same
  name on the server.
* When you need feedback, help or think you are ready,
  [submit a pull request](https://help.github.com/articles/using-pull-requests).
* Once the branch has been merged (or rebased) into `main`, delete it from both your local and
  remote repository.

Pull requests are squash-merged, so the pull request description becomes the commit message.
Fill in the [pull request template](.github/pull_request_template.md): pick the type of change,
describe what the change does, and link the issue it resolves (e.g. `- resolves #123`). Keep the
motivation in the linked issue rather than repeating it in the description.

To make sure modifications do not break this package functionality, we employ a CI workflow that tests the following:
 - Coding conventions (lint)
 - Expected outputs (tests)
 - Test code coverage

It is best to verify this before submitting a PR.

#### Prepare Environment
To make sure your environment matches the one in the CI servers, please create a new virtual environment. 
 For example, [venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment):
```shell
python3 -m venv .venv
source .venv/bin/activate
pip install .[dev]
```
Note
: The specific commands may change based on your local system.

#### Run linters
To make sure your modifications respect the project's coding standards, please run the following:
```shell
make lint
```

#### Run Tests
To make sure your modification does not change the expected behavior, please run the following.
```shell
make test
```
Testing is done with input/output examples.
If it fails, it will show the difference between generated and expected output.

To better view the difference after running `make test`, you can use the following command:
```bash
make diff DIFFTOOL=meld
```
You can replace 'DIFFTOOL=meld' with any "diff" tool you have on your local machine. The default is `meld`.


## Contributing Tests

Since this project is in its early stages, we lack meaningful examples.
We encourage you to suggest improvements, fixes, and additions to these tests by opening pull requests.

To contribute to this effort, please check out the following folders:
* [tests/source](/tests/source): input RST files and `conf.py`
* [tests/my_module](/tests/my_module): input code to produce documentation with the `sphinx.ext.autodoc` extension
* [tests/expected](/tests/expected): the desired output if applied to the input sources and code

You are encouraged to suggest changes to these files to address any discrepancies.

Important
: For resolving discrepancies, don't worry about passing CI tests.
Upon accepting your PR, developers will make additional effort to resolve these discrepancies and make the tests pass.


## Reading List

* [GitHub Flow](http://scottchacon.com/2011/08/31/github-flow.html)
* [On Commit Messages](http://who-t.blogspot.de/2009/12/on-commit-messages.html)
* [Semantic Versioning](http://semver.org/)
