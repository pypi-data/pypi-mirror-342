# Django Commands UI

This project offers a solution to list and execute all existing management commands in your Django project.

## Requirements

This project requires Python 3.10 or greater.

## Configuration

To install and configure it these steps should be followed:
1. Install the dependency from PyPi.
   ```
   pip install django-commands-ui
   ```
2. Add `commands_ui` as an installed app in your Django project.
3. If you haven't already done so, you will need to add celery to your django project. You can follow the steps in the [First steps with Django](https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html) guide if you haven't used celery before.
4. Add the root location of your management commands to your installed apps. For example, if your management commands are in the `commands` folder in your project root, you would add `your-project-name.commands` to your installed apps.
5. Add these required settings:
   ```
    # Celery app name.
    COMMANDS_UI_CELERY_APP = ""

    # Working celery queue name for delayed jobs.
    COMMANDS_UI_DELAYED_JOBS_QUEUE = ""

    # Working celery queue name for standard jobs.
    COMMANDS_UI_JOBS_QUEUE = ""

    # Tuple of compiled regexes to extract the runnable commands from.
    # By default, all commands from all installed apps are extracted.
    COMMANDS_UI_JOB_APPS = (re.compile(r".*"),)

    # Primary database identifyer, not the replica one.
    DATABASE_PRIMARY = getattr(settings, "DATABASE_PRIMARY", "default")

    # Define if the current environment is a cron environment.
    CRON_ENVIRONMENT = getattr(settings, "CRON_ENVIRONMENT", False)
   ```
6. Include package URLs to your base urls file like this:
   ```
   path("jobs/", include("commands_ui.urls")),
   ```

7. Create tables:
   ```
   python manage.py migrate commands_ui
   ```

It is recommended to override `base.html` so the appearance is customizable, as all `django-commands-ui` templates extend from it.

## Documentation

### Implementing a management command job

The only needed thing for implementing a working management command job in
`django-commands-ui` is extending the existing JobBasedCommand.
This class adds some default arguments (such as `--job-id`).

Example on how to use this class:
```
from typing import Any
from commands_ui import management_commands
from django.core.management.base import CommandParser

# Extend the JobBasedCommand class
class Command(management_commands.JobBasedCommand):
   def handle(self, *args: Any, **options: Any) -> None:
      # Any time `self.print` is used, the message will be added to both standard output and
      # Job output.
      self.print("Starting")
      for i in range(0, 20):
         self.print(i)
      self.print("Finishing")
```

### Command Grouping

You can group types of commands by adding a `interface_name` class attribute to your management command class. This will group all commands with the same `interface_name` together in the UI.
For example you can group cronjobs together by adding `interface_name = "cron"` to all your cronjobs.

```
from typing import Any
from commands_ui import management_commands
from django.core.management.base import CommandParser

# Extend the JobBasedCommand class
class Command(management_commands.JobBasedCommand):
    interface_name = "cron"
   def handle(self, *args: Any, **options: Any) -> None:
      ...
```
