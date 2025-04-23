# Modern Make

Proof of concept for a python make

# How to use

```
$ poetry install
$ poetry run momake
```

All tasks needs to be in `momaketasks.py` or `momaketasks` module.

Example:

```
from momake.dependency import FileDependency
from momake.task import Task


class Readme(Task):
    name = "readme"

    dependecies = [
        FileDependency(".", "README.md"),
    ]

    def action(self):
        print("readme task")


readme = Readme()


class Lint(Task):
    name = "lint"

    dependecies = [
        readme,
        FileDependency("momake", "*.py"),
    ]

    def action(self):
        print("lint task")

```
