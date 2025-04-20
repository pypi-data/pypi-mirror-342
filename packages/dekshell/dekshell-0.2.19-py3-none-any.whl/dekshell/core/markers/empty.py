from dektools.shell import shell_command
from .base import MarkerShellBase


class ShellCommand:
    def __init__(self, kwargs):
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        kwargs = kwargs | self.kwargs
        return self.shell(*args, **kwargs)

    def shell(self, *args, **kwargs):
        return shell_command(*args, **kwargs)


class MarkerShell(MarkerShellBase):
    tag_head = ""
    shell_cls = ShellCommand


class PrefixShellMarker(MarkerShell):
    tag_head = "@"

    def execute(self, context, command, marker_node, marker_set):
        _, command = self.split_raw(command, 1, self.tag_head)
        if command:
            self.execute_core(context, command, marker_node, marker_set)


class EmptyMarker(MarkerShell):
    pass
