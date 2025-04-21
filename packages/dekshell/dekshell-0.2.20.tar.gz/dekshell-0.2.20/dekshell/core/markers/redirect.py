import os

from dektools.shell import shell_wrapper
from dektools.attr import DeepObject
from ...core.redirect import redirect_shell_by_path_tree
from ...utils.cmd import ak2cmd, key_args, key_kwargs
from ..contexts.properties import make_shell_properties, current_shell
from .base import MarkerBase


class MarkerRedirect(MarkerBase):
    def execute(self, context, command, marker_node, marker_set):
        filepath = self.split_raw(command, 1, self.tag_head)[1]
        if not filepath:
            filepath = self.eval(context, 'fp')
        path_shell = redirect_shell_by_path_tree(filepath)
        if path_shell:
            self.execute_core(context, path_shell)

    def execute_core(self, context, path_shell):
        raise NotImplementedError


class RedirectMarker(MarkerRedirect):
    tag_head = "redirect"

    def execute_core(self, context, path_shell):
        shell_properties = make_shell_properties(path_shell)
        if shell_properties['shell'] != current_shell:
            fp = self.eval(context, "fp")
            fpp = os.path.dirname(fp).replace('/', os.sep)
            shell = shell_properties['sh']['rfc' if os.getcwd() == fpp else 'rf']
            args, kwargs = self.eval(context, f'({key_args}, {key_kwargs})')
            argv = ak2cmd(args, kwargs)
            shell_wrapper(f'{shell} {fp} {argv}', env=context.environ_full())
            self.exit()


class ShiftMarker(MarkerRedirect):
    tag_head = "shift"

    def execute_core(self, context, path_shell):
        context.update_variables(DeepObject(make_shell_properties(path_shell)).__dict__)
