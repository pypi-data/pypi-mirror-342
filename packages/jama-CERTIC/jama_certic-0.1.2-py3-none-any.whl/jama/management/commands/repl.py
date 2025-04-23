from django.core.management.commands.shell import Command
from django.contrib.auth.models import User
from rich.console import Console
from rich.table import Table
from typing import List

# from pick import pick
from resources.models import (
    Resource,
    Collection,
    Project,
    APIKey,
    ProjectAccess,
    Permission,
    File,
)


def _console_table(title: str, headers: List["str"]) -> Table:
    table = Table(title=title)
    for header in headers:
        table.add_column(header)
    return table


def user(*args, **kwargs):
    return User.objects.get(*args, **kwargs)


def project(*args, **kwargs):
    return Project.objects.get(*args, **kwargs)


def projects(*args, **kwargs):
    table = _console_table(
        "Projects",
        [
            "pk",
            "label",
            "description",
            "admin mail",
            "ARK redirect",
            "exiftool",
            "users",
        ],
    )

    for p in Project.objects.filter(*args, **kwargs):
        table.add_row(
            str(p.pk),
            str(p.label),
            str(p.description),
            str(p.admin_mail),
            str(p.ark_redirect),
            str(p.use_exiftool),
            ", ".join(
                f"{a.user.username} ({a.user.pk})"
                for a in ProjectAccess.objects.filter(project=p)
            ),
        )
    Console().print(table)


def users(*args, **kwargs):
    # option, index = pick(["some", "of", "this"], "choose...", multiselect=True)
    table = _console_table(
        "Users", ["pk", "username", "email", "active", "superuser", "projects"]
    )
    for u in User.objects.filter(*args, **kwargs):
        table.add_row(
            str(u.pk),
            str(u.username),
            str(u.email),
            str(u.is_active),
            str(u.is_superuser),
            ", ".join(
                f"{a.project.label} ({a.project.pk})"
                for a in ProjectAccess.objects.filter(user=u)
            ),
        )
    Console().print(table)


def accesses():
    for a in ProjectAccess.objects.order_by("project"):
        print(a.pk, a)


def bpython(self, options):
    import bpython

    bpython.embed(
        {
            "APIKey": APIKey,
            "Collection": Collection,
            "File": File,
            "Permission": Permission,
            "Project": Project,
            "ProjectAccess": ProjectAccess,
            "Resource": Resource,
            "User": User,
            "projects": projects,
            "users": users,
            "accesses": accesses,
        }
    )


Command.bpython = bpython
