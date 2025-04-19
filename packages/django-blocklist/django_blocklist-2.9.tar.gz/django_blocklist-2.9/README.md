# Django-blocklist

This is a [Django][] app that implements IP-based blocklisting. Its `BlocklistMiddleware` performs the blocking, and its `clean_blocklist` management command deletes entries which have satisfied the cooldown period. Entries also have a `reason` field, used in reporting. There are utility functions to add/remove IPs, an admin, and several management commands.

This app is primarily for situations where server-level blocking is not available, e.g. on platform-as-a-service hosts like PythonAnywhere or Heroku. Being an application-layer solution, it's not as performant as blocking via firewall or web server process, but is suitable for moderate traffic sites. It also offers better integration with the application stack, for easier management.

## Quick start

1. The [PyPI package name is `django-blocklist`](https://pypi.org/project/django-blocklist/); add that to your `requirements.txt` or otherwise install it into your project's Python environment.

1. Add "django_blocklist" to settings.INSTALLED_APPS
1. Add "django_blocklist.middleware.BlocklistMiddleware" to settings.MIDDLEWARE
1. Run `python manage.py migrate` to create the `django_blocklist_blockedip` table.
1. Add IPs to the list (via management commands, `utils.update_blocklist`, or the admin).
1. Set up a cron job or equivalent to run `manage.py clean_blocklist` daily.

## Management commands

Django-blocklist includes several management commands:

* `clean_blocklist` &mdash; remove entries that have fulfilled their cooldown period
* `import_blocklist` &mdash; convenience command for importing IPs from a file
* `remove_from_blocklist` &mdash; remove one or more IPs
* `report_blocklist` &mdash; information on the current entries
* `search_blocklist` &mdash; look for an IP in the list; in addition to info on stdout, returns an exit code of 0 if successful
* `update_blocklist` &mdash; add/update IPs; `--reason` and `--cooldown` optional; use `--skip-existing` to avoid updating existing records

The `--help` for each of these details its available options.

For exporting or importing BlockedIP entries, use Django's built-in `dumpdata` and `loaddata` management commands.

## Configuration

You can customize the following settings via a `BLOCKLIST_CONFIG` dict in your project settings:

* `cooldown` &mdash; Days to expire, for new entries; default 7
* `cache-ttl` &mdash; Seconds to cache the list of blocked IPs; default 60
* `denial-template` &mdash; For the denial response; an f-string with `{ip}` and `{cooldown}` placeholders

## Reporting

The `report_blocklist` command gives summary information about the current collection of IPs, including how many requests from those IPs have been blocked. See the [sample report][] for more.

## Utility methods

The `utils` module defines two convenience functions for updating the list from your application code:

* `update_blocklist(ips: set, reason: str, cooldown: int, last_seen: datetime)` adds IPs to the blocklist (all args except `set` are optional)
* `remove_from_blocklist(ip: str)` removes an entry, returning `True` if successful

[django]: https://www.djangoproject.com/
[sample report]: https://gitlab.com/paul_bissex/django-blocklist/-/blob/trunk/blocklist-report-sample.txt
