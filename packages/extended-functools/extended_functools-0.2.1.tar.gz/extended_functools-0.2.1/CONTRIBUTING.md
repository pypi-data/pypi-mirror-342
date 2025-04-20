# Contributing to the `extended-functools` project

## Filing a bug report

To file a bug report, [open the Issues tab][Issues] and add a new issue,
labeling it as a bug report. If you wish to try and fix it yourself, add
yourself as a contributor to that issue. You are allowed to group similar
bugs into one issue report, as long as you don't exceed the limit of three
different bugs. Otherwise, make another issue.

## Suggesting a new feature

To suggest a new feature:

- For small suggestions, [you can go directly to the Projects tab][Projects]
  and write a suggestion to the Suggestions/Ideas column
- For medium-to-large suggestions, write an issue, mark it as part of the
  current project and label it as a suggestion

You may NOT suggest features through email to the core developers.

## Setting up your development environment

The following should be enough for 95% of all contributors:

1. A working Git or GitHub Desktop installation
2. A text editor / Python IDE (VS Code suggested)
3. An installation of Python that supports Python version 3.10 or higher
4. A package manager, preferably `uv`
5. A working PGP toolchain, such as GnuPG

Start by generating a PGP key pair if you don't have them already. Then,
configure Git with your name, email, and PGP key; you can find a guide
[here][Git PGP guide]. Next, you should add the public key
[to your GitHub account][Adding PGP key to GitHub]. Consider backing up your
keys somewhere safe, so that in the event you lose access to the computer
you don't have to go through the hassle of adding new keys to GitHub.

Once Git has been configured, clone the repository, and install it.

```pwsh
uv install
```

Then, install the pre-commit hooks.

```pwsh
uv run pre-commit install
```

Your development environment should now be ready.

## Making changes

Create a new branch; the naming should follow Git Flow conventions, meaning

- `feature/<feature-name-here>` for feature branches, and
- `hotfix/<issue-id>` for hotfixes

For example, `feature/update-readme` would be a fine name for a feature branch.

Make your changes to this branch. You can create a draft PR as soon as you
have a feature branch on GitHub and update it to a normal one when ready,
or you can work on your feature until you think it's ready for review and
then create a normal PR. If your PR passes the tests and review process, it
will be merged. If the reviewer has feedback, it must be resolved until the PR
can be merged.

[Issues]: https://github.com/Diapolo10/extended-functools/issues
[Projects]: https://github.com/Diapolo10/extended-functools/projects
[Git PGP guide]: https://docs.github.com/en/authentication/managing-commit-signature-verification/telling-git-about-your-signing-key
[Adding PGP key to GitHub]: https://docs.github.com/en/authentication/managing-commit-signature-verification/adding-a-gpg-key-to-your-github-account
