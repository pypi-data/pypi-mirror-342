import logging
import shlex
import subprocess
from typing import Protocol

logger = logging.getLogger(__name__)


class GitInterface(Protocol):
    def get_tags(self, prefix: str) -> dict: ...

    def get_commit_sha(self, ref: str) -> str: ...


class GitCli:
    def cmd(self, args: list[str]) -> str:
        command = ["git"]
        command.extend(args)

        logger.debug("Executing `%s`", format(shlex.join(command)))
        p = subprocess.run(command, stdout=subprocess.PIPE, check=True, text=True)

        return p.stdout

    def get_tags(self, prefix: str) -> dict:
        output = self.cmd(
            [
                "for-each-ref",
                "--format=%(refname:strip=2) %(objectname)",
                f"refs/tags/{prefix}*",
            ]
        ).rstrip()

        output_lines = output.split("\n") if output else []

        tags = {}

        for line in output_lines:
            tag, sha = line.split(" ")

            tags[tag] = sha

        return tags

    def get_commit_sha(self, ref: str) -> str:
        return self.cmd(["rev-list", "-n", "1", ref]).rstrip()
