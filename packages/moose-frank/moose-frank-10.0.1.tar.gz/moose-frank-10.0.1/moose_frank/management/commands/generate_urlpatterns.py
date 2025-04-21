import os

from django.core.management.base import BaseCommand, OutputWrapper
from django.urls import get_resolver
from django.urls.resolvers import LocalePrefixPattern, RegexPattern
from django.utils.functional import Promise


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--output", default="/dev/stdout", help="Write to FILE instead of stdout"
        )

    def generate_urlpatterns(self, urls, indent=0):
        ws = "    " * indent
        for url in urls:
            if isinstance(url.pattern, LocalePrefixPattern):
                self.output.write(
                    """\
]

urlpatterns += i18n_patterns(
"""
                )
                self.generate_urlpatterns(url.url_patterns, 1)
                self.output.write(
                    """\
)

urlpatterns += ["""
                )
                continue

            if isinstance(url.pattern, RegexPattern):
                path = "re_path"
                pattern = (
                    f'_(r"{url.pattern}")'
                    if isinstance(url.pattern._regex, Promise)
                    else f'r"{url.pattern}"'
                )
            else:
                path = "path"
                pattern = (
                    f'_("{url.pattern}")'
                    if isinstance(url.pattern._route, Promise)
                    else f'"{url.pattern}"'
                )

            if hasattr(url, "url_patterns"):
                if url.namespace:
                    self.output.write(f"{ws}{path}({pattern}, include(([")
                    self.generate_urlpatterns(url.url_patterns, indent + 1)
                    self.output.write(f'{ws}], "{url.namespace}"))),')
                else:
                    self.output.write(f"{ws}{path}({pattern}, include([")
                    self.generate_urlpatterns(url.url_patterns, indent + 1)
                    self.output.write(f"{ws}])),")
            else:
                if url.name:
                    self.output.write(
                        f'{ws}{path}({pattern}, empty_view, name="{url.name}"),'
                    )
                else:
                    self.output.write(f"{ws}{path}({pattern}, empty_view),")

    def handle(self, *args, **options):
        if options["output"] == "/dev/stdout":
            self.output = self.stdout
            fd = None
        else:
            dir = os.path.dirname(options["output"])
            if dir and not os.path.exists(dir):
                os.makedirs(dir)
            fd = open(options["output"], "w")
            self.output = OutputWrapper(fd)

        self.output.write(
            """\
# fmt: off
from django.conf.urls.i18n import i18n_patterns  # noqa
from django.urls import include, path, re_path  # noqa
from django.utils.translation import gettext_lazy as _  # noqa


def empty_view(*args, **kwargs):
    pass


urlpatterns = ["""
        )
        self.generate_urlpatterns(get_resolver().url_patterns, 1)
        self.output.write("]")
        if fd:
            self.output.close()
            fd.close()
