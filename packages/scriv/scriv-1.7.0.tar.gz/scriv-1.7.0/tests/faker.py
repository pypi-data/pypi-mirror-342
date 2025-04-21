"""Fake implementations of some of our external information sources."""

import re
import shlex
from collections.abc import Iterable
from typing import Callable, Optional

from scriv.shell import CmdResult

# A function that simulates run_command.
CmdHandler = Callable[[list[str]], CmdResult]


# A regex to help with catching some (but not all) invalid Git config keys.
WORD = r"[a-zA-Z][a-zA-Z0-9-]*"
GIT_CONFIG_KEY = rf"{WORD}(\..*)?\.{WORD}"


class FakeRunCommand:
    """
    A fake implementation of run_command.

    Add handlers for commands with `add_handler`.
    """

    def __init__(self, mocker):
        """Make the faker."""
        self.handlers: dict[str, CmdHandler] = {}
        self.mocker = mocker
        self.patch_module("scriv.shell")

    def patch_module(self, mod_name: str) -> None:
        """Replace ``run_command`` in `mod_name` with our fake."""
        self.mocker.patch(f"{mod_name}.run_command", self)

    def add_handler(self, argv0: str, handler: CmdHandler) -> None:
        """
        Add a handler for a command.

        The first word of the command is `argv0`.  The handler will be called
        with the complete argv list.  It must return the same results that
        `run_command` would have returned.
        """
        self.handlers[argv0] = handler

    def __call__(self, cmd: str) -> CmdResult:
        """Do the faking!."""
        argv = shlex.split(cmd)
        if argv[0] in self.handlers:
            return self.handlers[argv[0]](argv)
        return (False, f"no fake command handler: {argv}")


class FakeGit:
    """Simulate aspects of our local Git."""

    def __init__(self, frc: FakeRunCommand) -> None:
        """Make a FakeGit from a FakeRunCommand."""
        # Initialize with basic defaults.
        self.config: dict[str, str] = {
            "core.bare": "false",
            "core.repositoryformatversion": "0",
        }
        self.branch = "main"
        self.editor = "vi"
        self.tags: set[str] = set()
        self.remotes: dict[str, tuple[str, str]] = {}

        # Hook up our run_command handler.
        frc.add_handler("git", self.run_command)

    def run_command(self, argv: list[str]) -> CmdResult:
        """Simulate git commands."""
        # todo: match/case someday
        if argv[1] == "config":
            if argv[2] == "--get":
                if argv[3] in self.config:
                    return (True, self.config[argv[3]] + "\n")
                else:
                    return (False, f"error: no such key: {argv[3]}")
        elif argv[1:] == ["rev-parse", "--abbrev-ref", "HEAD"]:
            return (True, self.branch + "\n")
        elif argv[1:] == ["tag"]:
            return (True, "".join(tag + "\n" for tag in self.tags))
        elif argv[1:] == ["var", "GIT_EDITOR"]:
            return (True, self.editor + "\n")
        elif argv[1:] == ["remote", "-v"]:
            out = []
            for name, (url, push_url) in self.remotes.items():
                out.append(f"{name}\t{url} (fetch)\n")
                out.append(f"{name}\t{push_url} (push)\n")
            return (True, "".join(out))
        return (False, f"no fake git command: {argv}")

    def set_config(self, name: str, value: str) -> None:
        """Set a fake Git configuration value."""
        if re.fullmatch(GIT_CONFIG_KEY, name) is None:
            raise ValueError(f"invalid key: {name!r}")
        self.config[name] = value

    def set_branch(self, branch_name: str) -> None:
        """Set the current fake branch."""
        self.branch = branch_name

    def set_editor(self, editor_name: str) -> None:
        """Set the name of the fake editor Git will launch."""
        self.editor = editor_name

    def add_tags(self, tags: Iterable[str]) -> None:
        """Add tags to the repo."""
        self.tags.update(tags)

    def add_remote(
        self, name: str, url: str, push_url: Optional[str] = None
    ) -> None:
        """Add a remote with a name and a url."""
        self.remotes[name] = (url, push_url or url)

    def remove_remote(self, name: str) -> None:
        """Remove the remote `name`."""
        del self.remotes[name]
